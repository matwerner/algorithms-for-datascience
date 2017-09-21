/*
Created on Sep 19, 2017

@author: Matheus Werner

motivation: Basic Vector Operations

*/

#include <stdlib.h> 
#include <stdio.h>
#include <limits.h>
#include "vector.h"

typedef struct SparseVector {
	int size;
	int real_size;
	int* indexes;
	float* values;
} SparseVector;

#define DEFAULT_VALUE 0.0

static SparseVector* sparse_vector_create_internal(int n, int real_n, int* indexes, float* values);

SparseVector* sparse_vector_create(int n, float* values){
	int i, j, real_n;
	SparseVector* v;
	
	// Count number of non-zero values in the vector
	real_n = 0;
	for(i = 0; i < n; i++){
		if(values[i] != DEFAULT_VALUE)
			real_n++;
	}

	// Instantiate sparse vector
	v = (SparseVector*)malloc(sizeof(SparseVector));

	// Fill sparse vector variables
	v->size = n;
	v->real_size = real_n;
	v->indexes = (int*)malloc(sizeof(int)*real_n);
	v->values = (float*)malloc(sizeof(float)*real_n);

	// Only stores non-zero values
	for(i = 0, j = 0; i < n; i++){
		if(values[i] == DEFAULT_VALUE)
			continue;

		v->indexes[j] = i;
		v->values[j] = values[i];
		j++;
	}	

	return v;
}

static SparseVector* sparse_vector_create_internal(int n, int real_n, int* indexes, float* values){
	// Instantiate sparse vector
	SparseVector* v = (SparseVector*)malloc(sizeof(SparseVector));

	// Fill sparse vector
	v->size = n;
	v->real_size = real_n;
	v->indexes = indexes;
	v->values = values;

	return v;
}

void sparse_vector_free(SparseVector* u){
	// Free all indexes
	free(u->indexes);
	u->indexes = NULL;
	
	// Free all values
	free(u->values);
	u->values = NULL;

	// Free sparse vector
	free(u);
	u = NULL;
}

float sparse_vector_multsv(SparseVector* u, SparseVector* v){
	int i, j, index_small, index_big;
	float tot = 0;
	SparseVector *v_small, *v_big;

	// Multiply by the smaller vector (For efficient purposes)
	v_small = u->real_size > v->real_size? v : u;
	v_big = u->real_size > v->real_size? u : v;

	// Only consider indexes that have value on both vectors
	i = 0, j = 0;
	while(i < v_small->real_size){
		index_small = v_small->indexes[i];
		index_big = v_big->indexes[j];		
		if(index_small > index_big){
			j++;
		}
		else if(index_small < index_big){
			i++;
		}
		else{
			tot += (v_small->values[i] * v_big->values[j]);
			i++;
			j++;
		}
	}
	
	return tot;
}

float sparse_vector_square_distance(SparseVector* u, SparseVector* v){
	int i, j, index_u, index_v;
	float tot = 0, parcial;

	// Only consider indexes that have value on, at least, one of the vectors
	i = 0, j = 0;
	while(i + j < u->real_size + v->real_size){
		index_u = i < u->real_size? u->indexes[i] : INT_MAX;
		index_v = j < v->real_size? v->indexes[j] : INT_MAX;
		
		parcial = 0;
		if(index_v > index_u){
			parcial = u->values[i];
			i++;
		}
		else if(index_v < index_u){
			parcial = v->values[j];
			j++;
		}
		else{
			parcial = (v->values[j] - u->values[i]);
			i++;
			j++;
		}

		tot += (parcial * parcial);
	}
	
	return tot;
}

float* sparse_vector_todense(SparseVector* u, int* n){
	int i, j;
	float* v, value;

	*n = u->size;

	v = (float*)malloc(sizeof(float)*u->size);
	for(i = 0, j = 0; i < u->size; i++){
		value = DEFAULT_VALUE;
		if(u->indexes[j] == i){
			value = u->values[j];
			j++;
		}
		v[i] = value;
	}
	return v;
}

void sparse_vector_show(SparseVector* u){
	int i, j;
	float value;
	for (i = 0, j = 0; i < u->size; i++){
		value = DEFAULT_VALUE;
		if(u->indexes[j] == i){
			value = u->values[j];
			j++;
		}
		printf("%.2f\t", value);
	}
	printf("\n");
}

// FOR TEST PURPOSES
/*
int main(void){
	int n = 12;
	float value;
	float u[] = {0, 0, 0, 1, 0, 2, 3, 0 , 0, 5, 1, 1};
	float v[] = {0, 2, 0, 0, 9, 0, 3, 0 , 0, 1, 0, 1};
	SparseVector *u_sparse, *v_sparse;

	u_sparse = sparse_vector_create(n, u);
	v_sparse = sparse_vector_create(n, v);

	sparse_vector_show(u_sparse);
	sparse_vector_show(v_sparse);

	value = sparse_vector_multsv(u_sparse, v_sparse);
	printf("%.2f\n", value);

	value = sparse_vector_square_distance(u_sparse, v_sparse);
	printf("%.2f\n", value);

	sparse_vector_free(u_sparse);	
	sparse_vector_free(v_sparse);
}
*/
