import datetime
import discord
import emoji
from discord.ext import commands
from discord.ext import menus
from discord import ui
import requests
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
            first_list = ["{0} - {1} - {2}".format(x[0],x[1][0],x[1][1]) for x in bababoi[:3]]
            second_list = ["#{0} - {1} - {2}".format(x[0],x[1][0],x[1][1]) for x in bababoi[3:]]
            first_list.extend(second_list)

        else:
            first_list = ["#{0} - {1} - {2}".format(x[0],x[1][0],x[1][1]) for x in bababoi]


        e = discord.Embed(
            title=f"👷‍♂️ Classifica Builder",
            description="\n".join(first_list),
            color=discord.Color.yellow()
            )

        e.set_footer(text=f"Page {(menu.current_page) + 1}/{(self._max_pages)} · Top 10 Builer BTE Italia ")
        return e


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(
        name='post',
        description='Will send provided links to the #notifiche channel.',
        usage='£post (Link/s)',
        brief='Posts link in #notifiche',
        aliases=["posta"]
    )
    @commands.has_role(701817511284441170)
    async def post(self, ctx, *, links: str):
        link_list = links.split()
        message = '🇮🇹 Nuovo Post!\n🇺🇸 New Post!'
        link_msg = '\n\n'.join(link_list)

        notifiche_channel = self.bot.get_channel(697169688005836810)

        await notifiche_channel.send(f'{message}\n\n{link_msg}')

        embed = discord.Embed(description='Postato!',
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(
        name='messaggio',
        description='Will make the bot message the content provided.',
        usage='£messaggio (Channel) (Message)',
        brief='Messages with bot',
        aliases=["message", "msg"]
    )
    @commands.has_any_role(859467091639009350, 881627300142129222)
    async def messaggio(self, ctx, channel=None, *, message=None):
        converter = commands.TextChannelConverter()

        if channel != None:

            if message != None or ctx.message.attachments != None:

                try:
                    destination_channel = await converter.convert(ctx, channel)

                    try:
                        attachments = ctx.message.attachments
                        files = []
                        for file in attachments:
                            files.append(await file.to_file())

                        await destination_channel.send(content=message, files=files)

                    except Exception as e:
                        embed = discord.Embed(
                            description="Non è stato possibile mandare un messaggio a questo canale.", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        print(e)
                        return

                    embed = discord.Embed(
                        description='Messaggio inviato!', color=discord.Color.green())
                    await ctx.send(embed=embed)

                except commands.ChannelNotFound:
                    embed = discord.Embed(
                        description='Canale non trovato.', color=discord.Color.red())
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    description='Perfavore invia un messaggio valido.', color=discord.Color.red())
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                description='Devi indicare un canale.', color=discord.Color.red())
            await ctx.send(embed=embed)


    @commands.command(
        name='reazione',
        description='Will react to specified messages with specified emojis.',
        usage='£reazione (Message ID) (Reaction)',
        brief='Reacts to messages',
        aliases=["react"]
    )
    @commands.has_any_role(859467091639009350, 881627300142129222)
    async def reazione(self, ctx, message=None, reaction=None):
        if message != None:

            if reaction != None:
                reaction_message = None
                try:
                    message_converter = commands.MessageConverter()
                    reaction_message = await message_converter.convert(ctx, message)

                except commands.MessageNotFound:
                    channels = ctx.guild.channels
                    for channel in channels:
                        try:
                            reaction_message = await channel.fetch_message(message)

                        except:
                            pass

                    if reaction_message == None:
                        embed = discord.Embed(
                            description="Non è stato possibile trovare il messaggio.", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

                if reaction in emoji.UNICODE_EMOJI_ENGLISH:
                    reaction_emoji = reaction

                else:
                    try:
                        emoji_converter = commands.PartialEmojiConverter()
                        reaction_emoji = await emoji_converter.convert(ctx, reaction)

                    except commands.PartialEmojiConversionFailure:
                        embed = discord.Embed(
                            description='Perfavore indica un emoji valida.', color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

                try:
                    await reaction_message.add_reaction(reaction_emoji)

                except Exception as e:
                    print(e)

                    embed = discord.Embed(
                        description="Non è stato possibile reagire al messaggio.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

                embed = discord.Embed(
                    description='Reagito!', color=discord.Color.green())
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    description='Devi indicare un emoji da reagire.', color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description='Devi indicare un messaggio.', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='oldApprova')
    @commands.has_any_role(704338128692838533, 881627300142129222)
    async def approva(self, ctx, member=None):
        approva_channel = ctx.guild.get_channel(891675282992431154)
        if ctx.channel == approva_channel:
            if member != None:
                try:
                    converter = commands.MemberConverter()
                    member = await converter.convert(ctx, member)

                    starter_role = ctx.guild.get_role(704332197628477450)
                    if not starter_role in member.roles:
                        try:
                            newbie_role = ctx.guild.get_role(
                                884464061851521065)
                            await member.remove_roles(newbie_role)

                        except Exception as e:
                            print(e)
                            embed = discord.Embed(
                                description="Non è stato possibile rimuovere il ruolo Newbie dal utente.", color=discord.Color.red())
                            await ctx.send(embed=embed)
                            return

                        try:
                            starter_role = ctx.guild.get_role(
                                704332197628477450)
                            await member.add_roles(starter_role)

                        except Exception as e:
                            print(e)
                            embed = discord.Embed(
                                description="Rimosso il ruolo Newbie ma non è stato posssibile assegnare Starter.", color=discord.Color.red())
                            await ctx.send(embed=embed)
                            return

                        # Search for the user in the sheets
                        applicationsList = sh.get()
                        minecraftName = ""
                        for application in applicationsList:
                            #      v-- Discord name + discriminator
                            if application[2] == f"{member.name}#{member.discriminator}":
                                # Minecraft In game name
                                minecraftName = application[1]

                        if minecraftName == "":
                            embed = discord.Embed(
                                description=f"{member.name}#{member.discriminator} è stato approvato su Discord ma non su Minecraft, per favore contatta il <@&696409124102996068>.", color=discord.Color.gold())
                            await ctx.send(embed=embed)
                        else:
                            # Send lp command to the console channel
                            console_channel = ctx.guild.get_channel(
                                778281056284442664)

                            await console_channel.send(f"lp user {minecraftName} group add starter")

                            embed = discord.Embed(
                                description=f"Approvato {member.name}#{member.discriminator}!", color=discord.Color.green())
                            await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(
                            description='Utente ha già il ruolo Starter.', color=discord.Color.red())
                        await ctx.send(embed=embed)

                except commands.MemberNotFound:
                    embed = discord.Embed(
                        description='Utente non trovato!', color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

            else:
                embed = discord.Embed(
                    description='Devi indicare un Utente!', color=discord.Color.red())
                await ctx.send(embed=embed)

        else:
            pass
		
            
            
    @commands.command(
        name='valuta',
        description='Will rate a users building.',
        usage='£valuta (Message ID) (Minecraft Username) (Points)',
        brief='Rates a users building',
        aliases=["rate"]
    )
    @commands.has_role(756854255662661643)
    async def valuta(self, ctx, post_id = None, minecraft_name = None, points = None):

        if post_id == None or minecraft_name == None or points == None:
            embed = discord.Embed(description=f'Assicurati di star mandando i valori in questo formato:\n`{await self.bot.get_prefix(ctx.message)}valuta [POST_ID] [MINECRAFT_USERNAME] [POINTS]`', color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            try:
                points = int(points)

            except:
                
                try:
                    points = float(points)
                
                except:
                    embed = discord.Embed(description=f'I Punti devono essere un valore numerico', color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
            
            emoji_converter = commands.PartialEmojiConverter()
            verify_emoji = await emoji_converter.convert(ctx, '<:Verified:707278127449112616>')
            
            try:
                channel = await self.bot.fetch_channel(704304928176209940)
                message = await channel.fetch_message(int(post_id))

            except:
                embed = discord.Embed(description=f"Non posso reagire al messaggio.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            await message.add_reaction(verify_emoji)

            italiano_role = ctx.guild.get_role(698617888675856514)
            international_role = ctx.guild.get_role(698566163738656909)

            if italiano_role in message.author.roles:
                if int(points) != 1:
                    notification_message = f"Hey *{minecraft_name}*, la tua costruzione è stata valutata **{points} Punti**\nPost di riferimento: https://discord.com/channels/686910132017430538/704304928176209940/{post_id}"
                else:
                    notification_message = f"Hey *{minecraft_name}*, la tua costruzione è stata valutata **{points} Punto**\nPost di riferimento: https://discord.com/channels/686910132017430538/704304928176209940/{post_id}"

            elif international_role in message.author.roles:
                if int(points) != 1:
                    notification_message = f"Hey *{minecraft_name}*, your building has been evaluated **{points} Points**\nReference post: https://discord.com/channels/686910132017430538/704304928176209940/{post_id}"
                else:
                    notification_message = f"Hey *{minecraft_name}*, your building has been evaluated **{points} Point**\nReference post: https://discord.com/channels/686910132017430538/704304928176209940/{post_id}"

            await message.author.send(notification_message)


            try:
                punti_valutazioni = ctx.guild.get_channel(779438755912220713)
                await punti_valutazioni.send(f"`{minecraft_name}` = {points}")
            
            except:
                embed = discord.Embed(description=f"Non posso mandare il messaggio a <#779438755912220713>", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            confirmation_message = discord.Embed(description=f":white_check_mark: Costruzione valutata!", color=discord.Color.green())
            await ctx.send(embed=confirmation_message)



    async def annouce(self, ctx, deadline, message):
        await discord.utils.sleep_until(deadline)
        print('Meeting annouced!')

        channel = ctx.guild.get_channel(758036680560345228)
        await channel.send(message)


    @commands.command(
        name='riunione',
        description='Will make a riunione reminder.',
        usage='£riunione (DD/MM/YYYY HH:MM)',
        brief='BTE Italia Riunione'
    )
    @commands.has_role(756854255662661643)
    async def riunione(self, ctx, *, date=None):
        if date != None:
            try:
                deadline = datetime.datetime.strptime(f"{date}" , "%d/%m/%Y %H:%M")
                before_deadline = deadline - datetime.timedelta(minutes=30)
                if before_deadline > datetime.datetime.now():
                    
                    message = "<@734716661474525244>\nRiunione tra 30 minuti! :bte_italy_animated:"
                    await asyncio.run(await self.annouce(ctx, before_deadline, message))
                
                if deadline > datetime.datetime.now():

                    message = "<@734716661474525244>\nRiunione in corso! :bte_italy_animated:"
                    await asyncio.run(await self.annouce(ctx, deadline, message))

            except Exception as e:
                print(e.__str__())
                embed = discord.Embed(
                    description="Formato non valido. Per favore provedi informazioni nel seguente formato:\n`£riunione [giorno/mese/anno ora:minuti]`", 
                    color=discord.Color.red()
                    )
                await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(
                description="Per favore provedi informazioni nel seguente formato:\n`£riunione [giorno/mese/anno ora:minuti]`", 
                color=discord.Color.blue()
                )
            await ctx.send(embed=embed)



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
        usage='£progressi',
        brief='BTE Italia staff member list',
        aliases=["stafflist", "mods", "moderatori", "supporto", "modlist", "lista mod", "lista moderatori", "tecnici", "lista staff", "list", "staffs", "staffer", "staffers"]
    )
    async def staff(self, ctx):         
        message = discord.Embed(title="<:bte_italy:991738968725000433> Lista Staff BTE Italia ", colour=discord.Colour.blue())
        message.add_field(name="<:presidente:1010588696573128784> Presidente", value="<:magix92:1010586235535888434> `Magix92`\n<:filippo_the_king:1010586249817497753> `filippo_the_king`", inline=False)
        message.add_field(name="<:teamlead:1010588694832500757> Team Lead", value="<:forgiobombi:1010585405889974312> `forgiobombi`\n<:Diamondpower500:1010587025205907516> `DiamondPower500`\n<:Martinsuperstar:1010590112205250580> `Martinsuperstar`\n<:MemoryOfLife:1010590510760611930> `MemoryOfLife`", inline=False)
        message.add_field(name="<:tecnico:1010588693423194233> Tecnico", value="<:forgiobombi:1010585405889974312> `forgiobombi`\n<:MemoryOfLife:1010590510760611930> `MemoryOfLife`\n<:filippo_the_king:1010586249817497753> `filippo_the_king`\n<:ElijahPepe:1010592808836546572> `ElijahPepe`\n<:MikChan:1010592810380054658> `MikChan`\n<:celery6:1010593496526229525> `celery6`\n<:Marcy2005:1010597530884636706> `spl1ce_`", inline=False)
        message.add_field(name="<:modesupporto:1010588684875202680> Mod e Supporto", value="<:Diamondpower500:1010587025205907516> `DiamondPower500`\n<:I_EricDraven_I:1010595264492470314> `I_EricDraven_I`\n<:FedexV2:1010595261535498330> `FedeXV2`\n<:HannibalLecter:1010595263401955459> `HannibalLecter`", inline=False)
        message.add_field(name="<:valutazioni:1010588685831524353> Valutazioni", value="<:Martinsuperstar:1010590112205250580> `Martinsuperstar`\n<:forgiobombi:1010585405889974312> `forgiobombi`\n<:magix92:1010586235535888434> `Magix92`", inline=False)
        message.add_field(name="<:personalerelazionipubbliche:1010588691388977153> Personale Relazioni Pubbliche", value="<:forgiobombi:1010585405889974312> `forgiobombi`\n<:I_EricDraven_I:1010595264492470314> `I_EricDraven_I`\n<:magix92:1010586235535888434> `Magix92`\n<:H2bomber_:1010603700412219523> `H2bomber_`\n<:howard9068:1010603701817331844> `howard9068`\n<:glurbB:1010603698730315787> `glurbB`", inline=False)
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
        
        r = requests.get("https://62.171.174.31:8000/points", verify=False)
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

        
                
    @valuta.error
    @post.error
    @messaggio.error
    @reazione.error
    @approva.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                description=":x: Non hai il permesso di usare questo comando.", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            print(error)
            

async def setup(bot):
    await bot.add_cog(Utilities(bot))
