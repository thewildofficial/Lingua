import discord
from discord.ext import commands
from discord.ext.commands import is_owner
from disputils import BotMultipleChoice, BotConfirmation

from bot import BotInformation
from firestorewrapper import FirebaseAPI


class SRS(commands.Cog):
    # initialize client class
    def __init__(self, client):
        self.client = client
        self.db = FirebaseAPI()

    @commands.command()
    async def deleteall(self, ctx):
        """🗑 deletes everything from your user database
        **WARNING**:   THIS CANNOT BE REVERSED!"""
        confirmation = BotConfirmation(ctx, BotInformation.embed_color)
        await confirmation.confirm("by confirming this,we will delete all information (chapters,subjects and dates) "
                                   "from your user database, which is IRREVERSIBLE."
                                   " \n are you sure you want to proceed?")
        if confirmation.confirmed:
            try:
                self.db.delete_user(ctx.author)
                await confirmation.update("Deleted!")
            except:
                await confirmation.update("😭 Something went wrong,please try again later.")
        else:
            await confirmation.update("Aborted.")

    @commands.command()
    async def add(self, ctx, subject=None, chapter=None, date=None):
        if subject is None:
            await ctx.send(f"😪 syntax is `{BotInformation.prefix}add <subject> <chapter> <date>` where chapter and "
                           f"date are optional \n (note: to be safe,you should encompass the parameters with quotes!)")
            return

    @commands.command()
    async def view(self, ctx):
        """📖 Shows a list of your subjects in an embed."""
        loading_embed = await ctx.send(embed=discord.Embed(title="🏃🏻‍♂️ Loading...",
                                                           description="please wait while our database processes your request.",
                                                           color=BotInformation.embed_color))
        user_info = self.db.read_user(ctx.author, "user")
        if len(user_info[u"Subjects"]) == 0:
            embed = discord.Embed(title="😐 Uh oh..",
                                  description=f"it appears that you havent added any subjects yet. Try adding one with the add command!",
                                  color=BotInformation.embed_color)
            await loading_embed.edit(embed=embed)
            return

        async def builder():
            subject_view = BotMultipleChoice(ctx,
                                             user_info[u"Subjects"],
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

        await loading_embed.delete()
        await builder()


def setup(client):
    client.add_cog(SRS(client))
