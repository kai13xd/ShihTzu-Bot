import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from discord.ext.commands.errors import BadArgument


class Roles(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.open_responses = []
		

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if user == self.bot.user:
			return
		for msg in self.open_responses:
			if msg["msg"].id == reaction.message.id and msg["user"] == user:
				if reaction.emoji == "✅":
					await user.remove_roles(msg["role"])
					channel = reaction.message.channel
					await channel.send(f"The role is removed {user.mention}.")
					self.open_responses.remove(msg)

	async def awaiting_user_response(self, ctx):
		for msg in self.open_responses:
			if msg["user"] == ctx.author:
				await ctx.channel.send(
					f"{ctx.message.author.mention}, please respond first before issuing another command."
				)
				return 1
			return 0

	@commands.command()
	async def letmein(self, ctx):
		def react_cond(m):
			if m.message_id == msg.id and m.user_id == ctx.author.id and str(m.emoji) == "✅":
				return True
			return False   
		role = get(ctx.guild.roles, name="Insider")
		if role in ctx.author.roles:
			try:
				msg = await ctx.send(f"{ctx.message.author.mention}.. You already have the {role.name} role. Would you like me to remove it?")
				await msg.add_reaction("✅")
				await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=react_cond)
			except asyncio.TimeoutError:
				await msg.delete()
				await ctx.send("Cool! So it seems you'll keep the role after all.")
			except discord.Forbidden:
				await ctx.msg('I am supposed to have reaction permissions to remove commands. Blame Kai for screwing this up.')
		else:
			await ctx.author.add_roles(role)
			channel = get(ctx.guild.channels, name="updates")
			await ctx.channel.send(
				f"I just got you signed up to recieve notifications from {channel.mention}! Thank you for your interest in this hack!"
			)

	@commands.command()
	async def artislove(self, ctx):
		def react_cond(m):
			if m.message_id == msg.id and m.user_id == ctx.author.id and str(m.emoji) == "✅":
				return True
			return False            
		role = get(ctx.guild.roles, name="Art")
		if role in ctx.author.roles:
			try:
				msg = await ctx.send(f"{ctx.message.author.mention}.. You already have the {role.name} role. Would you like me to remove it?")
				await msg.add_reaction("✅")
				await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=react_cond)
			except asyncio.TimeoutError:
				await msg.delete()
				await ctx.send("Cool! So it seems you'll keep the role after all.")
			except discord.Forbidden:
				await ctx.msg('I am supposed to have reaction permissions to remove commands. Blame Kai for screwing this up.')
		else:
			await ctx.author.add_roles(role)
			channel = get(ctx.guild.channels, name="art-sharing")
			await ctx.channel.send(
				f"Oooo! You like to draw {ctx.message.author.mention}? You can now upload your work in {channel.mention}!"
			)


def setup(bot):
	bot.add_cog(Roles(bot))
	print(f'Cog "Roles" loaded!')