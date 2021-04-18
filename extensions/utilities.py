import discord
from discord.ext import commands
from bot import BotInformation
import traceback

class GeneralCommands(commands.Cog):
    #initialize client class
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        ''' - 🔍 displays general information about the bot'''
        embed = discord.Embed(
            description="Lingua is a Spaced repetition revision and language learning bot that aids your learning journey.",
            color=BotInformation.embed_color)
        embed.set_author(name="Lingua ", url="https://github.com/thewildofficial/Lingua/tree/main",
                         icon_url=self.client.user.avatar_url)
        embed.add_field(name="Support server", value="https://discord.gg/Wa5wTgcF", inline=True)
        embed.add_field(name="Version", value=BotInformation.version, inline=True)
        embed.add_field(name="Github", value="https://github.com/thewildofficial/Lingua/tree/main", inline=True)
        embed.add_field(name="Invite Link",
                        value="https://discord.com/api/oauth2/authorize?client_id=828907102063558656&permissions=0&scope=bot",
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
        '''- 💌 send some feedback or suggestion!
        '''
        try:
            await self.client.get_channel(BotInformation.CAC_channel).send(f"`{ctx.author}` sent the following feedback: \n ```{suggestion}```")
            await ctx.send("✅ thank you for your feedback! we will review it as soon as possible.")
        except Exception:
            traceback.print_exc()
            await ctx.send("😔 uh oh.. something went wrong,please try again later.")



def setup(client):
    client.add_cog(GeneralCommands(client))


