import discord
from discord.ext import commands
import logging
import os
import subprocess

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s » %(message)s')

intents = discord.Intents.all()
intents.reactions = True
intents.messages = True

class MyBot(commands.Bot):
    async def setup_hook(self):

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"{filename} caricato!")

            else:
                logging.error(f"Unable to load {filename}.")
        
        print('BTE Italia Bot In Funzione!')

bot = MyBot(command_prefix='£', intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name='bteitalia.tk'))

bot.run(os.environ.get('TOKEN'))