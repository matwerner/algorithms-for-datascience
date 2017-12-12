import argparse
import json
import multiprocessing
import numpy as np
import unidecode
import re
import sys

def _universal_hash(prime, size):
    # Check values
    if prime < size:
        raise ValueError("Prime number should be greater than size")
    
    # Generate random values
    a = np.random.randint(1, prime)
    b = np.random.randint(1, prime)
    
    # Return hash function
    return lambda x: ((a * x + b) % prime) % size

# Due to compatibility issue between multiprocessing and classes
def _compute_min_hashing(documents, shingles_size, k, prime=2**31-1):
    # Due to multiprocessing
    np.random.seed()
    
    # Instantiate hash methods to be used as permutations
    hash_methods = [_universal_hash(prime, shingles_size)
                    for i in range(k)]
    
    # Signature of each document
    signatures = [[sys.maxsize
                for j in range(k)]
                for i in range(len(documents))]
    
    # Each shingle for each document just need to be computed once
    computed = [set() for i in range(len(documents))]
    
    for i, document in enumerate(documents):
        for shingle in document:
            # Shingle already computed
            if shingle in computed[i]:
                continue
            
            # Compute hash for shingle
            computed[i].add(shingle)
            for j, hash_method in enumerate(hash_methods):
                hash_value = hash_method(shingle)
                
                # Check if "permutation position" is lower
                if hash_value < signatures[i][j]:
                    signatures[i][j] = hash_value
    
    # Return signature of all documents
    return np.array(signatures, dtype=np.uint64)

class LSH():

    def __init__(self, k, rows, bands, threshold):
        np.random.seed(100)

        self.k = k
        self.n_rows = rows
        self.n_bands = bands
        self.n_hashes = rows * bands
        self.threshold = threshold

        self.cids = {}
        self.clusters = {}

    # All non-alphabet letters, non-spaces and break lines
    # Expect ':' due to other regex patterns
    __regex = re.compile(r'([^a-zA-Z :]|[\t\n\r\f\v])')

    @classmethod
    def __preprocessing(self, documents):
        for i in range(len(documents)):
            # Remove all accents
            documents[i] = unidecode.unidecode(documents[i])
            
            # Remove all non-alphabet letters or spaces
            documents[i] = self.__regex.sub(' ', documents[i])
            
            # Remove extra spaces
            documents[i] = ' '.join([token for token in documents[i].split(' ') if token])
            
            # To lower
            documents[i] = documents[i].lower()
        return documents

    # Local patterns
    __lookup_local = ["local\s*:\s*", "local\s*de\s*trabalho\s*:\s*",
                      "local\s*da\s*vaga\s*:\s*", "cidade\s*:\s*",
                      "localizada\s*em\s*", "local\s*do\s*trabalho\s*:\s*",
                      "localizacao\s*:\s*"]
    __local = re.compile("(" + "|".join(__lookup_local) + ")", re.IGNORECASE)

    # Get a fix legth chuck after pattern
    __local_length = 10

    ## Local Parser

    @classmethod
    def __parse_local(self, document):
        match = self.__local.search(document)
        if match:
            start, end = match.end(), match.end() + self.__local_length
            return document[start:end]

    ### Formation patterns
    __lookup_formation = ["formacao\s*requerida\s*:\s*","formacao\s*desejada\s*:\s*",
                          "escolaridade\s*requerida\s*:\s*", "escolaridade\s*:\s*",
                          "escolaridade\s*desejada\s*:\s*", "formacao\s*:\s*"]
    __formation = re.compile("(" + "|".join(__lookup_formation) + ")", re.IGNORECASE)

    # Get a fix legth chuck after pattern
    __formation_length = 10

    ## Formation Parser

    @classmethod
    def __parse_formation(self, document):
        match = self.__formation.search(document)
        if match:
            start, end = match.end(), match.end() + self.__formation_length
            return document[start:end]

    ## Shingling

    @classmethod
    def __to_shingles(self, documents, k):
        # Map keeping the "Hash" of the shingles
        shingle_map = {}
        idx = 0
        
        # New document structure
        doc_shingles = []
        for i, document in enumerate(documents):
            shingles = set()
            # Split each document in k-shingles
            for j in range(0, len(document) - k + 1):
                # Get shingle
                shingle = document[j:j+k]
                
                # For efficience purposes, apply hash
                if shingle in shingle_map:
                    hashed_shingle = shingle_map[shingle]
                else:
                    shingle_map[shingle] = idx
                    hashed_shingle = idx
                    idx += 1
                
                # Append to set of shingles
                shingles.add(hashed_shingle)
                
            # Attribute to document
            doc_shingles.append(shingles)
            
        return doc_shingles, shingle_map

    ## Min-Hashing

    @classmethod
    def __compute_min_hashing(self, documents, shingles_size, k, prime=2**31-1):
        return _compute_min_hashing(documents, shingles_size, k, prime)

    @classmethod
    def __compute_min_hashing_multiprocessing(self, documents, shingles_size, k, prime=2**31-1):
        # Instantiate
        threads = multiprocessing.cpu_count() - 1
        pool = multiprocessing.Pool(processes=threads)
        n, m = divmod(k, threads)    
        
        # Shared variable
        manager = multiprocessing.Manager()
        shared_documents = manager.list(documents)
        
        # Start threading
        jobs = []
        for i in range(threads):
            batch = n + (m if i == 0 else 0)
            job = pool.apply_async(_compute_min_hashing,
                                   args = (shared_documents, shingles_size, batch, prime))
            jobs.append(job)
        
        pool.close()
        pool.join()
        
        # Join all results
        results = [job.get() for job in jobs]
        return np.hstack(results)

    ## Locality-Sensitive Hashing

    @classmethod
    def __compute_lsh(self, signatures, rows, bands, prime=2**31-1):
        # Make n_buckets as large as possible
        # For now, we will use "1GB"
        n_buckets = int(10**9)
        
        # Instantiate hash methods
        hash_methods = [_universal_hash(prime, n_buckets)
                        for i in range(bands)]
        
        # Buckets for all hashes
        hash_buckets = [{} for i in range(bands)]
        
        for i, signature in enumerate(signatures):
            for j in range(bands):
                # Get mini signature
                mini_signature = signature[j*rows:j*rows+rows]
                
                # "Merge" entries of vector
                value = np.sum(np.power(mini_signature, 2))
                    
                # Compute hash/bucket for the band
                hash_value = hash_methods[j](value)

                if hash_value in hash_buckets[j]:
                    hash_buckets[j][hash_value].append(i)
                else:
                    hash_buckets[j][hash_value] = [i]
        
        return hash_buckets

    ## Find Candidates

    @classmethod
    def __find_candidates(self, hash_buckets, signatures, threshold):
        # Get signature size - signatures y-axis
        signature_size = signatures.shape[1]
        
        # Get all pairs
        pairs = set()
        for hash_bucket in hash_buckets:
            for bucket, values in hash_bucket.items():
                # Only interested in pairs
                if len(values) < 2:
                    continue
                
                # Check if items are candidates (> threshold)
                for i in range(0, len(values)):
                    for j in range(i + 1, len(values)):
                        # Keep order, so we can eliminate duplicates
                        if values[i] > values[j]:
                            pairs.add((values[j], values[i]))
                        else:
                            pairs.add((values[i], values[j]))
        
        # Find all candidates
        candidates = []
        for pair in pairs:
            idx, idy = pair
            equal_values = np.sum(signatures[idx] == signatures[idy])
            if equal_values >= threshold * signature_size:
                candidates.append(pair)
        
        return candidates

    ## Remove some false positives

    @classmethod
    def __check_false_positives(self, documents, pairs):
        true_positives = []
        for pair in pairs:
            idx, idy = pair
            
            # Check if same local
            local_x, local_y = self.__parse_local(documents[idx]), self.__parse_local(documents[idy])
            if local_x != local_y:
                continue
            
            # Check if same formation
            formation_x, formation_y = self.__parse_formation(documents[idx]), self.__parse_formation(documents[idy])
            if formation_x != formation_y:
                continue
            
            true_positives.append(pair)
        
        return true_positives        

    ## Convert documents to duplicates's clusters

    @classmethod
    def __set_clusters(self, candidates, n_items):
        # Initialize clusters
        cids = {i:i for i in range(n_items)}
        clusters = {i:set([i]) for i in range(n_items)}
        
        # Fill clusters
        for item_a, item_b in candidates:
            # Already in the same cluster due to composition
            if cids[item_a] == cids[item_b]:
                continue
                
            # Get current clusters
            cluster_a = clusters[cids[item_a]]
            cluster_b = clusters[cids[item_b]]
            
            # Merge clusters
            if len(cluster_a) >= len(cluster_b):
                new_cid = cids[item_a]
                old_cid = cids[item_b]
            else:
                new_cid = cids[item_b]
                old_cid = cids[item_a]

            # Update
            for item in clusters[old_cid]:
                cids[item] = new_cid
            clusters[new_cid].update(clusters[old_cid])
            del clusters[old_cid]
            
        return clusters, cids

    ## Split documents into clusters

    def fit_data(self, documents, check_fp=True):
        parsed_documents = self.__preprocessing(documents)

        documents_shingles, map_shingles = self.__to_shingles(parsed_documents, self.k)

        signatures = self.__compute_min_hashing_multiprocessing(documents_shingles, len(map_shingles), self.n_hashes)

        hash_buckets = self.__compute_lsh(signatures, self.n_rows, self.n_bands)

        candidates = self.__find_candidates(hash_buckets, signatures, self.threshold)

        if check_fp:
            candidates = self.__check_false_positives(documents, candidates)

        clusters, cids = self.__set_clusters(candidates, len(documents))

        self.cids = cids
        self.clusters = clusters

    ## Save clusters found

    def save(self, output_path, delimiter=' '):
        line_format = '%s' + delimiter + '%s\n'
        with open(output_path, 'w') as fp:
            for cid in self.cids.items():
                fp.write(line_format % cid)    

# Experiments

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Computes LSH for some documents')
    parser.add_argument('-f', action="store", dest="data_path",
                        type=str, default="../datasets/development.json", 
		                help="Input path to all documents to be clustered\n")
    parser.add_argument('-k', action="store", dest="shingle_size",
                        type=int, default=5,
                        help="Size of chunks which the documents will be splited\n")
    parser.add_argument('-r', action="store", dest="row_size",
                        type=int, default=20,
                        help="Number of rows of each band\n")
    parser.add_argument('-b', action="store", dest="band_size",
                        type=int, default=5,
                        help="Number of bands\n")
    parser.add_argument('-t', action="store", dest="threshold_value",
                        type=float, default=0.8,
                        help="Threshold to documents be considered duplicates\n")
    parser.add_argument('-c', action="store", dest="check_fp",
                        type=bool, default=True,
	                    help="Whether to check false positives due to local or formation differences\n") 
    parser.add_argument('-o', action="store", dest="output_path",
                        type=str, default="../datasets/cids.txt",
	                    help="File name containing clusted id of each document\n")
    args = parser.parse_args()

    ## Parameters

    data_path = args.data_path
    output_path = args.output_path

    ## Hyperparameters

    k = args.shingle_size
    n_rows = args.row_size
    n_bands = args.band_size
    threshold = args.threshold_value
    check_fp = args.check_fp

    ## Load dataset

    with open(data_path, mode="r", encoding="utf-8") as fp:
        documents = [document['description']
                    for document in json.loads(fp.readline())
                    if document['description']]

    ## LSH

    instance = LSH(k, n_rows, n_bands, threshold)
    instance.fit_data(documents, check_fp)
    instance.save(output_path)