import numpy as np 

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


def get_D():
	file = open("../datasets/matrix.txt","r")
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
	return D

def get_usalabels(): 

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

	return labels


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

