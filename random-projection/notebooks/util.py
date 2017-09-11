'''
Created on Sep 09, 2017

@author: Varela

motivation: useful cross module corpora functions; such as tokenization
'''
import string 
import numpy as np 
import pandas as pd 
from itertools import groupby 

def flatten(l):
	'''		
		l is a list of list, in our case a list of list of words		

		returns
		f : a flattened list 
	'''
	f = [item for sublist in l for item in sublist] 
	return f

def documents2bag_of_words(documents, tokenize=True): 
	'''
				Gets a documents i.e dict which the keys being articles(document) ids and the values being 
						the documents represented by a list (document) of lists of (sentences) strings (tokens)
		Returns
			bow: is a numpy matrix of size VxD (vocabulary size vs documents)
						such that bow[i,j] = 5 if and only if term i appears 5 times on 
						document j

	'''
	word2idx={} 
	doc2freq={} 
	doc2idx= {} 
	stopwords = get_stopwords()
	for doc_id, doc in documents.iteritems():
		# BEWARE OF DATA LOSS: Flattening the arrays and missing the information of sentence begin and end
		import code; code.interact(local=dict(globals(), **locals()))
		sentences = flatten(doc)
		if tokenize:
			sentences = tokenizer(sentences, stopwords=stopwords)
			
		
		indexed_sentences, word2idx = sentences2indexed_sentences(sentences, word2idx=word2idx)
		indices, idx_freq =indexed_sentences2idx_freq(indexed_sentences)
		
		doc2idx[doc_id]= indices 
		doc2freq[doc_id]= idx_freq 
		
	V= len(word2idx)
	D= len(doc)	

	bow = np.zeros((V,D), dtype=np.int32)
	for j, doc_id in enumerate(doc): 
		bow[doc2idx[doc_id],j]= doc2freq[doc_id]

	return bow 

def tokenizer(l, stopwords=None): 
	if stopwords is None: 
		stopwords= get_stopwords()

	tokens = [t.lower() for t in l] 		# to lowecase
	tokens = [remove_puctuation(t) for t in tokens] 
	tokens = [t for t in tokens if t not in stopwords] # remove stopwords

	return tokens

def get_stopwords():
	# stop_words=[]
	# for word in open('../../random-projection/datasets/stopwords.txt'):
	# 	stop_words.append(word) 
	df = pd.read_csv('../../random-projection/datasets/stopwords.txt', index_col=False) 
	import code; code.interact(local=dict(globals(), **locals()))
	return df.ix[:, 0].to_list()


def remove_puctuation(s):
	'''
		s is a string with punctuation; converts unicode to string which might get data loss
			url: https://stackoverflow.com/questions/23175809/typeerror-translate-takes-one-argument-2-given-python
	'''	
	return 	str(s).translate(None, string.punctuation)

def sentences2indexed_sentences(sentences, word2idx={}):
	'''
		Converts a document to a list 
		Gets 
				sentences: i.e  the element of a document dict which is represented 
					by flattened list of lists of (sentences) strings (tokens). 
					Information about of start and end periods is omitted

				word2idx: the previous word2idx dictionary if none exists then creates one

		Returns
			indexed_sentences: 	a flattened list of idx representing the tokens 
			word2idx :  				a token to index mapping 
			

	'''
	if not word2idx:
		idx= 0 
	else:
		idx= max(word2idx.keys())+1 
	indexed_sentences=[] 
	for sentence in sentences: 
		indexed_sentence= [] 
		for token in sentence: 
			token = token.lower()
			if token not in word2idx: 
				word2idx[token]= idx 
				idx += 1 	
			indexed_sentence.append(word2idx[token]) 
		indexed_sentences.append(indexed_sentence)

	return indexed_sentences, word2idx 

def indexed_sentences2idx_freq(indexed_sentences): 	
	'''
		Converts a document to a list 
		Gets 
			indexed_sentence: i.e  the element of a document dict which is represented 
					by flattened list of lists of (sentences) integer (indices). 
					Information about of start and end periods is omitted

		Returns
				indices: a set of integers representing the idx of every word that appears on 
					indexed_sentences 
				idx_freq: a list of integers represeting a count of every idx that appears on indices

				OBS: |indices| == |idx_freq|
							indices[5] = 8937 and idx_freq[5] = 7 that means that 8937 is the 5th smallest index,
							and it appears 7 times on document represented by indexed_sentences

	'''
	import code; code.interact(local=dict(globals(), **locals()))
	indices= set(indexed_sentences)
	indexed_sentences= sorted(indexed_sentences)
	idx_freq= [len(list(group)) for key, group in groupby(indexed_sentences)]
	
	return indices, idx_freq