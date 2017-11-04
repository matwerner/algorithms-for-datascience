# -*-encoding:utf8-*-
import argparse
import numpy as np
import matplotlib.pyplot as plt
import math

VERBOSE=True

def meanEstimate(elements):
    return np.mean(elements)

def medianEstimate(elements):
    return np.median(elements)

def chunks(elements,groupSize):
    nGroups = len(elements)/groupSize
    if VERBOSE:
        print "Quantidade de grupos: %s"%(nGroups)
    return np.array_split(elements,nGroups)

def minimumSizeOfGroup(nUniques):
    return math.log(nUniques,2)

def combineEstimates(elements,nUniques):
    groupSize = minimumSizeOfGroup(nUniques)
    groups = chunks(elements,groupSize)
    groupsMeans =  map(meanEstimate, groups)
    return medianEstimate(groupsMeans)

def getFileValues(fileName):
    values = None
    
    with open(fileName ,"r") as file:
        lines = file.readlines()

        valueCount = int(lines[0])
        values = map(int,lines[1:])
        
        if len(values) != valueCount:
            raise Exception("Estrutura de arquivo inválida")

    return values

def graficoVariacaoDeFuncoesHash(nValoresUnicos,tails):
    print "a"

if __name__ == '__main__':
    fileName = "FlajoletMartin.txt" 
    values = getFileValues(fileName)
    nUniques = 4
    minGroupSize = minimumSizeOfGroup(nUniques)

    # O número de experimentos realizados, todos considerando um numero de funções de batch que é potência de 2
    nExperiments = math.log(len(values),2)

    if not (nExperiments).is_integer():
        raise Exception("o numero de valores passados não é uma potencia de 2")
        
    experimentsResults = []

    if VERBOSE:
        print "O valor mínimo de itens no grupo é log(%s) :%s"%(nUniques,minGroupSize)

    for i in range(int(nExperiments)+1):
        
        if VERBOSE:
            print "\nExperimento com %s funções de hash\n"%(2**i)

        # O valor mínimo de elementos no grupo tem de ser log(unicos)
        # e só devemos plotar os casos em que temos o mínimo para um grupo
        if(minGroupSize > 2**i):
            if VERBOSE:
                print "Pulando o experimento 2^%s = %s já que o tamanho mínimo do grupo é %s"%(i,2**i,minGroupSize)
            continue
        
        estimate = combineEstimates(values[:2**i],nUniques)

        experimentsResults.append([i,estimate])
    
    estimates = [el[0] for el in experimentsResults]
    potences = [el[1] for el in experimentsResults]

    plt.plot(potences,estimates)
    plt.xlabel('potences')
    plt.ylabel('estimates')
    plt.axhline(y=nUniques, color='r', linestyle='-')

    plt.show()


# def teste():
#     import numpy as np
#     import matplotlib.mlab as mlab
#     import matplotlib.pyplot as plt

#     mu, sigma = 100, 15
#     x = mu + sigma*np.random.randn(10000)

#     # the histogram of the data
#     n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

#     # add a 'best fit' line
#     y = mlab.normpdf( bins, mu, sigma)
#     l = plt.plot(bins, y, 'r--', linewidth=1)

#     plt.xlabel('Smarts')
#     plt.ylabel('Probability')
#     plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
#     plt.axis([40, 160, 0, 0.03])
#     plt.grid(True)

#     plt.show()

# teste()
