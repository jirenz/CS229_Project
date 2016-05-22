from sklearn import linear_model
# each player information: [attack,health,can_attack?]
# state information f=[(minion1),...,(minion7),hero_health,hero_armor,state_value]

def learner(array_f, NumFeat):
	# this function receives a vector of state information (NumFeat-dimension, not including state_value)
	# this function returns a vector of coefficient terms (NumFeat+1 terms; first term is intercept)
	clf = linear_model.LinearRegression()
	X = []
	y = []
	for i in array_f:
		y.append(i[NumFeat])
		X.append([1, i[0:NumFeat]])
	clf.fit(X, y)
	return clf.coef_


