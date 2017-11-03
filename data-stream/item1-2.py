# -*-encoding:utf8-*-
import numpy as np
import sys
import hashlib
import json
import utils

np.random.seed(100)

def batchOfRandoms(batches,sizeOfRandomArray):
    random_numbers_size = sizeOfRandomArray#int(1e11)
    max_number = int(1e11) #int(1e11)

    for i in range(batches):
        array = np.random.uniform(low=0.0, high=1., size=sizeOfRandomArray)
        yield np.minimum(1./np.power(array, 2), max_number)


# Passo 1 Gere uma sequência de tamanho N e calcule o total de numeros distintos criados.

def calculateUniques(batches,sizeOfRandomArray):
    uniques = {}
    #for array in batchOfRandoms(batches = int(1e3), sizeOfRandomArray = int(1e8)):
    # values for feedback processing
    count = 0
    feedbackCount = 0
    total = batches*sizeOfRandomArray
    percentFeedback = 0.1

    for array in batchOfRandoms(batches, sizeOfRandomArray):
        for value in array:
            uniques[value] = 1
            
            # feedback
            count += 1
            if count % int(percentFeedback*total) is 0:
                feedbackCount+=1
                print "%s  processado \n"%(feedbackCount*percentFeedback*100)


        #uniques = np.unique(array)

    with open("uniquesOutput.txt") as uniquesOutput:
        uniquesOutput.write(str(len(uniques)))

    return len(uniques)

# Passo 2 Gere uma sequência de tamanho N e estime o total de numeros distintos criados através da
# abordagem vista na aula. Estude o impacto de variar o numero de funções de hash.

def FlajoletMartin(batches, sizeOfRandomArray,Nhashes,prime,size):
    
    # Averiguar quais funções de hash
    hashFunctions = []

    for i in range(Nhashes):      
        hashFunctions.append(HashFunction(prime,size))

    # valuies for feedback processing
    count = 0
    feedbackCount = 0
    total = batches*sizeOfRandomArray
    percentFeedback = 0.1

    for array in batchOfRandoms(batches, sizeOfRandomArray):

        for value in array:
            for i in range(len(hashFunctions)):
                hashFunctions[i].Hash(int(value))

            # feedback
            count += 1
            if count % int(percentFeedback*total) is 0:
                feedbackCount+=1
                print "%s  processado \n"%(feedbackCount*percentFeedback*100)


    # Results output...

    def logValue(file,valueName,value):
        file.write(str(valueName)+"---"+str(value)+"\n")

    with open("outputs.txt","w") as outputFile:
        for i in range(len(hashFunctions)):
            logValue(outputFile,"Hash function",str(i))
            logValue(outputFile,"Max tail",hashFunctions[i].maximumTail)
            logValue(outputFile,"Maximum tail number",hashFunctions[i].maximumTailNumber)

class HashFunction:
    def __init__ (self,primeNumber,size):
        self.primeNumber = primeNumber
        # self.coefficient = coefficient
        self.maximumTail = -1
        self.maximumTailNumber = None
        self._hashFunction = utils.universal_hash(primeNumber,size)

    def Hash(self,value):
        hashValue = self._hashFunction(value)
        hashValueTail = getTailLenght(hashValue)

        if hashValueTail > self.maximumTail:
            self.maximumTail = hashValueTail
            self.maximumTailNumber = value

        return hashValue
    
# http://www.planetmath.org/goodhashtableprimes

def getTailLenght(intValue):
    count = 0
    #bits = bin(intValue)
    
    v = 1 # Value for bitwise operation
    
    while (intValue & v) is  0:
        count += 1
        v =  v<<1
    return count


#testes
#print getTailLenght(64)

print calculateUniques(int(1e3),int(1e8))

#FlajoletMartin(batches= 1,sizeOfRandomArray= int(1e7),Nhashes=2**8,prime=1610612741,size=1)
