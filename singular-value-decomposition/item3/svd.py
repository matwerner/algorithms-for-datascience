# -*- coding: utf-8 -*-
'''
Created on Oct 15, 2017

@author: Varela

motivation: MDS
			 
'''

import numpy as np 
import sys
sys.path.append('..') # include utils

import matplotlib.pyplot as plt 
from sklearn.manifold import MDS
# from sklearn.preprocessing import normalize
from utils import rotate_counterclockwise, normalize, get_usalabels, get_D, computeXXT, computeX



if __name__ == '__main__':

	D = get_D() 

	n = len(D)
	XXT = computeXXT(D)
	# print(XXT)
	X = computeX(XXT,2)
	print(X)

	
	Xr = rotate_counterclockwise(X, 181)

	
	Xr = normalize(Xr, origin='center')
	
	print(Xr)
	img = plt.imread('../datasets/usamap.png')
	print(img.shape)
	height= img.shape[0]
	width = img.shape[1]

	# for images top-left is zero
	# for algos origin is center
	imgscale = np.array([[0.82*width, -0.8*height]]) # 0.95 compensates for the frame
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
	for i, txt in enumerate(get_usalabels()):
		ax.annotate(txt, (Xs[i,0],Xs[i,1]), fontsize=6)
	plt.title('SVD')
	plt.show()

	# mds= MDS()
	# Y = mds.fit_transform(D)

	# Yr = rotate_counterclockwise(Y, 90)

	
	# Yr = normalize(Yr, origin='center')
	
	# print(Yr)
	# img = plt.imread('../datasets/usamap.png')
	# print(img.shape)
	# height= img.shape[0]
	# width = img.shape[1]

	# # for images top-left is zero
	# # for algos origin is center
	# imgscale = 0.8*np.array([[width, -height]]) # 0.95 compensates for the frame
	# imgfactor= np.tile(imgscale, (n,1))
	# imgscale = np.array([[0.55*width, 0.5*height]])
	# imgintercept= np.tile(imgscale, (n,1))
	# # print(Xr)
	# Ys = imgfactor * Yr + imgintercept#scaled X
	# print(Ys)
	# # fig = plt.figure(figsize=(6,9))
	
	# # fig, ax = plt.subplots(2,1)
	# fig, ax = plt.subplots()
	# implot = ax.imshow(img, origin='upper')
	# ax.scatter(Ys[:,0], Ys[:,1], c='r', s=1)
	# for i, txt in enumerate(get_usalabels()):
	# 	ax.annotate(txt, (Ys[i,0],Ys[i,1]), fontsize=6)
	# plt.title('MDS')
	# plt.show()

	# 