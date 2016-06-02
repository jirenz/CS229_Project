import os
import sys
import pickle
import numpy as np
import random

if __name__ == "__main__":
    input_file = sys.argv[1]
    if input_file == "-d":
        input_file = "data.hsdat"
    num_to_sample = int(sys.argv[2])
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
    else:
        output_file = "samples/" + str(num_to_sample) + ".hssample"

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
    indices = random.sample(range(n), num_to_sample)
    Xs = X[indices]
    ys = y[indices]
    new_set = (Xs, ys)

    with open(output_file, "wb+") as f:
        pickle.dump(new_set, f)
