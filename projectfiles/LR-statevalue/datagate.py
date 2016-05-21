# this code reads data from a json file and output them in a pure-list form for learner.py to deal with
import json
from pprint import pprint

data = []
with open('log.txt') as data_file:    
	for i in data_file:
		while True:
			try:
				tmp = json.loads(i)
				break
			except ValueError:
				i += next(data_file)
		data.append(tmp)


