import os
from datetime import datetime

import discord
from discord.ext import commands
from decouple import config

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix='*',
    case_insensitive=True,
    intents=intents
)

#removed default help command as it is very ugly.
client.remove_command('help')

# Load all Extensions

def loadCogs():
    for filename in os.listdir("Extensions"):
        if filename.endswith(".py"):
            try:
                extname = f"extensions.{filename[:-3]}"
                client.load_extension(extname)
                print(f" * '{extname}'  has been loaded")
            except Exception as e:
                print(e)

# Ready Message

@client.event
async def on_ready():
    print(
        f'\n * Logged in as {client.user.name}#{client.user.discriminator} \n * Time: {datetime.now()}')

    await client.change_presence(
        activity=discord.Game(name=''), #come up with a cool status over here
        status=discord.Status.dnd
    )
    loadCogs()
    print("\n   LinguaRep is online and fully functional!")

client.run(config('token'))
