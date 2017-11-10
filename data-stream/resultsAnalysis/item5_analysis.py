'''
	Step 5: Analysis deciles of means and medians
'''
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 

if __name__ == '__main__':
	files= ['AMS_without_overflow.txt','AMSInfinite_without_overflow.txt']		
	# import code; code.interact(local=dict(globals(), **locals()))
	for f in files:
		df = pd.read_csv(f, dtype=np.int64) 
		s  = df.as_matrix()
		l  = len(s)

		filename= f.split('.')[0]
		print(filename)
		print(df.quantile([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]))
