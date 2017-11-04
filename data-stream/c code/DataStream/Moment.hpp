#ifndef MOMENT_HPP
#define MOMENT_HPP

#include <unordered_map>

#include "ProcessorBase.hpp"

using namespace std;

namespace DataStream {
    
    class Moment : public ProcessorBase {
        
        protected:

            std::vector<uint64_t> get_parcial_results(void) override;
        
            void process_data_stream_internal(uint64_t* dataStream, uint64_t size) override;

        public:

            int nthMoment;

            Moment(int nthMoment);

            std::unordered_map<uint64_t, uint64_t> elements;
    };
}

#endif