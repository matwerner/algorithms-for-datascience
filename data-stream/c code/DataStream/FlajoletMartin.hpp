#ifndef FLAJOLETMARTIN_HPP
#define FLAJOLETMARTIN_HPP

#include <unordered_map>
#include <vector>

#include "ProcessorBase.hpp"

namespace DataStream {

    class FlajoletMartin : public ProcessorBase {
        
        private:

            uint64_t get_zero_tail_size(uint64_t value);

            class HashFunction {

                public:

                    HashFunction(uint64_t prime, uint64_t size);

                    uint64_t compute_hash(uint64_t element);

                private:

                    uint64_t prime;
                    uint64_t size;
                    uint64_t angular;
                    uint64_t scalar;                    
            };

        protected:
            
            std::vector<uint64_t> get_parcial_results(void) override;

            void process_data_stream_internal(uint64_t* dataStream, uint64_t size) override;

        public:

            /***
            *   Prime number for hash function must be less than 2^27 - 1. Due to:
            *   -> Maximum size of distinct elements is 10^10 ~ 2^33 (Known)
            *   -> Maximum element to be computed is 10^11 ~ 2^37 (Known)
            *   -> angular * element must be less than 2^64 (Overflow)
            *   Randonly, the prime number choosen was ...
            ***/
            const uint64_t PRIME = 2147483647ULL; // 2^31 -1
            //const uint64_t PRIME = 524287ULL; // 2^19 -1

            std::unordered_map<uint64_t, bool> computed;
            std::vector<HashFunction> hashes;
            std::vector<uint64_t> maximumTails;
            uint64_t hashSize;
            uint64_t streamSize;

            FlajoletMartin(uint64_t hashSize, uint64_t streamSize);
    };    
}

#endif