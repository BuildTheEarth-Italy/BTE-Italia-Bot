import discord
from discord.ext import commands
from discord import ui
from discord.ext import menus
import requests
import math
import asyncio


class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source, page):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = page
        self.ctx = None
        self.message = None

    async def start(self, ctx, *, channel=None, wait=False):
        # We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        """This method calls ListPageSource.format_page class"""
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        """Only allow the author that invoke the command to be able to use the interaction"""
        return interaction.user == self.ctx.author

    # This is extremely similar to Custom MenuPages(I will not explain these)
    @ui.button(emoji='⏪', style=discord.ButtonStyle.blurple)
    async def first_page(self, interaction, button):
        await self.show_page(0)
        await interaction.response.defer()

    @ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
    async def before_page(self, interaction, button):
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.defer()

    @ui.button(emoji='⏹', style=discord.ButtonStyle.blurple)
    async def stop_page(self, interaction, button):
        self.stop()
        await interaction.response.defer()

    @ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction, button):
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.defer()

    @ui.button(emoji='⏩', style=discord.ButtonStyle.blurple)
    async def last_page(self, interaction, button):
        await self.show_page(self._source.get_max_pages() - 1)
        await interaction.response.defer()



class MySource(menus.ListPageSource):
    def __init__(self, ctx, entries, per_page):
        self.ctx = ctx
        self.per_page = per_page
        self.entries = entries
        pages, left_over = divmod(len(entries), per_page)
        if left_over:
            pages += 1

        self._max_pages = pages

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        bababoi= [list(x) for x in enumerate(entries, start=offset)]
        

        for x in bababoi[:3]:
            if x[0] == 1:
                x[0] = '🥇'
            elif x[0] == 2:
                x[0] = '🥈'
            elif x[0] == 3:
                x[0] = '🥉'

        total_data = len(self.entries)
        total = f"{offset:,} of {min(total_data, offset + self.per_page -1):,} of {total_data:,} banned users"
        if menu.current_page==0:
            first_list = ["{0} - `{1}` ➤ {2}".format(x[0],x[1][0],x[1][1]) for x in bababoi[:3]]
            second_list = ["#{0} - `{1}` ➤ {2}".format(x[0],x[1][0],x[1][1]) for x in bababoi[3:]]
            first_list.extend(second_list)

        else:
            first_list = ["#{0} - `{1}` ➤ {2}".format(x[0],x[1][0],x[1][1]) for x in bababoi]

        e = discord.Embed(
            title=f":medal: Classifica Builder",
            description="\n".join(first_list),
            color=discord.Color.yellow()
            )

        e.set_footer(text=f"Page {(menu.current_page) + 1}/{(self._max_pages)} · 👷‍♂️ {total_data:,} Costruttori")
        return e



class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='progressi',
        description='Will send link to BTE Italias progress map.',
        usage='£progressi',
        brief='BTE Italia progress map',
        aliases=["progress", "map", "mappa"]
    )
    async def progressi(self, ctx):         
            embed = discord.Embed(
                description=":map: **Ecco la mappa progressi!**\nhttps://maphub.net/BTEItalia/bte-italia-progressi", color=discord.Color.blue())
            await ctx.send(embed=embed)     

    @commands.command(
        name='staff',
        description='Will send a list of all BTE Italias staff member.',
        usage='£staff',
        brief='BTE Italia staff member list',
        aliases=["stafflist", "mods", "moderatori", "supporto", "modlist", "lista mod", "lista moderatori", "tecnici", "lista staff", "list", "staffs", "staffer", "staffers"]
    )
    async def staff(self, ctx):
        guild = self.bot.get_guild(686910132017430538)
        presidente_role = guild.get_role(695697978391789619)
        team_lead_role = guild.get_role(859467091639009350)
        personale_tecnico_role = guild.get_role(696409124102996068)
        mod_supporto_role = guild.get_role(701176339968950272)
        valutazioni_role = guild.get_role(756854255662661643)
        personale_relazioni_pubbliche_role = guild.get_role(701817511284441170)
        presidente_members = presidente_role.members
        team_lead_members = team_lead_role.members
        personale_tecnico_members = personale_tecnico_role.members
        mod_supporto_members = mod_supporto_role.members
        valutazioni_members = valutazioni_role.members
        personale_relazioni_pubbliche_members = personale_relazioni_pubbliche_role.members
        presidente_list = [f"`{member.name}#{member.discriminator}`" for member in presidente_members]
        team_lead_list = [f"`{member.name}#{member.discriminator}`" for member in team_lead_members]
        personale_tecnico_list = [f"`{member.name}#{member.discriminator}`" for member in personale_tecnico_members]
        mod_supporto_list = [f"`{member.name}#{member.discriminator}`" for member in mod_supporto_members]
        valutazioni_list = [f"`{member.name}#{member.discriminator}`" for member in valutazioni_members]
        personale_relazioni_pubbliche_list = [f"`{member.name}#{member.discriminator}`" for member in personale_relazioni_pubbliche_members]
        message = discord.Embed(title="<:bte_italy:991738968725000433> Lista Staff BTE Italia ", colour=discord.Colour.blue())
        message.add_field(name="<:presidente:1010588696573128784> Presidente", value="\n".join(presidente_list), inline=False)
        message.add_field(name="<:teamlead:1010588694832500757> Team Lead", value="\n".join(team_lead_list), inline=False)
        message.add_field(name="<:tecnico:1010588693423194233> Personale Tecnico", value="\n".join(personale_tecnico_list), inline=False)
        message.add_field(name="<:modesupporto:1010588684875202680> Mod e Supporto", value="\n".join(mod_supporto_list), inline=False)
        message.add_field(name="<:valutazioni:1010588685831524353> Valutazioni", value="\n".join(valutazioni_list), inline=False)
        message.add_field(name="<:personalerelazionipubbliche:1010588691388977153> Personale Relazioni Pubbliche", value="\n".join(personale_relazioni_pubbliche_list), inline=False)
        await ctx.send(embed=message)

    @commands.command(
        name='ip',
        description='Will send the ip to the BTE Italia Minecraft server.',
        usage='£ip',
        brief='BTE Italia Minecraft server IP',
        aliases=["adress", "inzirizzo", "server", "ipmc", "ipserver"]
    )
    async def ip(self, ctx):         
            embed = discord.Embed(
                description="<:bte_italy:991738968725000433> **Ecco gli IP per il nostro Server Minecraft!**\n\n<:java:1010963036342861824> **Java**: `mc.bteitalia.tk`\n<:bedrock:1010963327654055937> **Bedrock**: `bedrock.buildtheearth.net`", color=discord.Color.blue())
            await ctx.send(embed=embed)     



    @commands.command(
        name='minecraft_leaderboard',
        aliases=['mclb', 'mc_lb']
    )
    async def minecraft_leaderboard(self, ctx, page=1):
        
        r = requests.get("https://bteitalia.tk:2083/points", verify=True)
        data = r.json()
        lb_data = data['Leaderboard']
        sorted_lb_data = sorted(lb_data, key=lambda d: d['score'],  reverse=True)
        
        lb_list=[]
        for x in sorted_lb_data:
            values = list(x.values())
            lb_list.append(values)


        formatter = MySource(ctx, lb_list, per_page=10)
        menu = MyMenuPages(formatter, page-1)
        await menu.start(ctx)             

    @commands.command(
        name='serverinfo',
        description='Gives information about the server.',
        usage='£serverinfo',
        brief='Server information',
        aliases=["infoserver"]
    )
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            color=discord.Color.orange(),
            timestamp=ctx.message.created_at
            )
        
        embed.set_footer(text=f'ID: {ctx.guild.id}')
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.guild.name)
        embed.add_field(
            name=':desktop: Server info',
            value=f":beginner: Creato il {ctx.guild.created_at.strftime('%d %b %Y %H:%M')}\n:sparkles: Livello boost server: {ctx.guild.premium_tier}\n:crown: Creatore Server: {ctx.guild.owner.display_name}",
            inline=False
        )
        embed.add_field(
            name=':bust_in_silhouette: Membri',
            value=f"{ctx.guild.member_count} memberi nel server\n{ctx.guild.premium_subscription_count} persone hanno boostato il server",
            inline=False
        )
        role_output = ''
        for role in ctx.guild.roles:
            role_output += str(role)+' | '
        embed.add_field(
            name=':busts_in_silhouette: Ruoli',
            value=role_output,
            inline=False
        )

        await ctx.send(embed=embed)       



    @commands.command(
        name='userinfo',
        description='Gives information about a user.',
        usage='£userinfo (User)',
        brief='Information of a user',
        aliases=["whois", "infouser"]
    )
    async def userinfo(self, ctx, *, member = None):

        converter = commands.MemberConverter()

        if member != None:
            member = await converter.convert(ctx,member)

        else:
            member = ctx.author

        roles = [role for role in member.roles] 

        embed = discord.Embed(
            color=discord.Color.orange(),
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name=f'Informazioni su: {member.display_name}')

        if member.raw_status == "online":
            status = "online"

        elif member.raw_status == "offline":
            status = "offline"
        
        elif member.raw_status == "idle":
            status = "inattivo"

        elif member.raw_status == "dnd":
            status = "non disturbare"

        elif member.raw_status == "invisible":
            status = "offline"
        

        embed.add_field(
            name=':bust_in_silhouette: Informazioni Account',
            value=f":signal_strength: Attualmente {status}\n:beginner: Creato il {member.created_at.strftime('%d %b %Y %H:%M')}",
            inline=False
        )

        if member.premium_since == None:
            embed.add_field(
                name=':desktop: Informazioni Server',
                value=f":beginner: Entrato il {member.joined_at.strftime('%d %b %Y %H:%M')}\n:x: Non boostando il server",
                inline=False
            )

        else:
            embed.add_field(
                name=':desktop: Informazioni Server',
                value=f":beginner: Entrato il {member.joined_at.strftime('%d %b %Y %H:%M')}\n:sparkles: Boostando il server",
                inline=False
            )

        if len(roles) != 1:
            roles_value = " ".join([role.mention for role in roles[1:]])
        
        else:
            roles_value = "Questo utente non ha ruoli"

        embed.add_field(name=f":busts_in_silhouette: Ruoli ({len(roles) - 1}):", value=roles_value)
        embed.set_footer(
            text=f'ID: {member.id}'
        )
        await ctx.send(embed=embed)



    @commands.command(
        name='socials',
        description='Gives links to all BTE Italias official links.',
        usage='£socials',
        brief='BTE Italias Socials',
        aliases=["social", "links", "link"]
    )
    async def socials(self, ctx):
        message = discord.Embed(title="<:bte_italy:991738968725000433> Lista Social BTE Italia ", colour=discord.Colour.blue())
        message.add_field(name="<:TikTok:1008819190574104646> **TikTok**:", value="<https://tiktok.com/@bteitalia>", inline=False)
        message.add_field(name="<:Youtube:814457415599652904> **YouTube**:", value="<https://www.youtube.com/c/BuildTheEarthItaly/>", inline=False)
        message.add_field(name="<:Instagram:814457416296431656> **Instagram**:", value="<https://instagram.com/bteitalia/>", inline=False)
        message.add_field(name="<:Discord:847918459647164466> **Discord**:", value="<https://discord.gg/fuEg2aQTy9>", inline=False)
        message.add_field(name="<:bte_italy:991738968725000433> **Sito Web**:", value="<https://bteitalia.tk/>", inline=False)
        message.add_field(name="<:minecraft:1008821296131477535> **Server Minecraft**:", value="`mc.bteitalia.tk`", inline=False)
        await ctx.send(embed=message)    


    @userinfo.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                description="Non hai il permesso di usare questo comando.", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(Info(bot))
