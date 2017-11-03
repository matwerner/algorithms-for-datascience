#ifndef MOMENT_HPP
#define MOMENT_HPP

#include <unordered_map>

#include "ProcessorBase.hpp"

using namespace std;

namespace DataStream {
    
    class Moment : public ProcessorBase {
        
        public:
        
            std::unordered_map<uint64_t, uint64_t> elements;
        
            uint64_t result(void) override;
        
        protected:
        
            void process_data_stream_internal(uint64_t* dataStream, uint64_t size) override;
    };
}

#endif