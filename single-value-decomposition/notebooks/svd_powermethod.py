# -*- coding: utf-8 -*-
'''
Created on Oct 5, 2017

@author: Varela

motivation: The power method to SVD

'''


import numpy as np 
# testing with boston, buffalo, chicago, dallas, denver
D = np.array([
	[0, 		400,  851, 1551, 1769],
	[400, 	  0,  454, 1198, 1370],
	[ 851,  454, 	  0, 803, 	920],
	[1551, 1198, 	803, 	 0, 	663],
	[1769, 1370, 	920, 663, 		0]
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






