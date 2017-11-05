#include <algorithm>
#include <cmath>
#include <fstream>

#include "ProcessorBase.hpp"

void DataStream::ProcessorBase::dump(char* outputPath) {
    // Get parcial results
    std::vector<uint64_t> results = this->get_parcial_results();

    // Open output stream
    std::ofstream outputFile(outputPath);

    // Dump all to file
    outputFile << results.size() << "\n";
    for (std::vector<uint64_t>::iterator it = results.begin(); it != results.end(); it++) {
        outputFile << *it << "\n";
    }
}

uint64_t DataStream::ProcessorBase::get_result(void) {
    // Get parcial results
    std::vector<uint64_t> results = this->get_parcial_results();

    // Combine them to get a better approximation
    uint64_t result = this->combine_parcial_results(results);
    return result;
}

void DataStream::ProcessorBase::process_data_stream(uint64_t* dataStream, uint64_t size) {
    this->process_data_stream_internal(dataStream, size);
    this->dataProcessed += size;
}

uint64_t DataStream::ProcessorBase::combine_parcial_results(std::vector<uint64_t> results) {
    // Nothing to be done
    if(results.size() == 1) {
        return results[0];
    }

    // Compute number of groups needed
    int factor = 2 * 3, i = 1;
    int groupSize = factor * (int) std::log2(results.size());
    int resultsPerGroupSize = (int) results.size() / groupSize;

    // Keep all averages, so we can compute median
    std::vector<uint64_t> averagePerGroup;

    // Get average per group
    uint64_t average = 0;
    for (std::vector<uint64_t>::iterator it = results.begin(); it != results.end(); it++) {
        average += *it;

        if(i % resultsPerGroupSize == 0) {
            // Get average for current group
            average /= resultsPerGroupSize;
            averagePerGroup.push_back(average);

            // Go to next group
            average = 0;
        }

        i++;
    }

    // Check if results per group * groups == results size
    if(i % resultsPerGroupSize != 1) {
        resultsPerGroupSize = results.size() % resultsPerGroupSize;
        averagePerGroup.push_back(average/resultsPerGroupSize);
    }

    // Get median of all groups
    std::sort(averagePerGroup.begin(), averagePerGroup.end());
    if(groupSize % 2 == 1) {
        return averagePerGroup[groupSize/2];
    }
    else {
        return (averagePerGroup[groupSize/2] + averagePerGroup[groupSize/2 + 1])/2ULL;
    }
}