from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.agents import *

from projectfiles.random_deck_generator import RandomDeckGenerator
from projectfiles.agent import *
import sys
# import shelve

from projectfiles.deck_loader import DeckLoader
from projectfiles.hearthlogger import Hearthlogger
from projectfiles.agent import *
from projectfiles.feature_extract import *
from projectfiles.strategy_agent import *
from learning.function_approximator import *
# from learning.model import *

import numpy as np
# import pickle
# from projectfiles.util import spark_weights

def test_agent_once(one, other):
    generator = RandomDeckGenerator()
    deck1 = generator.generate()
    deck2 = deck1.copy()

    if other is None:
        other = TradeAgent()
        #other = RandomAgent()
    game = Game([deck1, deck2], [one, other])
    new_game = game.copy()
    try:
        new_game.start()
    except Exception as e:
        print("Game error: " + str(e))
        raise e
        # raise
        #print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
        # new_game
        return False
    print("Game lasted: " + str(new_game._turns_passed))
    print("winning agent: " + new_game.winner.agent.name)
    # spark_weights(ql.weights)
    return new_game.winner.agent.name

def test_agent(one, other, number = 20):
    i = 0
    err = 0
    winning_count = {one.name : 0, other.name : 0}
    while i < number:
        winner = test_agent_once(one, other)
        if winner:
            i += 1            
            winning_count[winner] += 1
            pass
            # print("Error")
            # err += 1
            #if err > 100:
            #   print("Aborting after 5 errors.")
            #   break
    print(winning_count)
    print("Winning_rate: " + one.name + ": " + str(winning_count[one.name]/winning_count[other.name]))

if __name__ == "__main__":
    function_approximator = None
    agent_1 = StrategyAgent(LinearFunctionApproximator(), "Learner")
    agent_2 = TradeAgent()
    #while True:
    test_agent(agent_1, agent_2, 5)