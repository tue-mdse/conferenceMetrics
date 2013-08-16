"""Some useful utilities for working with dictionaries
"""
__author__ =  'Bogdan Vasilescu'
__version__=  '1.0'

import pickle
import os, glob, sys
import types
# from collections import defaultdict



def isList(obj):
	"""isList(obj) -> Returns true if obj is a Python list.

	This function does not return true if the object supplied
	is a UserList object.
	"""
	return type(obj)==types.ListType

def isTuple(obj):
	"isTuple(obj) -> Returns true if obj is a Python tuple."
	return type(obj)==types.TupleType

def isPySeq(obj):
	"""isPySeq(obj) -> Returns true if obj is a Python list or a Python tuple.
    
	This function does not return true if the object supplied is
	a UserList object.
	"""
	return isList(obj) or isTuple(obj)

def isLongString(obj):
	"""isLongString(obj) -> Returns true if obj is a string of a size larger than 1.
 
	This function does not return true if the object supplied is
	a UserString object.
	"""
	return type(obj)==types.StringType and len(obj)>1



class MyDict:

	def __init__(self, path=None, encod=None):
		self.data = {}
		if path is not None:
			fdict = open(path, "r")
			if encod is not None:
				dict1 = pickle.load(fdict, encoding=encod)
			else:
				dict1 = pickle.load(fdict)
			print "Loaded dictionary from %s" % path
			fdict.close()
			self.data = dict1
	
	def update(self, dict=None):
		if dict is not None:
			for k, v in dict.items():
				self.data[k] = v
	
	# def clear(self):
		# self.data.clear()
		
	# def copy(self):
		# if self.__class__ is MyDict:
			# return MyDict(self.data)
		# import copy
		# return copy.copy(self)
	
	def keys(self):
		return self.data.keys()

	def items(self):
		return self.data.items()
	
	def values(self):
		return self.data.values()
		
	def append(self, key, value):
		try:
			self.data[key].append(value)
		except:
			self.data[key] = []
			self.data[key].append(value)
			
	def save(self, path):
		fdict = open(path, "w")
		pickle.dump(self.data, fdict)
		print "Wrote dictionary to %s" % path
		fdict.close()
		
	def saveAsCSV(self, path):
		f = open(path, 'w')
		
		for key in self.keys():
			row = []
			rs = ''
			vs = ''
			
			if isTuple(key):
				for item in list(key):
					row.append(item)
			else:
				row.append(key)
			
			values = []
			if isList(self.data[key]):
				for v in self.data[key]:
					values.append(str(v))
			else:
				values.append(str(self.data[key]))
			
			vs = ', '.join(values)
			
			rs = '; '.join(row)
			rs += '; '
			rs += vs
			
			f.write('%s\n' % rs)
				
		f.close()
		print "Wrote dictionary to %s" % path
		
		
	def __getitem__(self, key):
		if key in self.data:
			return self.data[key]
		if hasattr(self.__class__, "__missing__"):
			return self.__class__.__missing__(self, key)
		raise KeyError(key)
		
	def __setitem__(self, key, item):
		self.data[key] = item
		
	def get_key(self, value):
		"""find the key(s) as a list given a value"""
		return [item[0] for item in self.items() if value in item[1]][0]
 
	def get_value(self, key):
		"""find the value given a key"""
		return self[key]	
		
# def main():
	# d1 = MyDict()
	
	# d1.append('list', 230)
	# d1.append('list', 560)
	# d1.append('list', 170)
	
	# print d1.values()
	# print d1.keys()
	
	# # d1.save('C:\\Python27\\Lib\\own\\d1.dict')
	
	# d2 = MyDict('C:\\Python27\\Lib\\own\\d1.dict')
	# print d2.values()
	# d2.update(d1)
	# print d2.values()


# main()