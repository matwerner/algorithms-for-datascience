#include <cstring>
#include <iostream>

#include "DataStream/ProcessorBase.hpp"
#include "DataStream/Moment.hpp"
#include "DataStream/FlajoletMartin.hpp"
#include "DataStream/AMS.hpp"
#include "Utils.hpp"

using namespace std;

void experiment(DataStream::ProcessorBase* processor, uint64_t batchSize, uint64_t dataStreamSize, char* outputPath) {
    // Generate data stream in batches
    clock_t begin = clock();
    clock_t end = clock();
    double elapsed_secs = 0;        
    for(uint64_t i = 0; i < batchSize; i++) {
        cout << "Batch: "<< i << endl;

        // Generate batch stream
        begin = clock();
        uint64_t* randomStream = Utils::random_data_stream(dataStreamSize);
        end = clock();

        elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
        cout << "Generate data stream: "<< elapsed_secs << endl;

        // Process stream
        begin = clock();
        processor->process_data_stream(randomStream, dataStreamSize);
        end = clock();

        elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
        cout << "Process: " << elapsed_secs << endl << endl;

        // Delete stream
        delete randomStream;
    }

    // Dump processor result
    processor->dump(outputPath);

    // Output processor result
    uint64_t result = processor->get_result();
    cout << "Process result: " << result << endl;
}

int main(int argc, char** argv){
    uint64_t dataStreamSize = 0, batchSize = 0, nth = 0, variableSize = 0, hashSize = 0;
    char *command, *outputPath;

    // Read and parse arguments
    command = argv[1];
	for(int i = 2; i < argc; i++){
		if(strcmp(argv[i], "--batch") == 0) {
			batchSize = (uint64_t) atoi(argv[i+1]);
		}
		else if(strcmp(argv[i], "--stream") == 0) {
			dataStreamSize = (uint64_t) atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "--nth") == 0) {
			nth = (uint64_t) atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "--variable") == 0) {
			variableSize = (uint64_t) atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "--hash") == 0) {
			hashSize = (uint64_t) atoi(argv[i+1]);
        }
        else if(strcmp(argv[i], "--output") == 0) {
			outputPath = argv[i+1];
        }        
		else{
			cout << "Argument " << argv[i] <<  " not supported." << endl;
			exit(1);
        }
        i++;
    }

    // Select processor be run
    DataStream::ProcessorBase* processor = NULL;
    if(strcmp(command, "Moment") == 0) {
        processor = (DataStream::ProcessorBase*) new DataStream::Moment(nth);
    }
    else if(strcmp(command, "FlajoletMartin") == 0) {
        processor = (DataStream::ProcessorBase*) new DataStream::FlajoletMartin(hashSize, batchSize * dataStreamSize);
    }
    else if(strcmp(command, "AMS") == 0) {
        processor = (DataStream::ProcessorBase*) new DataStream::AMS(variableSize, batchSize * dataStreamSize);
    }
    else{
        cout << "Command " << command <<  " not supported." << endl;
        exit(1);
    }

    // Run experiment
    experiment(processor, batchSize, dataStreamSize, outputPath);

    // Delete processor
    delete processor;

    return 0;
}