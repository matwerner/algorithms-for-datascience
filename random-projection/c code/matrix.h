/*
Created on Sep 19, 2017

@author: Matheus Werner

motivation: Basic Sparse Matrix Operations

*/

#include "vector.h"

typedef struct SparseMatrix SparseMatrix;

SparseMatrix* sparse_matrix_create_empty(int m, int n);
SparseMatrix* sparse_matrix_create(int m, int n, float** rows);
void sparse_matrix_free(SparseMatrix* A);
void sparse_matrix_multsv(SparseMatrix* A, SparseVector* v, SparseVector** w);
void sparse_matrix_multsm(SparseMatrix* A, SparseMatrix* B, SparseMatrix* C);
void matrix_multsv(int m, int n, float** A, SparseVector* v, SparseVector** w);
void sparse_matrix_multdm(SparseMatrix* A, int m, int n, float** B, SparseMatrix* C);
void sparse_matrix_distances(SparseMatrix* A, SparseMatrix* D);
void sparse_matrix_show(SparseMatrix* A);
float** sparse_matrix_todense(SparseMatrix* A, int *m, int *n);
SparseMatrix* sparse_matrix_read(char* filename, int* m, int* n);
void sparse_matrix_write(char* filename, SparseMatrix* A);


