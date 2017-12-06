# -*- coding: utf-8 -*-
'''
	Created on Nov 24, 2017

	@author: Varela

	motivation: Benchmark module provinding clustering over distance matrix and goodness of fit metrics
			 
'''
#Regex
import glob # Unix style GLOB performs pattern matching on files
import re

#Datascience stuff
import pandas as pd 
import numpy as np 

#ML stuff
from sklearn.metrics import cohen_kappa_score



# Relative path to dataset
DATASET_PATH='../locality-sensitive-hashing/datasets/'
DISTANCE_MATRICES_PATTERN=DATASET_PATH + '*_distance_matrix.txt'
CLUSTER_MODELS_PATTERN=DATASET_PATH + '*_cluster.txt'



def cluster2txt(cluster, filename='distance_cluster.txt'):
	'''
		Persists cluster as txt
		INPUT 
			cluster<dict<int,int>>: cluster dict int, int 

			filename<string>: Name of the file to be generated

		OUTPUT
			- 				
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
		

def scoring(pattern_evaluate, pattern_gs='goldenset.csv', metrics_filename='confusion_matrix.txt'):
	'''
		Scans dataset for clusters glob matching pattern_evaluate and compares 
		against glob matching pattern_gs
		which is a count over a pair of clusters which neighbours agree

		INPUT 
			pattern_evaluate<str>

			pattern_gs<str>


		OUTPUT
			scoring<float<M,M>>: cross model comparison			
	'''	
	# matcher 				 = re.compile('(.*)_cluster.txt$')
	# pattern_evaluate1= DATASET_PATH + pattern_evaluate
	# files=glob.glob(pattern_evaluate1)	
	# M=len(files)
	# print('%d files found matching r\'%s\' suffix' % (M,pattern_gs))

	# names=[]
	# for i, file in enumerate(files):	
		
	# 	filename_i=file.split('/')[-1]
	# 	matchings= matcher.match(filename_i)
	# 	data_model=matchings.groups()[0]		

	# 	print('Fetching %d\t%s...' % (i+1,data_model))				
	# 	if i==0:
	# 		df= pd.read_csv(file, sep= ' ', index_col=0, header=None)		
	# 		df.columns=[data_model] 
	# 	else:
	# 		df_tmp= pd.read_csv(file, sep= ' ', index_col=0, header=None)		
	# 		df_tmp.columns=[data_model] 
	# 		df=pd.concat((df,df_tmp),axis=1)
	# 	names.append(data_model)
	# 	print('Fetching %d\t%s...done' % (i+1,data_model))				

	df_eval= df_cluster(pattern_evaluate)
	df_gs= df_cluster(pattern_gs)
	M = df_eval.shape[0] 
	N = df_gs.shape[0]


	D= np.zeros((M*N,9), dtype=np.float32)
	index=[]
	columns=[]
	count=0
	for m in range(M):
		for n in range(N):
			col_namem= list(df_eval.columns.names)[m]
			col_namen= list(df_gs.columns.names)[n]
			print('%d of %d Confusion matrix: %s vs %s...' % (count+1,N*M,col_namem,col_namen))				

			index.append( '%sx%s' % (col_namem,col_namen))

			#Sync data
			data=df_eval[col_namem].join(df_gs, how='inner')
			x=dict(zip(data.index,data[labelm]))
			y=dict(zip(data.index,data[labeln]))
			metrics=confusion_matrix_scoring(x, y)
				# import code; code.interact(local=dict(globals(), **locals()))
			D[count,:]=np.ndarray(metrics)
			# 	import code; code.interact(local=dict(globals(), **locals()))
			# S[r,c]=agreeableness_score(x,y)
			# S[r,c]=fn_score(x,y)
			
			print('%d of %d Confusion matrix: %s vs %s...' % (count+1,N*M,col_namem,col_namen))				
			count+=1			

	print(list(df.columns))		
	print(S)
	headers=['a','b','c','d','A','P','R','F-1','J']
	df=pd.DataFrame(data=S, columns=headers, index=index)
	df.to_csv(DATASET_PATH + metrics_filename, sep=' ')


def df_cluster(str_pattern):
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
	names=[]
	for i, file in enumerate(files):			
		colname=get_filename(file)

		print('Fetching %d\t%s...' % (i+1, colname))				
		if i==0:
			df= pd.read_csv(file, index_col=0, header=None)		
			df.columns=[colname] 
		else:
			df_tmp= pd.read_csv(file, index_col=0, header=None)		
			df_tmp.columns=[colname] 
			df=pd.concat((df,df_tmp),axis=1)
		

		print('Fetching %d\t%s...done' % (i+1,colname))				

	return df 	

def get_filename(filename):	
	'''
		Removes filename's prefix and suffix
		INPUT
			filename<str>: fullname path
		
		OUTPUT
			filename1<str>: filename without extension or file_system stuff
				
	'''
	filename1= filename.split('/')[-1]
	filename_parts= filename1.split('.')[:-2]
	filename1= '.'.join(filename_parts)
	return filename1

def agreeableness_score(c1, c2):
	'''
		Computes the aggreableness score 
		Count over a pair of clusters which neighbours agree

		INPUT 
			c1<list<int>>: cluster 1 labels

			c2<list<int>>: cluster 2 labels

		OUTPUT
			scoring<float<M,M>>: cross model comparison			
	'''	

	D = len(c1)
	c1_dict=dict(zip(range(D),c1))
	c2_dict=dict(zip(range(D),c2))

	
	c1_neighbours=mapping_neighbour(c1_dict)
	c2_neighbours=mapping_neighbour(c2_dict)

	count=0
	for i in range(D):
		factor_1 = c1_neighbours[i].intersection(c2_neighbours[i])
		factor_2 = c1_neighbours[i].union(c2_neighbours[i])
		count+= float(len(factor_1)) / len(factor_2)

	return float(count)/D	

def mapping_neighbour(cluster_dict):
	'''
		Receives a cluster dict and computes a neightbourhood dict

		INPUT
			cluster_dict<int,int>: each value from the cluster dict is an integer

		OUTPUT
			neighbour_dict<int,set<int>>: each value from the neightbour dict is a set of integers of variable size
		
		
	'''	
	neighbours_mapping={}
	for key, value in this_dict.items():
		if value in neighbours_mapping:
			neighbours_mapping[value].append(key)
		else:
			neighbours_mapping[value]=[key]	
	return {key:set(neighbours_mapping[value]) for key, value in this_dict.items()}	

def mapping_pairs(neighbour_dict):
	'''
		Receives a neighbour dict which is a dict of sets

		INPUT
			neighbour_dict<int,set<int>>: each value from the neightbour dict is a set of integers of variable size

		OUTPUT
			set<set<int>>: is a set of sets: the inner set has either one element or a pair 

	'''
	processed_docs=[]
	list_of_sets=[]
	for doc_id, doc_neigh in neighbour_dict.items():
		if not(doc_id in processed_docs):
			l= len(doc_neigh)	
			if l==1:
				new_set=doc_neigh
			else:
				new_set= set([[set([i,j])] for i in range(l-1) for j in range(i+1,l)])	
			processed_docs+=list(new_set)
			list_of_sets.append(new_set)
			
	return set(list_of_sets)


def confusion_matrix_scoring(c_a, c_b):
	'''
		Receives 2 clusters as list
		Computes a list with the following items
		* Flattened confusion matrix
		* Accuracy
		* Precision
		* Recall
		* F-1
		* Rand Index
		* Jaccard


		INPUT
			c_a dict<key:<int>,value<?>>: key is the observationid value is the clusterid (any comparable value)

			c_b dict<key:<int>,value<?>>: key is the observationid value is the clusterid (any comparable value)

		OUTPUT
			list<float[9]>:
				0-3 Flattened confusion matrix: 
					a true positives
					b false negatives
					c false positives
					d true negatives
				4 accuracy= (a + d)/(a + b + c + d) =rand_index
				5 precision=(a)/(a + c)=p
				6 recall=a/(a+b)
				7 F-1=  2*(recall*precision)/(recall+precision)				
				8 jaccard=(a)/(a+b+c)	
	'''	
	if not(len(c_a) == len(c_b)):
		msg='length of clusters must aggree got c_a[%d] vs c_b[%d]' % (len(c_a),len(c_b))
		raise ValueError(msg) 
	else:
		n=len(c_a)
	u=mapping_pairs(mapping_neighbour(c_a))
	v=mapping_pairs(mapping_neighbour(c_b))


	is_pair = lambda x: len(x)==2
	u_p= filter(is_pair,u)
	u_s= u - u_p
	v_p= filter(is_pair,v)
	v_s= v - v_p

	# c11: count (pairs) u in v (intersection) : 
	# both models aggree: True Positive, repetitions
	a = len(u_p in v_p) 
	# c12: count (pairs) u - v 	(set diff) 		 : 
	# models disaggree: repetions in u and not in v
	b = len(u_p - v_p) 
	# c21: count (pairs) v - u  (intersection)
	# models disaggree: repetions in v and not in u
	c = len(v_p - u_p) 
	# c22: count (pairs) u  v 	(set diff)
	d= len(u_s)+len(v_s)+n*(n-1)*0.5-(a+b+c)


	accuracy= float(a + d)/(a + b + c + d)

  precision= float(a)/(a + c)

	recall= float(a)/(a + b)

	f1_measure= 2*float(recall*precision)/(recall+precision)

	jaccard= float(a)/(a+b+c)

	return [a,b,c,d,accuracy,precision,recall,f1_measure,jaccard]


def distance_matrix_clustering():
	'''
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
		# import code; code.interact(local=dict(globals(), **locals()))
		print('Clustering of %s...' % (data_model))
		cluster_filename=data_model+'_cluster.txt'
		cluster=clusterize(dist)
		print('Clustering of %s...done' % (data_model))
		cluster2txt(cluster, filename=cluster_filename)




if __name__ == '__main__'	:

	# fn_score= lambda x,y :  agreeableness_score(x, y)
	# filename='aggreableness_score.txt'

	# scoring(fn_score, filename)
	confusion_matrix_scoring('gaussian_0.3_cluster.txt')

