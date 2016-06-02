from train_models import *
import sys
sys.setrecursionlimit(300)

if __name__ == "__main__":
	print("Hi")
	for size in [500]: #, 1000, 2000, 4000, 8000, 12000, 16000, 20000, 25000, 30000, 40000]:
		experience_replay_train( \
			model = StatePairLinearModel(RelativeResourceExtractor()), \
			epochs = int(size/20), \
			eta = 0.0001, \
			save_file = "models/ql_sp_relative_" + str(size) + ".t")
		experience_replay_train( \
			model = FinalStateLinearModel(ResourceExtractor()), \
			epochs = int(size/20), \
			eta = 0.0001, \
			save_file = "models/ql_fs_resource" + str(size) + ".t")
		#supervised_train( \
		#	model = FinalStateLinearModel(ResourceExtractor()), \
		#	data_file = "samples/" + str(size) + ".hssample",\
		#	save_file = "models/st_fs_resource" + str(size) + ".t")
		#supervised_train( \
		#	model = FinalStateNeuralModel(ResourceExtractor()), \
		#	data_file = "samples/" + str(size) + ".hssample", \
		#	save_file = "models/st_fs_neural" +str(size) + ".t")
		#supervised_train( \
		#	model = DeepNeuralModel(ResourceExtractor()), \
		#	data_file = "samples/" + str(size) + ".hssample", \
		#	save_file = "models/st_fs_deep_neural" + str(size) + ".t")

