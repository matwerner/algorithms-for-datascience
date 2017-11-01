# -*-encoding:utf8-*-
import argparse
import numpy as np

# Fix seed
np.random.seed(100)

def universal_hash(prime, size):
    # Check values
    if prime < size:
        raise ValueError("Prime number should be greater than size")
    
    # Generate random values
    a = np.random.randint(1, prime)
    b = np.random.randint(1, prime)
    
    # Return hash function
    return lambda x: ((a * x + b) % prime) % size

def random_data_stream(batch_size, array_size):
    # Max number of the distribution
    max_number = int(1e11)
    
    # Calculate number of batches
    batches = int(np.ceil(array_size/batch_size))

    for i in range(batches):
        # Due to array tail
        size = batch_size if (i + 1) * batch_size <= array_size else array_size - i * batch_size
        
        # Generate uniform random vector
        array = np.random.uniform(low=0., high=1., size=size)
        
        # Apply new distribution
        array = np.minimum(1./np.power(array, 2), max_number)
        
        # Round to int
        yield array.astype('int64')

def item1(batch_size, array_size):
    unique = {}
    for stream in random_data_stream(batch_size, array_size):
        for data in np.unique(stream):
            if data not in unique:
                unique[data] = 1
    return len(unique)        
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-b', action="store", dest="batch_size", type=int)
    parser.add_argument('-s', action="store", dest="stream_size", type=int)
    
    args = parser.parse_args()
    batch_size = args.batch_size
    stream_size = args.stream_size
    
    size = item1(batch_size, stream_size)
    
    print(size)