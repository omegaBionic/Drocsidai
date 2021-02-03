# TODO: Add logger
# TODO: Add args with parameters
import os

import cv2
import discord
from dotenv import load_dotenv
from utils.reddit import Reddit
from utils.weather import Weather
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
import numpy as np

bot_alias = ".b "
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
reddit = Reddit()
client = discord.Client()
weather = Weather()


# get an image as np.array when a user sends one and prepare it for the NN
def get_image_from_channel(message):
    image_is_sent = False

    IMAGE_WIDTH = 128
    IMAGE_HEIGHT = 128
    IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)

    # to check if the message is an image .jpg, png or jpeg
    pic_ext = ['.jpg', '.png', '.jpeg']
    # check if there is an attachment
    if message.attachments:
        for ext in pic_ext:
            if message.attachments[0].filename.endswith(ext):
                image_is_sent = True
                url = message.attachments[0].url
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                # img_np contains img as an np.array
                img_np = np.array(img)
                #prepare it for the NN
                img_np = cv2.resize(img_np, IMAGE_SIZE)
    if not image_is_sent:
        img_np = np.zeros(1, dtype='int')
    return img_np, image_is_sent




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
    image_np, image_is_sent = get_image_from_channel(message)
    if image_is_sent:
        print("image is sent")
        plt.imshow(image_np)
        plt.show()
        '''
            add instructions
        '''


client.run(TOKEN)


