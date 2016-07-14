"""
Class representing a player in a game of blackjack. This can be the dealer or a human player.
"""

import card


class Player:

    def __init__(self, member):
        self.member = member
        self.hand = list()
        self.is_playing = True # is currently playing in the game (Not holding or bust)
        self.has_played = False # has currently played in the round (Has not hit, held, or busted)

    def deal(self):
        """
        Assigns an initial hand of two random cards to the player.
        """
        self.is_playing = True
        for _ in range(2):
            self.hand.append(card.Card.draw_card())

    def hand_str(self):
        hand_string = ""
        for i in range(len(self.hand)):
            hand_string += self.hand[i].__str__() + ", " if i < len(self.hand) - 1 else self.hand[i].__str__()
        return hand_string


    def reset_hand(self):
        """
        Resets the players hand to an empty hand of no cards
        """
        self.hand.clear()

    def reset(self):
        self.reset_hand()
        self.is_playing = True
        self.has_played = False

    def hit(self):
        """
        Adds a card to the players hand
        :return: True if successfully hit, False if not
        """
        if self.is_playing and not self.has_played and not self.is_bust():
            self.hand.append(card.Card.draw_card())
            self.has_played = True
            return True
        return False

    def hold(self):
        """
        Holds the players current hand, preventing them from hitting more cards
        :return: True if a successful hold, False if not
        """
        if self.is_playing and not self.has_played:
            self.is_playing = False
            self.has_played = True
            return True
        return False

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
        for value in self.get_hand_values():
            if value <= 21:
                return False
        return True
