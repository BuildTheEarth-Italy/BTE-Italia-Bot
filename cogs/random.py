import discord, random
from discord.ext import commands

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

def setup(client):
    client.add_cog(Fun(client))
