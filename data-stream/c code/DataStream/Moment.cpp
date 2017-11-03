#include "Moment.hpp"

uint64_t DataStream::Moment::result(void) {
    uint64_t zeroth_moment = 0;
    for (std::unordered_map<uint64_t, uint64_t>::iterator it = elements.begin(); it != elements.end(); it++) {
        zeroth_moment += 1;
        ///second_moment += (it->second * it->second);
    }

    return zeroth_moment;
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
