# -*- coding: utf-8 -*-
'''
Created on Oct 5, 2017

@author: Varela

motivation: The power method to SVD
			 ref: BLUM, Foundations of datascience, 3.30

'''

import sys 
import numpy as np 
from numpy.linalg import norm 
import matplotlib.pyplot as plt

def computeXXT(D):
	n= len(D)
	nssq= 0 
	sd2=0 
	MD2= np.zeros(n,dtype=np.int32)

	# COMPUTE MEAN SQUARE DISTANCES
	for i in range(n):
		sd2=0 
		for j in range(n): 
			sd2 += D[i,j]*D[i,j]
		MD2[i] = float(sd2)/n 
		nssq += sd2

	msq = nssq / (2*(n**2))

	# COMPUTE OUTER DIAGONALS
	XXT = np.zeros(D.shape, dtype=np.int32)
	for i in range(n):	
		for j in range(n): 
			XXT[j,i] = -0.5*(D[i,j]*D[i,j] - MD2[i] - MD2[j] + 2*msq)
	return XXT

def computeX(XXT, d):			
	U, S, V = np.linalg.svd(XXT)
	# X = U[:,:d].dot(np.sqrt(S[:d]))
	n = len(XXT)
	X = np.zeros((n,d), dtype=np.int32)
	for i in range(n):
		for j in range(d):
			X[i,j] = U[i,j]*S[j]
	return X

if __name__ == '__main__':

	# testing with boston, buffalo, chicago, dallas, denver
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

	matrix = np.matrix(matrix)
	D = matrix

	X = computeX(D,2) 
	print(X)
	
	rot= np.array([[0,-1],[1,0]],float)

	rotated = []
	for point in X :
		t = np.array([[point[0]],[point[1]]],float)

		print("Point")
		print(point)
		print("Transpose")
		print(t)
		print("Rotated")
		r = np.matmul(rot,t)
		print(r)
		rotated.append([r[0][0],r[1][0]])
	
	rotated = np.matrix(rotated)
	print(rotated)
	
	x = rotated[:,0] # py3.6
	y = rotated[:,1] # py3.6

	fig, ax = plt.subplots()
	ax.scatter([x], [y])	
	labels = [
	"Boston"
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

	for i, txt in enumerate(labels):
		ax.annotate(txt, (x[i],y[i]))

	plt.show()

# POWER METHOD II see BLUM, Foundations of datascience exercices 3.30
# B = XXT.astype(np.float32) 	
# d = n 
# r = n

# if r > n or r > d: 
# 	print(' r[%d] <= n[%d] and r[%d] <= d[%d]' %(r,n,r,d))

# eps= 10e-10
# residuals= {} 
# flags= []
# iterations= []
# S = np.zeros(B.shape, dtype=np.float32)
# U = np.zeros(B.shape, dtype=np.float32)
# V = np.zeros(B.shape, dtype=np.float32)

# kmax=1000
# for i in range(n): 
# 	k=0
# 	vi = np.random.rand(n) 
# 	vi = vi / norm(vi)
# 	first= True 

# 	while first or (residuals[i]>eps and k<kmax): 						
# 		v0 = vi  
# 		vi =  B.dot(vi) 				
# 		vi = vi / norm(vi)
# 		k+=1	
# 		first= False

# 		residuals[i] =norm(vi-v0)		
# 		sys.stdout.write('i:%d\t:delta:%.2f\r' % (k, residuals[i]))
# 		sys.stdout.flush()			
# 	flags.append(residuals[i]<eps)	
# 	iterations.append(k)

# 	print('')
# 	S[i,i]= norm(B.dot(vi))
# 	V[i,:]= vi 
# 	U[:,i]= vi 

# 	vi= vi.reshape(n,1)
# 	B -= (S[i,i])*(vi*vi.T) 


# u, s, v = np.linalg.svd(XXT)
# print('%===========================S- experimental==========================%')	
# print(np.diag(S))
# print('%===========================S- theoretical==========================%')	
# print(s)
# print('%===========================S-exp vs S-theo==========================%')	
# print(np.allclose(np.diag(S)[:-1],s[:-1])) 
# print('%===========================V - experimental=========================%')	
# print(V)
# print('%===========================V - theoretical==========================%')	
# print(v)
# print('%===========================U - theoretical=========================%')	
# print(u)
# print('%===========================X - theoretical==========================%')	
# X = (u[:,:r] * np.sqrt(s[:r])
# # X = (np.diag(S)[:-1]*V[:-1,:].T)
# print(X)
# # x = s*v.T 
# # print(x)
# # print(np.allclose(X , x[:,:-1]))
# print('%===========================V - CLOSE=================================%')	
# # print(np.allclose(V[:-1,:],v[:-1,:])) 
# print('%============================RESIDUALS================================%')	
# print(list(residuals.values()))
# print('%========================CONVERGENCE FLAGS=============================%')	
# print(flags)