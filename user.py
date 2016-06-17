"""
Class representing a human player in blackjack.
"""

import player


class User(player.Player):

    def __init__(self):
        super().__init__()
        self.bank = 5000

    def bet(self):
        pass


