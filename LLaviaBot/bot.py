import discord
from discord.ext import commands
from TOKEN import token
from utils.lol import Lol

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='>', description='League of legends bot',intents=intents)
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
cliente = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print('I am ready')
    print(bot.user.name)
    print(bot.user.id)


@bot.command()
async def hi(ctx):
    await ctx.send('Hola como estas?')

@bot.command()
async def add(ctx, *, summoner: str):
    if '#' in summoner:
        parts = summoner.rsplit('#',1)
        if len(parts) == 2:
            summoner = parts[0].strip()
            tag = parts[1].strip()
            lol = Lol(summoner, tag)
            lol.rank()
        else:
            await ctx.send("Formato incorrecto. Debe ser 'Nombre#Etiqueta'.")
    else:
        await ctx.send("Debe incluir '#' para separar el Nombre de la Etiqueta.")
    




bot.run(token)