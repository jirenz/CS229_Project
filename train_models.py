from learning.model import *
from learning.strategy import StrategyManager
from learning.learning import *

from projectfiles.feature_extract import *
from projectfiles.feature_extract_2 import *

import numpy as np
from projectfiles.agent import *

if __name__ == "__main__":
	model = StatePairLinearModel(feature_extractor_2_initial(), feature_extractor_2_temporary)
	# model = FinalStateLinearModel(feature_extractor_initial(), feature_extractor)

	full_stage_strategy = StrategyManager()
	training_mdp = HearthstoneMDP(full_stage_strategy)

	ql = QLearningAlgorithm(mdp = training_mdp,
		eta = 0.001, 
		explore_prob = 0.2,
		function_approximator = model)

	ql = ExperienceReplayQ(mdp = training_mdp,
		eta = 0.001, 
		explore_prob = 0.2,
		function_approximator = model)

	ql.train(10)

	with open("ql_phi2_weights", "wb") as f:
		np.save(f, model.weights)

