/*
Created on Sep 19, 2017

@author: Matheus Werner

motivation: Basic Sparse Matrix Operations

*/

#include <stdlib.h> 
#include <stdio.h>
#include "matrix.h"

typedef struct SparseMatrix {
	int n_rows;
	int n_columns;
	SparseVector** rows;
} SparseMatrix;

SparseMatrix* sparse_matrix_create_empty(int m, int n){
	int i;
	SparseMatrix* A;

	// Instantiate sparse matrix
	A = (SparseMatrix*)malloc(sizeof(SparseMatrix));

	// Fill matrix vector variables
	A->n_rows = m;
	A->n_columns = n;
	A->rows = (SparseVector**)malloc(sizeof(SparseVector*)*m);

	// Instantiate NULL for each row
	for( i = 0; i < m; i++){
		A->rows[i] = NULL;
	}
	return A;
}

SparseMatrix* sparse_matrix_create(int m, int n, float** rows){
	int i;
	SparseMatrix* A;

	// Instantiate empty sparse matrix
	A = sparse_matrix_create_empty(m, n);

	// Instantiate an sparse vector for each row
	for( i = 0; i < m; i++){
		A->rows[i] = sparse_vector_create(n, rows[i]);
	}
	return A;
}

void sparse_matrix_free(SparseMatrix* A){
	int i;

	// Free each row
	for(i = 0; i < A->n_rows; i++){
		sparse_vector_free(A->rows[i]);
		A->rows[i] = NULL;
	}

	// Free rows variable
	free(A->rows);
	A->rows = NULL;
	
	// Free matrix variable
	free(A);
	A = NULL;
}

void sparse_matrix_multsv(SparseMatrix* A, SparseVector* v, SparseVector** w){
	int i;
	float* row;
	
	// Instantiate a vector to store all dot products
	row = (float*)malloc(sizeof(float)*A->n_rows);

	// Calculate dot products
	for( i = 0; i < A->n_rows; i++){
		row[i] = sparse_vector_multsv(A->rows[i], v);
	}
	
	// Instantiate a sparse vector
	*w = sparse_vector_create(A->n_rows, row);

	// Free vector
	free(row);
	row = NULL;
}

void sparse_matrix_multsm(SparseMatrix* A, SparseMatrix* B, SparseMatrix* C){
	int i;

	// OBS:	Here we're expecting that B is transposed. That is,
	//	Matrix A should be MxN
	//	Matrix B should be QxN
	//	Matrix C should be MxQ
	for(i = 0; i < B->n_rows; i++){
		sparse_matrix_multsv(A, B->rows[i], &(C->rows[i]));
	}
}

void sparse_matrix_distances(SparseMatrix* A, SparseMatrix* D){
	int i, j;
	float *d;

	// Instantiate a vector to store all dot products
	d = (float*)malloc(sizeof(float)*A->n_rows);

	for(i = 0; i < A->n_rows; i++){
		d[i] = 0;
		for(j = i + 1; j < A->n_rows; j++){
			d[j] = sparse_vector_square_distance(A->rows[i], A->rows[j]);
		}
		D->rows[i] = sparse_vector_create(A->n_rows, d);
	}

	// Free vector
	free(d);
	d = NULL;
}

void sparse_matrix_show(SparseMatrix* A){
	int i;
	for(i = 0; i < A->n_rows; i++){
		sparse_vector_show(A->rows[i]);
	}
}

SparseMatrix* sparse_matrix_read(char* filename, int* m, int* n){
	int i, j;
	float *row, value;
	SparseMatrix* A;
	FILE* pFile;

	// Open file
	pFile = fopen(filename, "r");
	if (pFile == NULL){
		printf("Error: file pointer is null.");
		exit(1);
	}

	// Get matrix dimensions
	fscanf(pFile, "%d %d", m, n);	

	// Instantiate a vector to store all dot products
	row = (float*)malloc(sizeof(float)*(*n));

	// Instantiate sparse matrix
	A = sparse_matrix_create_empty(*m, *n);

	// Fill sparse matrix
	for(i = 0; i < *m; i++){
		for(j = 0; j < *n; j++){
			fscanf(pFile, "%f", &value);
			row[j] = value;
		}
		A->rows[i] = sparse_vector_create(*n, row);
	}

	// Free row variable
	free(row);
	row = NULL;

	// Close file
	fclose(pFile);

	return A;
}

void sparse_matrix_write(char* filename, SparseMatrix* A){
	int i, j, n;
	float *v;
	FILE* pFile;

	// Open file
	pFile = fopen(filename, "w");
	if (pFile == NULL){
		printf("Error: file pointer is null.");
		exit(1);
	}

	// Write matrix dimensions
	fprintf(pFile, "%d %d\n", A->n_rows, A->n_columns);

	// Dump matrix
	for(i = 0; i < A->n_rows; i++){
		// Get dense row so we can write it
		v = sparse_vector_todense(A->rows[i], &n);

		// Write row
		for(j = 0; j < n; j++){
			if(j == n - 1)
				fprintf(pFile, "%f\n", v[j]);
			else
				fprintf(pFile, "%f ", v[j]);
		}

		// Free dense row
		free(v);
		v = NULL;
	}

	// Close file
	fclose(pFile);
}
