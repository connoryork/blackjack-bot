# blackjack-bot
### About
blackjack-bot is a simple blackjack simulator that allows a discord server to host a blackjack
game in chat. blackjack-bot is written in [Python](https://www.python.org "Python homepage").

It is able to play a basic version of Blackjack, which means that it does not support the
splitting of one's hand, insurance, surrendering, or double downing.

blackjack-bot can be played alone or with friends. There is a time limit to prevent the game from
freezing if a player does not respond in chat. The bot sends a lot of messages regarding status
in the game and may need it's own text channel to prevent the overload of messages
in a servers primary chat.

### Setup
blackjack-bot is checked as a "Public Bot", which means that anyone can add it to their server,
but I am not sure how to do that. If you know, please tell.

1. Install [Python](https://www.python.org/downloads/ "Download Python"). Make sure you install the latest version (should be version 3.x.x).
Make sure you install Python 3, NOT Python 2. When installing Python, make sure to check the checkbox to add
`python` and associated keywords to your computers environment variables. IF you are having trouble,
there are some good guides online on how to do this.
1. Create a [new bot account](https://twentysix26.github.io/Red-Docs/red_guide_bot_accounts/#creating-a-new-bot-account
"Guide to creating a new bot account")
2. Create a .txt file named `token.txt` in the same directory as the blackjack-bot files.
3. Place the token into the first line of `token.txt`. This is important for logging into your bot.
3. Add your bot to a server by adding your bot's client ID after `client_id=` in the link here.
https://discordapp.com/oauth2/authorize?&client_id=&scope=bot&permissions=0
4. Start your bot running the command prompt (or PowerShell) and typing `python bot.py` while in the
blackjack-bot project directory (This can also be done in an IDE such as PyCharm).

### How to play
After successfully setting up the bot, type `$blackjack` to start a session. Instructions to
play are in messages sent by the bot while playing.

### Mentions
* [Python](https://www.python.org "Python homepage") - language is was written in
* [Discord](https://discordapp.com/ "Discord homepage") - text and voice client for game to take place
* [discord.py](https://github.com/Rapptz/discord.py "discord Python API") - Python API wrapper for Discord written by
Rapptz

### TODO
* Instead of printing the names of cards when printing player's hands, send an image of their hand.
This would need to be small enough not to obstruct the chat and the format of the message (I wish
there were card emojis or something like that).
* Add splitting, insurance, surrendering, etc. This is honestly the least of my worries and
probably will not happen.

