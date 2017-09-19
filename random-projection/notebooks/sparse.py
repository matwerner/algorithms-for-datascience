'''
Created on Sep 18, 2017

@author: Matheus Werner

motivation: Basic sparse vector class and operations, as we cannot use external libraries due to Project restrictions
'''

class SparseVector:
	
	def __init__(self, obj, size=None):
		# Set default value. It must be 0, else most calculations will be invalid
		self.__default_value = 0

		# Parse object
		elements, alternative_size = self.__tosparse(obj)
		self.__elements = elements
		self.__len = size if size else alternative_size

	def __add__(self, other):
		if isinstance(other, self.__class__):
			# Check Dimensionality
			if self.__len != other.__len:
				raise ValueError('Dimension mismatch')

			# Select all indexes to be checked
			indexes = set(self.__elements.keys()) | set(other.__elements.keys())

			# Calculate new SparseVector
			result = {index: self.__getitem__(index) + other.__getitem__(index)
				  for index in indexes}
			return SparseVector(result, self.__len)
		if isinstance(other, int) or isinstance(other, float):
			# Calculate new SparseVector
			result = {index:value + other
				  for index, value in self.__elements.items()}
			return SparseVector(result, self.__len)
		raise TypeError("Type %s is not supported. Mathematical operators only support int, float and SparseVector." % (type(other),))		
	__radd__ = __add__

	def __mul__(self, other):
		if isinstance(other, self.__class__):
			# Check Dimensionality
			if self.__len != other.__len:
				raise ValueError('Dimension mismatch')

			# Select smaller vector for computational efficience
			is_smaller = True if len(self.__elements) < len(other.__elements) else False
			array_smaller = self.__elements if is_smaller else other.__elements
			array_bigger = other.__elements if is_smaller else self.__elements

			# Calculate new SparseVector
			result = {index:value * array_bigger[index]
				  for index, value in array_smaller.items()
				  if index in array_bigger}
			return SparseVector(result, self.__len)
		if isinstance(other, int) or isinstance(other, float):
			# Calculate new SparseArray
			result = {index:value * other
				  for index, value in self.__elements.items()}
			return SparseVector(result, self.__len)
		raise TypeError("Type %s is not supported. Mathematical operators only support int, float and SparseVector." % (type(other),))
	__rmul__ = __mul__

	def __sub__(self, other):
		return self.__add__(-1 * other)
	__rsub__ = __sub__

	#def __mod__(self, other):

	#def __truediv__(self, other):

	#def __lt__(self, other):

	#def __le__(self, other):

	#def __eq__(self, other):

	#def __ne__(self, other):

	#def __gt__(self, other):

	#def __ge__(self, other):

	def __setitem__(self, index, value):
		# Check index range
		if index < 0 or index > self.__len - 1:
			raise ValueError("SparseVector Index Out of Range: %d" % (index,))

		# Check if value is default value
		if value == self.__default_value:
			del self.__elements[index]
		else:
			self.__elements[index] = value			

	def __getitem__(self, index):
		if self.__contains__(index):
			return self.__elements[index]
		return self.__default_value

	def __contains__(self, index):
		# Check supported type
		if not isinstance(index, int):
			raise TypeError("Type %s is not supported. Index must be integer." % (type(index),))
		# Check index range
		if index < 0 or index > self.__len - 1:
			raise ValueError("SparseVector Index Out of Range: %d" % (index,))

		return index in self.__elements

	def __len__(self):
		return self.__len

	def __str__(self):
		# Get all elements (including default value) and parse to string
		elements = [str(self.__elements[index])
			    if index in self.__elements
			    else str(self.__default_value)
			    for index in range(self.__len)]
		return '[%s]' % (', '.join(elements), )

	def __tosparse(self, obj):
		# Select parser between supported types
		if isinstance(obj, dict):
			return obj, max(obj.keys())
		if isinstance(obj, list):
			return {index:value
				for index, value in enumerate(obj)
				if value is not self.__default_value}, len(obj)
		raise TypeError("Type %s is not supported. Input must be list or dict." % (type(obj),))

	def sum(self):
		return sum(self.__elements.values())

	def squared_euclidian_distance(self, other):
		# Check supported type
		if not isinstance(other, self.__class__):
			raise TypeError("Type %s is not supported. Input must be another SparseVector." % (type(other),))
		
		# Calculate distance
		result = self - other
		result *= result
		return result.sum()
		
if __name__ == "__main__":
	a = [1, 2, 3, 0, 0, 0, 2]
	b = [5, 3, 0, 1, 2, 3, 2]
	
	a = SparseVector(a)
	b = SparseVector(b)
	result = a - b

	print(a)
	print(b)
	print(result)
	print(a.squared_euclidian_distance(b))


