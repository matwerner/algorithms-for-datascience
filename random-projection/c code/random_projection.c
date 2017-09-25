/*
Created on Sep 19, 2017

@author: Matheus Werner

motivation:Random Projection Implementation

*/

#include <stdlib.h> 
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "random_projection.h"

static float calculate_cpu_time(clock_t begin, clock_t end){
	return (float)(end - begin) / CLOCKS_PER_SEC;
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

static float** create_gaussian(int m, int n){
	float** A, factor = sqrt(n/(float)m), mu = 0., sigma = 1./sqrt((float)n);
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

static float** create_achlioptas(int m, int n){
	float** A, random, factor = sqrt(n/(float)m), c = sqrt(3./(float)n);
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

static void dense_matrix_free(int m, float** A){
	int i;
	for( i = 0; i < m; i++){
		free(A[i]);
		A[i] = NULL;
	}
	free(A);
}

void random_projection(SparseMatrix* A, char* methodname, int d, SparseMatrix* ALower, float *matrix_cputime, float *proj_cputime){
	int m, n;
	float **P;
	clock_t start;

	// Get input matrix shape
	sparse_matrix_get_shape(A, &m, &n);

	// Select and run a dimensionality reduction method
	start = clock();
	if(strcmp(methodname, "gaussian") == 0){
		P = create_gaussian(d, n);
	}
	else if(strcmp(methodname, "achlioptas") == 0){
		P = create_achlioptas(d, n);
	}
	else{
		printf("Method %s not implemented.\n", methodname);
		exit(1);
	}
	*matrix_cputime = calculate_cpu_time(start, clock());	

	// Run projection to lower dimension
	start = clock();
	sparse_matrix_multdm(A, d, n, P, ALower);
	*proj_cputime = calculate_cpu_time(start, clock());

	// Free variables
	dense_matrix_free(d, P);
}
