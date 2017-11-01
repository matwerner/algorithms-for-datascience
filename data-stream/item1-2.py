# -*-encoding:utf8-*-
import numpy as np
import sys
import hashlib
import json

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



def FlajoletMartin(batches, sizeOfRandomArray):
    # Averiguar quais funções de hash
    hashFunctions = [{"function":hashFunction1,"maximumTail":-1,"maximumTailNumber":None},
                     {"function":hashFunction2,"maximumTail":-1,"maximumTailNumber":None}]

    for array in batchOfRandoms(batches, sizeOfRandomArray):
        for value in array:
            for i in range(len(hashFunctions)):
                hashFunction = hashFunctions[i]["function"]
                tail = getTailLenght(hashFunction(int(value)))

                if tail > hashFunctions[i]["maximumTail"]:
                    hashFunctions[i]["maximumTail"] = tail
                    hashFunctions[i]["maximumTailNumber"] = int(value)
                    

    with open("outputs.txt","w") as outputFile:
        for hashFunction in hashFunctions:
            outputFile.write( str(hashFunction["maximumTail"])+"---"+ str(hashFunction["maximumTailNumber"])+"\n" ) 
        # results


    
# http://www.planetmath.org/goodhashtableprimes
def standardHashFunction(primeNumber, value,coefficient=1):
    return (coefficient*value)%primeNumber
    
def hashFunction1(value):
    return standardHashFunction(3145739,value,3)

def hashFunction2(value):
    return standardHashFunction(12582917,value,4)

def getTailLenght(intValue):
    count = 0
    #bits = bin(intValue)
    
    v = 1 # Value for bitwise operation
    
    while (intValue & v) is  0:
        count += 1
        v =  v<<1

    return count


#testes
print getTailLenght(64)

print estimate(2,int(1e3))

FlajoletMartin(2, int(1e3))
