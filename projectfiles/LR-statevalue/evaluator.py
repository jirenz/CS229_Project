def evaluator(w,data):
	value = w[0] # intercept term
	for i in range(0:NumFeat):
		value = value + data[i] * w[i + 1]
	return value
