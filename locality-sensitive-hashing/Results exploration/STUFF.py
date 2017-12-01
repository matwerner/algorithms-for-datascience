import numpy as np
import sys
import json
from tinydb import TinyDB, where, Query

# DISTANCE_MATRIX_FILE_PATH = "/home/daniel/Repositories/big_outputs/LSH/datasets/datasets/distance_matrix.txt"
DISTANCE_MATRIX_FILE_PATH = "/home/daniel/Repositories/algorithms-for-datascience/locality-sensitive-hashing/Results exploration/testingDistancesMatrix.txt"
DOCUMENTS_JSON_PATH = "/home/daniel/Repositories/algorithms-for-datascience/locality-sensitive-hashing/datasets/Dataset-Treino-Anonimizado-3.json"
# File containing the documents that are the same
EQUAL_DOCUMENTS_FILE_PATH = "similar_documents.txt"

class DocumentManager:
	def __init__(self,
			  documentsJsonPath,
			  distanceMatrixFilePath,
			  equalDocumentsFilePath,
			  verbose=True):

		self.documentsJsonPath = documentsJsonPath
		self.distanceMatrixFilePath = distanceMatrixFilePath
		self.equalDocumentsFilePath = equalDocumentsFilePath
		self.verbose = verbose
		self.documents = []

	def loadDocumentsLikeness(self):
		with open(self.distanceMatrixFilePath, "r") as distancesMatrix:
			# This line contains information about the number of columns and rows of the matrix
			descriptionLine = distancesMatrix.readline()
			nRows = int(descriptionLine.split()[0])
			nColumns = int(descriptionLine.split()[1])

			if self.verbose:
				print >> sys.stderr, "Found %s rows and %s columns" % (nRows, nColumns)

			self._initializeDocumentsLikeness(nRows)
			count = 0
			for i in range(nRows):
				rowValues = distancesMatrix.readline().split()

				if i % 100 == 0:
					print i

				for j in range(0, i):
					item = (float(rowValues[j]), (i, j))
					self.docsLikeness[count] = item
					count += 1
					#print count

		print self.docsLikeness

	def _initializeDocumentsLikeness(self, nRows):
		nDistances = (((nRows * nRows) - nRows) / 2)
		self.docsLikeness = np.zeros(nDistances, dtype='float32,2int8')
		if self.verbose:
			print >> sys.stderr, "Documents likeness array created with %s bytes for %s entries" % (
				self.docsLikeness.nbytes, nDistances)

	def loadDocuments(self):
		with open(self.documentsJsonPath, "r") as docs:
			self.documents = json.load(docs)

	def sortByDistance(self):
		self.docsLikeness.sort(order="f0")  # inplace

	def getEntryByIndex(self, index):
		return self.documents[index]

class DocumentsComparisson:
	def __init__(self, documentManager, offset=0,verbose=True):
		self.documentManager = documentManager
		self.offset = offset
		self.verbose = verbose
		self.db = TinyDB('db.json') # Similarity db

	def _comparedAlready(self,docA,docB):
		query = Query()
		doc = Query

		queryResult = self.db.search(query.docs.all([docA,docB]))

		print queryResult

		compared = True if queryResult else False

		if self.verbose:
			if compared:
				print >> sys.stderr, "The documents %s %s were compared already"%(docA,docB)

		return compared

	def setDocumentsSimilarity(self, docA, docB, same):
		#table = self.db.table("similarity")
		self.db.insert({"docs": [docA,docB], "same": same})

	def startComparissonLoop(self):
		for i in range(self.offset, len(self.documentManager.docsLikeness)):
			likeness = self.documentManager.docsLikeness[i]
			docA = likeness[1][0].item()
			docB = likeness[1][1].item()
			if not self._comparedAlready(docA,docB):
				self.compare(likeness)

	def compare(self, item):
		entry1 = self.documentManager.getEntryByIndex(item[1][0])
		entry2 = self.documentManager.getEntryByIndex(item[1][1])

		print "Documento de index %s Titulo:" % (item[1][0])
		print entry1["title"]
		print "\n"

		print "Documento de index %s Titulo:" % (item[1][1])
		print entry2["title"]
		print "\n"

		print "Documento de index %s Descricao:" % (item[1][0])
		print entry1["description"]
		print "\n"

		print "Documento de index %s Descricao:" % (item[1][1])
		print entry2["description"]
		print "\n"

		while True:
			nb = raw_input('Same? y/n: ')
			same = None
			if nb == "y":
				same = True
			elif nb == "n":
				same = False
			else:
				continue
			docA = item[1][0].item()
			docB = item[1][1].item()
			self.setDocumentsSimilarity(docA,docB,same)
			break

	def _printTitle(self):
		pass

	def _printDescription(self, item):
	 	pass

if __name__ == '__main__':

	d = DocumentManager(DOCUMENTS_JSON_PATH,DISTANCE_MATRIX_FILE_PATH,EQUAL_DOCUMENTS_FILE_PATH)
	d.loadDocumentsLikeness()
	d.loadDocuments()
	d.sortByDistance()
	comparator = DocumentsComparisson(d)
	comparator.startComparissonLoop()

	#db = TinyDB('db.json') # Similarity db
	#User = Query()
	# db.insert({'name': 'user1', 'groups': ['user']})
	# db.insert({'name': 'user2', 'groups': [1, 'user']})
	# db.insert({'name': 'user3', 'groups': ['sudo', 'user']})

	# print db.search(User.groups.any(['user', 'sudo']))


	# n_rows = 100
	# with open("testingDistancesMatrix.txt","w") as d2:
	# 	d2.write(str(n_rows)+"\t"+str(n_rows)+"\n")

	# 	with open(DISTANCE_MATRIX_FILE_PATH,"r") as distancesMatrix:

	# 		descriptionLine = distancesMatrix.readline()

	# 		for i in range(n_rows):

	# 			rowValues = distancesMatrix.readline().split()
	# 			for j in range(n_rows):
	# 				d2.write(rowValues[j])
	# 				if j==n_rows-1:
	# 					break
	# 				d2.write("\t")
	# 			d2.write("\n")
