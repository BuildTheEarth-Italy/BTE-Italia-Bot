import datetime
import discord
import emoji
from discord.ext import commands
import asyncio


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.hybrid_command(
        name='post',
        description='Will send provided links to the #notifiche channel.',
        usage='£post (Link/s)',
        brief='Posts link in #notifiche',
        aliases=["posta"]
    )
    @commands.has_role(696409124102996068)
    async def post(self, ctx, *, links: str):
        link_list = links.split()
        message = '🇮🇹 Nuovo Post!\n🇺🇸 New Post!'
        link_msg = '\n\n'.join(link_list)

        notifiche_channel = self.bot.get_channel(697169688005836810)

        await notifiche_channel.send(f'{message}\n\n{link_msg}')

        embed = discord.Embed(description='Postato!',
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name='messaggio',
        description='Will make the bot message the content provided.',
        usage='£messaggio (Channel) (Message)',
        brief='Messages with bot',
        aliases=["message", "msg"]
    )
    @commands.has_any_role(696409124102996068, 881627300142129222)
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


    @commands.hybrid_command(
        name='reazione',
        description='Will react to specified messages with specified emojis.',
        usage='£reazione (Message ID) (Reaction)',
        brief='Reacts to messages',
        aliases=["react"]
    )
    @commands.has_any_role(696409124102996068, 881627300142129222)
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

    @commands.hybrid_command(name='oldapprova')
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
                            if application[2] == f"{member.name}{'#'+member.discriminator if (member.discriminator != '0') else ''}":
                                # Minecraft In game name
                                minecraftName = application[1]

                        if minecraftName == "":
                            embed = discord.Embed(
                                description=f"{member.name}{'#'+member.discriminator if (member.discriminator != '0') else ''} è stato approvato su Discord ma non su Minecraft, per favore contatta il <@&696409124102996068>.", color=discord.Color.gold())
                            await ctx.send(embed=embed)
                        else:
                            # Send lp command to the console channel
                            console_channel = ctx.guild.get_channel(
                                778281056284442664)

                            await console_channel.send(f"lp user {minecraftName} group add starter")

                            embed = discord.Embed(
                                description=f"Approvato {member.name}{'#'+member.discriminator if (member.discriminator != '0') else ''}!", color=discord.Color.green())
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
		
            
            
    @commands.hybrid_command(
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


    @commands.hybrid_command(
        name='riunione',
        description='Will make a riunione reminder.',
        usage='£riunione (DD/MM/YYYY HH:MM)',
        brief='BTE Italia Riunione'
    )
    @commands.has_role(696409124102996068)
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
