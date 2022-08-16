import discord, random
from discord.ext import commands
import requests
import json
import shutil
from io import BytesIO
import time
import datetime
from datetime import timedelta
from PIL import Image
import qrcode

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

        
    @commands.command()
    async def fact(self, ctx):
        start = "Curiosità: "
        facts = ["Sbattere la testa contro un muro per un'ora brucia 150 calorie.",
                 "I serpenti possono aiutare a prevedere i terremoti.",
                 "Il 7% degli adulti americani crede che il latte al cioccolato provenga da mucche marroni.",
                 "Se sollevi la coda di un canguro da terra, non può saltare.",
                 "Le banane sono curve perché crescono verso il sole.",
                 "I caproni urinano sulla propria testa per avere un odore più attraente per le femmine.",
                 "L'inventore del frisbee è stato cremato e trasformato in un frisbee dopo la sua morte.",
                 "Durante la tua vita, produrrai abbastanza saliva per riempire due piscine.",
                 "Gli orsi polari potrebbero mangiare fino a 86 pinguini in una sola seduta...",
                 "È più probabile che gli attacchi di cuore accadano di lunedì.",
                 "Nel 2017 più persone sono state uccise per le ferite causate dal farsi un selfie che per gli attacchi di squali.",
                 "Il ruggito di un leone può essere sentito a 5 miglia di distanza.",
                 "La Marina degli Stati Uniti ha iniziato a utilizzare i controller Xbox per i propri periscopi.",
                 "Una pecora, un'anatra e un gallo sono stati i primi passeggeri in mongolfiera.",
                 "Il maschio medio si annoia di fare shopping dopo 26 minuti.",
                 "Il riciclaggio di un barattolo di vetro consente di risparmiare energia sufficiente per guardare la televisione per 3 ore.",
                 "Circa il 10-20% delle interruzioni di corrente negli Stati Uniti sono causate da scoiattoli."
                ]

        fact_file = open("/home/container/cogs/facts.txt", mode="r", encoding="utf8")
        fact_file_facts = fact_file.read().split("\n")
        fact_file.close()

        for i in fact_file_facts:
            if i == "": fact_file_facts.remove(i)

        facts = facts + fact_file_facts
        
        message = discord.Embed(title="BTE Italia <:bte_italy:991738968725000433> ", colour=discord.Colour.orange())
        message.add_field(name=":face_with_monocle: Curiosità:", value=random.choice(facts), inline=True)
        await ctx.send(embed=message)        
        
    @commands.command()
    async def fact_en(self, ctx):
        start = "Curiosity: "
        facts = ["Banging your head against a wall for one hour burns 150 calories.",
                 "Snakes can help predict earthquakes.",
                 "7% of American adults believe that chocolate milk comes from brown cows.",
                 "If you lift a kangaroo’s tail off the ground it can’t hop.",
                 "Bananas are curved because they grow towards the sun.",
                 "Billy goats urinate on their own heads to smell more attractive to females.",
                 "The inventor of the Frisbee was cremated and made into a Frisbee after he died.",
                 "During your lifetime, you will produce enough saliva to fill two swimming pools.",
                 "Polar bears could eat as many as 86 penguins in a single sitting…",
                 "Heart attacks are more likely to happen on a Monday.",
                 "In 2017 more people were killed from injuries caused by taking a selfie than by shark attacks.",
                 "A lion’s roar can be heard from 5 miles away.",
                 "The United States Navy has started using Xbox controllers for their periscopes.",
                 "A sheep, a duck and a rooster were the first passengers in a hot air balloon.",
                 "The average male gets bored of a shopping trip after 26 minutes.",
                 "Recycling one glass jar saves enough energy to watch television for 3 hours.",
                 "Approximately 10-20% of U.S. power outages are caused by squirrels."
                ]

        fact_file = open("/home/container/cogs/facts_en.txt", mode="r", encoding="utf8")
        fact_file_facts = fact_file.read().split("\n")
        fact_file.close()

        for i in fact_file_facts:
            if i == "": fact_file_facts.remove(i)

        facts = facts + fact_file_facts

        message = discord.Embed(title="BTE Italia <:bte_italy:991738968725000433> ", colour=discord.Colour.orange())
        message.add_field(name=":face_with_monocle: Curiosity:", value=random.choice(facts), inline=True)
        await ctx.send(embed=message)        
        
    @commands.command(aliases=["8ball", "magicball", "enlightenme"])
    async def eightball(self, ctx, *, question):
        responses = ['É certo',
                    'Senza dubbi',
                    'Puoi fare affidamento su di esso',
                    'Sì, sicuramente',
                    'È decisamente così',
                    'Per come la vedo io, sì',
                    'Più probabilmente',
                    'Sì',
                    'Prospettiva buona',
                    'I segni indicano sì',
                    'Rispondi confusa riprova',
                    'Meglio non dirtelo ora',
                    "Chiedi un'altra volta più tardi",
                    'Non posso prevedere ora',
                    'Concentrati e chiedi ancora',
                    'Non ci contare',
                    'La prospettiva non è così buona',
                    'Le mie fonti dicono di no',
                    'Molto dubbioso',
                    'No']

        message = discord.Embed(title=":8ball: 8 Ball", colour=discord.Colour.orange())
        message.add_field(name=":question: Domanda:", value=question, inline=False)
        message.add_field(name=":pencil: Risposta:", value=random.choice(responses), inline=False)
        await ctx.send(embed=message)        
        
    @commands.command()
    async def stupid(ctx, member : discord.Member = None):
        percentage = (random.randint(0, 100))

        if member == None:

            if ctx.message.author.id == (477570902075113472):
                message = await ctx.channel.send("Calcolando...")
                await asyncio.sleep(3)
                await message.edit(content=f"Sei 100% stupido!")

            else:
                message = await ctx.channel.send("Calcolando...")
                await asyncio.sleep(3)
                await message.edit(content=f"Sei {percentage}% stupido!")

        if member == member:

            if member.id == (477570902075113472):
                message = await ctx.channel.send("Calcolando...")
                await asyncio.sleep(3)
                await message.edit(content=f"{member.mention} è 100% stupido!")

            elif member == bot.user:
                message = await ctx.channel.send("Calcolando...")
                await asyncio.sleep(3)
                await message.edit(content=f"Sono troppo intelligente, anullando calcolo...")

            else:
                message = await ctx.channel.send("Calcolando...")
                await asyncio.sleep(3)
                await message.edit(content=f"{member.mention} è {percentage}% stupido!")
                
                
    @commands.command(name='meteo', description='Fornisce il meteo della città richiesta.')
    async def meteo(self,ctx,*,city):
        try:
            base_url = "http://api.weatherapi.com/v1/forecast.json?key=713f2531413e4f02b95200222221407"
            city = city.replace(" ", "_")
            complete_url = base_url + "&q=" + city
            response = requests.get(complete_url)
            result = response.json()
            city = result['location']['name']
            country = result['location']['country']
            region = result['location']['region']
            time = result['location']['localtime']
            wcond = result['current']['condition']['text']
            fahrenheit = result['current']['temp_c']
            icon = result['current']['condition']['icon']
            max = result['forecast']['forecastday'][0]['day']['maxtemp_c']
            min = result['forecast']['forecastday'][0]['day']['mintemp_c']
            rise = result['forecast']['forecastday'][0]['astro']['sunrise']
            set = result['forecast']['forecastday'][0]['astro']['sunset']
            humid = result['forecast']['forecastday'][0]['day']['avghumidity']
            icon = result['forecast']['forecastday'][0]['day']['condition']['icon']
            icon = "http:" + icon
            embed = discord.Embed(title=f":white_sun_rain_cloud: Meteo: {city}, {region}", description=f"**Paese** {country}", color=0x19B9B9)
            embed.add_field(name="Temperatura Attuale C°", value=f"{fahrenheit}", inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="Condizione", value=f"{wcond}", inline=True)
            embed.add_field(name="Umidità",value=f'{humid}%',inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="Temperatura Min. C°", value=f"{min}", inline=True)
            embed.add_field(name="Temperatura Max. C°", value=f"{max}", inline=True)
            embed.add_field(name="\u200B", value="\u200B")  # newline
            embed.add_field(name="Alba", value=f"{rise}", inline=False)
            embed.add_field(name="Tramonto", value=f"{set}", inline=False)

            embed.set_thumbnail(url=icon)
            embed.set_footer(text='Orario: 'f"{time}")

            await ctx.send(embed=embed)
            
        except:
            embed = discord.Embed(title="Nessuna risposta", color=0x19B9B9)
            embed.add_field(name="Errore", value="Perfavore metti il nome di una città", inline=True)
            await ctx.send(embed=embed)       
            
    @commands.command(name='skin', description='Mostra la skin dell utente richiesto.')
    async def skin(self,ctx,user):
        url = "https://api.mojang.com/users/profiles/minecraft/" + user
        response = requests.get(url)
        result = json.loads(response.text)
        uuid = result['id']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        }
        uuid = uuid.strip()
        url = "https://crafatar.com/renders/body/" + uuid + "?size=512&default=MHF_Steve&overlay=true.png"

        response = requests.get(url,headers=headers,stream=True)
        response.raw.decode_content = True
        if response.status_code == 200:
            with open("mc.png", 'wb') as f:
                shutil.copyfileobj(BytesIO(response.content), f)
        else:
            print('Image Couldn\'t be retrieved :(')
        with open('mc.png', "rb") as fh:
            f = discord.File(fh, filename='mc.png')
        await ctx.send(file=f)
            
    @skin.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=':x: Perfavore fornisci un nome utente valido.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)
            
    @meteo.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=':x: Perfavore fornisci una città valida.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)              
            
    @commands.command(help='check bots ping')
    async def ping(self, ctx):
   
        await ctx.send(f':signal_strength: **Ping Attuale**: {round(self.client.latency * 1000)} ms')                    

    @commands.command(help = 'gives kanye quote')
    async def kanyequote(self, ctx):
        kanyeIMGS = [
          "https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTU0OTkwNDUxOTQ5MDUzNDQ3/kanye-west-attends-the-christian-dior-show-as-part-of-the-paris-fashion-week-womenswear-fall-winter-2015-2016-on-march-6-2015-in-paris-france-photo-by-dominique-charriau-wireimage-square.jpg",
          "https://storage.googleapis.com/afs-prod/media/1f764b198a42470189b99b4084be6cf0/800.jpeg",
          "https://www.gannett-cdn.com/presto/2019/03/07/USAT/71d24511-e504-40e1-95eb-180f883eeb81-LL_MW_KanyeWest_010319.JPG?width=600&height=900&fit=crop&format=pjpg&auto=webp",
          "https://pyxis.nymag.com/v1/imgs/014/a62/bc3a72ed5c47e8c0dd5bc52028c5df5005-kanye-west.2x.rsquare.w330.jpg",
          "https://www.aljazeera.com/wp-content/uploads/2020/09/Ye-1.jpg?resize=770%2C513",
          "https://images.businessoffashion.com/profiles/asset/1797/43897e2e4a6d155d72dd9df352017b546ef9e229.jpeg?auto=format%2Ccompress&fit=crop&h=360&w=660",
          "https://i.insider.com/5f624c55323fc4001e0d6a47?width=2000&format=jpeg&auto=webp",
          "https://www.wmagazine.com/wp-content/uploads/2019/10/25/5db30d540e538e000830c68a_GettyImages-1183294345.jpg?w=1352px",
          "https://i.guim.co.uk/img/media/07ad3146c3879e9d3da5e81aa32edf7160b93888/0_195_2326_1396/master/2326.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=8bdf6ca2f739479415c3a3b6d8fe890a",
      ]
        pick_img = random.choice(kanyeIMGS)

        response = requests.get('https://api.kanye.rest')
        data = response.json()

        embed = discord.Embed(
            title="From the Words of Kanye West:",
            description=f'"{data["quote"]}"',
            color=0,
      )

        embed.set_footer(
            text=f"Richiesto da {ctx.author}", icon_url=ctx.author.avatar_url
      )
        embed.set_thumbnail(url=pick_img)

        await ctx.message.reply(embed=embed)   

    @commands.command(aliases=['qr'], help = "Genera un codice QR")
    async def qrcode(self, ctx, *, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",
                            back_color="white").convert('RGB')
        img.save('qrcode.png')
        await ctx.message.reply(file=discord.File('qrcode.png'))    
        
    @qrcode.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=':x: Perfavore fornisci contenuto da mettere nel codice QR.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)         
    
def setup(client):
    client.add_cog(Fun(client))
