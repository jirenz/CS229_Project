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
        while 1:
            try:
                X_in, y_in = pickle.load(f)
            except EOFError:
                break
            X = np.concatenate((X, X_in))
            y = np.concatenate((y, y_in))

    n = len(X)
    print("There are", n, "data points.")
