import os

import discord
from dotenv import load_dotenv
from src.weather import getWeather

bot_alias = ".b "
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

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
    message_lower = message.content.lower()
    if message.author == client.user:
        return
    if 'test' in message_lower:
        await message.channel.send("One message")
        print("BOT: message sent")
    elif bot_alias + "/meteo" in message_lower:
        await message.channel.send(getWeather(message_lower.split()[2]))

client.run(TOKEN)

