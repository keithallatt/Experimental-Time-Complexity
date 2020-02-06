from structure import *
import time
import math
import sys
import subprocess
import os


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration	- Required	: current iteration (Int)
		total		- Required	: total iterations (Int)
		prefix		- Optional	: prefix string (Str)
		suffix		- Optional	: suffix string (Str)
		decimals	- Optional	: positive number of decimals in percent complete (Int)
		length		- Optional	: character length of bar (Int)
		fill		- Optional	: bar fill character (Str)
		printEnd	- Optional	: end character (e.g. "\r", "\r\n") (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
	# Print New Line on Complete
	if iteration == total: 
		print()

# null pipe to ignore output to file.
output_pipe = open(os.devnull, "w+")

if len(sys.argv) > 1:
	file_output = sys.argv[1]
	output_pipe = open(file_output, "w+")

class AlgoTest:
	def __init__(self, func, input_gen, sample_size, input_range):
		self.func = func
		self.input_gen = input_gen
		self.sample_size = sample_size
		# input_range = (a, b), min=a, max=b
		self.input_range = input_range
		self.current = 0

	def percent_done(self):
		return self.current / self.sample_size

	def test(self):
		for i in range(sample_size):
			input_size = self.input_range[0] + i * ((self.input_range[1] - self.input_range[0]) / self.sample_size)
			input_size = int(input_size)

			input_sample = self.input_gen(input_size)

			t1 = time.time()
			self.func(input_sample)
			t2 = time.time()
			
			self.current += 1
			yield (input_size, t2 - t1)
			

def linear_op(lst):
	for i in range(len(lst)):
		lst[i] += 1


def quadratic_op(lst):
	for i in range(len(lst)):
		linear_op(lst)

def cubic_op(lst):
	for i in range(len(lst)):
		quadratic_op(lst)

if __name__ == "__main__":
	try:
		input_range = [100, 100000]
		sample_size = 500

		test = AlgoTest(linear_op, gen_list, sample_size, input_range)
		if output_pipe is not None:
			output_pipe.write("n,t,logn,logt\n")
	
		progress_bar_length = 50
		printProgressBar(0, test.sample_size, prefix = 'Progress:', suffix = 'Complete', length = progress_bar_length)
	
		for line in test.test():
			output_pipe.write(",".join([str(x) for x in [line[0],line[1], math.log(line[0]), math.log(line[1])]])+"\n")

			printProgressBar(test.current, test.sample_size, prefix = 'Progress:', suffix = 'Complete', length = progress_bar_length)
	
	except KeyboardInterrupt:
		output_pipe.flush()
		output_pipe.close()
		
		printProgressBar(test.current, test.sample_size, prefix = 'Progress:', suffix = 'Complete', length = progress_bar_length)
		print(f"\nProcessed input saved to {output_pipe.name}\nProcess terminated via Keyboard Interrupt.")

