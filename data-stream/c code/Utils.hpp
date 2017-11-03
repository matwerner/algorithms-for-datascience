#ifndef UTILS_HPP
#define UTILS_HPP

#include <cstdint>

// Maximum number of the data stream
const double DATA_STREAM_MAX_VALUE = 1e11;

uint64_t* random_data_stream(uint64_t size);

#endif