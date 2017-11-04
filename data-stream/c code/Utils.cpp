#include <algorithm>
#include <random>

#include "Utils.hpp"

using namespace std;

// Get a random number generator
mt19937_64 e2(100);

uint64_t* Utils::random_data_stream(uint64_t size) {
    // Instantiate distribution method
    std:uniform_real_distribution<double> dist(0, 1);

    // Instantiate data stream
    uint64_t* dataStream = new uint64_t[size];
    for(uint64_t i = 0; i < size; i++){
        // Generate random number between 0 and 1
        double randomValue = dist(e2);

        // Convert number to new distribution
        dataStream[i] = (uint64_t) std::min(1.0/(randomValue * randomValue), Utils::DATA_STREAM_MAX_VALUE);
    }

    return dataStream;
}