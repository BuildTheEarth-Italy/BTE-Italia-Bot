import discord, random
from discord.ext import commands
import requests
import json
import shutil
from io import BytesIO
import qrcode
import wikipedia
import asyncio


class Random(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
                       
        
    @commands.hybrid_command(
        name='fact',
        description='Will send a random fact.',
        usage='£fact',
        brief='Gives random fact',
        aliases=["fatto", "curiosità", "curiosita"]
    )
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

        fact_file = open("/home/container/utils/facts.txt", mode="r", encoding="utf8")
        fact_file_facts = fact_file.read().split("\n")
        fact_file.close()

        for i in fact_file_facts:
            if i == "": fact_file_facts.remove(i)

        facts = facts + fact_file_facts
        
        message = discord.Embed(title="BTE Italia <:bte_italy:991738968725000433> ", colour=discord.Colour.orange())
        message.add_field(name=":face_with_monocle: Curiosità:", value=random.choice(facts), inline=True)
        await ctx.send(embed=message)        
        
    @commands.hybrid_command(
        name='fact_en',
        description='Will send a random fact.',
        usage='£fact_en',
        brief='Gives random fact',
        aliases=["curiosity"]
    )
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

        fact_file = open("/home/container/utils/facts_en.txt", mode="r", encoding="utf8")
        fact_file_facts = fact_file.read().split("\n")
        fact_file.close()

        for i in fact_file_facts:
            if i == "": fact_file_facts.remove(i)

        facts = facts + fact_file_facts

        message = discord.Embed(title="BTE Italia <:bte_italy:991738968725000433> ", colour=discord.Colour.orange())
        message.add_field(name=":face_with_monocle: Curiosity:", value=random.choice(facts), inline=True)
        await ctx.send(embed=message)        
        
    @commands.hybrid_command(
        name='eightball',
        description='Will give a random response to your provided question.',
        usage='£8ball (Question)',
        brief='Gives random response',
        aliases=["8ball", "magicball", "eight ball", "8 ball", "magic ball"]
    )
    async def eightball(self, ctx, *, question):
        responses = ["Ovvio. Che cosa ti aspettavi?",
                    'Non c’è alcun dubbio su tale affermazione.',
                    'Puoi scommetterci.',
                    'Direi proprio di sì.',
                    'Assolutamente sì.',
                    'A mio parere, sì.',
                    'Molto probabilmente.',
                    'Affermativo.',
                    'Buone probabilità.',
                    'L’oroscopo di Hannibal mi dice di sì.',
                    'Domanda confusa, riprova.',
                    'Te lo dirò quando sarai più grande.',
                    "Riprova più tardi.",
                    'No puedo.',
                    'Concentrati e riprova.',
                    'Non contarci.',
                    'Le probabilità non sono buone.',
                    'Il Lato Oscuro della Forza prevale.',
                    'Credo proprio di no.',
                    'Ma assolutamente no.']

        message = discord.Embed(title=":8ball: 8 Ball", colour=discord.Colour.orange())
        message.add_field(name=":question: Domanda:", value=question, inline=False)
        message.add_field(name=":pencil: Risposta:", value=random.choice(responses), inline=False)
        await ctx.send(embed=message)        
        
    @commands.hybrid_command(
        name='stupid',
        description='Measures how stupid someone is.',
        usage='£stupid (User)',
        brief='Measures how stupid a user is',
        aliases=["stupido"]
    )
    async def stupid(self, ctx, member = None):
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

        else:
            converter = commands.MemberConverter()
            member = converter.convert(ctx, member)

            if member.id == (477570902075113472):
                message = await ctx.channel.send("Calcolando...")
                await asyncio.sleep(3)
                await message.edit(content=f"{member.mention} è 100% stupido!")

            elif member.id == self.bot.user.id:
                message = await ctx.channel.send("Calcolando...")
                await asyncio.sleep(3)
                await message.edit(content=f"Sono troppo intelligente, anullando calcolo...")

            else:
                message = await ctx.channel.send("Calcolando...")
                await asyncio.sleep(3)
                await message.edit(content=f"{member.mention} è {percentage}% stupido!")
                
                
    @commands.hybrid_command(
        name='meteo',
        description='Will send weather information of provided city.',
        usage='£meteo (City)',
        brief='Weather information',
        aliases=["weather"]
    )
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
            embed.add_field(name="Errore", value="Per favore metti il nome di una città", inline=True)
            await ctx.send(embed=embed)       
            
    @commands.hybrid_command(
        name='skin',
        description='Will send provided users skin.',
        usage='£skin (User)',
        brief='Gather users skin',
        aliases=["pelle"]
    )
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
            with open("/home/container/utils/mc.png", 'wb') as f:
                shutil.copyfileobj(BytesIO(response.content), f)
        else:
            print('Image Couldn\'t be retrieved :(')
        with open('/home/container/utils/mc.png', "rb") as fh:
            f = discord.File(fh, filename='/home/container/utils/mc.png')
        await ctx.send(file=f)

    @commands.hybrid_command(
        name='testa',
        description='Will send provided users head.',
        usage='£testa (User)',
        brief='Gather users head',
        aliases=["head"]
    )
    async def testa(self,ctx,user):
        url = "https://api.mojang.com/users/profiles/minecraft/" + user
        response = requests.get(url)
        result = json.loads(response.text)
        uuid = result['id']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        }
        uuid = uuid.strip()
        url = "https://crafatar.com/renders/head/" + uuid + "?size=512&default=MHF_Steve&overlay=true.png"

        response = requests.get(url,headers=headers,stream=True)
        response.raw.decode_content = True
        if response.status_code == 200:
            with open("/home/container/utils/head.png", 'wb') as f:
                shutil.copyfileobj(BytesIO(response.content), f)
        else:
            print('Image Couldn\'t be retrieved :(')
        with open('/home/container/utils/head.png', "rb") as fh:
            f = discord.File(fh, filename='/home/container/utils/head.png')
        await ctx.send(file=f)

    @commands.hybrid_command(
        name='faccia',
        description='Will send provided users avatar.',
        usage='£faccia (User)',
        brief='Gather users avatar',
        aliases=["face"]
    )
    async def faccia(self,ctx,user):
        url = "https://api.mojang.com/users/profiles/minecraft/" + user
        response = requests.get(url)
        result = json.loads(response.text)
        uuid = result['id']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        }
        uuid = uuid.strip()
        url = "https://crafatar.com/avatars/" + uuid + "?size=512&default=MHF_Steve&overlay=true.png"

        response = requests.get(url,headers=headers,stream=True)
        response.raw.decode_content = True
        if response.status_code == 200:
            with open("/home/container/utils/faccia.png", 'wb') as f:
                shutil.copyfileobj(BytesIO(response.content), f)
        else:
            print('Image Couldn\'t be retrieved :(')
        with open('/home/container/utils/faccia.png', "rb") as fh:
            f = discord.File(fh, filename='/home/container/utils/faccia.png')
        await ctx.send(file=f)

    @faccia.error
    @testa.error         
    @skin.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=':x: Per favore inserisci un nome Minecraft valido.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)    
            
    @meteo.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=':x: Per favore fornisci una città valida.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)              
            
    @commands.hybrid_command(
        name='ping',
        description='Will send bots ping.',
        usage='£ping',
        brief='Bots ping',
        aliases=["latency"]
    )
    async def ping(self, ctx):
   
        await ctx.send(f':signal_strength: **Ping Attuale**: {round(self.bot.latency * 1000)} ms')                    


    @commands.hybrid_command(
        name='kanyequote',
        description='Will send a random Kanye West Quote.',
        usage='£kanyequote',
        brief='Gives random Kanye quote',
        aliases=["kq", "kanye", "quote"]
    )
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
            text=f"Richiesto da {ctx.author}", icon_url=ctx.author.avatar.url
      )
        embed.set_thumbnail(url=pick_img)

        await ctx.message.reply(embed=embed)   



    @commands.hybrid_command(
        name='qrcode',
        description='Will generate QR code with provided content.',
        usage='£qrcode (Content)',
        brief='Generates QR code',
        aliases=["qr"]
    )
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
        img.save('/home/container/utils/qrcode.png')
        await ctx.message.reply(file=discord.File('/home/container/utils/qrcode.png'))    
        
    @qrcode.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=':x: Per favore fornisci contenuto da mettere nel codice QR.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)         
    
    @commands.hybrid_command(
        name='wikipedia',
        description='Will send wikipedia article of provided argument.',
        usage='£wikipedia (Argument)',
        brief='Wikipedia article of argument',
        aliases=["wiki"]
    )
    async def wiki(self, ctx, *, query):
        embed = discord.Embed(title="Wikipedia", description="Ricercando {}".format(query), color=0x00ff00)
        page = wikipedia.summary(query, sentences=500)
        url = wikipedia.page(query).url
        embed.description = page
        embed.add_field(name="Link", value=url ,inline=False)
        await ctx.send(embed=embed)



    @commands.hybrid_command(
        name='wikisearch',
        description='Will research for arguments provided on wikipedia.',
        usage='£wikisearch (Argument)',
        brief='Does a wiki search',
        aliases=["ricerca"]
    )
    async def wikisearch(self, ctx, *, query):
        await ctx.send(wikipedia.search(query))



    @commands.hybrid_command(
        name='covid',
        description='Will send a covid statistic of a provided country.',
        usage='£covid (Country)',
        brief='Covid information on a country',
        aliases=["covid-19", "covid19", "coronavirus", "coronavirus19", "coronavirus-19", "corona", "virus"]
    )
    async def covid(self, ctx,*, country):
        x = country.replace(" ", "%20")
        try:
            url = f"https://coronavirus-19-api.herokuapp.com/countries/{x}"
            stats = requests.get(url)
            json_stats = stats.json()
            country = json_stats["country"]
            totalCases = json_stats["cases"]
            todayCases = json_stats["todayCases"]
            totalDeaths = json_stats["deaths"]
            todayDeaths = json_stats["todayDeaths"]
            recovered = json_stats["recovered"]
            active = json_stats["active"]
            critical = json_stats["critical"]
            casesPerOneMil = json_stats["casesPerOneMillion"]
            deathsPerOneMil = json_stats["deathsPerOneMillion"]
            totalTests = json_stats["totalTests"]
            testsPerOneMil = json_stats["testsPerOneMillion"]

            e = discord.Embed(
                title=f"Statistiche Covid-19 su {country}",
                description="Non si tratta di informazioni in tempo reale. Pertanto potrebbero non essere così precise, ma sono informazioni approssimative.",
                color=discord.Colour.red()
            )
            e.add_field(name="Totale Casi", value=totalCases, inline=True)
            e.add_field(name="Casi Di Oggi", value=todayCases, inline=True)
            e.add_field(name="Totale Morti", value=totalDeaths, inline=True)
            e.add_field(name="Morti Di Oggi", value=todayDeaths, inline=True)
            e.add_field(name="Recoverati", value=recovered, inline=True)
            e.add_field(name="Attivi", value=active, inline=True)
            e.add_field(name="Critici", value=critical, inline=True)
            e.add_field(name="Casi Su Un Millione", value=casesPerOneMil, inline=True)
            e.add_field(name="Morti Su Un Millione", value=deathsPerOneMil, inline=True)
            e.add_field(name="Tamponi Su Un Millione", value=testsPerOneMil, inline=True)
            e.add_field(name="Totale Tamponi", value=totalTests, inline=True)
            e.set_thumbnail(url="https://www.osce.org/files/imagecache/10_large_gallery/f/images/hires/8/a/448717.jpg")

            await ctx.send(embed=e)
        except:
            await ctx.send(f"Nome del paese non valido o errore API! Riprovare più tardi.")    



    @commands.hybrid_command(
        name='chucknorris',
        description='Will send random chucknorris fact or quote.',
        usage='£chucknorris',
        brief='Chucknorris quote or fact',
        aliases=["cn", "chuck", "norris", "chuck norris"]
    )
    async def chucknorris(self, ctx):
        url = 'https://api.chucknorris.io/jokes/random'
        jokeJSON = requests.get(url).json()['value']
        message = discord.Embed(title="BTE Italia <:bte_italy:991738968725000433> ", colour=discord.Colour.orange())
        message.add_field(name=":cowboy: Chuck Norris:", value=jokeJSON, inline=True)
        await ctx.send(embed=message)



    @commands.hybrid_command(
        name='advice',
        description='Will send random life advice.',
        usage='£advice',
        brief='Life advice',
        aliases=["consiglio"]
    )
    async def advice(self, ctx):
        url = 'https://api.adviceslip.com/advice'
        r = requests.get(url).json()
        advice = {
        'advice' : r['slip']['advice']
        }
        message = discord.Embed(title="BTE Italia <:bte_italy:991738968725000433> ", colour=discord.Colour.orange())
        message.add_field(name=":innocent: Advice:", value=advice['advice'], inline=True)
        await ctx.send(embed=message)


       
    @commands.hybrid_command(
        name='ftopayrespect',
        description='Send F to pay respect.',
        usage='£f',
        brief='Pay respect',
        aliases=["f", "pressf", "press f", "F"]
    )
    async def ftopayrespects(self, ctx):
        sender = ctx.message.author
        hearts = [
            ':heart:',
            ':purple_heart:',
            ':blue_heart:',
            ':green_heart:'
        ]
        await ctx.send("{} ha reso omaggio {}".format(sender.mention, random.choice(hearts)))



    @commands.hybrid_command(
        name='dadjoke',
        description='Sends a Dad joke.',
        usage='£dadjoke',
        brief='Dad joke',
        aliases=["dj", "joke", "dad"]
    )
    async def dadjoke(self, ctx):
        url = 'https://icanhazdadjoke.com/'
        joke = requests.get(url, headers={"Accept":'application/json '}).json()
        message = discord.Embed(title="BTE Italia <:bte_italy:991738968725000433> ", colour=discord.Colour.orange())
        message.add_field(name=":bearded_person: Dad Joke:", value=joke['joke'], inline=True)
        await ctx.send(embed=message)



    @commands.hybrid_command(
        name='flip',
        description='Will flip a coin, heads or tail.',
        usage='£coinflip',
        brief='Flips a coin',
        aliases=["cf", "coinflip", "coin"]
    )
    async def flip(self, ctx, user : discord.Member=None):
        if user != None:
            msg = ""
            if user.id == self.bot.user.id:
                user = ctx.message.author
                msg = "Nice try. You think this is funny? How about *this* instead:\n\n"
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await ctx.send(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await ctx.send("*Lancia una moneta e... " + random.choice(["TESTA!*", "CROCE!*"]))        
        
async def setup(bot):
    await bot.add_cog(Random(bot))
