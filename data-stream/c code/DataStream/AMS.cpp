#include <algorithm>
#include <random>

#include "AMS.hpp"

DataStream::AMS::AMS(uint64_t variableSize, uint64_t streamSize) {
    this->variableSize = variableSize;
    this->streamSize = streamSize;

    // Get a random number generator
    std::random_device rd;
    mt19937_64 e2(rd());
    e2.seed(100);
    std::uniform_int_distribution<uint64_t> dist(0, streamSize);

    // Generate random start times
    for(uint64_t i = 0; i != variableSize; i++) {
        uint64_t value = dist(e2);
        this->startTimes.push_back(value);
    }

    // Sorted start times
    std::sort(this->startTimes.begin(), this->startTimes.end());
}

void DataStream::AMS::update_variables(uint64_t* dataStream, uint64_t size) {
    // Calculate maximum 'time' to be reached during this batch
    uint64_t totalDataProcessed = this->dataProcessed + size;

    // Selected all start times starting during this batch
    std::vector<uint64_t> selectedTimes;
    for(uint64_t i = 0; i < this->startTimes.size(); i++) {
        // Stop when start times are greater than than total data processed
        if(this->startTimes[i] >= totalDataProcessed) {
            break;
        }

        // Append start time
        selectedTimes.push_back(this->startTimes[i]);
    }

    // Get elements of respective selected times
    std::vector<uint64_t> elements;
    for(uint64_t i = 0; i < selectedTimes.size(); i++) {
        uint64_t time = selectedTimes[i] - this->dataProcessed;
        elements.push_back(dataStream[time]);
    }

    // Add new variables to data structure
    for(uint64_t i = 0; i < selectedTimes.size(); i++) {
        // Instantiate variable
        AMS::Variable variable(elements[i], 1, selectedTimes[i]);

        // Check if element was already seen
        std::unordered_map<uint64_t, std::vector<AMS::Variable>>::iterator found;
        found = this->variables.find(elements[i]);
        
        // Update data structure
        if(found == this->variables.end()) {
            std::vector<Variable> elementVector;
            elementVector.push_back(variable);
            this->variables[elements[i]] = elementVector;
        }
        else {
            this->variables[elements[i]].push_back(variable);
        }
    }

    // Remove all start times already reached
    this->startTimes.erase(startTimes.begin(), startTimes.begin() + selectedTimes.size());
}

void DataStream::AMS::process_data_stream_internal(uint64_t* dataStream, uint64_t size) {
    // Add new variables starting in this batch
    this->update_variables(dataStream, size);

    // Increment counter of all variables
    std::unordered_map<uint64_t, std::vector<AMS::Variable>>::iterator found;
    for(uint64_t i = 1; i < size; i++) {
        // Check if element's variable exist
        found = this->variables.find(dataStream[i]);
        if(found == this->variables.end()) {
            continue;
        }
        
        // Try incrementing for each variable of element
        uint64_t time = i + this->dataProcessed;
        for (std::vector<AMS::Variable>::iterator it = found->second.begin(); it != found->second.end(); it++) {
            it->try_increment(time);
        }            
    }
}

std::vector<uint64_t> DataStream::AMS::get_parcial_results(void) {
    std::vector<uint64_t> results;  
    for (std::unordered_map<uint64_t, std::vector<AMS::Variable>>::iterator it = this->variables.begin(); it != this->variables.end(); it++) {
        for (std::vector<AMS::Variable>::iterator it_internal = it->second.begin(); it_internal != it->second.end(); it_internal++) {
             uint64_t sample = it_internal->compute_second_moment(this->streamSize);
             results.push_back(sample);
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

uint64_t DataStream::AMS::Variable::compute_second_moment(uint64_t size) {
    return size * (2 * this->value - 1);
}


