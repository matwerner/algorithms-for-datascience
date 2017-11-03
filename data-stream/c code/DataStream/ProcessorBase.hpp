#ifndef PROCESSORBASE_HPP
#define PROCESSORBASE_HPP

#include <cstdint>

namespace DataStream {

    class ProcessorBase {
        
        public:    
            void process_data_stream(uint64_t* dataStream, uint64_t size);
        
            virtual uint64_t result(void) = 0;
        
        protected:
            uint64_t dataProcessed = 0;
        
            virtual void process_data_stream_internal(uint64_t* dataStream, uint64_t size) = 0;
    };
}

#endif