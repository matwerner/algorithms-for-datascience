'''
	Step 0: X distribution ~ min(floor(1/z**2), 1e11)	

'''
import numpy as np 
import matplotlib.pyplot as plt 

# points= int(1e6)
# z = np.random.uniform(size=(points,1))
# x = np.fmin((1/z**2), 1e11).astype(np.int64)

# plt.hist(x)
# plt.show()


z= np.linspace(1e-4, 1-1e-4, num=1e5)
x= np.fmin((1/z**2), 1e11).astype(np.int64)

plt.plot(z,x)
plt.show()


