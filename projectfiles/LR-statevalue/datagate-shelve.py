# this code reads game-state data from shelve 'gamefiles.dat' and return a vector of useful information
import shelve
def getdata():
	data = []
	s = shelve.open("gamefiles.dat")
	for i in s:
		print(s[i])
	collect = s["gamelogger"]
	print(collect)
	for i in collect:
		tmp = []
		print(i)
		data.append(tmp)		
	return data
	
getdata()
