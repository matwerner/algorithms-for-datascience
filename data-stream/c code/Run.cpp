#include <iostream>
#include <cstring>

#include "DataStream/ProcessorBase.hpp"
#include "DataStream/Moment.hpp"
#include "Utils.hpp"

using namespace std;

void experiment(uint64_t batchSize, uint64_t dataStreamSize) {
    // Instantiate all processor to be applied in the stream
    int processorSize = 1;
    DataStream::ProcessorBase** processors = new DataStream::ProcessorBase*[processorSize];
    processors[0] = (DataStream::ProcessorBase*) new DataStream::Moment();

    // Generate data stream in batches
    clock_t begin = clock();
    clock_t end = clock();
    double elapsed_secs = 0;        
    for(uint64_t i = 0; i < batchSize; i++) {
        cout << "Batch: "<< i << endl;

        // Generate batch stream
        begin = clock();
        uint64_t* randomStream = random_data_stream(dataStreamSize);
        end = clock();

        elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
        cout << "Generate data stream: "<< elapsed_secs << endl;

        // Process stream
        for(int j = 0; j < processorSize; j++) {
            begin = clock();
            processors[j]->process_data_stream(randomStream, dataStreamSize);
            end = clock();
    
            elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
            cout << "Process " << j << ": " << elapsed_secs << endl;
        }
        cout << endl;

        // Delete stream
        delete randomStream;
    }

    // Output processor results
    for(int j = 0; j < processorSize; j++) {
        uint64_t result = processors[j]->result();
        cout << "Process " << j << ": " << result << endl;
    }
    cout << endl;

    // Delete variables
    for(int j = 0; j < processorSize; j++) {
        delete processors[j];
    }
    delete processors;
}

int main(int argc, char** argv){
    uint64_t streamSize = -1, batchSize = -1;

	// Read and parse arguments
	for(int i = 1; i < argc; i++){
		if(strcmp(argv[i], "--batch") == 0) {
			batchSize = (uint64_t) atoi(argv[i+1]);
		}
		else if(strcmp(argv[i], "--stream") == 0) {
			streamSize = (uint64_t) atoi(argv[i+1]);
		}
		else{
			cout << "Argument " << argv[i] <<  " not supported." << endl;
			exit(1);
        }        
        i++;
    }

    // Run experiment
    experiment(batchSize, streamSize);

    return 0;
}