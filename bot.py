import discord
from discord.ext import commands
from decouple import config
import randfacts
from discord.ext.commands import DefaultHelpCommand

from datetime import datetime
import os


class EmbedHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page)
            await destination.send(embed=embed)


class BotInformation:
    # all the information used by the Cogs to be stored here
    CAC_channel = int(config('info_channel'))
    prefix = "%"
    embed_color = 0x03fc6f
    bot_token = config('bot_token')
    firebase_credentials = config('firebase_credentials')
    bot_version = ""
    github = "https://github.com/thewildofficial/Lingua/tree/main"
    server = "https://discord.gg/Wa5wTgcF"
    invite_link = "https://discord.com/api/oauth2/authorize?client_id=828907102063558656&permissions=0&scope=bot"


intents = discord.Intents.default()
client = commands.Bot(command_prefix=[BotInformation.prefix], intent=intents, help_command=EmbedHelpCommand())
intents.members = True


def get_extensions():
    ncogs = 0
    # Loads extensions at start
    for filename in os.listdir("extensions"):
        ncogs += 1
        if filename.endswith(".py"):
            extname = f"extensions.{filename[:-3]}"
            client.load_extension(extname)
            print(f" * '{extname}'  has been loaded")
    return ncogs


# starting
@client.event
async def on_ready():
    print(
        f'\n * Logged in as {client.user.name}#{client.user.discriminator} \n * Time: {datetime.now()}')
    await client.change_presence(
        activity=discord.Game(name=f'Did you know that {randfacts.getFact().lower()}'),  # gets a cool,interesting fact
        status=discord.Status.dnd
    )

    print(f"\n  {client.user} is online and fully functional!")


# changes bot_version ad hoc
BotInformation.bot_version = f"{get_extensions() / 10}"
# hosting.py
client.run(BotInformation.bot_token)
