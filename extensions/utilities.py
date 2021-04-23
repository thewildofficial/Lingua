import discord
from discord.ext import commands
from bot import BotInformation

class General(commands.Cog):
    """General utility commands"""
    #initialize client class
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        """ 🔍 displays general information about the bot"""
        embed = discord.Embed(
            description="Lingua is a Spaced repetition revision and language learning bot that aids your learning "
                        "journey.",
            color=BotInformation.embed_color)
        embed.set_author(name=self.client.user, url=BotInformation.github,
                         icon_url=self.client.user.avatar_url)
        embed.add_field(name="Support server", value=BotInformation.server, inline=True)
        embed.add_field(name="Version", value=BotInformation.bot_version, inline=True)
        embed.add_field(name="Github", value=BotInformation.github, inline=True)
        embed.add_field(name="Invite Link",
                        value=BotInformation.invite_link,
                        inline=True)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        #returns the prefix
        mention = f'<@!{self.client.user.id}>'
        if mention in message.content and message.author.id != self.client.user.id:
            await message.channel.send(f'Current command for {mention} is `{BotInformation.prefix}`')

    @commands.command()
    async def feedback(self,ctx,*,suggestion):

        """ 💌 send some feedback or suggestion!"""
        try:
            await self.client.get_channel(BotInformation.CAC_channel).send(f"`{ctx.author}` sent the following feedback: \n ```{suggestion}```")
            await ctx.send("✅ thank you for your feedback! we will review it as soon as possible.")
        except Exception as e:
            await ctx.send(f"😔 uh oh.. something went wrong,please try again later")


def setup(client):
    client.add_cog(General(client))


