"""
Project Name: blackjack-bot
File Name: player.py
Author: Connor York (cxy1054@rit.edu)
Updated: 7/20/16

Discord is a voice and chat app for gamers created by Hammer & Chisel, a startup based in Burlingame, CA.
More information on Discord and Hammer & Chisel can be found through the following links:
    https://discordapp.com/
    https://discordapp.com/company

blackjack-bot is developed using the unofficial API for Discord. It is made and run by developers not affiliated with
the company. The library used in this project can be found in the link below:
    https://github.com/Rapptz/discord.py

Description: blackjack-bot is a Discord 'bot' for emulating the card game Blackjack in the chat channels of servers.
    A 'bot' is essentially a user that is run by some sort of AI instead of a person. They perform actions based on
    messages in chat that are interpreted as commands. blackjack-bot uses commands in chat to emulate Blackjack.

(These are probably not the correct terms in Blackjack, but they are consistently used within their definition in this project)
TERMS:
    ROUND = A decision, where each player decides what to do with their hand ONCE.
    GAME = All of the rounds, from the initial betting till each player cannot play anymore and either wins or loses.
    SESSION = All of the games. 'in session' means that there are currently players playing.

The MIT License (MIT)

Copyright (c) 2016 Connor York
"""

import card

class Player:
    """
    Represents a player in Blackjack, which can be a dealer or a human player.

    Parameters:
        member | :class: 'Member'
            The member to be connected to the in-game player.

    Attributes:
        member | :class: 'Member'
            Unique id for a specific user
        hand | list
            Amount of money the player currently possesses
        is_playing | bool
            States if the player is currently playing in the game (Not holding or bust)
            This will be False if the player is not eligible to play more rounds in the game (busted or held hand)
        has_played | bool
            States if the player has currently played in the round (Has not hit or held)
            This will always be True if the player is not eligible to play more rounds (busted or held hand)
    """


    def __init__(self, member):
        self.member = member
        self.hand = list()
        self.is_playing = True
        self.has_played = False
        self.is_busted = False

    def deal(self):
        """
        Assigns an initial hand of two random cards to the player.
        """
        self.is_playing = True
        for _ in range(2):
            self.hand.append(card.Card.draw_card())

    def hand_str(self):
        """
        Creates a string from the player's hand
        :return: str of cards in hand
        """
        hand_string = ""
        for i in range(len(self.hand)):
            hand_string += "    " + self.hand[i].__str__() + "\n" if i < len(self.hand) - 1 \
                else "    " + self.hand[i].__str__()
        return hand_string


    def reset_hand(self):
        """
        Resets the players hand to an empty hand of no cards
        """
        self.hand.clear()

    def reset(self):
        """
        Resets the player to initial state
        """
        self.reset_hand()
        self.is_playing = True
        self.has_played = False
        self.is_busted = False

    def hit(self):
        """
        Adds a card to the players hand
        :return: True if successful hit, False if not
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
        This is useful when a player has an Ace in their hand, as it can be of value 1 or 11.
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
        Determines if the current player is busted (has a hand value of over 21).
        If the hand has multiple values, both must be a value over 21 in order to be considered busted.
        :return: Boolean stating if busted
        """
        for value in self.get_hand_values():
            if value <= 21:
                return False
        return True

    def has_blackjack(self):
        """
        Determines if the player has blackjack, a hand of value 21.
        :return: Boolean stating if the player has 21
        """
        for value in self.get_hand_values():
            if value is 21:
                return True
        return False

    def bust(self):
        """
        Sets the player's state to that of a player that cannot play anymore.
        """
        self.is_playing = False
        self.has_played = True
        self.is_busted = True
