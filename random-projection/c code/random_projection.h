#ifndef RANDOM_PROJECTION_H
#define RANDOM_PROJECTION_H

/*
Created on Sep 19, 2017

@author: Matheus Werner

motivation:Random Projection Implementation

*/

#include "matrix.h"

void random_projection(SparseMatrix* A, char* methodname, int d, SparseMatrix* ALower, float *matrix_cputime, float *proj_cputime);

#endif
