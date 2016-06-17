""" """
# TODO
import card


class Player:
    def __init__(self):
        self.hand = list()
        self.isPlaying = False

    # TODO
    def deal(self):
        """

        :return:
        """
        self.isPlaying = True
        for _ in range(2):
            self.hand.append(card.Card)

    # TODO
    def hit(self):
        """

        :return:
        """
        if self.isPlaying and not self.isBust():
            self.hand.append(card.Card)

    # TODO
    def hold(self):
        """

        :return:
        """
        self.isPlaying = False

    # TODO
    def getHandValues(self):
        """

        :return:
        """
        values = list()
        hasAce = False
        handValue = 0
        for c in self.hand:
            if isinstance(c, card.Card):
                if c.value is 1:
                    hasAce = True
                else:
                    handValue += c.value
        if hasAce:  # append the current hand value with the two values of an Ace
            values.append(handValue + 1)
            values.append(handValue + 11)
        else:
            values.append(handValue)
        return values

    def isBust(self):
        """
        Determines if the current player is busted (has a hand value of over 21)
        :return: Boolean stating if busted
        """
        busted = True
        handValues = self.getHandValues()
        for value in handValues:
            if value <= 21:
                busted = False
                break  # only need one possible hand to be below 21
        return busted
