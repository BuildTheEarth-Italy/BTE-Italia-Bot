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

bot = commands.Bot(command_prefix='£', intents=intents)


async def run_once_when_ready():
    await bot.wait_until_ready()
    print('BTE Italia Bot In Funzione!')
    
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='bteitalia.tk'))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")
        logging.info(f"{filename} caricato!")

    else:
        logging.error(f"Unable to load {filename}.")
        
@bot.listen('on_message')
async def antiserverads(message):
    if message.author.id == (833995282773049344):
        return

    elif "discord.gg" in message.content.lower():
        await message.delete()
        await message.channel.send(":x: **Non publicizzare il tuo server!**")        

bot.loop.create_task(run_once_when_ready())
bot.run(os.environ.get('TOKEN'))
