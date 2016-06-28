""" Basic Discord Bot"""

import discord
import logging

logging.basicConfig(level=logging.DEBUG)


class BlackJackBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.in_session = False # tells if current game is in progress
        self.in_intermission = False # tells if the add/remove players stage is in progress

    async def on_message(self, message):

        if isinstance(message, discord.Message): # temporary for message access
            pass

        await self.wait_until_ready()
        message_content = message.content.strip()

        if not message_content.startswith("!"):
            return
        if message.author == self.user:
            return
        if not self.in_session: # if there is no current game, game commands should not be accessible
            if message_content.startswith("!blackjack"):
                await self.send_message(message.channel, 'test123')
                await self.shutdown(message.channel)
                #self.in_session = True
                # send message that the game is starting
                # send message that users should type !join to join the game and !quit to leave the game
                # load users based on who responded
                # display who is in the game
                # start game
                    # give users time to bet
                    # send message that a new hand is starting and show everyone playing and their cards, including the dealer
                    # give users time to decide whether to hit or hold
                    # react based on what users typed in
                    # display users and their cards, or if they are bust
                    # repeat until all users are either holding or bust
                # display end game
                    # display users and their current bank, and what they lost or gained
                # repeat from beginning, if there are no users currently playing, the game will end.
        else:
            pass

    async def shutdown(self, channel):
        await self.send_message(channel, "Bye!")
        await self.logout()




credentials = open("credentials.txt", 'r')
email = credentials.readline().strip()
password = credentials.readline().strip()
credentials.close()

client = BlackJackBot()
client.run(email, password)