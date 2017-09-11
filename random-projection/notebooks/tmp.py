from brown import get_documents
from util import documents2bag_of_words 
if __name__== '__main__':
	# doc2idx, word2idx = get_documents_with_word2idx(verbose=True)
	brown_documents= get_documents(verbose=True)
	BoW=  documents2bag_of_words(brown_documents)
	print BoW.shape

