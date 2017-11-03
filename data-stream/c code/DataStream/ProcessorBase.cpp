#include "ProcessorBase.hpp"

void DataStream::ProcessorBase::process_data_stream(uint64_t* dataStream, uint64_t size) {
    this->process_data_stream_internal(dataStream, size);
    this->dataProcessed += size;
}