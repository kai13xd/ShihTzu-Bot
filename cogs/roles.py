import discord
from discord.ext import commands
from discord.ext.commands.errors import BadArgument

class Roles(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.open_responses = []
		print(f'Cog "Roles" loaded!')
  

         
	@commands.Cog.listener()
	async def on_reaction_add(self,reaction, user):
		if user == self.bot.user:
			return
		for msg in self.open_responses:
			if msg['msg'].id == reaction.message.id and msg['user'] == user:
				if reaction.emoji == '✅':
					await user.remove_roles(msg['role'])
					channel = reaction.message.channel
					await channel.send(f'The role is removed {user.mention}.')
					self.open_responses.remove(msg)


	async def awaiting_user_response(self,ctx):
		for msg in self.open_responses:
			if msg['user'] == ctx.author:
				await ctx.channel.send(f'{ctx.message.author.mention}, please respond first before issuing another command.')
				return 1
			return 0
	 
	@commands.command()
	async def letmein(self,ctx):
		if await self.awaiting_user_response(ctx):
			return
		role = self.get(ctx.guild.roles, name='Insider')
		if role in ctx.author.roles:
			msg = await ctx.send(f'{ctx.message.author.mention}.. You already have the {role.name} role. Would you like me to remove it?')
			await msg.add_reaction('✅')
			response_msg = {'msg': msg, 'user': ctx.author,
							'role': role, 'expires': 60}
			self.open_responses.append(response_msg)
		else:
			await ctx.author.add_roles(role)
			channel = self.get(ctx.guild.channels, name='updates')
			await ctx.channel.send(f'I just got you signed up to recieve notifications from {channel.mention}! Thank you for your interest in this hack!')


	@commands.command()
	async def artislove(self,ctx):
		if await self.awaiting_user_response(ctx):
			return
		role = self.get(ctx.guild.roles, name='Art')
		if role in ctx.author.roles:
			msg = await ctx.send(f'{ctx.message.author.mention}.. You already have the {role.name} role. Would you like me to remove it?')
			await msg.add_reaction('✅')
			response_msg = {'msg': msg, 'user': ctx.author,
							'role': role, 'expires': 60}
			self.open_responses.append(response_msg)
		else:
			await ctx.author.add_roles(role)
			channel = self.get(ctx.guild.channels, name='art-sharing')
			await ctx.channel.send(f'Oooo! You like to draw {ctx.message.author.mention}? You can now upload your work in {channel.mention}!')

def setup(bot):
    bot.add_cog(Roles(bot))