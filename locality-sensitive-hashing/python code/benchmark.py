# -*- coding: utf-8 -*-
'''
	Created on Nov 24, 2017

	@author: Varela

	motivation: Benchmark module provinding goodness of fit metrics
			 
	clutch: import code; code.interact(local=dict(globals(), **locals()))				 	
'''
#Regex
import glob # Unix style GLOB performs pattern matching on files
import re

#Datascience stuff
import pandas as pd 
import numpy as np 

#Command line parsing 
import argparse

#cluster transformation functions
from cluster_helper import cluster_txt2df, cluster_dict2set, cluster_set2pairwise

# Relative path to dataset
DATASET_PATH='../../locality-sensitive-hashing/datasets/'
# Fullpath
# DATASET_PATH='/Users/guilhermevarela/wrk/py/gv/algorithms-for-datascience/locality-sensitive-hashing/datasets/' 
DISTANCE_MATRICES_PATTERN=DATASET_PATH + '*_distance_matrix.txt'
CLUSTER_MODELS_PATTERN=DATASET_PATH + '*_cluster.txt'

def scoring(pattern_evaluate, pattern_gs='goldenset.csv', metrics_filename='confusion_matrix.txt'):
	'''
		Scans dataset for clusters glob matching pattern_evaluate and compares 
		against glob matching pattern_gs
		which is a count over a pair of clusters which neighbours agree

		INPUT 
			pattern_evaluate<str>: This is a string pattern to match a filename

			pattern_gs<str>:


		OUTPUT
			scoring<float<M,M>>: cross model comparison			
	'''	
	df_eval=   cluster_txt2df(pattern_evaluate)
	df_gs=   cluster_txt2df(pattern_gs)

	M = df_eval.shape[1] 
	N = df_gs.shape[1]
	fposneg={}
	D= np.zeros((M*N,9), dtype=np.float32)
	index=[]
	columns=[]
	count=0
	for m in range(M):
		for n in range(N):
			colname_m= list(df_eval.columns)[m]
			colname_n= list(df_gs.columns)[n]
			print('%d of %d Confusion matrix: %s vs %s...' % (count+1,N*M,colname_m,colname_n))				
			


			index.append( '%s_x_%s' % (colname_m,colname_n))

			#Sync data			
			data=df_gs[colname_n].to_frame()			
			data=data.join(df_eval[colname_m].to_frame(), how='inner')

			x=dict(zip(data.index,data[colname_m]))
			y=dict(zip(data.index,data[colname_n]))
			metrics,f_positives, f_negatives=confusion_matrix_scoring(x, y)
			#update false positive false negative			
			fposneg=update_fposneg(fposneg, f_positives, f_negatives, index[-1])

			D[count,:]=np.array(metrics)
			print('%d of %d Confusion matrix: %s vs %s...' % (count+1,N*M,colname_m,colname_n))				
			count+=1			

	headers=['a','b','c','d','A','P','R','F-1','J']	
	df=pd.DataFrame(data=D, columns=headers, index=index)
	print(df)
	df.to_csv(DATASET_PATH + metrics_filename, sep=' ')

	posneg_filename=str(metrics_filename)
	posneg_filename=posneg_filename.replace('matrix', 'pos_neg')
	
	headers=['i','j','pos_neg','files']	
	df=pd.DataFrame.from_dict(fposneg, orient='index')
	df.columns=headers
	print(df.head())
	df.to_csv(DATASET_PATH + posneg_filename, sep=' ')



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

	u_dupl,u_uniq=cluster_set2pairwise( cluster_dict2set(c_a))
	v_dupl,v_uniq=cluster_set2pairwise( cluster_dict2set(c_b))
	
	# c11: count (pairs) u in v (intersection) : 
	# both models aggree: True Positive, repetitions
	a = len(u_dupl & v_dupl) 
	# c12: count (pairs) u - v 	(set diff) 		 : 
	# models disaggree: repetions in u and not in v
	false_positives=u_dupl - v_dupl
	b = len(false_positives) 
	# c21: count (pairs) v - u  (intersection)
	# models disaggree: repetions in v and not in u
	false_negatives=v_dupl - u_dupl	
	c = len(false_negatives)  
	# c22: count (pairs) u  v 	(set diff)
	d= len(u_uniq)+len(v_uniq)+n*(n-1)*0.5-(a+b+c)


	accuracy= float(a + d)/(a + b + c + d)

	precision= float(a)/(a + c)

	recall= float(a)/(a + b)

	f1_measure= 2*float(recall*precision)/(recall+precision) if recall+precision>0 else 0

	jaccard= float(a)/(a+b+c)

	return [a,b,c,d,accuracy,precision,recall,f1_measure,jaccard],list(false_positives),list(false_negatives)



def update_fposneg(fposneg, f_pos, f_neg, name):
	counter=len(fposneg)
	for fs in f_pos:
		row_list=list(fs)
		row_list.append('fp')
		row_list.append(name)
		fposneg[counter]=row_list
		counter+=1

	for fs in f_neg:
		row_list=list(fs)
		row_list.append('fn')
		row_list.append(name)
		fposneg[counter]=row_list
		counter+=1		

	return fposneg

	


if __name__ == '__main__'	:	
	# Example  1 class example
	# scoring('toyU_cluster.txt', 'toyV_cluster.txt', 'toy_confusion_matrix.txt')
	# Example  2  using gaussian_0.3_cluster.txt as benchmark
	# scoring('gaussian_0.5_cluster.txt', 'gaussian_0.3_cluster.txt', 'gaussian_confusion_matrix.txt')
	# Example  3  using goldenset.csv as benchmark
	# scoring('gaussian_0.3_cluster.txt')
	# Example  4  benchmark all clusters with a single call
	# scoring('*_cluster.txt')
	parser = argparse.ArgumentParser(description='Computes confusion matrix and metrics for models')

	parser.add_argument('-f', action="store", dest="pattern_evaluate", type=str, default='*_cluster.txt', 
		help="Input cluster filename or pattern to benchmark\n")

	parser.add_argument('-g', action="store", dest="pattern_gs", type=str, default='goldenset.csv',
		help="Golden-standard cluster filename or pattern to benchmark against\n")

	parser.add_argument('-o', action="store", dest="filename", type=str, default='confusion_matrix',
	help="""Output filename to store output data\n""")

	args = parser.parse_args()

	pattern_eval = args.pattern_evaluate
	pattern_gs = args.pattern_gs
	metrics_filename = args.filename

	# main(projection_type, eps, store, refresh)	
	scoring(pattern_eval, pattern_gs=pattern_gs, metrics_filename=metrics_filename)
