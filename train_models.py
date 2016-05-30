from learning.model import *
from learning.strategy import StrategyManager
from learning.learning import *

from projectfiles.feature_extract import *
from projectfiles.feature_extract_2 import *

import numpy as np
import pickle
from projectfiles.agent import *

import sys

if __name__ == "__main__":
	# phi = TestResourceExtractor()
	# model = StateDifferenceLinearModel(phi)
	# eta = 0.001

	phi = RelativeResourceExtractor()
	model = StatePairLinearModel(phi)
	eta = 0.0001

	# phi = ResourceExtractor()
	# model = FinalStateLinearModel(phi)
	# eta = 0.001

	full_stage_strategy = StrategyManager()
	training_mdp = HearthstoneMDP(full_stage_strategy)

	# ql = QLearningAlgorithm(mdp = training_mdp,
		# eta = 0.001, 
		# explore_prob = 0.2,
		# function_approximator = model)

	ql = ExperienceReplayQ(mdp = training_mdp,
		eta = eta, 
		explore_prob = 0.2,
		function_approximator = model)

	ql.train(int(sys.argv[1]))

	phi.debug(model.weights)

	with open("ql_phi1_weights", "wb") as f:
		pickle.dump(model, f)

