# Declare stream parameters
BATCH_SIZE=100
STREAM_SIZE=100000000
# Run experiments
time ./Run Moment --batch $BATCH_SIZE --stream $STREAM_SIZE --output "Results/ZerothMoment.txt" --nth 0
time ./Run Moment --batch $BATCH_SIZE --stream $STREAM_SIZE --output "Results/SecondMoment.txt" --nth 2
time ./Run FlajoletMartin --batch $BATCH_SIZE --stream $STREAM_SIZE --output "Results/FlajoletMartin.txt" --hash 2048
time ./Run AMS --batch $BATCH_SIZE --stream $STREAM_SIZE --output "Results/AMS.txt" --variable 256