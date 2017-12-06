# -*- coding: utf-8 -*-
'''
	Created on Dec 6th, 2017

	@author: Varela

	motivation: module provides clustering from distance and transforming (from structs)
			 
'''
#Regex
import glob # Unix style GLOB performs pattern matching on files
import re

#Datascience stuff
import pandas as pd 
import numpy as np 

#Nice command line 
import sys 

DATASET_PATH='../locality-sensitive-hashing/datasets/'
DISTANCE_MATRICES_PATTERN=DATASET_PATH + '*_distance_matrix.txt'
CLUSTER_MODELS_PATTERN=DATASET_PATH + '*_cluster.txt'

def cluster2txt(cluster, filename='distance_cluster.txt'):
	'''
		Converts a cluster dictionary into a file
		INPUT 
			cluster<dict<int,int>>: cluster dict int, int 

			filename<string>: Name of the file to be generated

		OUTPUT
			
	'''	
	file_path=DATASET_PATH + filename	
	df = pd.DataFrame.from_dict(cluster,orient='index')
	df.to_csv(file_path, sep=' ',index=True, index_label=False,header=None)

def clusterize(dist):
	'''
		INPUT 
			dist<float<D,D>>: dist numpy matrix 
				D<int>: number of original documents

		OUTPUT
			cluster<dict<int,int>>: cluster dict int, int 
				
	'''	
	thresh=1e-3 # this is our float 0
	nrows, ncols= dist.shape 
	index= np.arange(ncols)
	cluster={}
	cluster_count=0
	for r in range(nrows):
		if not(r in cluster): #not a key then ways wasn't added
			#Always add non added document
			cluster[r]= cluster_count 
			ind = (dist[:,r]<thresh) & (index>r) # garantees dimensionality equivalence			
			if np.any(ind):
				for i in index[ind]:
					cluster[i]=cluster_count							
			cluster_count+=1
	return cluster	

def distance_matrix_clustering():
	'''
		This function generates a cluster for each file matching the regex *_distance_matrix.txt

		INPUT 
			dist<float<D,D>>: Distance matrices @ dataset directory
				D<int>: number of original documents

		OUTPUT
			cluster<int<D,2>>: 
				D<int>: number of original documents
	'''
	matcher = re.compile('(.*)_distance_matrix.txt$')
	files=glob.glob(DISTANCE_MATRICES_PATTERN)	
	print('%d files found matching distance_matrix suffix' % len(files))


	for i, file in enumerate(files):

		print('Fetching %d file...' % (i+1))
		df= pd.read_csv(file, sep= ' ', index_col=None, header=None, skiprows=1 ) 
		dist= df.as_matrix() 
		print('Fetching %d file... done' % (i+1))


		filename=file.split('/')[-1]
		matchings= matcher.match(filename)
		data_model=matchings.groups()[0]
		print('Clustering of %s...' % (data_model))
		cluster_filename=data_model+'_cluster.txt'
		cluster=clusterize(dist)
		print('Clustering of %s...done' % (data_model))
		cluster2txt(cluster, filename=cluster_filename)

def cluster_txt2df(str_pattern):
	'''
		Scans dataset for clusters glob matching str_pattern and 
			returns all 		

		INPUT 
			str_pattern<str>: Fetches a glob of files that match

		OUTPUT
			df<pandas.DataFrame>: index: observationsid
														column.names: filenames
														values:clusterid

		examples: 
		str_pattern= '*_cluster.txt'
		matches: 'gaussian_0.3_cluster.txt', 'sparse_0.4_cluster.txt' but not 'goldenset.csv'
	'''
	matcher 				 = re.compile('(.*)_cluster.txt$')
	str_pattern1= DATASET_PATH + str_pattern
	files=glob.glob(str_pattern1)	
	M=len(files)
	print('%d files found matching r\'%s\' pattern' % (M,str_pattern))
	newnames=[]
	for i, file in enumerate(files):			
		colname=get_filename(file)

		print('Fetching %d\t%s...' % (i+1, colname))				
		if i==0:
			df= pd.read_csv(file, sep= ' ',index_col=0, header=None)		
			df.columns=[colname] 
		else:
			df_tmp= pd.read_csv(file, sep= ' ', index_col=0, header=None)		
			df_tmp.columns=[colname] 
			df=pd.concat((df,df_tmp),axis=1)						
		print('Fetching %d\t%s...done' % (i+1,colname))				
	
	return df 	

def  cluster_dict2set(cluster_dict):
	'''
		Receives a cluster dict and computes a neightbourhood dict

		INPUT
			cluster_dict<int,int>: each value from the cluster dict is an integer

		OUTPUT
			neighbour_dict<int,set<int>>: each value from the neightbour dict is a set of integers of variable size
		
		
	'''	
	neighbours_mapping={}
	for key, value in cluster_dict.items():
		if value in neighbours_mapping:
			neighbours_mapping[value].append(key)
		else:
			neighbours_mapping[value]=[key]	
	return {key:set(neighbours_mapping[value]) for key, value in cluster_dict.items()}	

def cluster_set2pairwise(neighbour_dict):
	'''
		Receives a neighbour dict which is a dict of sets

		INPUT
			neighbour_dict<int,set<int>>: each value from the neightbour dict is a set of integers of variable size

		OUTPUT
			list<set<int>>: is a list of sets: the inner set has either one element or a pair 

	'''
	processed=set([])
	list_of_pairs=[]
	list_of_uniques=[]
	count=0
	x=len(neighbour_dict)
	for doc_id, doc_neighbours in neighbour_dict.items():
		sys.stdout.write('cluster_set2pairwise:%d of %d doc_id:%s \r' % (count,x,str(doc_id)))
		sys.stdout.flush()

		if not(doc_id in processed):
			l= len(doc_neighbours)	
			this_elements={i for i in doc_neighbours}
			if l==1:				
				list_of_uniques+=list(doc_neighbours)
			else:
				neighbours=list(doc_neighbours)
				list_of_pairs+= [[neighbours[i],neighbours[j]] for i in range(l-1) for j in range(i+1,l)]
			
			processed =processed.union(this_elements)

		count+=1	


	set_uniques=set(list_of_uniques)
	set_duplicates=lol2sos(list_of_pairs)

	return set_duplicates, set_uniques

def lol2sos(list_of_lists):
	'''
		converts a list of list to a set of frozen sets
		INPUT
			pair_map<int,set<int>>: 

		OUTPUT
			list<set<int>>: is a list of sets: the inner set has either one element or a pair 

	'''	

	return set(map(frozenset,list_of_lists))	

def get_filename(filename):	
	'''
		Removes filename's prefix and suffix
		INPUT
			filename<str>: fullname path
		
		OUTPUT
			filename1<str>: filename without extension or file_system stuff
				
	'''	
	filename1= filename.split('/')[-1]
	filename_parts= filename1.split('.')[:-1]
	filename1= '.'.join(filename_parts)
	return filename1

if __name__ == '__main__':		
	distance_matrix_clustering()