"""
Class representing the dealer. This is run by the CPU and not a person.
"""

import player


class Dealer(player.Player):

    def __init__(self):
        super().__init__()

    def hit(self):
        """
        Adds a card to the hand only if the hand has a possible value of 16 or less
        """
        if self.isPlaying:
            for value in self.getHandValues():
                if value <= 16:
                    super().hit()
                    return
            self.hold()
