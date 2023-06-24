from discord import Embed, Color
from discord.ext import commands
from discord.ext import tasks
from os import environ
from utils.spreadsheet import Spreadsheet
import asyncio

sh = Spreadsheet(environ.get('SPREADSHEET_ID'))

@tasks.loop(seconds=3600)
async def refresh_spreadsheet():
    sh.fetch()  # 1 hour


class Approva(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name='approva',
        description='Approves a user from rank Newbie to rank Starter.',
        usage='£approva (User)',
        brief='Approve a user',
        aliases=["approve"]
    )
    @commands.has_role(756854255662661643)
    async def approva(self, ctx, member=None):
        approva_channel = ctx.guild.get_channel(891675282992431154)
        starter_role = ctx.guild.get_role(704332197628477450)
        newbie_role = ctx.guild.get_role(884464061851521065)
        technical_role = ctx.guild.get_role(696409124102996068)

        if ctx.channel != approva_channel:
            embed = Embed(
                description='Usa il seguente comando nel canale <#891675282992431154>!', color=Color.red())           
            await ctx.send(embed=embed)          
            return

        if member == None:
            embed = Embed(
                description='Devi indicare un Utente!', color=Color.red())
            await ctx.send(embed=embed)
            return

        try:
            converter = commands.MemberConverter()
            member = await converter.convert(ctx, member)
        except commands.MemberNotFound:
            embed = Embed(
                description='Utente non trovato!', color=Color.red())
            await ctx.send(embed=embed)
            return

        if starter_role in member.roles:
            embed = Embed(
                description=f"Utente ha già il ruolo {starter_role.mention}.", color=Color.red())
            await ctx.send(embed=embed)
            return

        try:
            await member.remove_roles(newbie_role)
        except Exception as e:
            print(e)
            embed = Embed(
                description=f"Non è stato possibile rimuovere il ruolo {newbie_role.mention} dal utente.", color=Color.red())
            await ctx.send(embed=embed)
            return

        try:
            await member.add_roles(starter_role)
        except Exception as e:
            print(e)
            embed = Embed(
                description=f"Rimosso il ruolo {newbie_role.mention} ma non è stato possibile assegnare {starter_role.mention}.", color=Color.red())
            await ctx.send(embed=embed)
            return

        # Search for the user in the sheets
        applicationsList = sh.get()
        minecraftName = ""
        for application in applicationsList:
            #      v-- Discord name + discriminator
            if application[2] == f"{member.name}{'#'+member.discriminator if (member.discriminator != '0') else ''}":
                # Minecraft In game name
                minecraftName = application[1]

        if minecraftName == "":
            embed = Embed(
                description=f"{member.name}{'#'+member.discriminator if (member.discriminator != '0') else ''} è stato approvato su Discord ma non su Minecraft, per favore contatta il {technical_role.mention}.", color=Color.gold())
            await ctx.send(embed=embed)
        else:
            # Send lp command to the console channel
            console_channel = ctx.guild.get_channel(
                778281056284442664)

            await console_channel.send(f"lp user {minecraftName} group add starter")

            embed = Embed(
                description=f"Approvato {member.name}{'#'+member.discriminator if (member.discriminator != '0') else ''}!", color=Color.green())
            await ctx.send(embed=embed)

    @approva.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = Embed(
                description="Non hai il permesso di usare questo comando.", color=Color.red())
            await ctx.send(embed=embed)
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(Approva(bot))
    refresh_spreadsheet.start()
