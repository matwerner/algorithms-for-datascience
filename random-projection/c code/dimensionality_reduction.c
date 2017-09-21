/*
Created on Sep 19, 2017

@author: Matheus Werner

motivation: API for Dimensionality Reduction methods

*/

#include <stdlib.h> 
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "matrix.h"

void print_time(clock_t begin, clock_t end){
    float elapsed = (float)(end - begin) / CLOCKS_PER_SEC;
    printf("%f\n", elapsed);
}

// Marsaglia polar method
// https://phoxis.org/2013/05/04/generating-random-numbers-from-normal-distribution-in-c/
static float rand_normal(float mu, float sigma){
    float U1, U2, W, mult;
    static float X1, X2;
    static int call = 0;

    if (call == 1)
    {
        call = !call;
        return (mu + sigma * (float) X2);
    }

    do
    {
        U1 = -1 + ((float) rand() / RAND_MAX) * 2;
        U2 = -1 + ((float) rand() / RAND_MAX) * 2;
        W = pow (U1, 2) + pow (U2, 2);
    }
    while (W >= 1 || W == 0);

    mult = sqrt ((-2 * log (W)) / W);
    X1 = U1 * mult;
    X2 = U2 * mult;

    call = !call;

    return (mu + sigma * (float) X1);
}

float** create_gaussian(int m, int n){
	float** A, factor = sqrt(n/m), mu = 0, sigma = 1/sqrt(n);
	int i,j;
	A = (float**)malloc(sizeof(float*)*m);
	for( i = 0; i < m; i++){
		A[i] = (float*)malloc(sizeof(float)*n);
		for( j = 0; j < n; j++){
			A[i][j] = factor * rand_normal(mu, sigma);
		}
	}
	return A;
}

float** create_achlioptas(int m, int n){
	float** A, random, factor = sqrt(n/m), c = sqrt(3./n);
	int i,j;
	A = (float**)malloc(sizeof(float*)*m);
	for( i = 0; i < m; i++){
		A[i] = (float*)malloc(sizeof(float)*n);
		for( j = 0; j < n; j++){
			random = (float) rand() / RAND_MAX;
			random = (random < (1./6) ? -1: (random < (5./6) ? 0 : 1));
			A[i][j] = factor * c * random;
		}
	}
	return A;
}

void dense_matrix_free(int m, float** A){
	int i;
	for( i = 0; i < m; i++){
		free(A[i]);
		A[i] = NULL;
	}
	free(A);
}

void reduce_command(char* inputfile, char* outputfile, char* methodname, int d){
	int m, n;
	float **PDense;
	SparseMatrix *A, *ALower, *D, *P;
	clock_t begin;

	// Read Input Matrix
	begin = clock();	
	A = sparse_matrix_read(inputfile, &m, &n);
	print_time(begin, clock());

	// Instantiate the Lower Dimension (Dimensionality Reduction) Input Matrix
	ALower = sparse_matrix_create_empty(m, d);

	// Instantiate a Distance Matrix between all vectors
	D = sparse_matrix_create_empty(m, m);

	// Select and run a dimensionality reduction method
	begin = clock();
	if(strcmp(methodname, "gaussian") == 0){
		PDense = create_gaussian(d, n);
	}
	else if(strcmp(methodname, "achlioptas") == 0){
		PDense = create_achlioptas(d, n);
	}
	else{
		printf("Method %s not implemented.\n", methodname);
		exit(1);
	}
	print_time(begin, clock());

	// Convert Project Matrix from Dense to Sparse
	P = sparse_matrix_create(d, n, PDense);
	dense_matrix_free(d, PDense);

	// Run projection to lower dimension
	begin = clock();
	sparse_matrix_multsm(P, A, ALower);
	print_time(begin, clock());

	// Calculate Distance Matrix
	begin = clock();
	sparse_matrix_distances(ALower, D);
	print_time(begin, clock());

	// Write Distance Matrix
	begin = clock();
	sparse_matrix_write(outputfile, D);
	print_time(begin, clock());

	// Free variables
	sparse_matrix_free(A);
	sparse_matrix_free(P);
	sparse_matrix_free(D);
	sparse_matrix_free(ALower);
}

void distance_command(char* inputfile, char* outputfile){
	int m, n;
	float **A, **D;

	// Read Input Matrix
	A = sparse_matrix_read(inputfile, &m, &n);

	// Instantiate a Distance Matrix between all vectors
	D = sparse_matrix_create_empty(m, m);

	// Calculate Distance Matrix
	sparse_matrix_distances(A, D);

	// Write Distance Matrix
	sparse_matrix_write(outputfile, D);

	// Free variables
	sparse_matrix_free(A);
	sparse_matrix_free(D);
}

int main(int argc, char** argv){
	int i, d = -1;
	char *command, *inputfile, *outputfile, *methodname;

	// Read and parse arguments
	command = argv[1];
	for(i = 2; i < argc; i++){
		if(strcmp(argv[i], "-i") == 0){
			inputfile = argv[i+1];
		}
		else if(strcmp(argv[i], "-o") == 0){
			outputfile = argv[i+1];
		}
		else if(strcmp(argv[i], "-m") == 0){
			methodname = argv[i+1];
		}
		else if(strcmp(argv[i], "-d") == 0){
			d = atoi(argv[i+1]);
		}
		else{
			printf("Argument %s not supported.\n", argv[i]);
			exit(1);
		}		
		i++;
	}

	// Run selected command
	if(strcmp(command, "reduce") == 0){
		reduce_command(inputfile, outputfile, methodname, d);
	}
	else if(strcmp(command, "distance") == 0){
		distance_command(inputfile, outputfile);
	}
	else{
		printf("Command %s not implemented.\n", methodname);
		exit(1);
	}
		
	return 0;
}
