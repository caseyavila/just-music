import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import random
import os

admin_list = ['kc#0123']

TOKEN = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix = '_')

ytdlopts = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = YoutubeDL(ytdlopts)


# class audio_source():
#     def __init__(self, url):
#         self.url = url
# 
#     def init


@bot.command()
async def hello(ctx):
    await ctx.send('Hello there')


@bot.command()
async def igger(ctx):
    embed = discord.Embed(color=0x693f1a)
    embed.set_author(name='Amanda O', icon_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/248/baby_dark-skin-tone_1f476-1f3ff_1f3ff.png')
    embed.add_field(name='04/01/2020', value='Because it’s too close to the n word. \nIf you replace the underscore with an n, it’s a very offensive racial slur. \nIf you change the name to something more appropriate, I’d be glad to remove it.', inline=True)
    await ctx.send(embed=embed)


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
async def play(ctx, url):
    await connect(ctx)

    voice_client = ctx.voice_client

#    if voice_client.is_playing():

    data = ytdl.extract_info(url, download=False)
    stream_url = data['formats'][0]['url']

    audio = discord.FFmpegPCMAudio(stream_url)
    voice_client.play(audio)


@bot.command()
async def pause(ctx):
    voice_client = ctx.voice_client
    if not voice_client.is_paused():
        voice_client.pause()


@bot.command()
async def resume(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_paused():
        voice_client.resume()


@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    voice_client.stop()


# Joins the voice channel if the user that sends the command
@bot.command()
async def connect(ctx):
    author_channel = ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.move_to(author_channel)
    else:
        voice_client = await author_channel.connect()


@rename.error
async def rename_error(ctx, error):
    print(error)
    await ctx.send('```{}```'.format(error))


bot.run(TOKEN)

