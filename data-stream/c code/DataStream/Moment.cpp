#include <cmath>

#include "Moment.hpp"

DataStream::Moment::Moment(int nthMoment) {
    this->nthMoment = nthMoment;
}

std::vector<uint64_t> DataStream::Moment::get_parcial_results(void) {
    uint64_t moment = 0;
    std::vector<uint64_t> results;    
    for (std::unordered_map<uint64_t, uint64_t>::iterator it = elements.begin(); it != elements.end(); it++) {
        moment += std::pow(it->second, this->nthMoment);
    }

    results.push_back(moment);

    return results;
}
    
void DataStream::Moment::process_data_stream_internal(uint64_t* dataStream, uint64_t size) {

    for(uint64_t i = 0; i < size; i++) {
        // Get current element of data stream
        uint64_t element = dataStream[i];

        // Check if element was already seen
        std::unordered_map<uint64_t, uint64_t>::const_iterator found;
        found = elements.find(element);

        // Increment element counter
        elements[element] = found == elements.end()?  1 : elements[element] + 1;
    }
}
