import os
import sys
import pickle
import random
import numpy as np

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "data.hsdat"

    with open(input_file, "rb") as f:
        X, y= pickle.load(f)
        i = 2
        while 1:
            try:
                X_in, y_in = pickle.load(f)
            except EOFError:
                break
            print("Iteration: " + str(i))
            X = np.concatenate((X, X_in))
            y = np.concatenate((y, y_in))
            i += 1
    n = len(X)
    print("There are", n, "data points.")
