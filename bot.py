"""
Discord Blackjack Bot
Created by Connor York (cxy1054@rit.edu)

TERMS:
ROUND = A decision, where each player decides what to do with their hand ONCE.
GAME = All of the rounds, from the initial betting till each player cannot play anymore and either wins or loses.
SESSION = All of the games. 'in session' means that there are currently players playing.

"""

import dealer
import user
import discord
import logging
import time
import card

logging.basicConfig(level=logging.DEBUG)


class BlackJackBot(discord.Client):

    intermission_time = 10
    betting_time = 15
    playing_time = 30

    def __init__(self):
        super().__init__()
        self.in_session = False # tells if current game is in progress
        self.players = list()
        self.channel = None
        self.dealer = dealer.Dealer(self.user)

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
                await self.send_message(message.channel, "Blackjack game commencing. Type \"!join\" to join the table!")
                self.in_session = True
                self.channel = message.channel
                await self.run_session()
                # send message that the game is starting
                # send message that users should type !join to join the game and !quit to leave the game
                # load users based on who responded
                # display who is in the game
                # start game
                # display end game
                    # display users and their current bank, and what they lost or gained
                # repeat from beginning, if there are no users currently playing, the game will end.

################################################################################################
######################################### GAME METHODS #########################################
################################################################################################


        # give users time to bet
        # send message that a new hand is starting and show everyone playing and their cards, including the dealer
        # give users time to decide whether to hit or hold
        # react based on what users typed in
        # display users and their cards, or if they are bust
        # repeat until all users are either holding or bust

    async def run_session(self):
        game_counter = 0
        while self.still_playing_session() or game_counter == 0:
            await self.print_players()
            await self.run_intermission()
            await self.print_players()
            await self.run_game()

    async def run_game(self):
        """
        Runs the game, which is the time from after the bets have been placed, and the last player has finished
        playing.
        """
        self.deal_cards()
        await self.run_betting()
        while self.still_playing_game():
            await self.print_players()
            await self.run_round()
            await self.print_players()
        self.reset_players()

    async def run_betting(self):
        pass

    async def run_round(self):
        start_time = time.clock()
        await self.send_message(self.channel, "Enter !hit or !hold")
        while time.clock() - start_time < self.playing_time:

            def msg_check(msg):
                return msg.content.startswith("!hit") or msg.content.startswith("!hold")

            play_msg = await self.wait_for_message(timeout=30, check=msg_check) if self.still_deciding() else None
            if play_msg:
                player = self.get_player(play_msg.author)
                if player:
                    if play_msg.content.startswith("!hit"):
                        if player.hit(): #success
                            await self.send_message(self.channel, "{} hit!".format(player.mention_user()))
                        else:
                            await self.send_message(self.channel, "{} can not hit!".format(player.mention_user()))
                    elif play_msg.content.startswith("!hold"):
                        if player.hold(): #success
                            await self.send_message(self.channel, "{} held their hand!".format(player.mention_user()))
                        else:
                            await self.send_message(self.channel, "{} cannot hold! They may have already played or "
                                                                  "are not playing this round. ".format(player.mention_user()))
            else:
                break
        await self.print_players()
        await self.force_hold()
        await self.evaluate_players()

    async def run_intermission(self):
        start_time = time.clock()
        join_list = list()
        while time.clock() - start_time < self.intermission_time:
            join_msg = await self.wait_for_message(timeout=10, content="!join")
            if join_msg:
                if join_msg.author not in join_list:
                    join_list.append(join_msg.author)
                    self.players.append(user.User(join_msg.author))
                    await self.send_message(self.channel, "{} joined!".format(join_msg.author.name))

################################################################################################
######################################## HELPER METHODS ########################################
################################################################################################

    def deal_cards(self):
        card.Card.create_deck()
        for player in self.players:
            player.deal()

    async def evaluate_players(self):
        # evaulate players after they hit of held
        pass

    def reset_players(self): #TODO
        pass

    async def force_hold(self):
        for player in self.players:
            if isinstance(player, user.User):
                if not player.has_played:
                    player.hold()
                    await self.send_message(self.channel, "Forced {} to hold because they took too long to decide" \
                                            .format(player.mention_user()))

    def still_playing_session(self):
        """
        Determines if there are still players playing blackjack
        :return: True if there are still players playing, False otherwise
        """
        return len(self.players) != 1 # the bot itself

    def still_playing_game(self):
        """
        Determines if there are still players that are eligible to play in a round. This means that they are not
        holding or busted.
        :return: True if there are still eligible players, False if not
        """
        for player in self.players:
            if player.is_playing:
                return True
        return False

    def still_deciding(self):
        """
        Determines if the decision time is still in action, meaning that players still have not hit or held their hand.
        :return: Whether or not there are players that have not decided what to do (hit or hold)
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

###############################################################################################
######################################## PRINT METHODS ########################################
###############################################################################################

    async def print_players(self): # in progress
        name_length = self.get_longest_player_name_length()
        top = "_"*(name_length*2 + 14) + "\n" # similar length of categories
        categories = "{:>{}} |{:^10}| Hand\n".format("Name",name_length,"Bank")
        message = top + categories
        players_string = ""
        for player in self.players:
            hand = player.hand#.join ##????????????????????
            if isinstance(player, user.User):
                players_string += "{:^{}} |{:^10}| {}\n".format(player.name, name_length, '$'+str(player.bank),
                                                                player.hand_str())
            else:
                message += "{:^{}} |{:^10}| {}\n".format("Dealer", name_length, "Infinite", hand)
        message += players_string
        await self.send_message(self.channel, message)


    async def shutdown(self):
        await self.send_message(self.channel, "Bye!")
        await self.logout()

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