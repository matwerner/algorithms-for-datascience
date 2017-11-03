#include <algorithm>

#include "Utils.hpp"

using namespace std;

uint64_t* random_data_stream(uint64_t size) {
    // Instantiate data stream
    uint64_t* dataStream = new uint64_t[size];
    for(uint64_t i = 0; i < size; i++){
        // Generate random number between 0 and 1
        double_t randomValue = (double_t) rand() / (double_t) RAND_MAX;

        // Convert number to new distribution
        dataStream[i] = (uint64_t) std::min(1.0/(randomValue * randomValue), DATA_STREAM_MAX_VALUE);
    }

    return dataStream;
}