# TODO: Add logger
# TODO: Add args with parameters
import os

import discord
from dotenv import load_dotenv
from utils.reddit import Reddit
from utils.weather import Weather

bot_alias = ".b "
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
reddit = Reddit()
client = discord.Client()
weather = Weather()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if bot_alias + "youssef" in message.content.lower():
        await message.channel.send('Hi Youssef! 🎈🎉🎉🎉🎉🎉')

    message_lower = message.content.lower()
    if bot_alias + "/meteo" in message_lower:  # TODO: Remove '/'
        ret_message = weather.weatherEmbed(message_lower.split()[2])
        if isinstance(ret_message, discord.Embed):
            await message.channel.send(embed=ret_message)
        else:
            await message.channel.send(str(ret_message))

    if bot_alias + "reddit" in message.content.lower():  # TODO: Add reddit in utils
        list_news = message.content.lower().split(" ")[2:]

        ret_message = reddit.get_news(list_news)
        if isinstance(ret_message, discord.Embed):
            await message.channel.send(embed=ret_message)
        else:
            await message.channel.send(str(ret_message))


client.run(TOKEN)

