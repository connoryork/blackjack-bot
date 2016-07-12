"""
Class representing a human player in blackjack.
"""


import player


class User(player.Player):

    def __init__(self, member):
        super().__init__(member)

        self.id = member.id # unique id
        self.name = member.display_name
        self.bank = 5000
        self.bet = 0 # zero means that there is no current bet

    def bet(self, bet):
        """
        Bets a certain amount of money during a round of blackjack.
        :param bet: integer number of money user wants to bet
        """
        import bot
        if isinstance(bet, int):
            if bet > self.bank or bet < 1:
                bot.send_message("Bet must be a positive integer that is divisible by 50 and less than the amount"
                                 " in your bank.\n You ({}) currently have ${}.".format(self.mention_user(), self.bank))
            elif bet % 50 != 0:
                #send message that bet must be a factor of 50
                pass
            else:
                #send message that user bet a certain amount
                self.bet = bet
        else:
            #send message that bet must be an integer
            pass

    def reset_bet(self):
        """
        Resets the users bet to no bet (zero)
        """
        self.bet = 0

    def mention_user(self):
        if self.member.nick:
            return '<@!{}>'.format(self.id)
        return '<@{}>'.format(self.id)



