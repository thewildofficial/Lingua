import discord
from discord.ext import commands

class FileGUI(commands.Cog):
    #initialize client class
    def __init__(self, client):
        self.client = client

    # list of reactions
    reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","➡️","⬅️"]
    subjects = []
    chapters = []

    @commands.command()
    async def view(self, ctx):
        reactions = self.reactions #gets all applicable reactions
        filewalker = discord.Embed(title="file structure",
                                   description="select a number to go to a particular directory,and ➡️ and ⬅️ to navigate pages!",
                                   color=0x38cc93)
        filewalker.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        FW_message = await ctx.send(embed=filewalker)
        for reaction in reactions:
            await FW_message.add_reaction(reaction)


def setup(client):
    client.add_cog(FileGUI(client))