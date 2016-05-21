from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup, Game
from hearthbreaker.cards import *
from hearthbreaker.replay import *
from hearthbreaker.agents.basic_agents import *
import sys
from projectfiles.deck_loader import DeckLoader

class RandomDeckGenerator

	def generate(self, class)
		cur_card_list = {}
		all_cards = get_cards()
		for i in range(1, 30)
			cur_card_list << 
