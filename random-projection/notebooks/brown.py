'''
Created on Sep 09, 2017

@author: Varela

motivation: Brown corpus data

'''
from nltk.corpus import brown 
import operator
# import numpy as np 
import pandas as pd
import sys 
import random 
# we absolutely want to keep these words in order to make comparisons
KEEP_WORDS = set([
	'king', 'man', 'queen', 'woman',
	'italy', 'rome', 'france', 'paris',
	'london', 'britain', 'england',
])

def get_sentences(): 
	# return 57340  sentences of brown corpus
	#each sentence is represent by a list of individual string tokens
	return brown.sents() 

def get_browndocs(verbose=False): 
	'''
		Gets brown corpus's articles as documents

		Returns
			browndocs: dict with the keys being articles(document) ids and the values being 
						the documents representing a list of lists of strings representing sentences 
						within documents

	'''
	#defines all dcouments categories 
	df= pd.read_csv('../../random-projection/datasets/brown_fileids.txt', sep=' ')
	documentids= df.ix[:,0]
	
	#iterates all documents withing corpus adding sentences and at the same time conveting
	# it's tokens to idx
	doc2idx= {}	
	for d, docid in enumerate(documentids):
		sentences= brown.sents(fileids=[docid])
		doc2idx[docid]= sentences

	return doc2idx



def get_documents_with_word2idx(verbose=False):	
	'''
		Gets brown corpus's articles as documents and the corresponding word2idx representation

		Returns
			doc2idx: dict with the keys being articles(document) ids and the values being 
						the documents representing a list of lists of integer(idx)

			word2idx: dict with keys being tokens(words) and values being an idx(integer)

	'''

	#defines all dcouments categories 
	df= pd.read_csv('../../random-projection/datasets/brown_fileids.txt', sep=' ')
	documentids= df.ix[:,0]
	
	#iterates all documents withing corpus adding sentences and at the same time conveting
	# it's tokens to idx
	doc2idx= {}
	word2idx= {'START': 0, 'END': 1}
	idx=2 
	word_count=0
	anytoken=''
	for d, docid in enumerate(documentids):
		sentences= brown.sents(fileids=[docid])
		doc2idx[docid]= []  
		for sentence in sentences: 
			indexed_sentence= [] 
			for token in sentence: 
				token = token.lower()
				if token not in word2idx: 
					word2idx[token]= idx 
					idx += 1 
				word_count+= 1
				anytoken= random.choice(sentence)
			indexed_sentence.append(word2idx[token]) 
		doc2idx[docid]= doc2idx[docid].append(indexed_sentence)
		if verbose:
			sys.stdout.write('document:%d\tdocid:%s\ttoken:%s\tV:%d\n' % (d, docid, anytoken, len(word2idx)))
			sys.stdout.flush()
	return doc2idx, word2idx

def get_sentences_with_word2idx(): 
	# Returns sentences as indexes of words and word2idx mapping
	sentences= get_sentences()
	indexed_sentences= [] 

	i=2
	word2idx= {'START': 0, 'END': 1}
	for sentence in sentences: 
		indexed_sentence= [] 
		for token in sentence: 
			token = token.lower()
			if token not in word2idx: 
				word2idx[token]= i
				i +=1 

			indexed_sentence.append(word2idx[token])
		indexed_sentences.append(indexed_sentence)

	print 'Vocab size:', i 
	return indexed_sentences, word2idx

def get_sentences_with_word2idx_limit_vocab(n_vocab=2000, keep_words=KEEP_WORDS):
	# Returns sentences as indexes of words and word2idx mapping
	# but limits to n_vocab and forces to keep WORDS
	sentences = get_sentences() 
	indexed_sentences= [] 

	i=2
	word2idx=  {'START':0, 'END':1}
	idx2word=  ['START', 'END']

	word_idx_count={
		0: float('inf'),
		1: float('inf'),
	}
	for sentence  in sentences: 
		indexed_sentence= [] 
		# This loop converts words to index and 
		# it fills the word2idx dictionary
		for token in sentence: 
			token= token.lower()
			if token not in word2idx: 
				idx2word.append(token)
				word2idx[token]= i 
				i +=1 

			#keep track of counts for later sorting
			idx = word2idx[token]
			word_idx_count[idx] = word_idx_count.get(idx,0) +1

			indexed_sentence.append(idx)
		indexed_sentences.append(indexed_sentence)

		#restrict vocab size
		#set all the words I want to keep to infinity
		# so that they are included when I pick the most common words
  	for word in keep_words:
			word_idx_count[word2idx[word]] = float('inf')


	#remapping to new smaller vocabulary words
	#updates the dictionary	
	sorted_word_idx_count= sorted(word_idx_count.items(), key=operator.itemgetter(1), reverse=True)
	word2idx_small = {}
	new_idx =0 
	idx_new_idx_map= {} 
	for idx, count in sorted_word_idx_count[:n_vocab]: 
		word= idx2word[idx]
		print word, count 

		word2idx_small[word]= new_idx
		idx_new_idx_map[idx]= new_idx 
		new_idx +=1 

	# let 'unknown' be the last token
	word2idx_small['UNKNOWN']= new_idx 
	unknown= new_idx 

	# sanity check
	assert('START' in word2idx_small)
	assert('END' in word2idx_small)
	for word in keep_words:
		assert( word in word2idx_small)

	#map old idx to new idx
	sentences_small = [] 
	for sentence in indexed_sentences: 
		if len(sentence) > 1:
			new_sentence = [idx_new_idx_map[idx] if idx in idx_new_idx_map else unknown] 
			sentences_small.append(new_sentence)

	return sentences_small, word2idx_small 



