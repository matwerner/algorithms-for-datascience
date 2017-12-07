import pandas as pd 
import numpy as np 
import random

file = "datasets\word1_cluster.txt"
df_cluster= pd.read_csv(file, sep= ' ', header=None)
df_cluster = df_cluster.sort_values(by=0)
arr=np.arange(9998)
random.shuffle(arr)
df_cluster[0] = arr
df_cluster = df_cluster.sort_values(by=0)
file_path="datasets/randomword1_cluster.txt"
df_cluster.to_csv(file_path, sep=' ',index=False, index_label=False,header=None)