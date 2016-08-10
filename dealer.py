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
        return "Dealer:\n" + self.hand_str()

    def hit(self):
        """
        Adds a card to the hand only if the hand has a possible value of 16 or less. Holds otherwise.
        """
        if self.is_playing and not self.has_played:
            for value in self.get_hand_values():
                if value <= 16:
                    super().hit()
                    return
            self.hold()
