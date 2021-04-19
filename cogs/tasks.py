import discord
import random
from discord.ext import commands, tasks
from discord.ext.commands.errors import BadArgument
from utils.config import saveconfig

class Tasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.old_config = bot.config
        print(f'Cog "Tasks" loaded!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member.name}, has joined the server. Sending welcome message.')
        channel = self.bot.get_channel(463278430218354688)
        await channel.send(random.choice(self.bot.config['welcome_responses']).format(member.mention))
        dm = await member.create_dm()
        await dm.send(f'''
    Hey {member.name}!
    Just wanted to personally welcome you to **The Lost Freighter**!

    Please make sure to look at the ``read-me`` channel to get 
    acquainted with the rules around here! You can get better 
    chat permissions check out the ``role-info`` channel to find
    out how to receive them!

    Know others who may be interested in this mod? You can shoot 
    them this link here: https://discord.gg/8uuaU2zTBy

    Things may be a bit slow but stick around and see what The Lost Freighter will become!''')

    @tasks.loop(minutes=5)
    async def getMemberCount(self):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(449518189072744449)
        count = 0
        for member in guild.members:
            if member.bot:
                continue
            else:
                count += 1
        self.bot.config["member_count"] = count
        channel = self.bot.get_channel(795858976310558740)  # channel ID goes here
        msg = f"Member Count: {str(count)}"
        if channel.name == msg:
            return
        await channel.edit(timeout=5, name=msg)
        print(msg)
        
    @tasks.loop(minutes=10)
    async def auto_save_config(self):
        if self.bot.config == self.old_config:
            print("old config!")
            return
        else:
            saveconfig(self.bot.config)
            self.old_config = self.bot.config
            print("new config!")
            
def setup(bot):
    cog = Tasks(bot)
    bot.add_cog(cog)
    cog.getMemberCount.start()
    cog.auto_save_config.start()