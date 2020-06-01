import discord
from discord.ext import commands
import random
import os

admin_list = ['kc#0123', 'JustLuck#6936', 'jeff#1275', 'Dahling,SayAhhhhhhh#3332', '123cynhsu#6051']

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
    if str(ctx.message.author) in admin_list:
        await bot.user.edit(username=name)
    else:
        await ctx.send('ur not allowed to do that...')

@bot.command()
async def play(ctx, name):
    await pass

@rename.error
async def rename_error(ctx, error):
    print(error)
    await ctx.send('```{}```'.format(error))

bot.run(TOKEN)

