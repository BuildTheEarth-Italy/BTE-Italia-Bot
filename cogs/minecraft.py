from javascript import require, On, Once, AsyncTask, once, off
from discord.ext import commands
import discord
import time
import asyncio
import os

async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

mineflayer = require('mineflayer')

bot_shit = {
    'host': 'it.buildtheearth.net',
    'username': 'imalimitgod@gmail.com',
    'auth': 'microsoft',
    'version': "1.12.2"
  }

bot = mineflayer.createBot(bot_shit)

class MCBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name='connect',
        description='Minecraft bot connects to the server.',
        usage='£connect',
        brief='MCBot connect command'
    )
    async def connect(self, ctx):
        bot = mineflayer.createBot(bot_shit)
        await ctx.reply(embed=discord.Embed(description="Bot connected the server.", color=discord.Color.green))


    @commands.hybrid_command(
        name='reconnect',
        description='Minecraft bot reconnects the server.',
        usage='£reconnect',
        brief='MCBot reconnect command'
    )
    async def reconnect(self, ctx):
        bot.end()
        bot = mineflayer.createBot(bot_shit)
        await ctx.reply(embed=discord.Embed(description="Bot reconnected to the server.", color=discord.Color.green))


    @commands.hybrid_command(
        name='disconnect',
        description='Minecraft bot disconnects from the server.',
        usage='£disconnect',
        brief='MCBot disconnect command'
    )
    async def disconnect(self, ctx):
        bot.end()
        await ctx.reply(embed=discord.Embed(description="Bot disconnected from the server.", color=discord.Color.green))


@On(bot, 'chat')
def chat(this, username, message, *rest):
    if username == bot.username:
        return

@On(bot, 'kicked') 
def kicked(this, reason):
    print("Bot kicked: ${reason}")
    bot = mineflayer.createBot(bot_shit)

@On(bot, 'error')
def error(this, error):
    print('Bot encountered an error: ${error.message}')


@On(bot, 'spawn') 
def spawn(this):
    time.sleep(5)
    bot.chat('/bt it')

@On(bot, 'end')
def end(this):
    print('Bot disconnected. Reconnecting...')
    bot = mineflayer.createBot(bot_shit)

async def setup(bot):
    await bot.add_cog(MCBot(bot))
