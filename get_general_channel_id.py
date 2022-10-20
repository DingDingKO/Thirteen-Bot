# Type something in the 'general' channel of the server to get its id
import discord

TOKEN = "*******************************************************"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.channel.id)


if __name__ == '__main__':
    client.run(TOKEN)
