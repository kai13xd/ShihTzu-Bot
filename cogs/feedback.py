from utils.config import saveconfig
import discord
import random
import re
from discord.ext import commands, tasks
from discord.ext.commands.errors import BadArgument

class Feedback(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		print(f'Cog "Feedback" loaded!')
		 
	@commands.Cog.listener()
	async def on_message(self,message):
		await self.bot.process_commands(message)
		if message.guild is None and message.author != self.bot.user:
			if re.sub('[^A-Za-z0-9]+', '', message.content) == 'ihaveanidea':
				await message.add_reaction('👍')
				await message.channel.send('ree')
			print(
				f'DM command not found! ''{message.content}'' from user {message.author.name}!')

def setup(bot):
	bot.add_cog(Feedback(bot))