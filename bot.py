import discord
from discord.ext import commands
from decouple import config
from discord.ext.commands.core import command

from datetime import datetime
import os
#hosting we are using for the bot
import hosting

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=["*"], intent=intents)

# Loads extensions at start
for filename in os.listdir("extensions"):
    if filename.endswith(".py"):
        try:
            extname = f"extensions.{filename[:-3]}"
            client.load_extension(extname)
            print(f" * '{extname}'  has been loaded")
        except Exception as e:
            print(e)

#starting
@client.event
async def on_ready():
    print(
        f'\n * Logged in as {client.user.name}#{client.user.discriminator} \n * Time: {datetime.now()}')

    await client.change_presence(
        activity=discord.Game(name='remembering to remind!'),
        status=discord.Status.dnd
    )

    print(f"\n  {client.user} is online and fully functional!")

# hosting.py
client.run(config('token'))
