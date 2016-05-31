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

	model.feature_extractor.debug(model.weights)

	if save_file is not None:
		with open(save_file, "wb") as f:
			pickle.dump(model, f)

def supervised_train(model, epochs = 10, save_file = None):
	st = SupervisedLearningAlgorithm(
			model = model,
			agent1 = TradeAgent(),
			agent2 = TradeAgent())

	st.train(epochs)

	model.feature_extractor.debug(model.weights)

	if save_file is not None:
		with open(save_file, "wb") as f:
			pickle.dump(model, f)

if __name__ == "__main__":
	# RelativeResourceExtractor

	# experience_replay_train( \
		# model = StatePairLinearModel(RelativeResourceExtractor()), \
		# epochs = int(sys.argv[1]), \
		# eta = 0.0001, \
		# save_file = "ql_sp_relative")

	# ResourceExtractor

	# experience_replay_train( \
		# model = StateDifferenceLinearModel(ResourceExtractor()),
		# epochs = int(sys.argv[1]), \
		# eta = 0.0005, \
		# save_file = "ql_sd_resource")

	# nice try, but no
	# with open("ql_sd_resource", "rb") as f:
		# model = pickle.load(f)
	# m2 = FinalStateLinearModel(ResourceExtractor(), model.weights)
	# with open("ql_sd_resouce_to_fs", "wb") as f:
		# pickle.dump(m2, f)

	# experience_replay_train( \
		# model = FinalStateLinearModel(ResourceExtractor()), \
		# epochs = int(sys.argv[1]), \
		# eta = 0.0001, \
		# save_file = "ql_fs_resource")

	# supervised_train( \
		# model = FinalStateLinearModel(ResourceExtractor()), \
		# epochs = int(sys.argv[1]), \
		# save_file = "st_fs_resource")


	# PearExtractor

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
