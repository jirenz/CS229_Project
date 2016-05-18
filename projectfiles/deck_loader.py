#from hearthbreaker.agents import registry
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Deck, card_lookup # Game, 
# from hearthbreaker.ui.game_printer import GameRender
from hearthbreaker.cards import *

class DeckLoader:
	def load_deck(self, filename):
		cards = []
		character_class = CHARACTER_CLASS.MAGE

		with open(filename, "r") as deck_file:
			contents = deck_file.read()
			items = contents.splitlines()
			for line in items[0:]:
				parts = line.split(" ", 1)
				count = int(parts[0])
				for i in range(0, count):
					card = card_lookup(parts[1])
					if card.character_class != CHARACTER_CLASS.ALL:
						character_class = card.character_class
					cards.append(card)

		if len(cards) > 30:
			pass
		return Deck(cards, hero_for_class(character_class))

# if __name__ == "__main__":
# 	DeckLoader.load_deck("zoo.hsdeck")
