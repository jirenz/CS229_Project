import os
import sys
import pickle

import random

if __name__ == "__main__":
	input_file = sys.argv[1]
	num_to_sample = int(sys.argv[2])
	output_file = sys.argv[3]

	with open(input_file, "rb") as f:
		training_set = pickle.load(f)
	
	X, y = training_set
	n = len(X)
	indices = random.sample(range(n), num_to_sample)
	Xs = X[indices]
	ys = y[indices]
	new_set = (Xs, ys)

	with open(output_file, "wb") as f:
		pickle.dump(new_set, f)
