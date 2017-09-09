'''
Created on Sep 09, 2017

@author: Varela

motivation: useful cross module corpora functions; such as tokenization
'''

import string  


def tokenizer(s, stopwords=None): 
	if stopwords is None: 
		stopwords= get_stopwords()

	tokens = s.lower()
	tokens = remove_puctuation(tokens)
	tokens = [t for t in tokens if t not in stopwords] # remove stopwords
	return tokens

def get_stopwords():
	stop_words=[]
	for word in open('../random-projections/datasets/stopwords.txt'):
		stop_words.append(word)
	return stop_words

def remove_puctuation(s):
	return 	s.translate(None, string.punctuation)

