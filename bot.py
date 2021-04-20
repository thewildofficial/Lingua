import discord
from discord.ext import commands
from decouple import config
import randfacts
from discord.ext.commands import MinimalHelpCommand, DefaultHelpCommand

from datetime import datetime
import os


class BotInformation:
    #all the information used by the Cogs to be stored here
    CAC_channel = int(config('info_channel'))
    prefix = "%"
    embed_color = 0x03fc6f
    bot_token = config('bot_token')
    firebase_credentials = config('firebase_credentials')
    version = "0.2"


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=[BotInformation.prefix], intent=intents, help_command=DefaultHelpCommand())
# Loads extensions at start
for filename in os.listdir("extensions"):
    if filename.endswith(".py"):
        extname = f"extensions.{filename[:-3]}"
        client.load_extension(extname)
        print(f" * '{extname}'  has been loaded")

#starting
@client.event
async def on_ready():
    print(
        f'\n * Logged in as {client.user.name}#{client.user.discriminator} \n * Time: {datetime.now()}')

    await client.change_presence(
        activity=discord.Game(name=f'Did you know that {randfacts.getFact().lower()}'), #gets a cool,interesting fact
        status=discord.Status.dnd
    )

    print(f"\n  {client.user} is online and fully functional!")

# hosting.py
client.run(BotInformation.bot_token)
