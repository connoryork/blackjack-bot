"""
Class representing a card in the game of blackjack.
Contains some other data members that help define a card.
"""

from random import randint

SUITES = ["Hearts", "Clubs", "Spades", "Diamonds"]

CARDS = ['Ace', 'Two' 'Three', 'Four',
                'Five', 'Six', 'Seven', 'Eight',
                'Nine', 'Ten', 'Jack', 'Queen', 'King']


class Card:

    deck = set()

    def __init__(self):
        """
        Creates a random Card that is not already in play
        """
        while True:
            self.value = randint(1, 10)
            self.suite = SUITES[randint(0, 3)]
            self.name = CARDS[self.value - 1] + " of " + self.suite if self.value < 10 \
                else CARDS[self.value - 1 + randint(0, 3)] + " of " + self.suite
            if self not in Card.deck:
                Card.deck.add(self)
                break
