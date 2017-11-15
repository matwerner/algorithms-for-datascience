'''
	author: Guilherme Varela
	
	Utility functions for text edition
'''
import numpy as np 
import string 
import sys 

from nltk.corpus import stopwords as _stopwords
from nltk.stem import * 



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


def matrix2txt(mtrx, filename='mtrx.txt'):
	'''		
		mtrx is a numpy matrix
		writes the bow matrix to text, or distance matrix to text
	'''	
	path= '../../locality-sensitive-hashing/datasets/' + filename	
	n_headers=bow.shape[1]-2
	headers = list(bow.shape) + ['']*n_headers
	df = pd.DataFrame(data=bow.astype(np.int32), columns=headers, index=None)
	df.to_csv(path, sep=' ',index=False, index_label=False)


def data2bow(data, word2idx):
	'''	
		Converts idx_description to bow a VxD
		D: documents (idx_description)		
		V: Vocabulary
		
	'''	
	nrows= data.shape[0]
	ncols=len(word2idx)
	bow= np.zeros((nrows, ncols),dtype=np.int32)
	for r in range(nrows):		
		indexes=list(map(int,data.loc[r,'idx_description'].split(' '))	)		
		for c in indexes:
			bow[r, c]+=1

	return bow.T  

def data2idx(data, word2idx):
	'''	
		Converts a token_description column to idx_description
	'''	
	nrows=data.shape[0]
	token_count=0
	for i in range(nrows):
		# import code; code.interact(local=dict(globals(), **locals()))
		tokens=data.loc[i,'token_description'].split(' ')	
		indexes= token2idx(tokens , word2idx)
		token_count+=len(indexes)
		data.loc[i,'token_description']=" ".join([str(idx) for idx in indexes])
		
		sys.stdout.write('document:%d of %d\tVOCAB:%d\tWORD COUNT:%d\t\r' % (i, nrows, len(word2idx), token_count))
		sys.stdout.flush()
	data= data.rename(columns={'token_description': 'idx_description'})
	print()
	return data 

def token2idx(tokens, word2idx):
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
# 	'''
# 		s is a string with punctuation; converts unicode to string which might get data loss
# 			url: https://stackoverflow.com/questions/23175809/typeerror-translate-takes-one-argument-2-given-python
# 					 https://pypi.python.org/pypi/Unidecode
# 					 https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
# 	'''	
# 	# return str(s).translate(None, string.punctuation)
	# s = unidecode.unidecode(s) # Converts unicode s into closest ascii s, removes accents
# 	if s: 
# 		# This uses the 3-argument version of str.maketrans
# 		# with arguments (x, y, z) where 'x' and 'y'
# 		# must be equal-length strings and characters in 'x'
# 		# are replaced by characters in 'y'. 'z'
# 		# is a string (string.punctuation here)
# 		# where each character in the string is mapped
# 		# to None
	s= s.translate(str.maketrans('','',string.punctuation)) # removes punctuation
	s= s.translate(str.maketrans('','','\n')) 							# removes \n
	s= s.translate(str.maketrans('','','\t')) 							# removes \t
	s= s.translate(str.maketrans('','','\r')) 							# removes \r

	return s
