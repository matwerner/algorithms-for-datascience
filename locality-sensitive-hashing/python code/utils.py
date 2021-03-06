'''
	author: Guilherme Varela
	
	Utility functions for text edition
'''

import glob # Unix style GLOB performs pattern matching on files

#Invoking cmd line experiments 
import argparse

import pandas as pd 
import numpy as np 
import string 
import sys 
import re

#making some profiling 
from datetime import datetime


from nltk.corpus import stopwords as _stopwords
from nltk.stem import * 

from sklearn.metrics import jaccard_similarity_score

INVALID_TOKENS=[None, '', ' ']

DATASET_PATH= '../../locality-sensitive-hashing/datasets/'
PROFILE_PATH= '../../locality-sensitive-hashing/profiles/'

def tokenizer2(rawtxt, stopwords=None, stemmer=None): 
	'''
		INPUT
			rawtxt a string with arbitrary characters

		OUTPUT
			string: list of words complient with
						word in a-z, A-Z, 0-9, / 
						special portuguese characters also included: ã, ç, há
						^[a-z\u00E0-\u00FCA-Z\u00E0-\u00FC]+$/i

	'''
	txt= preprocess(str(rawtxt))
	tokens= txt.split(' ')
	tokens= [t for t in tokens if not(t in INVALID_TOKENS)]
		
	if stopwords is None:
		stopwords= get_stopwords()

	if stemmer is None:
		stemmer= get_stemmer()		

	tokens = [t.lower() for t in tokens] 							  # to lowercase	
	tokens = [t for t in tokens if t not in stopwords]  # remove stopwords
	tokens = [stemmer.stem(t) for t in tokens] 					# stemmify			
	tokens = [re.sub(r'[^a-z0-9]','', t) for t in tokens]
	tokens = [t for t in tokens if not(t in INVALID_TOKENS)]

	return ' '.join(tokens)

def preprocess(rawtxt):
	'''
		Performs operations on entire rawtxt (word set)

		INPUT
			rawtxt a string with arbitrary characters. 

		OUTPUT
			txt: list of words complient with
						word in a-z, A-Z, 0-9, / 
						special portuguese characters also included: ã, ç, há
						^[a-z\u00E0-\u00FCA-Z\u00E0-\u00FC]+$/i

	'''
	txt = remove_puctuation(rawtxt)

	#every invalid character is a split word
	txt= re.sub(r'^[a-z\u00E0-\u00FCA-Z\u00E0-\u00FC]+$/i', ' ', txt)
	return txt



def tokenizer(sentences, stopwords=None, stemmer=None): 
	# print('%s\r' %(tokens))
	tokens= str(sentences).split(' ')
	tokens= [t for t in tokens if not(t=='')]
	# import code; code.interact(local=dict(globals(), **locals()))
	
	if stopwords is None:
		stopwords= get_stopwords()

	if stemmer is None:
		stemmer= get_stemmer()		

	tokens = [t.lower() for t in tokens] 							 # to lowercase	
	tokens = [remove_puctuation(t) for t in tokens] 	
	tokens = [t for t in tokens if t not in stopwords] # remove stopwords
	tokens = [stemmer.stem(t) for t in tokens] 				# stemmify	
	tokens = [t for t in tokens if not(t == None)]
	
	return ' '.join(tokens)


def bow2dist(bow, verbose=True, distance_type='normalize'):
	'''		
	INPUT
		bow: bag-of-words VxD numpy matrix 		

	OUTPUT	
		dist: distance DxD lower triangular matrix

	'''	
	d = bow.shape[1]
	dist=np.zeros((d,d), dtype=np.float32)
	starttime= datetime.now()
	total= d*(d-1)*0.5
	counter=0
	doc_norm={}
	#Preprocessing bow
	if distance_type=='jaccard':
		bow=bow.astype(bool)

	if distance_type=='euclidian':
		doc_norm={key:1 for key in range(d)}

	if distance_type=='normalize':
		doc_norm={key:np.linalg.norm(bow[:,key]) for key in range(d)}
	
	for i in range(d):
		for j in range(0,i):
			if distance_type=='jaccard':				
				dist[i,j]=1-jaccard_similarity_score(bow[:,i], bow[:,j])
			else:
 				dist[i,j]=compute_distance(bow[:,i], bow[:,j], norm_x=doc_norm[i], norm_y=doc_norm[j])	

			if verbose:
				status= (i,j,dist[i,j], elapsed_time(starttime), float(counter) *100 / total)				
				sys.stdout.write('%05d,%05d:\t%0.2f\t\tELAPSED TIME:%s\tCOMPLETE:%.2f\r' % status)
				sys.stdout.flush()
			counter+=1
	print('')				
	return dist

def compute_jaccard_distance(x, y):
	'''		
	Computes jaccard distance between arrays x, y 
	jaccard distance: (x in y) / (x union y)

	INPUT
		x<int<V,1>>: column of bow

		y<int<V,1>>: column of bow

	
	OUTPUT
		dist<float>: dist in [0.0,1.0]
	
	'''	
	ind_x= x>0 
	ind_y= y>0
	return float(sum(ind_x & ind_y))/(sum(ind_x)+sum(ind_y))

def compute_distance(x, y, norm_x=1, norm_y=1):	
	'''		
	Computes eulidian / normalized distance between arrays x, y 

	INPUT
		x<int<V,1>>: column of bow

		y<int<V,1>>: column of bow

	
	OUTPUT
		dist<float>: dist in [0.0,1.0] if normx != 1  and normy != 1 
	
	'''	
	diff = x-y
	return np.sqrt(np.dot(diff,diff))/(norm_x*norm_y)  


def matrix2txt(mtrx, filename='mtrx.txt'):
	'''		
	Stores numpy matrix to a file

	INPUT
		mtrx: a generic numpy matrix ex: bow or dist
	
		filename: name for the text file
						default:'mtrx.txt'

	OUTPUT
		matrix representation in text format
		header: nrows ncols
		body: matrix
	'''	
	path= DATASET_PATH + filename	
	n_headers=mtrx.shape[1]-2
	headers = list(mtrx.shape) + ['']*n_headers
	df = pd.DataFrame(data=mtrx.astype(np.int32), columns=headers, index=None)
	df.to_csv(path, sep=' ',index=False, index_label=False)


def word2idx2txt(word2idx,filename='word2idx.txt'):
	'''		
	Stores word2idx dictionary to a file

	INPUT
		word2idx: dict(keys:tokens,values:integer)											

		filename: name for the text file
						default:'word2idx.txt'

	OUTPUT
		-
	'''	
	idx2word = {v:k for k,v in word2idx.items()}        
	path= DATASET_PATH + filename	
	df = pd.DataFrame.from_dict(idx2word,orient='index')
	df.to_csv(path, sep=' ',index=True, index_label=False,header=None)


def data2bow(data, word2idx, colname='idx_description'):
	'''	
		INPUT
			data: a pandas.DataFrame
							processes column idx_description
			
			word2idx: dict(keys:tokens,values:integer)											

			colname: pandas.DataFrame column to process
							default: 'idx_description'

		OUTPUT
			bow: bag-of-words VxD numpy matrix 		
					D: documents 
					V: Vocabulary
			example: if word w<=>idx appears 10 times on document d then
					bow[idx,d]=10

	'''	
	nrows= data.shape[0]
	ncols=len(word2idx)
	bow= np.zeros((nrows, ncols),dtype=np.int32)
	starttime= datetime.now()
	for r in range(nrows):		
		indexes=list(map(int,data.loc[r,colname].split(' '))	)		
		for i, c in enumerate(indexes):
			bow[r, c]+=1
			status= (r, ncols, i, len(indexes), elapsed_time(starttime))
			sys.stdout.write('data2bow:%d of %d\ttokens in documents:%d of %d\t\tELAPSED TIME:%s\r' % status)
			sys.stdout.flush()
			

	return bow.T  

def data2idx(data, word2idx, colname='token_description', new_colname='idx_description'):
	'''	
		INPUT
			data: pandas.DataFrame

			word2idx: dict(keys:tokens,values:integer)											

			colname: pandas.DataFrame column to process
							default: 'idx_description'

		OUTPUT
			data: pandas.DataFrame
						column: token_description -> idx_description
		
	'''	
	nrows=data.shape[0]
	token_count=0
	starttime= datetime.now()
	for i in range(nrows):
		# import code; code.interact(local=dict(globals(), **locals()))
		tokens=data.loc[i,colname].split(' ')	
		indexes= token2idx(tokens , word2idx)
		token_count+=len(indexes)
		data.loc[i,colname]=" ".join([str(idx) for idx in indexes])		

		status=(i, nrows, len(word2idx), token_count, elapsed_time(starttime))
		sys.stdout.write('data2idx:%d of %d\tVOCAB:%d\tWORD COUNT:%d\t\tELAPSED TIME:%s\r' % status)
		sys.stdout.flush()

	if new_colname:	
		old2new={}
		old2new[colname]=new_colname
		data= data.rename(columns=old2new)		
	print('')
	return data 

def token2idx(tokens, word2idx):
	'''	
		INPUT
			tokens: a list of strings
							
			word2idx: dict(keys:tokens,values:integer)				

		OUTPUT
			bow: bag-of-words VxD numpy matrix 		
					D: documents (idx_description)		
					V: Vocabulary
		
	'''	
	nextidx= max(word2idx.values())+1 if len(word2idx)>0  else 0	
	indexes= [] 
	for t in tokens:
		if not(t in word2idx):
			word2idx[t]=nextidx
			nextidx+=1
		indexes.append(word2idx[t]) 
	return indexes


def get_stopwords(lang='portuguese'):	
	return set(_stopwords.words(lang))		

def get_stemmer(lang='portuguese'):
	return SnowballStemmer(lang) 

def remove_puctuation(s):
	'''
		replaces punctuation with space

		INPUT 
		s unformated string
		s is a string with punctuation; converts unicode to string which might get data loss
 				url: https://stackoverflow.com/questions/23175809/typeerror-translate-takes-one-argument-2-given-python
 					 https://pypi.python.org/pypi/Unidecode
 					 https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
 	'''	
	delimiters=  string.punctuation 
	delimiters+= '\n\r\t' 												# additions
	this_translation=str.maketrans(delimiters,' '*len(delimiters))
	s= s.translate(this_translation) # removes punctuation	 								
	return s

def elapsed_time(starttime):
	this_timedelta= datetime.now() - starttime
	return str(this_timedelta).split('.')[0]

def profiles_pivot():
	'''
		Reads glob from profiles, saving a pivot table @ profile		
		
	'''
	matcher = re.compile(PROFILE_PATH +'(.*)_profiler')
	files=glob.glob(PROFILE_PATH + '*.txt')	
	# import code; code.interact(local=dict(globals(), **locals()))
	newcolumns=['model', 'eps', 'dim']
	dataframes=[]
	pivotframes=[]
	for i,f in enumerate(files):
		#Parse filename
		matched=matcher.match(f)
		filename=matched.groups()[0]
		newvalues=filename.split('_')

		#Fetch data
		df = pd.read_csv(f, sep=' ', header=None, index_col=None)
		df.columns=['task', 'time']

		#Add new data
		for j,newcol in enumerate(newcolumns):
			df[newcol]= newvalues[j]

		#add
		dataframes.append(df)
	
	df=pd.concat(dataframes, axis=0, ignore_index=True)
	df['time'] = pd.to_timedelta(df['time'])
	df['seconds']  = df['time'].dt.total_seconds()
	# import code; code.interact(local=dict(globals(), **locals()))
	df1=pd.pivot_table(df,values=['seconds'],index=['model','eps','dim','task'],aggfunc=len)
	df1.columns=['N']
	pivotframes.append(df1)

	df1  =pd.pivot_table(df,values=['seconds'],index=['model','eps','dim','task'],aggfunc=np.mean)
	df1.columns=['Avg.']
	pivotframes.append(df1)

	df1   =pd.pivot_table(df,values=['seconds'],index=['model','eps','dim','task'],aggfunc=np.std)	
	df1.columns=['Std.']
	pivotframes.append(df1)

	df1   =pd.pivot_table(df,values=['seconds'],index=['model','eps','dim','task'],aggfunc=np.min)
	df1.columns=['Min.']
	pivotframes.append(df1)

	df1   =pd.pivot_table(df,values=['seconds'],index=['model','eps','dim','task'],aggfunc=np.max)
	df1.columns=['Max.']
	pivotframes.append(df1)

	df_pivot= pd.concat(pivotframes, axis=1)
	df_pivot.to_csv(DATASET_PATH + 'statistics_profiler.txt', sep=' ')

if __name__ == '__main__':
	profiles_pivot()


