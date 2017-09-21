CC = gcc
CFLAGS  = -g -Wall

all: dimensionality_reduction

dimensionality_reduction: vector.o matrix.o dimensionality_reduction.o
	$(CC) $(CFLAGS) vector.o matrix.o dimensionality_reduction.o -o dimensionality_reduction -lm

vector.o: vector.c
	$(CC) $(CFLAGS) -c vector.c

matrix.o: matrix.c
	$(CC) $(CFLAGS) -c matrix.c

dimensionality_reduction.o: dimensionality_reduction.c
	$(CC) $(CFLAGS) -c dimensionality_reduction.c

.PHONY: clean
clean:
	$(RM) *.o
