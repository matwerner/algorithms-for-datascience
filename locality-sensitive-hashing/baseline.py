# -*- coding: utf-8 -*-
'''
	Created on Nov 28, 2017

	@author: Varela

	motivation: Distance matrix models
			 
'''
def main(projection_type, eps, store, refresh):
	'''	
		INPUT
		projection_type<string>: Gaussian for gaussian projection OR
				Sparse 	 for Achiloptas projection
				default: Sparse

		eps<float>: threshold for acceptable distorsions 
				higher eps -> higher theoretical probability of distorsions
				is bounded between 0-1

		refresh<bool>: refreshes data model, recomputing word2idx, bow

		store<bool>: stores 3 intermediary results: word2idx, bow, proj_bow. 

		OUTPUT
			dist<float<D,D>>: matrix of distances using random projections algorithm
			values are always saved following the pattern <projection>_<eps>_distance_matrix.txt						
				D: original count of documents

			<int<v,D>>: matrix of distances using random projections algorithm
			values are always saved following the pattern <projection>_<eps>_bow.txt									
				v<int>: v<<V is the new vocabulary size 
				D<int>: original count of documents			

		
	'''		


	filename_distance_matrix= '%s_%.1f_distance_matrix.txt' % (projection_type, eps)	
	filename_projection_bow=  '%s_%.1f_bow.txt' % (projection_type, eps)	

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

		if store: 
			print('')
			print('storing indexes...\r')
			word2idx2txt(word2idx, filename='word2idx2.txt')
			print('storing indexes...done\r')
		
			print('')
			print('storing bag of words...')
			matrix2txt(bow2, filename='bow2.txt')
			print('storing bag of words...done\r')

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
	print('compute random projection...\r')	
	proj= bow2rnd_proj(bow2, projection_type=projection_type, eps=eps)
	print('compute random projection... done new (reduced) dimensions:%dx%d\r' % proj.shape)

	if store: 
		print('')
		print('storing bag of words...\r')
		matrix2txt(proj, filename=filename_projection_bow)
		print('storing bag of words...done\r')

	print('')
	print('compute %s distance...\r' % (projection_type))
	proj_dist=bow2dist(proj)
	print('compute %s distance...done\r' % (projection_type))
	
	print('')
	print('storing %s distance matrix...\r' % (projection_type))
	
	matrix2txt(proj_dist, filename=filename_distance_matrix)
	print('storing %s distance matrix...done\r' % (projection_type))	

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