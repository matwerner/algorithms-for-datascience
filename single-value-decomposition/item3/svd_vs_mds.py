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

def normalize(A, origin='img'): 

	N = np.zeros(A.shape)
	for i in range(A.shape[1]):

		minX = np.min(A[:,i])
		meanX =np.mean(A[:,i]) 
		maxX = np.max(A[:,i])

		if origin == 'img':
			N[:,i] = (A[:,i] + abs(minX))/ (maxX+abs(minX)-minX)	
		else: 
			N[:,i] = (A[:,i] - meanX)/ (maxX-minX)

		
	return N


def rotate_counterclockwise(A, degrees=45): 
	degrees = degrees % 360
	rad = 2 * np.pi * (degrees / 360)
	R = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad),np.cos(rad)] ])
	
	Y = np.zeros(A.shape, dtype=np.float32)	

	for i in range(A.shape[0]):		
		Y[i,:] = (R.dot(A[i,:]))

	return Y

labels = ["Boston"
	,"Buffalo"
	,"Chicago"
	,"Dallas"
	,"Denver"
	,"Houston"
	,"Los Angeles"
	,"Memphis"
	,"Miami"
	,"Minneapolis"
	,"New York"
	,"Omaha"
	,"Philadelphia"
	,"Phoenix"
	,"Pittsburgh"
	,"Saint Louis"
	,"Salt Lake City"
	,"San Francisco"
	,"Seattle"
  ,"Washington D.C."]



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

	n = len(D)
	XXT = computeXXT(matrix)
	# print(XXT)
	X = computeX(XXT,2)
	print(X)

	
	Xr = rotate_counterclockwise(X, 180)

	
	Xr = normalize(Xr, origin='center')
	
	print(Xr)
	img = plt.imread('../img/usamap.png')
	print(img.shape)
	height= img.shape[0]
	width = img.shape[1]

	# for images top-left is zero
	# for algos origin is center
	imgscale = 0.8*np.array([[width, -height]]) # 0.95 compensates for the frame
	imgfactor= np.tile(imgscale, (n,1))
	imgscale = np.array([[0.55*width, 0.5*height]])
	imgintercept= np.tile(imgscale, (n,1))
	# print(Xr)
	Xs = imgfactor * Xr + imgintercept#scaled X
	print(Xs)
	# fig = plt.figure(figsize=(6,9))
	
	# fig, ax = plt.subplots(2,1)
	fig, ax = plt.subplots()
	implot = ax.imshow(img, origin='upper')
	ax.scatter(Xs[:,0], Xs[:,1], c='r', s=1)
	for i, txt in enumerate(labels):
		ax.annotate(txt, (Xs[i,0],Xs[i,1]), fontsize=6)
	plt.title('SVD')
	plt.show()

	mds= MDS()
	Y = mds.fit_transform(D)

	Yr = rotate_counterclockwise(Y, 90)

	
	Yr = normalize(Yr, origin='center')
	
	print(Yr)
	img = plt.imread('../img/usamap.png')
	print(img.shape)
	height= img.shape[0]
	width = img.shape[1]

	# for images top-left is zero
	# for algos origin is center
	imgscale = 0.8*np.array([[width, -height]]) # 0.95 compensates for the frame
	imgfactor= np.tile(imgscale, (n,1))
	imgscale = np.array([[0.55*width, 0.5*height]])
	imgintercept= np.tile(imgscale, (n,1))
	# print(Xr)
	Ys = imgfactor * Yr + imgintercept#scaled X
	print(Ys)
	# fig = plt.figure(figsize=(6,9))
	
	# fig, ax = plt.subplots(2,1)
	fig, ax = plt.subplots()
	implot = ax.imshow(img, origin='upper')
	ax.scatter(Ys[:,0], Ys[:,1], c='r', s=1)
	for i, txt in enumerate(labels):
		ax.annotate(txt, (Ys[i,0],Ys[i,1]), fontsize=6)
	plt.title('MDS')
	plt.show()

	