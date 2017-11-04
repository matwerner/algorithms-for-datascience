#include <algorithm>
#include <random>

#include "Utils.hpp"

using namespace std;

uint64_t* random_data_stream(uint64_t size) {
    // Get a random number generator
    std::random_device rd;
    mt19937_64 e2(rd());
    e2.seed(100);
    std:uniform_real_distribution<double> dist(0, 1);

    // Instantiate data stream
    uint64_t* dataStream = new uint64_t[size];
    for(uint64_t i = 0; i < size; i++){
        // Generate random number between 0 and 1
        double randomValue = dist(e2);

        // Convert number to new distribution
        dataStream[i] = (uint64_t) std::min(1.0/(randomValue * randomValue), DATA_STREAM_MAX_VALUE);
    }

    return dataStream;
}