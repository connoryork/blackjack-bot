"""
Project Name: blackjack-bot
File Name: card.py
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

from random import randint

class Card:
    """
    Represents a playing card in a deck of cards.

    Attributes:
        SUITES | list of str
            The string literals of the suites in a 52 card deck of playing cards
        CARDS | list of str
            The string literals of the types of cards in a 52 card deck of playing cards
        deck | list of :class: 'Card'
            Iterable of Card objects that have not been removed from the current deck.
        value | int
            Number value of the current Card in the game Blackjack
        suite | str
            String from SUITES
        name | str
            Definition of the card in common playing card terms e.g. 'Ace of Hearts'
    """

    SUITES = ["Hearts", "Clubs", "Spades", "Diamonds"]

    CARDS = ['Ace', 'Two', 'Three', 'Four',
             'Five', 'Six', 'Seven', 'Eight',
             'Nine', 'Ten', 'Jack', 'Queen', 'King']

    deck = list()

    def __init__(self, value, suite, card):
        self.value = value
        self.suite = suite
        self.name = card + " of " + suite

    def __str__(self):
        return self.name

    @staticmethod
    def create_deck():
        """
        Creates an ordered deck of 52 standard playing cards.
        """
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
        """
        Draws a random Card from the deck.
        :return: Card object
        """
        if len(Card.deck) == 0:
            Card.create_deck()
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
