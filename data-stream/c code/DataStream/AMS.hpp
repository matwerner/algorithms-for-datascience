#ifndef AMS_HPP
#define AMS_HPP

#include <unordered_map>

#include "ProcessorBase.hpp"

using namespace std;

namespace DataStream {

    class AMS : public ProcessorBase {

        private:

            void update_variables(uint64_t* dataStream, uint64_t size);

            class Variable {

                public:

                    Variable(uint64_t element, uint64_t value, uint64_t startTime);

                    bool try_increment(uint64_t currentTime);

                    uint64_t compute_second_moment(uint64_t size);

                private:

                    uint64_t element;
                    uint64_t value;
                    uint64_t startTime;
            };

        protected:
            
            std::vector<uint64_t> get_parcial_results(void) override;

            void process_data_stream_internal(uint64_t* dataStream, uint64_t size) override;

        public:
        
            std::unordered_map<uint64_t, std::vector<AMS::Variable>> variables;
            std::vector<uint64_t> startTimes;
            uint64_t streamSize;
            uint64_t variableSize;

            AMS(uint64_t variableSize, uint64_t streamSize);
    };
}

#endif