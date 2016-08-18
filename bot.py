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
import sqlite3
import os.path

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

    INTERMISSION_TIME = 20
    BETTING_TIME = 50
    PLAYING_TIME = 120
    MESSAGE_GAP = 10

    PREFIX = "$"

    def __init__(self):
        super().__init__()
        self.in_session = False
        self.players = list()
        self.channel = None
        self.dealer = _dealer.Dealer(self.user)
        if not os.path.isfile("users.db"):
            file = open("users.db", 'a')
            file.close()
            self.sqlite_conn = sqlite3.connect("users.db")
            self.conn_cursor = self.sqlite_conn.cursor()
            self.conn_cursor.execute('''CREATE TABLE users (id text, bank integer)''')
        else:
            self.sqlite_conn = sqlite3.connect("users.db")
            self.conn_cursor = self.sqlite_conn.cursor()


    async def on_message(self, message):

        await self.wait_until_ready()
        message_content = message.content.strip()

        if not message_content.startswith(self.PREFIX):
            return
        if message.author == self.user:
            return
        if not self.in_session: # if there is no current game, game commands should not be accessible
            if message_content.startswith(self.PREFIX + "blackjack"): # start game command
                self.in_session = True
                self.channel = message.channel
                await self.run_session()
                self.in_session = False

################################################################################################
######################################### GAME METHODS #########################################
################################################################################################

    async def run_session(self):
        await self.send_message(self.channel, "Blackjack game commencing. Creating table.")
        time.sleep(self.MESSAGE_GAP)
        game_counter = 0
        while self.still_playing_session() or game_counter == 0:
            await self.run_intermission()
            if self.still_playing_session():
                await self.print_players_with_bank()
                time.sleep(self.MESSAGE_GAP)
                await self.run_game()
                for player in self.players: # updates database every round
                    self.write_user(player)
            game_counter += 1
        await self.send_message(self.channel, "Session ending, destroying table. Thanks for playing!")
        self.reset_bot()

    async def run_game(self):
        """
        Runs the game, which is the time from after the bets have been placed, and the last player has finished
        playing.
        """
        await self.run_betting()
        self.force_bet()
        await self.print_players_with_bet()
        time.sleep(self.MESSAGE_GAP)
        cards_msg = await self.send_message(self.channel, "Retrieving a new deck, shuffling, and dealing cards! Please hold!")
        self.deal_cards()
        time.sleep(self.MESSAGE_GAP)
        await self.edit_message(cards_msg, cards_msg.content + "\n\n" + self.str_players_with_hand())
        time.sleep(self.MESSAGE_GAP)
        while self.still_playing_game():
            await self.run_round()
            self.ready_new_round_players()
        await self.send_message(self.channel, "There are no more players eligible to play, so the game is over!"
                                              " Here evaluation to see who won!\n" + self.evaluate_game())
        time.sleep(self.MESSAGE_GAP)
        await self.send_message(self.channel, "Resetting players for next game...")
        time.sleep(self.MESSAGE_GAP)
        self.reset_players()

    async def run_betting(self):
        start_time = time.clock()
        await self.send_message(self.channel, "Betting commencing. Enter '{}bet #' with '#' replaced with your bet! All "
                                              "bets must be between 100 and 500 memes.".format(self.PREFIX))
        confirm_msg = None
        while time.clock() - start_time < self.BETTING_TIME:

            def msg_check(msg):
                return msg.content.startswith(self.PREFIX + "bet")

            bet_msg = await self.wait_for_message(timeout=self.BETTING_TIME, check=msg_check) if self.still_betting() else None
            if bet_msg:
                player = self.get_player(bet_msg.author)
                if player: # if message author not in game, do nothing
                    msg_content = bet_msg.content.strip(' ').split(' ')
                    if len(msg_content) != 2:
                        pass
                    else:
                        bet_amount = msg_content[1]
                        if bet_amount.isdigit():
                            if player.bet(int(bet_amount)):
                                if not confirm_msg:
                                    confirm_msg = await self.send_message(self.channel, "{} bet {} memes!".format(player.mention_user(),
                                                                                           player.current_bet))
                                else:
                                    await self.edit_message(confirm_msg, confirm_msg.content + "\n\n" + "{} bet {} memes!".format(player.mention_user(), player.current_bet))
                            else:
                                if not confirm_msg:
                                    confirm_msg = await self.send_message(self.channel,
                                                        "Bet must be a positive integer between 100 and 500 memes that is less than the amount"
                                                        " in your bank.\n You ({}) currently have {} memes.".format(
                                                            player.mention_user(), player.bank))
                                else:
                                    await self.edit_message(confirm_msg, confirm_msg.content + "\n\n" +
                                                        "Bet must be a positive integer between 100 and 500 memes that is less than the amount"
                                                        " in your bank.\n You ({}) currently have {} memes.".format(
                                                            player.mention_user(), player.bank))
                        else:
                            if not confirm_msg:
                                confirm_msg = await self.send_message(self.channel,
                                                    "Bet must be a positive integer between 100 and 500 memes that is less than the amount"
                                                    " in your bank.\n You ({}) currently have {} memes.".format(
                                                        player.mention_user(), player.bank))
                            else:
                                await self.edit_message(confirm_msg, confirm_msg.content + "\n\n" +
                                                    "Bet must be a positive integer between 100 and 500 memes that is less than the amount"
                                                    " in your bank.\n You ({}) currently have {} memes.".format(
                                                        player.mention_user(), player.bank))


    async def run_round(self):
        start_time = time.clock()
        await self.send_message(self.channel, "The round in commencing. Enter '{}hit' or '{}hold' to play!".format(self.PREFIX, self.PREFIX))
        while time.clock() - start_time < self.PLAYING_TIME:

            def msg_check(msg):
                return msg.content.startswith(self.PREFIX + "hit") or msg.content.startswith(self.PREFIX + "hold")

            play_msg = await self.wait_for_message(timeout=self.PLAYING_TIME, check=msg_check) if \
                self.still_deciding() else None
            if play_msg:
                player = self.get_player(play_msg.author)
                if player:
                    if play_msg.content.startswith(self.PREFIX + "hit"):
                        if player.hit(): #success
                            await self.send_message(self.channel, "{} hit!".format(player.mention_user()))
                        else:
                            await self.send_message(self.channel, "{} can not hit!".format(player.mention_user()))
                    elif play_msg.content.startswith(self.PREFIX + "hold"):
                        if player.hold(): #success
                            await self.send_message(self.channel, "{} held their hand!".format(player.mention_user()))
                        else:
                            await self.send_message(self.channel, "{} cannot hold! They may have already played or "
                                                                  "are not playing this round. ".format(player.mention_user()))
            else:
                break
        end_message = await self.send_message(self.channel, "Either all players played or the time is up! The round is now over. Preparing everyone for post round evaluation.")
        time.sleep(self.MESSAGE_GAP)
        forced_players = self.force_hold()
        if forced_players:
            end_message = await self.edit_message(end_message, end_message.content + "\n\n" + forced_players)
            time.sleep(self.MESSAGE_GAP)
        await self.edit_message(end_message, end_message.content + "\n\n" + "Here comes the new hands!")
        time.sleep(self.MESSAGE_GAP)
        await self.edit_message(end_message, end_message.content + "\n\n" + self.str_players_with_hand())
        time.sleep(self.MESSAGE_GAP)
        eval_message = await self.send_message(self.channel, "Running algorithms to evaluate players based on last round.")
        time.sleep(self.MESSAGE_GAP)
        busted = self.evaluate_players()
        if busted:
            await self.edit_message(eval_message, eval_message.content + "\n\n" + busted)

    async def run_intermission(self):
        start_time = time.clock()
        await self.send_message(self.channel, "Intermission commencing. Type '{}join' to join the table or '{}quit' to leave!"
                                              " All new players start with 5000 memes.".format(self.PREFIX, self.PREFIX))
        confirm_msg = None
        while time.clock() - start_time < self.INTERMISSION_TIME:

            def msg_check(msg):
                return msg.content.startswith(self.PREFIX + "join") or msg.content.startswith(self.PREFIX + "quit")

            join_msg = await self.wait_for_message(timeout=self.INTERMISSION_TIME, check=msg_check) \
                                                                    if time.clock() - start_time < self.INTERMISSION_TIME \
                                                                    else None
            if join_msg:
                if join_msg.content.startswith(self.PREFIX + "join"):
                    if self.get_player(join_msg.author) is None:
                        self.players.append(user.User(join_msg.author))
                        if not confirm_msg:
                            confirm_msg = await self.send_message(self.channel, "{} joined!".format(self.get_player(join_msg.author).mention_user()))
                        else:
                            await self.edit_message(confirm_msg, confirm_msg.content + "\n\n" + "{} joined!".format(self.get_player(join_msg.author).mention_user()))
                        self.load_user(self.get_player(join_msg.author))
                elif join_msg.content.startswith(self.PREFIX + "quit"):
                    player = self.get_player(join_msg.author)
                    if player:
                        self.players.remove(player)
                        if not confirm_msg:
                            confirm_msg = await self.send_message(self.channel, "{} quit!".format(player.mention_user()))
                        else:
                            await self.edit_message(confirm_msg, confirm_msg.content + "\n\n" + "{} quit!".format(player.mention_user()))
                        self.write_user(player)
        self.sqlite_conn.commit()

################################################################################################
######################################## HELPER METHODS ########################################
################################################################################################

    def deal_cards(self):
        """
        Creates a new deck and deals 2 cards to every player, including the dealer.
        """
        card.Card.create_deck()
        self.dealer.deal()
        for player in self.players:
            player.deal()

    def evaluate_players(self):
        #check each player to see if they have busted and update their variables
        message = ""
        for player in self.players:
            if isinstance(player, user.User):
                if player.is_playing and player.is_bust():
                    message += "    " + player.mention_user()
                    player.bust()
        if message:
            return "Busted players:\n\n" + message

    def evaluate_game(self):
        """
        Determines the winners and losers of the game. This method is called at the end of the game to create a str
        representation of the end game statistics and to edit the banks of the players in the game.
        :return: str representing the end game stats
        """
        self.dealer.hit_until_hold()
        message = self.bold_message(self.dealer.final_str_with_hand()+ "\n")
        if self.dealer.has_blackjack():
            message += "The Dealer has Blackjack. All players without blackjack will lose the round.\n\n"
            for player in self.players:
                if not player.has_blackjack():
                    message += "    " + player.mention_user() + " lost " + self.bold_message(str(player.lose_bet())) + " memes\n"
                else:
                    message += "    " + player.mention_user() + " also had blackjack so they gained/lost no memes.\n"
        elif self.dealer.is_bust():
            message += "The Dealer is busted. All players left in the game win.\n\n"
            for player in self.players:
                if player.is_busted or player.is_bust():
                    message += "    " + player.mention_user() + " lost " + self.bold_message(str(player.lose_bet())) + " memes\n"
                else:
                    message += "    " + player.mention_user() + " won " + self.bold_message(str(player.gain_bet())) + " memes\n"
        else:
            # players with a higher point total win, players with a lower point total than dealer lose
            dealer_hand_value = min(i for i in self.dealer.get_hand_values())
            message += "The Dealer has a hand value of {}. All non-busted players above this value win!\n\n".format(dealer_hand_value)
            for player in self.players:
                player_hand_value = min(i for i in player.get_hand_values())
                for value in player.get_hand_values(): # picks the largest value below 21 as the value to use when comparing
                    if 21 >= value > player_hand_value:
                        player_hand_value = value
                if not player.is_bust() and player_hand_value > dealer_hand_value:
                    message += "    " + player.mention_user() + " won " + self.bold_message(str(player.gain_bet())) + " memes\n"
                elif not player.is_bust() and player_hand_value == dealer_hand_value:
                    message += "    " + player.mention_user() + " tied and gained/lost no memes.\n"
                else:
                    message += "    " + player.mention_user() + " lost " + self.bold_message(str(player.lose_bet())) + " memes\n"
        return message

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
        self.dealer.reset()
        for player in self.players:
            player.reset()
            if player.bank <= 500:
                player.set_bank(1000)

    def force_hold(self):
        """
        Forces players who did not input a command for the round to hold.
        :return: str stating the players that did not respond
        """
        names = ""
        for player in self.players:
            if isinstance(player, user.User):
                if not player.has_played:
                    player.hold()
                    names += player.mention_user() + ","
        if names:
            return "Forced {} to hold because they took too long to decide last round.".format(names)

    def force_bet(self):
        names = ""
        for player in self.players:
            if player.current_bet == 0:
                player.bet(100)
                names += player.mention_user() + ","
        if names:
            return "Forced {} to bet because they took too long to bet.".format(names)

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

    def str_players_with_hand(self):
        """
        Creates a str of all the players in the session with their hands.
        This does not send a message.
        :return: str of players with their hands
        """
        message = "Players and their hands\n\n" + self.bold_message(self.dealer.str_with_hand()) + "\n"
        for player in self.players:
            if isinstance(player, user.User):
                message += player.str_with_hand() + "\n"
        return message

    async def print_players_with_bet(self):
        bet_msg = await self.send_message(self.channel, "Here comes everyone's bets for the round!")
        time.sleep(self.MESSAGE_GAP)
        message = "Players and their bets\n\n"
        for player in self.players:
            if isinstance(player, user.User):
                message += player.str_with_bet() + "\n"
        await self.edit_message(bet_msg, bet_msg.content + "\n\n" + message)

    async def print_players_with_bank(self):
        message = "Players and their banks\n\n"
        for player in self.players:
            if isinstance(player, user.User):
                message += player.str_with_bank() + "\n"
        await  self.send_message(self.channel, message)

###############################################################################################
###################################### DATABASE METHODS #######################################
###############################################################################################

    def write_user(self, _user):
        """
        Updates the user's bank value to it's current value
        :param _user: 'User' class object to update bank value of
        """
        try:
            self.conn_cursor.execute("INSERT INTO users (id,bank) VALUES (?, ?)", (_user.id, _user.bank))
        except sqlite3.IntegrityError:
            pass
        self.conn_cursor.execute("UPDATE users SET bank=? WHERE id=?", (_user.bank, _user.id ))

    def load_user(self, _user):
        """
        If the user is in the database, loads the bank value from the database as the user's current bank
        :param _user: 'User' class object to update bank value of
        """
        self.conn_cursor.execute("SELECT bank FROM users WHERE id=?", (_user.id,))
        data = self.conn_cursor.fetchone()
        if data:
            _user.set_bank(int(data[0]))

    @staticmethod
    def bold_message(message):
        return "**{}**".format(message)

    async def shutdown(self):
        await self.send_message(self.channel, "Bye!")
        await self.logout()

token_file = open("token.txt", "r")
token = token_file.readline().strip()
token_file.close()

client = BlackJackBot()
client.run(token)