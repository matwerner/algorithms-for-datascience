CC = gcc
CFLAGS  = -g -Wall

all: run

run: vector.o matrix.o random_projection.o run.o
	$(CC) $(CFLAGS) vector.o matrix.o random_projection.o run.o -o run -lm

vector.o: vector.c
	$(CC) $(CFLAGS) -c vector.c

matrix.o: matrix.c
	$(CC) $(CFLAGS) -c matrix.c

random_projection.o: random_projection.c
	$(CC) $(CFLAGS) -c random_projection.c

run.o: run.c
	$(CC) $(CFLAGS) -c run.c

.PHONY: clean
clean:
	$(RM) *.o
