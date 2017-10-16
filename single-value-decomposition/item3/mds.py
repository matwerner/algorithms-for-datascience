# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2017

@author: Varela

motivation: MDS
			 
'''

import numpy as np 
import sys
sys.path.append('../item2')
from svd_powermethod_v2 import computeXXT, computeX 

import matplotlib.pyplot as plt 
from sklearn.manifold import MDS
# from sklearn.preprocessing import normalize

def normalize(A): 
	minX = np.min(A[:,0])
	meanX =np.mean(A[:,0]) 
	maxX = np.max(A[:,0])

	minY = np.min(A[:,1])
	meanY =np.mean(A[:,1]) 
	maxY = np.max(A[:,1])

	N = np.zeros(A.shape)
	N[:,0] = (A[:,0] - meanX)/ (maxX-minX)
	N[:,1] = (A[:,1] - meanY)/ (maxY-minY)
	return N


def rotate_counterclockwise(A, degrees=45): 
	degrees = degrees % 360
	rad = 2 * np.pi * (degrees / 360)
	R = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad),np.cos(rad)] ])
	
	Y = np.zeros(A.shape, dtype=np.float32)	

	for i in range(A.shape[0]):

		# import code; code.interact(local=dict(globals(), **locals()))
		Y[i,:] = (R * A[i,:]).reshape(1,2)
	return Y





if __name__ == '__main__':

	# df = pd.read_csv('matrix.txt', header=None)
	# D = df.values
	# D = D.reshape(20,20)
	# D = D.astype(np.int32)
	file = open("matrix.txt","r")
	matrix = []
	for rawLine in file:
		line = rawLine.strip()
		if line:
			if "-" in line:
				matrix.append(0.0);
			else:
				matrix.append(float(line))

	matrix = np.array(matrix, float)

	matrix.shape = (20,20)

	D = np.matrix(matrix)
	# print(matrix)

	XXT = computeXXT(matrix)
	# print(XXT)
	X = computeX(XXT,2)
	print(X)

	mds= MDS()
	Y = mds.fit_transform(D)

	Yn = normalize(Y)
	print(Yn)
	Yr = rotate_counterclockwise(Yn, 45)
	print(Yr)
	plt.scatter(Yn[:,0], Yn[:,1])
	plt.show()
	