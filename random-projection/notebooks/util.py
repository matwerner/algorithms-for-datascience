'''
Created on Sep 09, 2017

@author: Varela

motivation: useful cross module corpora functions; such as tokenization
'''
import string 
import numpy as np 

def flatten(l):
	'''		
		l is a list of list, in our case a list of list of words		

		returns
		f : a flattened list 
	'''
	f = [item for sublist in l for item in sublist] 
	return f

def document2bag_of_words(doc2idx, word2idx): 
		'''
		Converts a doc2idx to a bag of words

		Returns
			bow: is a numpy matrix of size VxD (vocabulary size vs documents)
						such that bow[i,j] = 5 if and only if term i appears 5 times on 
						document j


	'''
	V = len(word2idx) 
	D = len(doc2idx)
	stopwords = get_stopwords()
	bow= np.zeros((V,D), dtype=np.int32)
	for docid, doc in doc2idx.iteritems():
		




def tokenizer(l, stopwords=None): 
	if stopwords is None: 
		stopwords= get_stopwords()

	tokens = [t.lower() for t in l] 		# to lowecase
	tokens = [remove_puctuation(t) for t in tokens] 
	tokens = [t for t in tokens if t not in stopwords] # remove stopwords

	return tokens

def get_stopwords():
	stop_words=[]
	for word in open('../../random-projection/datasets/stopwords.txt'):
		stop_words.append(word) 
	return stop_words


def remove_puctuation(s):
	'''
		s is a string with punctuation; converts unicode to string which might get data loss
			url: https://stackoverflow.com/questions/23175809/typeerror-translate-takes-one-argument-2-given-python
	'''	
	return 	str(s).translate(None, string.punctuation)

