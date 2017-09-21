# -*- coding: utf-8 -*-
'''
Created on Sep 20, 2017

@author: Varela

motivation: G1 corpus data

'''
import json
import sys

def g1_url2id(url):
	'''
		Gets an url and extract it's inner text (g1_id)
		example: 
			url: http://g1.globo.com/sp/campinas-regiao/noticia/2013/04/apos-100-dias-veja-como-andam-propostas-do-prefeito-de-campinas.html
			g1_id: apos-100-dias-veja-como-andam-propostas-do-prefeito-de-campinas
	'''
	g1_id= url.split('/')[-1]
	g1_id= g1_id.split('.html')[0]
	return g1_id 



def get_sentences(verbose=True):
	'''
		Get g1 corpora as nested list (corpora) of list (words)
	'''
	datasets_path= '../../random-projection/datasets/'
	g1filename= '4000_g1_articles.json'
	g1_path= datasets_path + g1filename 

	def to_word(X):
		return X.split(' ')

	corpora=[] 
	total_sentences=0
	total_words=0
	with open(g1_path) as data_file:
		articles = json.load(data_file, encoding='utf-8')
		for a, article in enumerate(articles):
			g1_id= g1_url2id( article["URL"] ) 
			# print article["URL"]
			sentences= article["TEXT"].split('. ') #space prevents URLs to be split as phrases
			words= map(to_word, sentences)
			corpora+= words 
			#print article["TEXT"]
			
			total_sentences+= len(sentences)
			total_words+= sum(map(len,words))

			if verbose: 
				sys.stdout.write('article:%s of 4000\tphrases:%s of %s\twords:%s of %s\tg1_id:%s\r' % (format(a + 1, '05d'), format(len(sentences),'03d'), format(total_sentences,'05d'), format(sum(map(len,words)),'05d'), format(total_words,'05d'), g1_id))
				sys.stdout.flush()
  	print len(articles)
	return corpora




def get_documents(verbose=False): 
	'''
		Gets g1 articles as documents

		Returns
			g1docs: Gets a document i.e dict which the keys being articles(document) ids and the values being 
				the documents represented by a list (document) of lists of (sentences) strings (tokens)

	'''
	#iterates all documents withing corpus adding sentences 
	datasets_path= '../../random-projection/datasets/'
	g1filename= '4000_g1_articles.json'
	g1_path= datasets_path + g1filename 

	def to_word(X):
		return X.split(' ')

	g1docs={}	
	total_words=0
	vocab=set([])
	with open(g1_path) as data_file:
		articles = json.load(data_file, encoding='utf-8')
		
	for a, article in enumerate(articles):
		g1_id= g1_url2id( article["URL"] ) 
		# print article["URL"]
		sentences= article["TEXT"].split('.')		#splits phrases
		sentences= map(to_word, sentences)			#splits phrases into words	
		vocab= vocab.union(set([word for sentence in sentences for word in sentence]))
		g1docs[g1_id]= sentences
		total_words+= sum(map(len,sentences))

		if verbose: 
			sys.stdout.write('article:%s of 4000\tV:%s\tWORD COUNT:%s\tdocid:%s\r' % (format(a + 1, '04d'), format(len(vocab),'05d'), format(total_words,'05d'), g1_id))
			sys.stdout.flush()			
	print ''
	return g1docs



# def get_documents_with_word2idx(verbose=False):	
# 	'''
# 		Gets brown corpus's articles as documents and the corresponding word2idx representation

# 		Returns
# 			doc2idx: dict with the keys being articles(document) ids and the values being 
# 				the documents representing a list of lists of integer(idx)

# 			word2idx: dict with keys being tokens(words) and values being an idx(integer)

# 	'''

# 	#defines all documents categories 
# 	df= pd.read_csv('../../random-projection/datasets/brown_fileids.txt', sep=' ')
# 	documentids= df.ix[:,0]
	
# 	#iterates all documents withing corpus adding sentences and at the same time conveting
# 	# it's tokens to idx
# 	doc2idx= {}
# 	word2idx= {'START': 0, 'END': 1}
# 	idx=2 
# 	word_count=0
# 	anytoken=''
# 	for d, docid in enumerate(documentids):
# 		sentences= brown.sents(fileids=[docid])
# 		doc2idx[docid]= []  
# 		for sentence in sentences: 
# 			indexed_sentence= [] 
# 			for token in sentence: 
# 				token = token.lower()
# 				if token not in word2idx: 
# 					word2idx[token]= idx 
# 					idx += 1 
# 				word_count+= 1
# 				anytoken= random.choice(sentence)
# 			indexed_sentence.append(word2idx[token]) 
# 		doc2idx[docid]= doc2idx[docid].append(indexed_sentence)
# 		if verbose:
# 			sys.stdout.write('document:%d\tdocid:%s\ttoken:%s\tV:%d\r' % (d, docid, anytoken, len(word2idx)))
# 			sys.stdout.flush()
# 	return doc2idx, word2idx

# def get_sentences_with_word2idx(): 
# 	# Returns sentences as indexes of words and word2idx mapping
# 	sentences= get_sentences()
# 	indexed_sentences= [] 

# 	i=2
# 	word2idx= {'START': 0, 'END': 1}
# 	for sentence in sentences: 
# 		indexed_sentence= [] 
# 		for token in sentence: 
# 			token = token.lower()
# 			if token not in word2idx: 
# 				word2idx[token]= i
# 				i +=1 

# 			indexed_sentence.append(word2idx[token])
# 		indexed_sentences.append(indexed_sentence)

# 	print('Vocab size:', i)
# 	return indexed_sentences, word2idx

def main():
	# get_sentences()
	get_documents(verbose=True)
# if __name__ == '__main__':
# 	main()