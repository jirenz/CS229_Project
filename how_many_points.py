import os
import sys
import pickle

import random

if __name__ == "__main__":
	input_file = sys.argv[1]

	with open(input_file, "rb") as f:
		training_set = pickle.load(f)
	
	X, y = training_set
	n = len(X)
	print("There are", n, "data points.")
