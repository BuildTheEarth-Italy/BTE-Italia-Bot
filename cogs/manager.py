import os
import discord
import json
import asyncio
from discord.ext import commands

class Manager(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command(
        name='unload',
        description='Unloads cog from the bot.',
        usage='£unload (Cog)',
        brief='Unload cog',
        aliases=["ul"]
    )
    @commands.has_role(859467091639009350)
    async def unload(self, ctx, extension:str="all"):
        await self.handle_cog(ctx, self.client.unload_extension, extension)

    @commands.command(
        name='reload',
        description='Reload cog from the bot.',
        usage='£reload (Cog)',
        brief='Reload cog',
        aliases=["rl"]
    )
    @commands.has_role(859467091639009350)
    async def reload(self, ctx, extension:str="all"):
        await self.handle_cog(ctx, self.client.reload_extension, extension)

    @commands.command(
        name='load',
        description='Loads cog from the bot.',
        usage='£load (Cog)',
        brief='Load cog',
        aliases=["ld"]
    )
    @commands.has_role(859467091639009350)
    async def load(self, ctx, extension:str="all"):
        await self.handle_cog(ctx, self.client.load_extension, extension)
        
    async def handle_cog(self, ctx, func, extension):
        """load/unload/reload given cog, or all cogs, based on func arg"""
        extension = extension.lower()

        func_name = {
            "unload_extension": "unload",
            "reload_extension": "reload",
            "load_extension": "load"
        }[func.__name__]  # get proper function name to use it like a verb

        if extension == "all":
            message = ""
            for i, file in enumerate(os.listdir("./cogs")):
                if file.endswith(".py"):
                    file = file[:-3]
                    try:
                        func(f"cogs.{file}")
                        message += f"+ [{i}] cog \"{file}\" {func_name}ed successfully\n"
                    except Exception as e:
                        message += f"- [{i}] unable to {func_name} cog \"{file}\". {e.__class__.__name__}: {e}\n"

            embed = discord.Embed(description=f"```diff\n{message}\n```")
            return await ctx.reply(embed=embed)

        try:
            func(f"cogs.{extension}")
            embed = discord.Embed(description=f"```diff\n+ cog \"{extension}\" {func_name}ed successfully\n```")
            await ctx.reply(embed=embed)
        except Exception as e:
            embed= discord.Embed(description=f"```diff\n- unable to {func_name} cog \"{extension}\". {e.__class__.__name__}: {e}```\n")
            await ctx.reply(embed=embed)

            
    @unload.error
    @load.error
    @reload.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                description=":x: Non hai il permesso di usare questo comando.", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            print(error)            
            
def setup(client):
    client.add_cog(Manager(client))
