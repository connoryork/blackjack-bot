"""
Class representing a card in the game of blackjack.
Contains some other data members that help define a card.
"""

from random import randint

class Card:

    SUITES = ["Hearts", "Clubs", "Spades", "Diamonds"]

    CARDS = ['Ace', 'Two', 'Three', 'Four',
             'Five', 'Six', 'Seven', 'Eight',
             'Nine', 'Ten', 'Jack', 'Queen', 'King']

    deck = list()

    def __init__(self, value, suite, card):
        """
        Creates a Card object based on inputted parameters
        """

        self.value = value
        self.suite = suite
        self.name = card + " of " + suite

    def __str__(self):
        return self.name

    # def __ne__(self, other):
    #     return not self.__eq__(other)
    #
    # def __eq__(self, other):
    #     return self.name == other.name
    #
    # def __hash__(self):
    #     return len(self.name)

    @staticmethod
    def create_deck():
        Card.clear_deck()
        for suite in Card.SUITES:
            value = 1
            for card in Card.CARDS:
                Card.deck.append(Card(value, suite, card))
                if value < 10:
                    value += 1

    @staticmethod
    def clear_deck():
        Card.deck.clear()

    @staticmethod
    def draw_card():
        if len(Card.deck) != 0:
            return Card.deck.pop(randint(0, len(Card.deck) - 1))


def test():
    Card.create_deck()
    for _ in Card.deck:
        print(_)



if __name__ == "__main__":
    test()
    print("\n\n\n")
    for _ in range(0,52):
        print(Card.draw_card())
