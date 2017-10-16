# -*- coding: utf-8 -*-
import numpy as np

MATRIX_SHAPE = (20,20)

def algorithm(D):

    # COMPUTE MSQ
    NSSQ=0
    for i in range(MATRIX_SHAPE[0]):
        for j in range(MATRIX_SHAPE[1]):
            NSSQ = NSSQ + D[i,j] * D[i,j]
    
    MSQ = NSSQ/2*MATRIX_SHAPE[0]*MATRIX_SHAPE[1]

    # COMPUTE TRACE
    
    # TODO - Aqui a nossa matriz não é simetrica completamente, os pontos na diagonal que são 0, i.e - distancia de LA com LA é só nos primeiros 10x10
    # TODO - Mudei o loop para pegar a primeira submatriz 10x10
    XXT = np.zeros(MATRIX_SHAPE)
    for i in range(MATRIX_SHAPE[0]):
        xx_i = 0
        for j in range(MATRIX_SHAPE[1]):
            xx_i =  xx_i + D[i,j]
        XXT[i,i] = xx_i - MSQ

    # COMPUTE OTHER DIAGONALS

    # TODO - Aqui não é para ignorar as diagonais?
    for i in range(MATRIX_SHAPE[0]):
        for j in range(MATRIX_SHAPE[1]):
            # TODO - não tenho certeza de que entendi a letra no rascunho dessa parte
            # TODO XXT[j,j] é out of bounds inexoravelmente
            XXT[i,j] = -0.5 * (D[i,j]*D[i,j] - XXT[i,i] - XXT[j,j])

    u, s, v = np.linalg.svd(XXT)
    X = u*np.sqrt(s)

    return X

# BUILD MATRIX FROM FILE

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

matrix.shape = MATRIX_SHAPE

matrix = np.matrix(matrix)

#print matrix

print algorithm(matrix)


m =  algorithm(matrix)

m = m[0:2,:]
print len(m[0])
import matplotlib.pyplot as plt
plt.plot(m[0,:], m[1,:], 'ro')
plt.axis([-10, 10, -10, 10])
plt.show()
