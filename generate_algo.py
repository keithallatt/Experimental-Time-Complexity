from generate_structure import *
import time


class AlgoTest:
	def __init__(self, func, input_gen, sample_size, input_range):
		self.func = func
		self.input_gen = input_gen
		self.sample_size = sample_size
		# input_range = (a, b), min=a, max=b
		self.input_range = input_range


	def test(self):
		results = []
		for i in range(sample_size):
			input_size = self.input_range[0] + i * ((self.input_range[1] - self.input_range[0]) / self.sample_size)
			input_size = int(input_size)
			
			input_sample = self.input_gen(input_size)
			
			t1 = time.time()
			self.func(input_sample)
			t2 = time.time()

			results.append( (input_size, t2 - t1) )
		return results

def linear_op(lst):
	for i in range(len(lst)):
		# do something
		lst[i] += 1

input_range = [1000, 10000000]

sample_size = 300

test = AlgoTest(linear_op, gen_list, sample_size, input_range)

for t in test.test():
	print(t[0], ",", t[1], sep="")



