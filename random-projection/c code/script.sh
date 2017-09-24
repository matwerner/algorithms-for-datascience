./run distance --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt"

./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "gaussian" --dimension 4
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "gaussian" --dimension 16
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "gaussian" --dimension 64
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "gaussian" --dimension 256
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "gaussian" --dimension 1024
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "gaussian" --dimension 4096
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "gaussian" --dimension 16384

./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "achlioptas" --dimension 4
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "achlioptas" --dimension 16
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "achlioptas" --dimension 64
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "achlioptas" --dimension 256
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "achlioptas" --dimension 1024
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "achlioptas" --dimension 4096
./run experiment --bow "g1_corpus.txt" --distance "g1_distance_matrix.txt" --time 30 --method "achlioptas" --dimension 16384


