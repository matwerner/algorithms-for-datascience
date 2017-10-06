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
D = np.array([
	[0, 		400,  851, 1551, 1769],
	[400, 	  0,  454, 1198, 1370],
	[ 851,  454, 	  0, 803, 	920],
	[1551, 1198, 	803, 	 0, 	663],
	[1769, 1370, 	920, 663, 		0]
])

print(D)		
n= len(D)
nssq= 0 
# COMPUTE MEAN SQUARE DISTANCES
for i in range(n):
	for j in range(n): 
		nssq += D[i,j]**2

msq = nssq / (2*(n**2))

# COMPUTE TRACE
XXT = np.zeros(D.shape, dtype=np.int32)
for i in range(n):
	xxi= 0 
	for j in range(n): 
		xxi += D[j,i]**2
	XXT[i,i] = xxi / n - msq

# COMPUTE OUTER DIAGONALS
for i in range(n):	
	for j in range(i+1,n): 
		XXT[i,j] = -0.5*(D[i,j]**2 - XXT[i,i] - XXT[j,j])
		XXT[j,i] = XXT[i,j]


# POWER METHOD II see BLUM, Foundations of datascience exercices 3.30
B = XXT.astype(np.float32) 
d = n 
r = n

if r > n or r > d: 
	print(' r[%d] <= n[%d] and r[%d] <= d[%d]' %(r,n,r,d))

eps= 10e-10
residuals= {} 
flags= []
iterations= []
S = np.zeros(B.shape, dtype=np.float32)
U = np.zeros(B.shape, dtype=np.float32)
V = np.zeros(B.shape, dtype=np.float32)

kmax=1000
for i in range(n): 
	k=0
	vi = np.random.rand(n) 
	vi = vi / norm(vi)
	first= True 

	while first or (residuals[i]>eps and k<kmax): 						
		v0 = vi  
		vi =  B.dot(vi) 				
		vi = vi / norm(vi)
		k+=1	
		first= False

		residuals[i] =norm(vi-v0)		
		sys.stdout.write('i:%d\t:delta:%.2f\r' % (k, residuals[i]))
		sys.stdout.flush()			
	flags.append(residuals[i]<eps)	
	iterations.append(k)

	print('')
	S[i,i]= norm(B.dot(vi))
	V[i,:]= vi 
	U[:,i]= vi 

	vi= vi.reshape(n,1)
	B -= (S[i,i])*(vi*vi.T) 


u, s, v = np.linalg.svd(XXT)
print('%===========================S- experimental==========================%')	
print(np.diag(S))
print('%===========================S- theoretical==========================%')	
print(s)
print('%===========================S-exp vs S-theo==========================%')	
print(np.allclose(np.diag(S)[:-1],s[:-1])) 
print('%===========================V - experimental=========================%')	
print(V)
print('%===========================V - theoretical==========================%')	
print(v)
print('%===========================U - theoretical=========================%')	
print(u)
print('%===========================X - theoretical==========================%')	
X = (u[:,:r] * s[:r])
# X = (np.diag(S)[:-1]*V[:-1,:].T)
print(X)
# x = s*v.T 
# print(x)
# print(np.allclose(X , x[:,:-1]))
print('%===========================V - CLOSE=================================%')	
# print(np.allclose(V[:-1,:],v[:-1,:])) 
print('%============================RESIDUALS================================%')	
print(list(residuals.values()))
print('%========================CONVERGENCE FLAGS=============================%')	
print(flags)








