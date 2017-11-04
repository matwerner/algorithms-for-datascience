#ifndef PROCESSORBASE_HPP
#define PROCESSORBASE_HPP

#include <cstdint>
#include <cstring>
#include <vector>

namespace DataStream {

    class ProcessorBase {
        
        protected:
            uint64_t dataProcessed = 0;

            uint64_t combine_parcial_results(std::vector<uint64_t> results);

            virtual std::vector<uint64_t> get_parcial_results(void) = 0;

            virtual void process_data_stream_internal(uint64_t* dataStream, uint64_t size) = 0;

        public:    
            
            void dump(char* outputPath);
            
            uint64_t get_result(void);

            void process_data_stream(uint64_t* dataStream, uint64_t size);
    };
}

#endif