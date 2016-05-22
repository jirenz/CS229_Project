# this code reads data from a json file and output them in a pure-list form for learner.py to deal with
import json
from pprint import pprint

# in this code, NumFeat = 23
def getdata(NumberOfGames):
	data = []
	for i in range(1,NumberOfGames+1):
		singlegame = []
		filename = "logfiles/test_one_"+str(i)+".hslog"
		with open(filename) as data_file:    
			for f in data_file:
				while True:
					try:
						tmp = json.loads(f)
						break
					except ValueError:
						f += next(data_file)
				singlegame.append(tmp)	
		winner = singlegame[-1]["active_player"]
		size = len(singlegame)
		for i in range(0,size):
			useful = []
			nowstate = singlegame[i]
			nowactive = nowstate["active_player"]
			if nowactive == winner : 
				flag = 1
			else:
				flag = -1
			# estimate how well this state is
			value = flag * (0.7 ** int((size - i - 1) / 2))
			tmp = nowstate["players"][nowactive - 1]
			count = 0
			for j in tmp["minions"]:
				useful += [j["attack"], j["max_health"], 1]
				count += 1
			for j in range(0,7 - count):
				useful += [0, 0, 0]
			useful += [tmp["hero"]["armor"], tmp["hero"]["health"], value]
			data.append(useful)			
	return data


