from datetime import datetime
import json
import random
import re
import os
from os import path, getenv

from discord import channel, mentions, message
from discord.ext import commands, tasks
from discord.flags import Intents
from discord.utils import get


bot = commands.Bot(command_prefix='!', case_insensitive=True,
                   intents=Intents.all())
bot.data = {}

cwd = os.getcwd()

@tasks.loop(minutes=5)
async def getMemberCount():
    await bot.wait_until_ready()
    guild = bot.get_guild(449518189072744449)
    count = 0
    for member in guild.members:
        if member.bot:
            continue
        else:
            count += 1
    bot.data['member_count'] = count
    channel = bot.get_channel(795858976310558740)  # channel ID goes here
    msg = f'Member Count: {str(count)}'
    if (channel.name == msg):
        return
    await channel.edit(timeout=5, name=msg)
    print(msg)


@tasks.loop(minutes=1)
async def saveData():
    f = open(f'{cwd}\\save.json', 'w')
    json.dump(bot.data, f, indent=2)
    f.close()


def loadSaveData():
    f = open(f'{cwd}\\save.json', 'r')
    bot.data = json.load(f)
    f.close()


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} ID: {bot.user.id}')
    loadSaveData()
    saveData.start()
    getMemberCount.start()

open_responses = []


@bot.event
async def on_member_join(member):
    print(f'{member.name}, has joined the server. Sending welcome message.')
    channel = bot.get_channel(463278430218354688)
    await channel.send(random.choice(bot.data['welcome_responses']).format(member.mention))
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

Things may be a bit slow but stick around and see what The Lost Freighter will become! 💖''')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.guild is None and message.author != bot.user:
        if re.sub('[^A-Za-z0-9]+', '', message.content) == 'ihaveanidea':
            await message.add_reaction('👍')
            await message.channel.send('ree')
        print(f'DM command not found! ''{message.content}'' from user {message.author.name}!')


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    for msg in open_responses:
        if msg['msg'].id == reaction.message.id and msg['user'] == user:
            if reaction.emoji == '✅':
                await user.remove_roles(msg['role'])
                channel = reaction.message.channel
                await channel.send(f'The role is removed {user.mention}.')
                open_responses.remove(msg)


async def awaiting_user_response(ctx):
    for msg in open_responses:
        if msg['user'] == ctx.author:
            await ctx.channel.send(f'{ctx.message.author.mention}, please respond first before issuing another command.')
            return 1
        return 0


@bot.command()
async def letmein(ctx):
    if await awaiting_user_response(ctx):
        return
    role = get(ctx.guild.roles, name='Insider')
    if role in ctx.author.roles:
        msg = await ctx.send(f'{ctx.message.author.mention}.. You already have the {role.name} role. Would you like me to remove it?')
        await msg.add_reaction('✅')
        response_msg = {'msg': msg, 'user': ctx.author,
                        'role': role, 'expires': 60}
        open_responses.append(response_msg)
    else:
        await ctx.author.add_roles(role)
        channel = get(ctx.guild.channels, name='updates')
        await ctx.channel.send(f'I just got you signed up to recieve notifications from {channel.mention}! Thank you for your interest in this hack!')


@bot.command()
async def artislove(ctx):
    if await awaiting_user_response(ctx):
        return
    role = get(ctx.guild.roles, name='Art')
    if role in ctx.author.roles:
        msg = await ctx.send(f'{ctx.message.author.mention}.. You already have the {role.name} role. Would you like me to remove it?')
        await msg.add_reaction('✅')
        response_msg = {'msg': msg, 'user': ctx.author,
                        'role': role, 'expires': 60}
        open_responses.append(response_msg)
    else:
        await ctx.author.add_roles(role)
        channel = get(ctx.guild.channels, name='art-sharing')
        await ctx.channel.send(f'Oooo! You like to draw {ctx.message.author.mention}? You can now upload your work in {channel.mention}!')

bot.run(getenv('DISCORD_TOKEN'))
