import datagate
import learner
import evaluator
import sys

NumFeat = 46
NumberOfGames = int(sys.argv[1])
pastdata = datagate.getdata(NumberOfGames)

# this part uses learner.py , which applies linear regression and get a vector of coefficients
print("Begin learning...")
coe = learner.learner(pastdata, NumFeat)
print(coe)

# this part is to test whether learner works reasonably by
# allowing manual input 
while (True):
	inp = input().split(" ")
	for i in range(0, len(inp)): inp[i] = int(inp[i])
	if (inp[0] == -1): break
	if (len(inp) != NumFeat):
		print("Not a legal vector\n")
	else:
		print(evaluator.evaluator(coe, inp, NumFeat))

