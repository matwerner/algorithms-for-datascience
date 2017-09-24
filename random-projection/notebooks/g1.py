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
	g1_id= g1_id.replace('.html','').replace('.ghtml','')
	return g1_id 



def get_sentences(verbose=True, limit_documents=3000):
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
			words= list(map(to_word, sentences))
			corpora+= words 
			#print article["TEXT"]
			
			total_sentences+= len(sentences)
			total_words+= sum(map(len,words))

			if verbose: 
				sys.stdout.write('article:%s of 4000\tphrases:%s of %s\twords:%s of %s\tg1_id:%s\r' % (format(a + 1, '05d'), format(len(sentences),'03d'), format(total_sentences,'05d'), format(sum(map(len,words)),'05d'), format(total_words,'05d'), g1_id))
				sys.stdout.flush()
		print(len(articles))
	return corpora




def get_documents(verbose=False, limit_documents=3000): 
	'''
		Gets g1 articles as documents

		Returns
			g1docs: Gets a document i.e dict which the keys being articles(document) ids and the values being 
				the documents represented by a list (document) of lists of (sentences) strings (tokens)

	'''
	#iterates all documents withing corpus adding sentences 
	if not limit_documents: 
		limit_documents= 1e10

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
		if a<limit_documents: 
			g1_id= g1_url2id( article["URL"] ) 
			# print article["URL"]
			sentences= article["TEXT"].split('.')		#splits phrases
			# import code; code.interact(local=dict(globals(), **locals()))
			sentences= list(map(to_word, sentences))			#splits phrases into words	
			vocab= vocab.union(set([word for sentence in sentences for word in sentence]))
			g1docs[g1_id]= sentences

			total_words+= sum(map(len,sentences))

			if verbose: 
				sys.stdout.write('article:%s of %s\tV:%s\tWORD COUNT:%s\tdocid:%s\r' % (format(a + 1, '04d'), format(limit_documents, '04d'),format(len(vocab),'05d'), format(total_words,'05d'), g1_id))
				sys.stdout.flush()			
	print('')
	return g1docs


def main():
	# get_sentences()
	get_documents(verbose=True)
if __name__ == '__main__':
	main()