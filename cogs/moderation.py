import discord
import time
from discord.ext import commands
from discord.ext.commands.core import has_permissions

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', description='Deletes the amount of messages provided.')
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        limit=100
        if amount<=limit:
            await ctx.channel.purge(limit=amount+1)
            embed=discord.Embed(description=f'Cleared {amount} messages.', color=discord.Color.green())
            message = await ctx.channel.send(embed=embed)
            time.sleep(10)
            await message.delete()

        else:
            embed=discord.Embed(description='Perfavore inserisci un numero tra `0-100`.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)

    @clear.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description='Perfavore inserisci un numero valido tra `0-100`.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
def setup(bot):
    bot.add_cog(Moderation(bot))
