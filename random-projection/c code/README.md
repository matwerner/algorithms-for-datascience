# Random Projection
After compiling the code, the following commands are available:
* Experiment
* Distance

## Experiment

From the original bag of words and distance matrix between all pairs of vector,
apply random projection algorithm to reduce to a given number of dimensionalities
and them calculates the maximum distortion between the original and approximated
distance matrices.

./run experiment --bow \<bow-path> --distance \<distance-matrix-path>\
	--time \<number-of-experiments> --method \<gaussian|achlioptas>
	--dimension \<new-number-of-dimensions>

## Distance

From the original bag of words, calculates the distance between all pairs of vectors.

./run distance --bow \<bow-path> --distance \<distance-matrix-path>
