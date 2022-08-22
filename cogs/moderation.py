from telnetlib import STATUS
import discord
import time
from discord import ui
from discord.ext import commands
from discord.ext import menus
from discord.ext.menus import button, First, Last
import time
import math

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

    @ui.button(emoji='⏹️', style=discord.ButtonStyle.blurple)
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
        total_data = len(self.entries)
        total = f"{offset:,} - {min(total_data, offset + self.per_page -1):,} of {total_data:,} banned users"

        e = discord.Embed(title=f"Ban list · Page {(menu.current_page) + 1} of {(self._max_pages)}", color=discord.Color.blue())

        for name, value in entries:
            e.add_field(name=name, value=value, inline=False)

        e.set_footer(text=f"{total} · Only {self.ctx.author.name}#{self.ctx.author.discriminator} can control this list!", icon_url=self.ctx.author.avatar.url)
        return e


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='clear',
        description='Deletes a specified amount of messages.',
        usage='£clear (1-100)',
        brief='Clears messages'
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        limit=100
        if 1 <= amount <= limit:
            await ctx.channel.purge(limit=amount+1)
            embed=discord.Embed(description=f':wastebasket: Cancellati {amount} messaggi.', color=discord.Color.green())
            message = await ctx.channel.send(embed=embed)
            time.sleep(10)
            await message.delete()

        else:
            embed=discord.Embed(description=':x: Perfavore inserisci un numero tra `0-100`.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)

    @clear.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=':x: Perfavore inserisci un numero valido tra `0-100`.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)
    
    @commands.command(
        name='banlist',
        description='Gives a list of banned users.',
        usage='£banlist',
        brief='Gives ban list'
    )
    @commands.has_permissions(ban_members=True)
    async def banlist(self, ctx, page = 1):
        bans = [entry async for entry in ctx.guild.bans()]
        banlist = [(x.user, x.reason) for x in bans]
        formatter = MySource(ctx, banlist, per_page=10)
        menu = MyMenuPages(formatter, page-1)
        await menu.start(ctx)

    @commands.command(
        name='ban',
        description='Bans a user from the server.',
        usage='£ban (User) (Reason)',
        brief='Bans a user'
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member = None, *, reason=None):
        if member == None:
            embed = discord.Embed(
                description=':x: Perfavore specifica un utente da bannare', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            
            converter = commands.MemberConverter()
            member = await converter.convert(ctx, member)

            await member.ban(reason=reason)
            embed = discord.Embed(
                description='✅ Bannato {} per ``{}``'.format(
                    member.mention, reason),
                colour=discord.Colour.green()
            )

            await ctx.send(embed=embed)

            
    @commands.command(
        name='unban',
        description='Unbans a user from the server.',
        usage='£unban (User)',
        brief='Unbans a user'
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if member == None:
            embed = discord.Embed(
                description=':x: Perfavore specifica un utente da sbannare', color=discord.Color.red())
            await ctx.send(embed=embed)
             
        else:
            bans = [entry async for entry in ctx.guild.bans()]

            for ban_entry in bans:
                user = ban_entry.user

                if f"{user.name}#{user.discriminator}" == member:
                    await ctx.guild.unban(user)
                    
                    embed = discord.Embed(
                        description='✅ Sbannato {}'.format(
                            user.mention),
                        colour=discord.Colour.green()
                    )
                    await ctx.send(embed=embed)
                    return

                elif str(user.id) == member:
                    await ctx.guild.unban(user)

                    embed = discord.Embed(
                        description='✅ Sbannato {}'.format(
                            user.mention),
                        colour=discord.Colour.green()
                    )
                    await ctx.send(embed=embed)
                    return

            embed = discord.Embed(
                description="Couldn't find that user.",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)

    @commands.command(
        name='kick',
        description='Kicks a user from the server.',
        usage='£kick (User) (Reason)',
        brief='Kicks a user'
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member = None, *, reason=None):
        if member == None:
            embed = discord.Embed(
                description=':x: Perfavore specifica un utente da kickare', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            converter = commands.MemberConverter()
            member = await converter.convert(ctx, member)
            await member.kick(reason=reason)
            embed = discord.Embed(
                description='✅ Kickato {} per ``{}``'.format(
                    member.mention, reason),
                colour=discord.Colour.green()
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

        embed.add_field(name=f":busts_in_silhouette: Ruoli ({len(roles)}):", value=roles_value)
        embed.set_footer(
            text=f'ID: {member.id}'
        )
        await ctx.send(embed=embed)
        
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
        name='listserver',
        description='List of servers the bot is present in.',
        usage='`£listserver`',
        aliases=['ls', 'serverlist', 'sl']        
    )
    async def listserver(self, ctx, page: int = 1):
        output = ''
        guilds = self.bot.guilds
        pages = math.ceil(len(guilds)/10)
        if 1 <= page <= pages:
            counter = 1+(page-1)*10
            for guild in guilds[(page-1)*10:page*10]:
                output += f'{counter}. {guild.name}\n'
                counter += 1
            embed = discord.Embed(
                color=discord.Color.orange(),
                description=output,
                title='**LISTA SERVER**',
                timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f'Pagina {page} su {pages}'
            )
            await ctx.send(
                embed=embed
            )
        else:
            await ctx.send(
                embed=create_embed(
                    ':x: La pagina che hai specificato non esiste'
                ),
                delete_after=10
            )                
            

    @commands.command(
        name='setnickname',
        description='Sets a users nickname.',
        usage='£setnickname (User) (Nickname)',
        brief='Change users nickname',
        aliases=["setnick"]
    )
    @commands.bot_has_permissions(manage_nicknames = True)
    async def setnickname(self, ctx, member = None, *name):
        if member == None:
            member = ctx.author
        
        else:
            converter = commands.MemberConverter()
            member = await converter.convert(ctx, member)

        nickname = ' '.join(name)
        await member.edit(nick=nickname)
        if nickname:
            msg = f'Impostato il nickname di `{member}` a: **{nickname}**'
        else:
            msg = f'Resettato il nickname di `{member}` a: **{member.name}**'
        await ctx.send(msg)
            
    @commands.command(
        name='avatar',
        description='Grabs a users profile picture.',
        usage='£avatar (User)',
        brief='Grabs profile picture',
        aliases=["pfp", "av"]
    )
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:member=ctx.message.author

        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar.url)

        await ctx.send(embed=message)            
               
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


    @setnickname.error
    @kick.error
    @ban.error
    @unban.error
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description='Non hai il permesso di usare questo comando',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                description="Couldn't find that user.",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            print(error)



async def setup(bot):
    await bot.add_cog(Moderation(bot))
