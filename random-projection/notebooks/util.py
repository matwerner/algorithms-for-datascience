'''
Created on Sep 09, 2017

@author: Varela

motivation: useful cross module corpora functions; such as tokenization
'''
import string 

def flatten(l):
	'''
		l is a list of list, in our case a list of list of words		
	'''
	f = [item for sublist in l for item in sublist] 
	return f

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

