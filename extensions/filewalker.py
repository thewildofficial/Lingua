import discord
from discord.ext import commands
from disputils import BotMultipleChoice

from bot import BotInformation
from firestorewrapper import FirebaseAPI


class SRS(commands.Cog):
    # initialize client class
    def __init__(self, client):
        self.client = client
        self.db = FirebaseAPI()

    @commands.command()
    async def view(self, ctx):
        """- 📖 Shows a list of your subjects in an embed."""

        async def builder():
            subject_view = BotMultipleChoice(ctx,
                                             ["subject view"],
                                             f"{ctx.author}'s Subject View",
                                             color=BotInformation.embed_color)
            await subject_view.run()
            if subject_view.choice is not None:
                # uses embed.choice to get subject list + the Dates related to each subject
                choice = subject_view.choice
                await subject_view.quit()
                # quits previous MultipleChoice object and creates a new embed
                chapter_view = discord.Embed(title=f"{choice} chapters", color=BotInformation.embed_color)
                chapter_view.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                chapter_view_message = await ctx.send(embed=chapter_view)
                await chapter_view_message.add_reaction("⬅️")
                if (await self.client.wait_for("reaction_add",
                                               check=lambda reaction, user: user == ctx.author and str(
                                                   reaction.emoji) == "⬅️")):
                    await chapter_view_message.delete()
                    await builder()

            else:
                await subject_view.quit()

        await builder()


def setup(client):
    client.add_cog(SRS(client))
