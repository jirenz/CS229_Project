from learning.model import *
from learning.strategy import StrategyManager
from learning.learning import *

from projectfiles.feature_extract import *
from projectfiles.feature_extract_2 import *

import numpy as np
from projectfiles.agent import *

if __name__ == "__main__":
	model = FinalStateLinearModel(feature_extractor_2_initial(), feature_extractor_2_temporary)

	full_stage_strategy = StrategyManager(model)
	training_mdp = HearthstoneMDP(full_stage_strategy)

	ql = QLearningAlgorithm(mdp = training_mdp,
		eta = 0.01, 
		explore_prob = 0.1,
		function_approximator = model)

	ql.train(1)
