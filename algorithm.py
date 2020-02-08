from structure import *
import time
import math
import sys
import subprocess
import os

import numpy as np
#from sklearn.linear_model import LinearRegression
from scipy import stats

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
	bar = fill * filledLength + ' ' * (length - filledLength)
	sys.stdout.write('\x1b[1A')

	print('Processing element (' + str(iteration)+"/"+str(total)+")")

	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)

	# Print New Line on Complete
	if iteration == total: 
		print()

# null pipe to ignore output to file.
output_pipe = open(os.devnull, "w+")

if len(sys.argv) > 1:
	file_output = sys.argv[1]
	output_pipe = open(file_output, "w+")

   
   
def calc_lin_regress(n_value, t_value):
	"""
		Calculate the linear regression of 
	"""
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	
	return (slope, std_err)


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
			
def const_op(lst):
	time.sleep(0.0001)

def linear_op(lst):
	for i in range(len(lst)):
		continue

def quadratic_op(lst):
	for i in range(len(lst)):
		linear_op(lst)

def cubic_op(lst):
	for i in range(len(lst)):
		quadratic_op(lst)

if __name__ == "__main__":
	print()  # needed for progres bar to appear correctly.

	n     = np.array([])
	t     = np.array([])
	log_t = np.array([])
	log_n = np.array([])
	try:
		input_range = [100, 100000]
		sample_size = 1000

		test = AlgoTest(quadratic_op, gen_list, sample_size, input_range)
		if output_pipe is not None:
			output_pipe.write("n,t,logn,logt\n")
	
		progress_bar_length = 80
		printProgressBar(0, test.sample_size, prefix = 'Progress:', suffix = 'Complete', length = progress_bar_length)
	
		# store results

		for line in test.test():
			
			ln = 0
			try:
				ln = math.log(line[0])
			except ValueError:
				pass

			lt = 0
			try:
				lt = math.log(line[1])
			except ValueError:
				pass


			output_pipe.write(",".join([str(x) for x in [line[0],line[1], ln, lt]])+"\n")
			
			n     = np.append(n, [[line[0]]])
			t     = np.append(t, [[line[1]]])
			log_n = np.append(log_n, [[ln]])
			log_t = np.append(log_t, [[lt]])

			printProgressBar(test.current, test.sample_size, prefix = 'Progress:', suffix = 'Complete', length = progress_bar_length)
	
	except KeyboardInterrupt:
		output_pipe.flush()
		output_pipe.close()
		
		printProgressBar(test.current, test.sample_size, prefix = 'Progress:', suffix = 'Complete', length = progress_bar_length)
		print(f"\nProcessed input saved to {output_pipe.name}\nProcess terminated via Keyboard Interrupt.")
	finally:	
		slope, intercept, r_value, p_value, std_err = stats.linregress(log_n,log_t)
		
		degree = int(slope+1) # go overboard, and check within

		z = np.polyfit(n, t, degree)
		
		max_data = max(z.data)
		power = 0
		while z.data[power] != max_data:
			power += 1
		max_term = degree - power

		print(z)
		print(max_term)

