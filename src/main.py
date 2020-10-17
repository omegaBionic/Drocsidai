import os

import discord
# openweathermap
from dotenv import load_dotenv

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
    if message.author == client.user:
        return
    if 'test' in message.content.lower():
        await message.channel.send("One message")
        print("BOT: message sent")



client.run(TOKEN)

# # bot.py
# import os
#
# import discord
# from dotenv import load_dotenv
#
# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
#
# client = discord.Client()
#
# @client.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')
#
# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )
#
# client.run(TOKEN)