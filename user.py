"""
Project Name: blackjack-bot
File Name: user.py
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

class User(player.Player):
    """
    Represents a human player in Blackjack.

    Parameters:
        member | :class: 'Member'
            The member to be connected to the in-game player.

    Attributes:
        id | str
            Unique id for a specific user
        bank | int
            Amount of money the player currently possesses
        bet | int
            Bet for the current game
    """

    def __init__(self, member):
        super().__init__(member)

        self.id = member.id
        self.bank = 5000
        self.current_bet = 0 # zero means that there is no current bet

    def str_with_hand(self):
        return self.mention_user() + ":\n" + self.hand_str()

    def str_with_bet(self):
        return "{0} bet {1} memes".format(self.mention_user(), str(self.current_bet))

    def str_with_bank(self):
        return "{0} has {1} memes".format(self.mention_user(), str(self.bank))

    def bet(self, amount):
        """
        Bets a certain amount of money during a round of blackjack.
        :param amount: integer number of money user wants to bet
        :return bool stating if the bet was valid or not
        """
        if isinstance(amount, int):
            if amount > self.bank or amount < 50:
                return False
            else:
                self.current_bet = amount
                return True
        else:
            return False

    def reset(self):
        """
        Resets the user to initial values
        """
        super().reset()
        self.current_bet = 0

    def mention_user(self):
        if self.member.nick:
            return '<@!{}>'.format(self.id)
        return '<@{}>'.format(self.id)

    def gain_bet(self):
        if self.has_blackjack():
            self.bank += int(self.current_bet * 1.5)
            return int(self.current_bet * 1.5)
        self.bank += self.current_bet
        return self.current_bet

    def lose_bet(self):
        self.bank -= self.current_bet
        return self.current_bet

    def set_bank(self, new):
        """
        Sets the user's bank to the passed amount
        :param new: int value of new bank
        """
        self.bank = new
