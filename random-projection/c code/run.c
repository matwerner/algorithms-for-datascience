/*
Created on Sep 19, 2017

@author: Matheus Werner

motivation: API for run the experiments requested by the Random Projections project

*/

#include <math.h>
#include <stdlib.h> 
#include <stdio.h>
#include <string.h>
#include <time.h>
#include "matrix.h"
#include "random_projection.h"

static float calculate_cpu_time(clock_t begin, clock_t end){
	return (float)(end - begin) / CLOCKS_PER_SEC;
}

static void dense_matrix_free(int m, float** A){
	int i;
	for( i = 0; i < m; i++){
		free(A[i]);
		A[i] = NULL;
	}
	free(A);
}

static float distance_max_distortion(int m, float** A, float** B){
	int i, j;
	float distortion, max_distortion = 0;

	for(i = 0; i < m; i++){
		for(j = i+1; j < m; j++){
			distortion = fabs((A[i][j] / B[i][j]) - 1);
			if(distortion > max_distortion){
				max_distortion = distortion;
			}
		}
	}

	return max_distortion;
}

void experiment(SparseMatrix* A, SparseMatrix* D, char* methodname, int d){
	int m, n;
	float CPU_Time[3], **DDense, **DAproxDense, max_distortion;
	SparseMatrix *ALower, *DAprox;
	clock_t start;

	// Get input matrix shape
	sparse_matrix_get_shape(A, &m, &n);

	// Instantiate the Lower Dimension Input Matrix
	ALower = sparse_matrix_create_empty(m, d);

	// Generate the Lower Dimension Matrix
	random_projection(A, methodname, d, ALower, &CPU_Time[0], &CPU_Time[1]);

	// Instantiate a Distance Matrix between all vectors
	DAprox = sparse_matrix_create_empty(m, m);

	// Calculate Distance Matrix
	start = clock();
	sparse_matrix_distances(ALower, DAprox);
	CPU_Time[2] = calculate_cpu_time(start, clock());

	// Calculate Max Distorcion
	DDense = sparse_matrix_todense(D, &m, &m);
	DAproxDense = sparse_matrix_todense(DAprox, &m, &m);
	max_distortion = distance_max_distortion(m, DAproxDense, DDense);

	// Print Experiment Results
	printf("%s\t%d\t\t%f\t%f\t%f\t%f\n", methodname, d, CPU_Time[0], CPU_Time[1], CPU_Time[2], max_distortion);

	sparse_matrix_write("ALower.txt", ALower);
	sparse_matrix_write("DAprox.txt", DAprox);

	// Free variables
	sparse_matrix_free(ALower);
	sparse_matrix_free(DAprox);
	dense_matrix_free(m, DDense);
	dense_matrix_free(m, DAproxDense);
}

void experiment_command(char* bowfile, char* distancefile, int t, char* methodname, int d){
	int m, n, i;
	SparseMatrix *A, *D;

	// Read Original Document BoW Matrix
	A = sparse_matrix_read(bowfile, &m, &n);

	// Read Original Document Distance Matrix
	D = sparse_matrix_read(distancefile, &m, &m);

	// Print Experiment Results Header
	printf("Method\t\tDimension\tMatrix (sec)\tProj (sec)\tDistance (sec)\tMax Distorsion\n");

	// Run all experiments
	for(i = 0; i < t; i++){
		experiment(A, D, methodname, d);
	}

	// Free variables
	sparse_matrix_free(A);
	sparse_matrix_free(D);
}

void distance_command(char* inputfile, char* outputfile){
	int m, n;
	SparseMatrix *A, *D;

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
	int i, d = -1, t = -1;
	char *command, *bowfile, *distancefile, *methodname;

	// Read and parse arguments
	command = argv[1];
	for(i = 2; i < argc; i++){
		if(strcmp(argv[i], "--bow") == 0){
			bowfile = argv[i+1];
		}
		else if(strcmp(argv[i], "--distance") == 0){
			distancefile = argv[i+1];
		}
		else if(strcmp(argv[i], "--dimension") == 0){
			d = atoi(argv[i+1]);
		}
		else if(strcmp(argv[i], "--method") == 0){
			methodname = argv[i+1];
		}
		else if(strcmp(argv[i], "--time") == 0){
			t = atoi(argv[i+1]);
		}
		else{
			printf("Argument %s not supported.\n", argv[i]);
			exit(1);
		}		
		i++;
	}

	// Run selected command
	if(strcmp(command, "experiment") == 0){
		experiment_command(bowfile, distancefile, t, methodname, d);
	}
	else if(strcmp(command, "distance") == 0){
		distance_command(bowfile, distancefile);
	}
	else{
		printf("Command %s not implemented.\n", command);
		exit(1);
	}
	
	return 0;
}
