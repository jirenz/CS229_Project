from learning.model import *
from learning.strategy import StrategyManager
from learning.learning import *

from projectfiles.feature_extract import *

import numpy as np
import pickle
from projectfiles.agent import *

import sys

def experience_replay_train(model, epochs = 10, eta = 0.001, save_file = None):
	full_stage_strategy = StrategyManager()
	training_mdp = HearthstoneMDP(full_stage_strategy)

	ql = ExperienceReplayQ(mdp = training_mdp,
			eta = eta, 
			explore_prob = 0.2,
			function_approximator = model,
			experience_size = 100,
			replays_per_epoch = 50)

	ql.train(epochs)

	try:
		model.feature_extractor.debug(model.weights)
	except:
		pass

	if save_file is not None:
		with open("models." + save_file, "wb+") as f:
			pickle.dump(model, f)

def supervised_train(model, data_file = None, save_file = None):
	with open("samples/" + data_file, "rb") as f:
		training_set = pickle.load(f)

	model.train(training_set)

	try:
		model.feature_extractor.debug(model.weights)
	except:
		pass

	if save_file is not None:
		with open("models/" + save_file, "wb+") as f:
			pickle.dump(model, f)

if __name__ == "__main__":
	model_name = sys.argv[1]

	if model_name.find("ql_sp_relative") != -1:
		experience_replay_train( \
			model = StatePairLinearModel(RelativeResourceExtractor()), \
			epochs = int(sys.argv[2]), \
			eta = 0.0001, \
			save_file = model_name)
	elif model_name.find("ql_fs_resource") != -1:
		experience_replay_train( \
			model = FinalStateLinearModel(ResourceExtractor()), \
			epochs = int(sys.argv[2]), \
			eta = 0.0001, \
			save_file = model_name)
	elif model_name.find("st_fs_resource") != -1:
		supervised_train( \
			model = FinalStateLinearModel(ResourceExtractor()), \
			data_file = sys.argv[2], \
			save_file = model_name)
	elif model_name.find("st_fs_neural") != -1:
		supervised_train( \
			model = FinalStateNeuralModel(ResourceExtractor()), \
			data_file = sys.argv[2], \
			save_file = model_name)
	elif model_name.find("st_fs_deep_neural") != -1:
		supervised_train( \
			model = DeepNeuralModel(ResourceExtractor()), \
			data_file = sys.argv[2], \
			save_file = model_name)
	
	# experience_replay_train( \
		# model = StateDifferenceLinearModel(PearExtractor()), \
		# epochs = int(sys.argv[1]), \
		# eta = 0.001, \
		# save_file = "ql_sd_pear")

	# experience_replay_train( \
		# model = FinalStateLinearModel(PearExtractor()), \
		# epochs = int(sys.argv[1]), \
		# eta = 0.001, \
		# save_file = "ql_fs_pear")

	# supervised_train( \
		# model = FinalStateLinearModel(PearExtractor()), \
		# epochs = int(sys.argv[1]), \
		# save_file = "st_fs_pear")

	# supervised_train(
		# model = FinalStateLinearModel(ResourceExtractor()), \
		# data_file = "supervised_data", \
		# save_file = "st_test")

