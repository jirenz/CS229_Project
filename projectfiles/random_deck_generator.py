from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, get_all_cards
from hearthbreaker.cards import *
import random

class RandomDeckGenerator:

	def generate(self, character_class = None):
		cur_card_list = []
		all_cards = list(get_all_cards().values())
		if character_class is None:
			character_class = random.randint(1, 9)
			if character_class == 3:
				character_class += 1
		while len(cur_card_list) < 30:
			new_card_name = random.choice(all_cards)
			new_card = new_card_name()
			if new_card.collectible:
				if new_card.character_class == CHARACTER_CLASS.ALL or new_card.character_class == character_class:
					cur_card_list.append(new_card)
		deck = Deck(cur_card_list, hero_for_class(character_class))
		return deck