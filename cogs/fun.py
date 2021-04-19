import discord
from discord.ext import commands
from discord.ext.commands.errors import BadArgument

class Fun(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		
		
def setup(bot):
	bot.add_cog(Fun(bot))
	print(f'Cog "Fun" loaded!')