"""
Project Name: blackjack-bot
File Name: bot.py
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

(These are probably not the correct terms in Blackjack,
 but they are consistently used within their definition in this project)
TERMS:
    ROUND = A decision, where each player decides what to do with their hand ONCE.
    GAME = All of the rounds, from the initial betting till each player cannot play anymore and either wins or loses.
    SESSION = All of the games. 'in session' means that there are currently players playing.

The MIT License (MIT)

Copyright (c) 2016 Connor York
"""

import dealer as _dealer
import user
import discord
import logging
import time
import card

logging.basicConfig(level=logging.DEBUG)

class BlackJackBot(discord.Client):
    """
    Represents the bot user client for blackjack-bot to run on.

    Attributes:
        INTERMISSION_TIME | int
            The number of seconds that intermission lasts
        BETTING_TIME | int
            The number of seconds that players are allowed to bet
        PLAYING_TIME | int
            The number of seconds that players are allowed to player per
        in_session | bool
            States if there is a current session in progress. This is used to prevent access to certain commands
            when a session is present or not present.
        players | list of :class: 'User' from blackjack-bot, not discord.py
            Iterable of all players currently playing in the game.
        channel | :class: 'Channel'
            The current channel which is used to input and output messages.
        dealer | :class: 'Dealer'
            The user that the client is connected to represented as a player in Blackjack
    """

    INTERMISSION_TIME = 10
    BETTING_TIME = 15
    PLAYING_TIME = 30

    def __init__(self):
        super().__init__()
        self.in_session = False
        self.players = list()
        self.channel = None
        self.dealer = _dealer.Dealer(self.user)

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
                await self.send_message(message.channel, "Blackjack game commencing. Creating table.")
                self.in_session = True
                self.channel = message.channel
                await self.run_session()
                self.in_session = False
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
            await self.run_intermission()
            if self.still_playing_session():
                await self.print_players_with_bank()
                await self.run_game()
                game_counter += 1
        self.reset_bot()
        await self.send_message(self.channel, "Session ending, destroying table. Thanks for playing!")

    async def run_game(self): #TODO PRINT DEALER HAND AND DEAL DEALER CARDS
        """
        Runs the game, which is the time from after the bets have been placed, and the last player has finished
        playing.
        """
        self.deal_cards()
        await self.print_players_with_hand()
        await self.run_betting()
        await self.print_players_with_bet()
        while self.still_playing_game():
            await self.run_round()
            self.ready_new_round_players()
        await self.evaluate_round()
        self.reset_players()

    async def run_betting(self):
        start_time = time.clock()
        await self.send_message(self.channel, "Betting commencing. Enter '!bet #' with '#' replaced your bet! All "
                                              "bets must be greater than $50.")
        while time.clock() - start_time < self.BETTING_TIME:

            def msg_check(msg):
                return msg.content.startswith("!bet")

            bet_msg = await self.wait_for_message(timeout=self.BETTING_TIME, check=msg_check) if self.still_betting() else None
            if bet_msg:
                player = self.get_player(bet_msg.author)
                if player: # if message author not in game, do nothing
                    msg_content = bet_msg.content.strip(' ').split(' ')
                    if len(msg_content) != 2:
                        self.send_message(self.channel, "{}, bet message must follow the format of '!bet #' with '#'"
                                                        "replaced with your bet.".format(player.mention_user()))
                    else:
                        bet_amount = msg_content[1]
                        if bet_amount.isdigit():
                            if player.bet(int(bet_amount)):
                                await self.send_message(self.channel, "{} bet ${}!".format(player.mention_user(),
                                                                                           player.current_bet))
                            else:
                                await self.send_message(self.channel,
                                                        "Bet must be a positive integer greater than 50 that is less than the amount"
                                                        " in your bank.\n You ({}) currently have ${}.".format(
                                                            player.mention_user(), player.bank))
                        else:
                            await self.send_message(self.channel,
                                                    "Bet must be a positive integer greater than 50 that is less than the amount"
                                                    " in your bank.\n You ({}) currently have ${}.".format(
                                                        player.mention_user(), player.bank))


    async def run_round(self):
        start_time = time.clock()
        await self.send_message(self.channel, "The round in commencing. Enter '!hit' or '!hold' to play!")
        while time.clock() - start_time < self.PLAYING_TIME:

            def msg_check(msg):
                return msg.content.startswith("!hit") or msg.content.startswith("!hold")

            play_msg = await self.wait_for_message(timeout=self.PLAYING_TIME, check=msg_check) if self.still_deciding() else None
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
        await self.print_players_with_hand()
        await self.force_hold()
        self.evaluate_players()

    async def run_intermission(self):
        start_time = time.clock()
        await self.send_message(self.channel, "Intermission commencing. Type '!join' to join the table or '!quit' to leave!")
        while time.clock() - start_time < self.INTERMISSION_TIME:

            def msg_check(msg):
                return msg.content.startswith("!join") or msg.content.startswith("!quit")

            join_msg = await self.wait_for_message(timeout=self.INTERMISSION_TIME, check=msg_check) \
                                                                    if time.clock() - start_time < self.INTERMISSION_TIME \
                                                                    else None
            if join_msg:
                if join_msg.content.startswith("!join"):
                    if self.get_player(join_msg.author) is None:
                        self.players.append(user.User(join_msg.author))
                        await self.send_message(self.channel, "{} joined!".format(self.get_player(join_msg.author).mention_user()))
                elif join_msg.content.startswith("!quit"):
                    player = self.get_player(join_msg.author)
                    if player:
                        self.players.remove(player)
                        await self.send_message(self.channel, "{} quit!".format(player.mention_user()))

################################################################################################
######################################## HELPER METHODS ########################################
################################################################################################

    def deal_cards(self):
        card.Card.create_deck()
        for player in self.players:
            player.deal()

    def evaluate_players(self):
        #check each player to see if they have busted and update their variables
        for player in self.players:
            if isinstance(player, user.User):
                if player.is_playing and player.is_bust():
                    player.bust()

    async def evaluate_round(self):
        message = ""
        if self.dealer.has_blackjack():
            message += "The Dealer has Blackjack. All players without blackjack will lose the round.\n\n"
            for player in self.players:
                if not player.has_blackjack():
                    message += "    " + player.mention_user() + " lost " + self.bold_message(player.lose_bet())
                else:
                    message += "    " + player.mention_user() + " had blackjack so they lost nothing."
        elif self.dealer.is_bust():
            message += "The Dealer is busted. All players left in the game win.\n\n"
            for player in self.players:
                if player.is_busted or player.is_bust():
                    message += "    " + player.mention_user() + " lost " + self.bold_message(player.lose_bet())
                else:
                    message += "    " + player.mention_user() + " won " + self.bold_message(player.gain_bet())
        else:
            # players with a higher point total win, players with a lower point total than dealer lose
            dealer_hand_value = min(i for i in self.dealer.get_hand_values())
            message += "The Dealer has a hand value of {}. All players above this value win!".format(dealer_hand_value)
            for player in self.players:
                player_hand_value = min(i for i in player.get_hand_values())
                if not player.is_bust() and player_hand_value > dealer_hand_value:
                    message += "    " + player.mention_user() + " won " + self.bold_message(player.gain_bet())
                elif not player.is_bust() and player_hand_value == dealer_hand_value:
                    message += "    " + player.mention_user() + " tied and lost nothing."
                else:
                    message += "    " + player.mention_user() + " lost " + self.bold_message(player.lose_bet())
        await self.send_message(self.channel, message)

    def reset_bot(self):
        """
        Resets the bot client's state to initial values, preparing it for a new session.
        """
        self.players.clear()
        self.channel = None
        self.dealer = _dealer.Dealer(self.user)

    def reset_players(self):
        """
        Resets the state of all players to initial values.
        """
        for player in self.players:
            player.reset()

    async def force_hold(self):
        names = ""
        for player in self.players:
            if isinstance(player, user.User):
                if not player.has_played:
                    player.hold()
                    names += player.mention_user() + ","
        await self.send_message(self.channel, "Forced {} to hold because they took too long to decide".format(names))

    def ready_new_round_players(self):
        """
        Resets valid player's 'has_played' variable so that they are allowed to play in the next round
        """
        for player in self.players:
            if player.is_playing:
                player.has_played = False

    def still_playing_session(self):
        """
        Determines if there are still players playing blackjack
        :return: True if there are still players playing, False otherwise
        """
        return len(self.players) != 0

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

    def still_betting(self):
        """
        Determines if there are still players in the game who have not bet.
        :return: True if there are currently players with no bet, False otherwise
        """
        for player in self.players:
            if player.current_bet is 0:
                return True
        return False

    def get_player(self, member):
        for player in self.players:
            if player.id == member.id:
                return player
        return None

###############################################################################################
######################################## PRINT METHODS ########################################
###############################################################################################

    async def print_players_with_hand(self):
        message = "Players and their hands\n\n"
        for player in self.players:
            if isinstance(player, user.User):
                message += player.str_with_hand()
        await self.send_message(self.channel, message)

    async def print_players_with_bet(self):
        message = "Players and their bets\n\n"
        for player in self.players:
            if isinstance(player, user.User):
                message += player.str_with_bet()
        await self.send_message(self.channel, message)

    async def print_players_with_bank(self):
        message = "Players and their banks\n\n"
        for player in self.players:
            if isinstance(player, user.User):
                message += player.str_with_bank()
        await  self.send_message(self.channel, message)

    @staticmethod
    def bold_message(message):
        return "**{}**".format(message)

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