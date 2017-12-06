# HOW TO:

## BENCHMARK YOUR CLUSTER MODEL

Start by running the following incantation:

Example 1 
> python benchmark.py -f 'toyU_cluster.txt' -g 'toyV_cluster.txt' -o  'toy_confusion_matrix.txt'

This yields the class example. It should print: 

>1 files found matching r'toyU_cluster.txt' pattern
Fetching 1	toyU_cluster...
Fetching 1	toyU_cluster...done
1 files found matching r'toyV_cluster.txt' pattern
Fetching 1	toyV_cluster...
Fetching 1	toyV_cluster...done
1 of 1 Confusion matrix: toyU_cluster vs toyV_cluster...
1 of 1 Confusion matrix: toyU_cluster vs toyV_cluster...
                               a    b    c     d         A    P    R  F-1  J  
toyU_cluster_x_toyV_cluster  1.0  4.0  4.0  12.0  0.619048  0.2  0.2  0.2   0.111111

### BENCHMARK ARGUMENTS

* -f 'toyU_cluster.txt' this is the file saved on /datasets to be evaluated. It's a required parameter

* -b 'toyV_cluster.txt' this is the file saved on /datasets to used as benchmark. It's optional and reverts to 'goldenset.csv' if not provided

* -o 'toy_confusion_matrix.txt' this is the output file to store results on /datasets. It's optional and reverts to 'confusion_matrix.txt' if not provided

* -f, -o accept a RegExp like string so multiple models might be bechmarked against each other

* '*cluster.txt' files are space separated files containing the index of the observation ( document ) on the first column and a cluster denomination on the second column

### MAKING SENSE OF THE BENCHMARK

There are 9 output items all relating to a confusion matrix over the count of pairs of documents that reside in a cluster set. Or the duplicate items for this project.
[more about benchmark used](https://en.wikipedia.org/wiki/Confusion_matrix).


1. a = TP The number of pair of items where both model and benchmark evaluate to be duplicates.

2. b = FN The number of pair of items where model classified as duplicate but do not belong to benchmark.

3.  c = FP The number of pair of items where model has not classified as duplicate but benchmark has.

4.  d = TN The sum of all singleton observation minus the items seem so far (a+b+c) plus all possible pairings.

5. accuracy=(a+d)/(a + b + c + d).

6. precision=a/(a + c).

7. recall=a/(a + d).

8. f1_measure=2\*(precision\*recall)/(precision + recall).

9. jaccard=a/(a+b+c).

### MORE EXAMPLES, BECAUSE MORE IS THE MERRIER

Example 2: 

This will benchmark any files saved on /datasets that end with _cluster.txt using 'goldenset.csv' as golden standard.

> python benchmark.py -f  '\*\_cluster.txt'


Example 3: 

This will benchmark  'gaussian\_0.5\_cluster\.txt' and 'gaussian\_0.3\_cluster\.txt' as golden standard and save the results on 'gaussian\_confusion\_matrix\.txt'

> python benchmark.py -f 'gaussian\_0.5\_cluster\.txt' -g 'gaussian\_0\.3\_cluster.txt' -o  'gaussian\_confusion\_matrix\.txt'


















