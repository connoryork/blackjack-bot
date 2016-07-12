"""
Class representing the dealer. This is run by the CPU and not a person.
"""

import player


class Dealer(player.Player):

    def __init__(self, user):
        """
        :param user: Discord bot client.user, which represents the connected client as a user similar to a person.
        """
        super().__init__(user)
        self.name = "Dealer"

    def hit(self):
        """
        Adds a card to the hand only if the hand has a possible value of 16 or less. Holds otherwise.
        """
        if self.is_playing:
            for value in self.get_hand_values():
                if value <= 16:
                    super().hit()
                    return
            self.hold()
