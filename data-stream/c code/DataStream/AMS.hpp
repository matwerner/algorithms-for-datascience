#ifndef AMS_HPP
#define AMS_HPP

#include <unordered_map>

#include "ProcessorBase.hpp"

using namespace std;

namespace DataStream {

    class AMS : public ProcessorBase {

        private:

            void remove_variable(uint64_t index);

            void insert_variable(uint64_t element, uint64_t startTime);

            void reservoir_sampling(uint64_t element, uint64_t currentTime);

            void finite_length(uint64_t element, uint64_t currentTime);

            class Variable {

                public:

                    Variable(uint64_t element, uint64_t value, uint64_t startTime);

                    bool try_increment(uint64_t currentTime);

                    bool multiplication_is_safe(uint64_t a, uint64_t b);

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
            bool finiteLength;

            AMS(uint64_t variableSize, uint64_t streamSize, bool finiteLength);
    };
}

#endif