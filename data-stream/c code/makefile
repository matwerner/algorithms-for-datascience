CC = g++
CFLAGS  = -g -O3 -std=c++11 -Wall

all: Run

Run: Utils.o Moment.o ProcessorBase.o Run.o
	$(CC) $(CFLAGS) Utils.o Moment.o ProcessorBase.o Run.o -o Run

Moment.o: DataStream/Moment.cpp
	$(CC) $(CFLAGS) -c DataStream/Moment.cpp

ProcessorBase.o: DataStream/ProcessorBase.cpp
	$(CC) $(CFLAGS) -c DataStream/ProcessorBase.cpp

Utils.o: Utils.cpp
	$(CC) $(CFLAGS) -c Utils.cpp

Run.o: Run.cpp
	$(CC) $(CFLAGS) -c Run.cpp

.PHONY: clean
clean:
	$(RM) *.o
