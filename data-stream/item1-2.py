# -*-encoding:utf8-*-
import numpy as np
import sys
import hashlib
import struct

np.random.seed(100)

def batchOfRandoms(batches,sizeOfRandomArray):
    random_numbers_size = sizeOfRandomArray#int(1e11)
    max_number = int(1e11) #int(1e11)

    for i in range(batches):
        array = np.random.uniform(low=0.0, high=1., size=sizeOfRandomArray)
        yield np.minimum(1./np.power(array, 2), max_number)


# Passo 1 Gere uma sequência de tamanho N e calcule o total de numeros distintos criados.

def estimate(batches,sizeOfRandomArray):
    uniques = np.array([])
    #for array in batchOfRandoms(batches = int(1e3), sizeOfRandomArray = int(1e8)):
    for array in batchOfRandoms(batches, sizeOfRandomArray):
        uniques = np.unique(np.concatenate((uniques,array)))
        #uniques = np.unique(array)
    return len(uniques)

# Passo 2 Gere uma sequência de tamanho N e estime o total de numeros distintos criados através da
# abordagem vista na aula. Estude o impacto de variar o numero de funções de hash.

def getTailLenght(hex):
    bits = int(hex)
    print type(bits)
    count = 0
    bitIndex = 1 
    while(bits&bitIndex is 0):
        count += 1
        bitIndex += 1

    return count

def FlajoletMartin(batches, sizeOfRandomArray):
    # Averiguar quais funções de hash
    hashFunctions = []
    
    for array in batchOfRandoms(batches, sizeOfRandomArray):
        for value in array:
            ba = bytearray(struct.pack("f", value))
            for hashFunction in hashFunctions:
                # Pegar as maiores tails
                tail = getTailLenght(hashFunction(ba))

#testes
print getTailLenght("4")

print estimate(2,int(1e3))