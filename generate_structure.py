"""
Generate inputs, from lists to trees, of specific forms. 

"""
import random


def gen_list(input_size):
	lst = [i for i in range(input_size)]
	random.shuffle(lst)
	return lst


class Tree:
	def __init__(self):
		self.value = None
		self.left = None
		self.right = None
	
	def push(self, element):
		if self.value is None:
			self.value = element
		else:
			if element < self.value:
				if self.left is None:
					self.left = Tree()
				self.left.push(element)
			elif element > self.value:
				if self.right is None:
					self.right = Tree()
				self.right.push(element)

	def print(self, indent=0):
		if self.value is not None:
			print("\t"*indent + str(self.value))
			if self.left is not None:
				self.left.print(indent=indent+1)
			if self.right is not None:
				self.right.print(indent=indent+1)

def gen_tree(input_size):
	t = Tree()
	
	for i in gen_list(input_size):
		t.push(i)

	return t

