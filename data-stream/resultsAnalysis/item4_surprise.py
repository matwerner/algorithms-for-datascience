'''
	Step 4: Generate a stream of size N estimate the surprise number AMS. What's the impact on the number of variables
'''
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 

if __name__ == '__main__':

	files= ['AMS_00128.txt', 'AMS_00512.txt', 'AMS_01024.txt', 'AMS_02048.txt', 'AMS_04056.txt', 'AMS_08112.txt', 'AMS_16384.txt' ,'AMS_32448.txt'] 
	powers= np.array([8,9,10,11,12,13,14,15])
	surprise=[] 
	for f in files: 
		# import code; code.interact(local=dict(globals(), **locals()))
		df = pd.read_csv(f, dtype=np.int64) 
		s  = np.mean(df.as_matrix())
		surprise.append(s)

	S = np.array(surprise) 
	plt.plot(powers, surprise)
	plt.title('Suprise number by number of variables')
	plt.ylabel('surprise number')
	plt.xlabel('powers of 2')
	plt.show() 




