from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.replay import *
from hearthbreaker.agents import *

from projectfiles.random_deck_generator import RandomDeckGenerator
from projectfiles.agent import *
import sys
import shelve

from projectfiles.deck_loader import DeckLoader
from projectfiles.hearthlogger import Hearthlogger

def test_agent_once():
    generator = RandomDeckGenerator()
    deck1 = generator.generate()
    deck2 = deck1.copy()
    game = Game([deck1, deck2], [AIAgent(), RandomAgent()])
    new_game = game.copy()
    try:
        new_game.start_with_debug()
    except Exception as e:
       #print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__(), indent=1))
       #print(new_game._all_cards_played)
       del new_game
       del game_log
       return False
    print("winning agent: " + new_game.winner.agent.__class__.__name__)
    return new_game.winner.agent.__class__.__name__

def test_agent(number):
    i = 0
    winning_count = {}
    while i < number:
        winner = test_agent_once()
        if winner:
            i += 1
            if winner in winning_count:
                winning_count[winner] += 1
            else:
                winning_count[winner] = 1
    print(winning_count)

if __name__ == "__main__":
    test_agent(int(sys.argv[1]))


