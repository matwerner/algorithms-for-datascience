/*
Created on Sep 19, 2017

@author: Matheus Werner

motivation: Basic Sparse Vector Operations

*/

typedef struct SparseVector SparseVector;

SparseVector* sparse_vector_create(int n, float* values);
void sparse_vector_free(SparseVector* v);
float sparse_vector_multdv(SparseVector* u, float* v);
float sparse_vector_multsv(SparseVector* u, SparseVector *v);
float sparse_vector_square_distance(SparseVector* u, SparseVector* v);
float* sparse_vector_todense(SparseVector* u, int* n);
void sparse_vector_show(SparseVector* u);
