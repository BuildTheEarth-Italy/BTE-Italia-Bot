from pickletools import int4
from telnetlib import STATUS
import discord
import time
from discord import ui
from discord.ext import commands
from discord.ext import menus
import time
from io import BytesIO
import PIL



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

        e = discord.Embed(title=f":hammer: Ban list · Page {(menu.current_page) + 1} of {(self._max_pages)}", color=discord.Color.blue())

        for name, value in entries:
            e.add_field(name=name, value=value, inline=False)

        e.set_footer(text=f"{total} · Only {self.ctx.author.name}{'#'+self.ctx.author.discriminator if (self.ctx.author.discriminator != '0') else ''} can control this list!", icon_url=self.ctx.author.avatar.url)
        return e


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
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
    

    @commands.hybrid_command(
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


    @commands.hybrid_command(
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

            
    @commands.hybrid_command(
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

                if f"{user.name}{'#'+self.ctx.author.discriminator if (ctx.author.discriminator != '0') else ''}" == member:
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

    @commands.hybrid_command(
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

            

    @commands.hybrid_command(
        name='setnickname',
        description='Sets a users nickname.',
        usage='£setnickname (User) (Nickname)',
        brief='Change users nickname',
        aliases=["setnick"]
    )
    @commands.bot_has_permissions(manage_nicknames = True)
    async def setnickname(self, ctx, member = None, *, name):
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
            

    @commands.hybrid_command(
        name='avatar',
        description='Grabs a users profile picture.',
        usage='£avatar (User)',
        brief='Grabs profile picture',
        aliases=["pfp", "av"]
    )
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:
            member=ctx.message.author

        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar.url)

        await ctx.send(embed=message)  

    @commands.guild_only()
    @commands.hybrid_command(
        name='access',
        description='Shows who have access to the channel it is used in.',
        brief='Returns who can see a channel.',
        usage="[channel]",
    )
    async def access(self, ctx, *, channel: discord.TextChannel = None):

        if channel == None:
            channel = ctx.channel
        else:
            converter = commands.GuildChannelConverter()
            channel = await converter.convert(ctx, channel)
        members = channel.members
        
        if len(members) > 25:
            return

        embed = discord.Embed(title="🔐 Access", description=f"👆 A text file is attached above with every user with access to  `{channel.name}` 👆", color=discord.Colour.blue())
        
        buffer = BytesIO()
        members_string = ""
        for member in members:
            roles = []
            for role in member.roles: 
                roles.append(role.name)
            
            members_string += f"NAME: {member.name}, ID: {member.id}, ROLES: {', '.join(roles) }\n"

        buffer = BytesIO(members_string.encode("utf8"))

        await ctx.reply(embed=embed, file=discord.File(buffer, "members.txt"))


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
