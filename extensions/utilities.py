from discord.ext import commands
import bot

class GeneralCommands(commands.Cog):
    #initialize client class
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        #returns the prefix
        mention = f'<@!{self.client.user.id}>'
        if mention in message.content and message.author.id != self.client.user.id:
            await message.channel.send(f'Current command for {mention} is `{bot.BotInformation.prefix}`')
    

def setup(client):
    client.add_cog(GeneralCommands(client))