import discord
from discord.ext import commands
import randfacts

from datetime import datetime
import os

from config import Configurations


class EmbedHelpCommand(commands.MinimalHelpCommand):
    """builds embed for help command"""

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page,color=BotInformation.embed_color)
            await destination.send(embed=embed)


class BotInformation:
    # all the information used by the Cogs to be stored here
    bot_token = Configurations.bot_token
    CAC_channel = Configurations.info_channel
    prefix = "%"
    embed_color = 0x03fc6f
    firebase_credentials = Configurations.firebase_credentials
    bot_version = ""  # gets updated on_bot_run
    github = "https://github.com/thewildofficial/Lingua/tree/main"
    server = "https://discord.gg/Wa5wTgcF"
    invite_link = "https://discord.com/api/oauth2/authorize?client_id=828907102063558656&permissions=0&scope=bot"

intents = discord.Intents.default()
client = commands.Bot(command_prefix=[BotInformation.prefix], intent=intents, help_command=EmbedHelpCommand())
intents.members = True
for filename in os.listdir("extensions"):
        if filename.endswith(".py"):
            try:
                extname = f"extensions.{filename[:-3]}"
                client.load_extension(extname)
                print(f" * '{extname}'  has been loaded")
            except Exception as e: print(e)

# starting
@client.event
async def on_ready():
    BotInformation.bot_version = f"v{len(client.commands) / 10}"
    print(
        f'\n * Logged in as {client.user.name}#{client.user.discriminator} \n * Time: {datetime.now()}')
    await client.change_presence(
        activity=discord.Game(name=f'Did you know that {randfacts.getFact().lower()}'),  # gets a cool,interesting fact
        status=discord.Status.dnd
    )
    print(f"\n  {client.user} is online and fully functional!")


client.run(Configurations.bot_token)
