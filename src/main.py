# TODO: Add logger
# TODO: Add args with parameters
import os

import discord
from dotenv import load_dotenv
from utils.reddit import Reddit
from utils.weather import Weather
from utils.additionnal_main_functions import *

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
    if bot_alias + "meteo" in message_lower:
        ret_message = weather.weatherEmbed(message_lower.split()[2])
        if isinstance(ret_message, discord.Embed):
            await message.channel.send(embed=ret_message)
        else:
            await message.channel.send(str(ret_message))

    if bot_alias + "reddit" in message.content.lower():
        list_news = message.content.lower().split(" ")[2:]

        ret_message = reddit.get_news(list_news)
        if isinstance(ret_message, discord.Embed):
            await message.channel.send(embed=ret_message)
        else:
            await message.channel.send(str(ret_message))

    #check if an image is sent
    image_np, image_is_sent = get_image_from_channel_to_predict(message)
    if image_is_sent:
        print("image is sent")
        type_image, certitude = predict_type_image(image_np)
        await message.channel.send(type_image + " (" + str(certitude*100)[:6] + " %)")
        # resend the image in the proper channel
        # if a cat's image is sent to dogs channel
        if message.channel.name == "chien" and type_image == categorie[0]: # categorie[0] = "Chat"
            await message.channel.send("This image will be redirected to the proper channel")
            image_extension = download_image_from_channel(message)
            for channel in client.get_all_channels():
                if channel.name == "chat":
                    print("canal chat détecté")
                    await channel.send(file=discord.File('image_downloaded_by_bot' + image_extension))
                    await channel.send("[REDIRECTED IMAGE] sent by: " + str(message.author))
                    break
        # if a dog's image is sent to cats channel
        elif message.channel.name == "chat" and type_image == categorie[1]: # categorie[1] = "Chien"
            await message.channel.send("This image will be redirected to the proper channel")
            image_extension = download_image_from_channel(message)
            for channel in client.get_all_channels():
                if channel.name == "chien":
                    print("canal chien détecté")
                    await channel.send(file=discord.File('image_downloaded_by_bot' + image_extension))
                    await channel.send("[REDIRECTED IMAGE] sent by: " + str(message.author))
                    break


client.run(TOKEN)


