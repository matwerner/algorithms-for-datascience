# -*- coding: utf-8 -*-
'''
	Created on Nov 28, 2017

	@author: Varela

	motivation: Distance matrix models
			 
'''
import pandas as pd 
from utils import get_stemmer, get_stopwords, tokenizer2, data2idx, data2bow, bow2dist, matrix2txt, word2idx2txt  

import argparse

# Relative path to dataset
DATASET_PATH='../locality-sensitive-hashing/datasets/' 


def main(distance_type,  refresh):
	'''	
		INPUT
		distance_type<string>: Gaussian for gaussian projection OR
				Sparse 	 for Achiloptas projection
				default: Sparse

		refresh<bool>: refreshes data model, recomputing word2idx, bow

		OUTPUT
			dist<float<D,D>>: matrix of distances using random projections algorithm
			values are always saved following the pattern <projection>_<eps>_distance_matrix.txt						
				D: original count of documents


		
	'''		


	filename_distance_matrix= '%s_distance_matrix.txt' % (distance_type)	

	if refresh:		
		devel_path= DATASET_PATH + 'development.json'
		print('reading...\r')
		data = pd.read_json(devel_path, orient='records')	
		print('reading...done\r')

		print('')
		print('tokenizing...\r')
		this_stemmer= get_stemmer()
		this_stopwords=get_stopwords()
		tokenfy = lambda x : tokenizer2(x, stemmer=this_stemmer, stopwords=this_stopwords)
	
		data['token_description']=data['description'].apply(tokenfy)
		print('tokenizing...done\r')

		print('')
		print('indexing...\r')
		word2idx={}
		data=data2idx(data, word2idx, colname='token_description', new_colname='idx_description')
		print('indexing...done\r')


		print('')
		print('generating bag of words...\r')
		print('')
		bow2=data2bow(data, word2idx)
		print('generating bag of words...done\r')

	else:
		print('')
		print('retrieving word2idx...')
		word2idx_path=  DATASET_PATH + 'word2idx2.txt'
		df= pd.read_csv(word2idx_path, sep= ' ', index_col=0, header=None)		
		word2idx= {k:v for k, v in zip(df.index, df.iloc[:,0]) } 
		print('retrieving word2idx...done')

		print('retrieving bow2...')
		bow2_path=  DATASET_PATH + 'bow2.txt'
		df= pd.read_csv(bow2_path, sep= ' ', index_col=None, header=None, skiprows=1 ) 
		bow2= df.as_matrix()
		print('retrieving bow2...done')
	

	print('')
	print('compute %s distance...\r' % (distance_type))
	dist=bow2dist(bow2, verbose=True, distance_type=distance_type)
	print('compute %s distance...done\r' % (distance_type))
	
	print('')
	print('storing %s distance matrix...\r' % (distance_type))
	
	matrix2txt(dist, filename=filename_distance_matrix)
	print('storing %s distance matrix...done\r' % (distance_type))	

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Computes distance matrix')

	parser.add_argument('-d', action="store", dest="distance_type", type=str, default='euclidian', 
		help="""Permitted values are euclidian, jaccard, normalize stores following the pattern
		<distance_type>_distance_matrix.txt\n""")

	parser.add_argument('-r', action="store", dest="refresh", type=str2bool, default=False,
	help="""refreshes data model: tokenization, word2idx and bow\n""")

	args = parser.parse_args()

	distance_type = args.distance_type
	refresh = args.refresh 

	params=(distance_type, refresh)  

	print('starting distance matrix computation:')  
	print('distance_type:%s\trefresh:%d'% params)  
	main(distance_type, refresh)