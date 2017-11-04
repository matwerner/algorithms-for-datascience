#include <cmath>
#include <random>

#include "FlajoletMartin.hpp"

using namespace std;

// Get a random number generator
mt19937_64 e3(1000);

DataStream::FlajoletMartin::FlajoletMartin(uint64_t hashSize, uint64_t streamSize) {
    this->hashSize = hashSize;
    this->streamSize = streamSize;

    for(uint64_t i = 0; i < hashSize; i++) {
        // Instantiate hash function
        FlajoletMartin::HashFunction hash(this->PRIME, streamSize);

        // Add to data structures
        this->hashes.push_back(hash);
        this->maximumTails.push_back(0);
    }
}

uint64_t DataStream::FlajoletMartin::get_zero_tail_size(uint64_t value) {
    uint64_t tailSize = 0;
    while((value & 1) == 0 && tailSize < 63) {        
        tailSize++;
        value = value >> 1;
    }

    return tailSize;
}

void DataStream::FlajoletMartin::process_data_stream_internal(uint64_t* dataStream, uint64_t size) { 
    std::unordered_map<uint64_t, bool>::iterator found;
    for(uint64_t i = 0; i < size; i++) {
        // Get element
        uint64_t element = dataStream[i];

        // Check if element was computed
        found = this->computed.find(element);

        // Already computed
        if(found != this->computed.end()) {
            continue;
        }

        // Not computed yet
        for(uint64_t j = 0; j < this->hashSize; j++) {
            uint64_t hashValue = this->hashes[j].compute_hash(element);
            uint64_t tailSize = this->get_zero_tail_size(hashValue);

            if(this->maximumTails[j] < tailSize) {
                this->maximumTails[j] = tailSize;
            }
        }

        this->computed[element] = true;
    }
}

std::vector<uint64_t> DataStream::FlajoletMartin::get_parcial_results(void) {
    std::vector<uint64_t> results;
    for (std::vector<uint64_t>::iterator it = this->maximumTails.begin(); it != this->maximumTails.end(); it++) {
        uint64_t result = std::pow(2, *it);
        results.push_back(result);
    }

    return results;
}

DataStream::FlajoletMartin::HashFunction::HashFunction(uint64_t prime, uint64_t size) {
    std::uniform_int_distribution<uint64_t> dist(0, UINT64_MAX);

    this->prime = prime;
    this->size = size;
    this->angular = dist(e3) % prime;
    this->scalar = dist(e3) % prime;
}

uint64_t DataStream::FlajoletMartin::HashFunction::compute_hash(uint64_t element) {
    return ((this->angular * element + this->scalar) % this->prime) % this->size;
}