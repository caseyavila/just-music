import discord
from discord.ext import commands
import random
import os

TOKEN = os.environ.get('TOKEN')

bot = commands.Bot(command_prefix = '_')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello there')

@bot.command()
async def rng(ctx, max: int):
    await ctx.send(random.randint(1, max))

@bot.command()
async def rename(ctx, name):
    await bot.user.edit(username=name)
    print('rename ended')

@rename.error
async def rename_error(ctx, error):
    print(error)
    await ctx.send('i broke, plz fix me: \n' + '```{}```'.format(error))

bot.run(TOKEN)

