# Thirteen-Bot 🤖
An online multiplayer version of the card game Thirteen playable via a Discord Bot. 

## Commands

* Type 'join' to join the game
* Type 'start' to start the game
* Type 'quit' to quit the game (you cannot rejoin a game until it has finished)

* Type 'join!' followed by an emoji of your choice to join the game with an emoji identifier

These operations can be performed in the general channel or your DMs.

## Gameplay
After the game has been started, the bot will open a DM channel for all of the players and message you your hand. From this point forwards, the game is played by interacting with the Bot in your DMs.

* When it is your turn, play cards from your hand by typing the card(s) you want to play into the chat e.g. if you want to play the Three of Spades type '3s'. 
* If you want to play multiple cards, add a comma between the cards e.g. '3s,3c'. 
* If you cannot play a card, type 'pass'.

Note: all commands can be be typed in upper/lowercase.

<img width="619" alt="Screenshot 2022-10-20 at 09 48 50" src="https://user-images.githubusercontent.com/102842055/196980470-96f550b6-d2aa-448a-9a02-ac652352b858.png">

The rules for Thirteen can be found here:
https://cardgames.io/thirteen/

## Before Running
To use the Discord Bot, a new Discord server needs to be created.

* Before running the program, a Discord Bot token needs to be added. These can be accessed by registering the bot in the Discord Developer Portal (See link below).
* The channel id of the general channel also needs to be found, the included get_general_channel_id.py can find the id of the channel when you type something in the chat. 

Information on how to get the required Discord Bot Token can be found here: https://realpython.com/how-to-make-a-discord-bot-python/
