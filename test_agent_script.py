from agent_test import *

sys.setrecursionlimit(300)

if __name__ == "__main__":
	num_games = 100
	max_depth = 2
	oppo = "trade"
	for size in [1000]:#[40000, 16000, 20000, 25000, 30000]:
		for model_name in ["st_fs_deep_neural", "st_fs_resource"]: #"st_fs_resource",   #"ql_fs_resource"  "ql_sp_relative"
			model_name = "models/" + model_name + "_" + str(size) + ".t"
			with open(model_name, "rb") as f:
				model = pickle.load(f)
			our_agent = StrategyAgent(model, model_name, max_depth)
			result = run_agent(our_agent, TradeAgent(), num_games)
			with open("results", "a") as f:
				f.writelines(["{} {} {} {} => {}\n".format(model_name, oppo, num_games, max_depth, result[model_name])])
