""" Basic Discord Bot"""

import discord
import logging
import time

logging.basicConfig(level=logging.DEBUG)


class BlackJackBot(discord.Client):

    intermission_time = 10

    def __init__(self):
        super().__init__()
        self.in_session = False # tells if current game is in progress
        self.in_intermission = False # tells if the add/remove players stage is in progress
        self.players = list()
        self.channel = None

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
            if message_content.startswith("!blackjack"): # start game command
                await self.send_message(message.channel, "Blackjack game commencing. Type \"!join\" to join the match!")
                self.in_session = True
                self.in_intermission = True
                self.channel = message.channel
                await self.run_intermission()
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
 #       else:
#            if message_content.startswith("!join"):
    async def run_intermission(self):
        start_time = time.clock()
        while time.clock() - start_time < self.intermission_time:
            join_msg = await self.wait_for_message(timeout=10, content="!join")
            if join_msg:
                self.players.append(join_msg.author)
                await self.send_message(self.channel, "@%s joined!" % join_msg.author.name)
        await self.send_message(self.channel, self.players)

    async def shutdown(self, channel):
        await self.send_message(channel, "Bye!")
        await self.logout()




credentials = open("credentials.txt", 'r')
email = credentials.readline().strip()
password = credentials.readline().strip()
credentials.close()

client = BlackJackBot()
client.run(email, password)