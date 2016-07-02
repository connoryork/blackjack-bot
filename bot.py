"""
Discord Blackjack Bot
Created by Connor York (cxy1054@rit.edu)
"""

import user
import discord
import logging
import time

logging.basicConfig(level=logging.DEBUG)


class BlackJackBot(discord.Client):

    intermission_time = 10
    betting_time = 15
    playing_time = 30

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
                # display end game
                    # display users and their current bank, and what they lost or gained
                # repeat from beginning, if there are no users currently playing, the game will end.

    async def run_game(self):

        pass
        # give users time to bet
        # send message that a new hand is starting and show everyone playing and their cards, including the dealer
        # give users time to decide whether to hit or hold
        # react based on what users typed in
        # display users and their cards, or if they are bust
        # repeat until all users are either holding or bust

    def deal_cards(self):
        for player in self.players:
            player.deal()

    async def run_betting(self):
        pass

    async def run_play(self):
        start_time = time.clock()
        while time.clock() - start_time < self.playing_time:

            def msg_check(msg):
                return msg.content.startswith("!hit") or msg.content.startswith("!hold")

            play_msg = await self.wait_for_message(timeout=30, check=msg_check) if self.still_playing() else \
                None
            player = self.get_player(play_msg.author)
            if player: # only cares about messages from players
                if play_msg.content.startswith("!hit"):
                    if player.hit():
                        #print success message
                        pass
                elif play_msg.content.startswith("!hold"):
                    if player.hold():
                        #print success message
                        pass

    async def evaluate_players(self):
        #evaulate players after they hit of held
        pass

    async def run_intermission(self):
        start_time = time.clock()
        while time.clock() - start_time < self.intermission_time:
            join_msg = await self.wait_for_message(timeout=10, content="!join")
            if join_msg:
                self.players.append(user.User(join_msg.author))
                await self.send_message(self.channel, "{} joined!".format(join_msg.author.name))
        self.players.append()
        await self.print_players()

    async def shutdown(self):
        await self.send_message(self.channel, "Bye!")
        await self.logout()

    def still_playing(self):
        """
        Determines if the game is still in action, meaning that players still have not hit or held their hand.
        :return:
        """
        for player in self.players:
            if isinstance(player, user.User):
                if not player.has_played:
                    return True
        return False

    def get_player(self, member):
        for player in self.players:
            if player.id == member.id:
                return player
        return None

    def get_longest_player_name_length(self):
        longest = 0
        for player in self.players:
            if longest < len(player.name):
                longest = len(player.name)
        return longest

    async def print_players(self): # in progress
        name_length = self.get_longest_player_name_length()
        top = "_"*(name_length*2 + 14) + "\n" # similar length of categories
        categories = "{:>{}} |{:^10}| Hand\n".format("Name",name_length,"Bank")
        message = top + categories
        players_string = ""
        for player in self.players:
            hand = player.hand#.join ##????????????????????
            if isinstance(player, user.User):
                players_string += "{:^{}} |{:^10}| {}\n".format(player.name, name_length, '$'+str(player.bank), hand)
            else:
                message += "{:^{}} |{:^10}| {}\n".format("Dealer", name_length, "Infinite", hand)
        message += players_string
        await self.send_message(self.channel, message)

async def send_message(content):
    """
    Function to send messages to the chat by outside objects that are not the bot itself
    :param content: string content of message
    """
    await client.send_message(client.channel, content)


token_file = open("token.txt", "r")
token = token_file.readline().strip()
token_file.close()

client = BlackJackBot()
client.run(token)