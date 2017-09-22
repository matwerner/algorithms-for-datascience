
#To build:
#$ python setup.py build_ext --inplace

def hello():
    print "zup"

file_separator = "\n"
attribute_separator = "\t"

def get_distances_dictionary(file_list):
    
    dictionary = {}

    for file in file_list:
        dictionary[file] = get_distance_matrix(file)
    
    return dictionary


def get_distance_matrix(file_name):
    file = open(file_name,'r')

    file_lines = file.read().split(file_separator)
    n_lines = len(file_lines)

    distances_matrix = [[0 for x in range(0, n_lines)] for y in range(0, n_lines)]

    for i in range(0,n_lines):
        for j in range(i+1,n_lines):
            vec1 = file_lines[i].split(attribute_separator)
            vec2 = file_lines[j].split(attribute_separator)

            d =  distance(vec1,vec2)
            
            distances_matrix[i][j] = d 
            distances_matrix[j][i] = d 

    file.close()
    return distances_matrix


def distance(vec1,vec2):
    internal_summation = 0
    dimension = len(vec1)#len(vec1) == len(vec2)

    for i in range(0,dimension):
        coordinates_dif = vec1[i] - vec2[i]
        internal_summation = internal_summation + coordinates_dif * coordinates_dif
    
    return internal_summation



