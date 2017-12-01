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
		

def kappa_scoring():
	'''
		INPUT 
			cluster<dict<int,int>>: cluster dict int, int 

		OUTPUT
			scoring<float<M,M>>: cross model comparison			
	'''	
	matcher = re.compile('(.*)_cluster.txt$')
	files=glob.glob(CLUSTER_MODELS_PATTERN)	
	M=len(files)
	print('%d files found matching _cluster.txt suffix' % M)

	names=[]
	for i, file in enumerate(files):	
		
		filename=file.split('/')[-1]
		matchings= matcher.match(filename)
		data_model=matchings.groups()[0]		

		print('Fetching %d\t%s...' % (i+1,data_model))				
		if i==0:
			df= pd.read_csv(file, sep= ' ', index_col=0, header=None)		
			df.columns=[data_model] 
		else:
			df_tmp= pd.read_csv(file, sep= ' ', index_col=0, header=None)		
			df_tmp.columns=[data_model] 
			df=pd.concat((df,df_tmp),axis=1)
		names.append(data_model)
		print('Fetching %d\t%s...done' % (i+1,data_model))				


	S= np.zeros((M,M), dtype=np.float32)
	N = M*(M-1)/2 + M
	n=0
	for r in range(M-1):
		for c in range(r,M):
			
			print('%d of %d computing %s vs %s...' % (n+1,N,names[r],names[c]))				
			x=df[names[r]].as_matrix()
			y=df[names[c]].as_matrix()
			# 	import code; code.interact(local=dict(globals(), **locals()))
			S[r,c]=cohen_kappa_score(x,y)
			print('%d of %d computing %s vs %s...done' % (n+1,N,names[r],names[c]))				
			n+=1			
	print(list(df.columns))		
	print(S)
	df_kappa=pd.DataFrame(data=S, columns=df.columns,index=df.columns)
	df_kappa.to_csv(DATASET_PATH + 'kappa_score.txt', sep=' ')

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
	# distance_matrix_clustering()
	kappa_scoring()

