'''
	author: Guilherme Varela
	
	Utility functions for text edition
'''
# from nltk import download
import string 

from nltk.corpus import stopwords as _stopwords
from nltk.stem import * 

def tokenizer(tokens, stopwords=None, stemmer=None): 
	# print('%s\r' %(tokens))
	tokens= str(tokens).split(' ')
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
