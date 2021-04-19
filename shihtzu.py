import discord
from discord.ext import commands, tasks
from discord.flags import Intents

import json
import random
from datetime import datetime
import re
import atexit
import os
from os import path, getenv
from utils.config import saveconfig, getconfig

async def logout(bot:commands.Bot):
    saveconfig(bot.config)

    
config = getconfig()
bot = commands.Bot(command_prefix=config['prefix'],
                   owner_ids=config['owners'],
                   intents=Intents.all())
bot.config = config
atexit.register(logout, bot)

# Load Cog extensions
for file in os.listdir('cogs'):
    name = file[:-3]
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{name}')
    
@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Game("Now 24/7!"))
    
print('Attempting to login...')
bot.run(getenv('DISCORD_TOKEN'))
