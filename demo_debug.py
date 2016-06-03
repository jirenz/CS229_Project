import os

def demo_log(message):
	with open("ai_thoughts", "a") as f:
		f.writelines([message + "\n"])
