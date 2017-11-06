#include <algorithm>
#include <cmath>
#include <random>

#include "AMS.hpp"

DataStream::AMS::AMS(uint64_t variableSize, uint64_t streamSize, bool finiteLength) {
    this->variableSize = variableSize;
    this->streamSize = streamSize;
    this->finiteLength = finiteLength;

    // Reservoir Sampling does not need choosen start times
    if(!finiteLength) {
        return;
    }

    // Get a random number generator
    std::random_device rd;
    mt19937_64 e2(rd());
    e2.seed(200);
    std::uniform_int_distribution<uint64_t> dist(0, streamSize);

    // Generate random start times
    for(uint64_t i = 0; i < variableSize; i++) {
        uint64_t value = dist(e2);
        this->startTimes.push_back(value);
    }

    // Sorted start times
    std::sort(this->startTimes.begin(), this->startTimes.end());
}

void DataStream::AMS::remove_variable(uint64_t index) {
    int currentIndex = 0;

    // Search for element to be throw out    
    std::unordered_map<uint64_t, std::vector<AMS::Variable>>::iterator it;
    for (it = this->variables.begin(); it != this->variables.end(); it++) {
        // Iterate until find position
        if(index > currentIndex + it->second.size()) {
            currentIndex += it->second.size();
            continue;
        }

        // Shift to correct index at the current vector
        index -= currentIndex;

        // Remove variable
        it->second.erase(it->second.begin() + index);

        // Check if vector is empty
        if(it->second.size() == 0) {
            this->variables.erase(it);
        }

        // Finished removing
        break;
    }
}

void DataStream::AMS::insert_variable(uint64_t element, uint64_t startTime) {
    // Instantiate variable
    AMS::Variable variable(element, 0, startTime);

    // Check if element was already seen
    std::unordered_map<uint64_t, std::vector<AMS::Variable>>::iterator found;
    found = this->variables.find(element);
    
    // Update data structure
    if(found == this->variables.end()) {
        std::vector<Variable> elementVector;
        elementVector.push_back(variable);
        this->variables[element] = elementVector;
    }
    else {
        this->variables[element].push_back(variable);
    }
}

void DataStream::AMS::reservoir_sampling(uint64_t element, uint64_t currentTime) {
    // Sampling still not needed
    if(currentTime < this->variableSize) {
        this->insert_variable(element, currentTime);
        return;
    }

    // Probability of element enter variables
    double probability = ((double) this->variableSize / currentTime);

    // Random number between 0 and 1
    double threshold = ((double) rand() / (RAND_MAX));

    // Element will not be add to variables
    if (threshold > probability) {
        return;
    }
    
    // Now we have to choose one element to throw out
    int index = (int) std::floor(this->variableSize * ((double) rand() / (RAND_MAX)));
    
    // Remove choosen element
    this->remove_variable(index);

    // Finally, add new variable
    this->insert_variable(element, currentTime);
}

void DataStream::AMS::finite_length(uint64_t element, uint64_t currentTime) {
    // Check if current is a selected time
    if(currentTime == this->startTimes[0]) {
        this->insert_variable(element, currentTime);
        this->startTimes.erase(startTimes.begin(), startTimes.begin() + 1);
    }
}

void DataStream::AMS::process_data_stream_internal(uint64_t* dataStream, uint64_t size) {
    // Increment counter of all variables
    std::unordered_map<uint64_t, std::vector<AMS::Variable>>::iterator found;
    for(uint64_t i = 0; i < size; i++) {
        // Current time
        uint64_t time = i + this->dataProcessed;

        // Select variables update method
        if(this->finiteLength) {
            this->finite_length(dataStream[i], time);
        }
        else {
            this->reservoir_sampling(dataStream[i], time);
        }

        // Check if element's variable exist
        found = this->variables.find(dataStream[i]);
        if(found == this->variables.end()) {
            continue;
        }
        
        // Try incrementing for each variable of element
        for (std::vector<AMS::Variable>::iterator it = found->second.begin(); it != found->second.end(); it++) {
            it->try_increment(time);
        }            
    }
}

std::vector<uint64_t> DataStream::AMS::get_parcial_results(void) {
    std::vector<uint64_t> results;
    for (std::unordered_map<uint64_t, std::vector<AMS::Variable>>::iterator it = this->variables.begin(); it != this->variables.end(); it++) {
        for (std::vector<AMS::Variable>::iterator it_internal = it->second.begin(); it_internal != it->second.end(); it_internal++) {
             uint64_t result = it_internal->compute_second_moment(this->streamSize);
             results.push_back(result);
        }
    }

    return results;
}

DataStream::AMS::Variable::Variable(uint64_t element, uint64_t value, uint64_t startTime) {
    this->element = element;
    this->value = value;
    this->startTime = startTime;
}

bool DataStream::AMS::Variable::try_increment(uint64_t currentTime) {
    // Only increment start time has began
    if(currentTime >= this->startTime) {
        this->value += 1;
        return true;
    }

    return false;
}

bool  DataStream::AMS::Variable::multiplication_is_safe(uint64_t a, uint64_t b) {
    size_t a_bits=std::log2(a), b_bits=std::log2(b);
    return (a_bits+b_bits<=64);
}

uint64_t DataStream::AMS::Variable::compute_second_moment(uint64_t size) {
    // Check for overflow
    bool safe = this->multiplication_is_safe(size, this->value);    

    return safe ? size * (2ULL * this->value - 1ULL) : std::pow(2, 64);;
}


