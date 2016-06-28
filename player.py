"""
Class representing a player in a game of blackjack. This can be the dealer or a human player.
"""

import card


class Player:
    def __init__(self):
        self.hand = list()
        self.is_playing = False

    def deal(self):
        """
        Assigns an initial hand of two random cards to the player.
        """
        self.is_playing = True
        for _ in range(2):
            self.hand.append(card.Card())

    def reset_hand(self):
        """
        Resets the players hand to an empty hand of no cards
        """
        self.hand.clear()

    def hit(self):
        """
        Adds a card to the players hand
        """
        if self.is_playing and not self.is_bust():
            self.hand.append(card.Card())

    def hold(self):
        """
        Holds the players current hand, preventing them from hitting more cards
        """
        self.is_playing = False

    def get_hand_values(self):
        """
        Determines the possible values of the current players hand
        :return: list of possible integer values of the players current hand
        """
        values = list()
        has_ace = False
        hand_value = 0
        for c in self.hand:
            if isinstance(c, card.Card):
                if c.value is 1:
                    has_ace = True
                else:
                    hand_value += c.value
        if has_ace:  # append the current hand value with the two values of an Ace
            values.append(hand_value + 1)
            values.append(hand_value + 11)
        else:
            values.append(hand_value)
        return values

    def is_bust(self):
        """
        Determines if the current player is busted (has a hand value of over 21)
        :return: Boolean stating if busted
        """
        busted = True
        hand_values = self.get_hand_values()
        for value in hand_values:
            if value <= 21:
                busted = False
                break  # only need one possible hand to be below 21
        return busted
