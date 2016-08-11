"""
Project Name: blackjack-bot
File Name: dealer.py
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

import player

class Dealer(player.Player):
    """
    Represents a human player in Blackjack.

    Parameters:
        member | :class: 'Member'
            The Member object representing the blackjack-bot client

    Attributes:
        name | str
            Name of the dealer in Blackjack
    """

    def __init__(self, member):
        """
        :param member: discord.py :class: 'Member' of the client bot
        """
        super().__init__(member)

    def str_with_hand(self):
        """
        Only shows the first card in the hand, like in a real blackjack game.
        :return: str depicting the dealer and the first card in it's hand
        """
        return "Dealer:\n" + self.hand_str(1)

    def final_str_with_hand(self):
        """
        Shows all of the dealer's hand, for post game printing to players.
        :return: str depicting the dealer and i's entire hand
        """
        return "Dealer's final hand:\n" + self.hand_str()

    def hit_until_hold(self):
        """
        Keeps on adding cards to the hand until the lowest value of the hand is above 16, then holds.

        This method assumes that the dealer has already been dealt cards, and is to be used after all players are done
        playing.
        """
        while min(value for value in self.get_hand_values()) < 17:
            self.hit()
        self.hold()

