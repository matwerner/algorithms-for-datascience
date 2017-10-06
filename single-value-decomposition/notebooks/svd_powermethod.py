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
# testing with boston, buffalo, chicago, dallas, denver
# D = np.array([
# 	[0, 		400,  851, 1551, 1769],
# 	[400, 	  0,  454, 1198, 1370],
# 	[ 851,  454, 	  0, 803, 	920],
# 	[1551, 1198, 	803, 	 0, 	663],
# 	[1769, 1370, 	920, 663, 		0]
# ])
D = np.array([
	[0, 		400,  851],
	[400, 	  0,  454],
	[ 851,  454, 	  0]	
])
print(D)		
n_cities= len(D)
nssq= 0 
# COMPUTE MEAN SQUARE DISTANCES
for i in range(n_cities):
	for j in range(n_cities): 
		nssq += D[i,j]**2

msq = nssq / (2*(n_cities**2))
print(n_cities)
print(msq)

# COMPUTE TRACE
XXT = np.zeros(D.shape, dtype=np.int32)
for i in range(n_cities):
	xxi= 0 
	for j in range(n_cities): 
		xxi += D[j,i]**2
	XXT[i,i] = xxi / n_cities - msq

# COMPUTE OUTER DIAGONALS
for i in range(n_cities):	
	for j in range(i+1,n_cities): 
	# for j in range(0,n_cities): 
		XXT[i,j] = -0.5*(D[i,j]**2 - XXT[i,i] - XXT[j,j])
		XXT[j,i] = XXT[i,j]

print(XXT)		

# POWER METHOD II see BLUM, Foundations of datascience
B = XXT.astype(np.float32) 
eps= 10e-3

V = np.zeros(B.shape, dtype=np.float32)
S = np.zeros(B.shape, dtype=np.float32)
kmax=1000
for i in  range(n_cities): 
	k=0
	x = np.random.rand(n_cities) 
	x = x / norm(x)
	first= True 
	y = 1000
	yold=0
	while first or (norm(y-yold)>eps and k<kmax): 				
		xold = x 
		x = B.dot(x)
		x = x / norm(x)
		y = x
		yold = xold 
		k+=1	
		first= False
		# print(norm(y-yold))
		sys.stdout.write('i:%d\t:delta:%.2f\r' % (k, norm(y-yold)))
		sys.stdout.flush()			
	print('')
	S[i,i]= norm(B.dot(x))	
	V[i,:]= y 

	y= y.reshape(n_cities,1)
	print(B)
	B -= (S[i,0]**2)*(y*y.T) 
	print(B)
	
# print(S)
# print(V)
print(B)








