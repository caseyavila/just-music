import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import datetime
import random
import os


admin_list = ['kc#0123']

TOKEN = os.environ.get('TOKEN')
bot = commands.Bot(command_prefix = '_')

ytdl_opts = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_opts = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
ytdl = YoutubeDL(ytdl_opts)


class music():
    def __init__(self, url):
        self.url = url
        self.data = ytdl.extract_info(self.url, download=False)
        self.title = self.video()['title']
        self.webpage_url = self.video()['webpage_url']
        self.thumbnail_url = self.video()['thumbnail']

    def video(self):
        # Enable search compatibility with youtube_dl search
        if self.data['extractor'] == 'youtube:search':
            return self.data['entries'][0]
        else:
            return self.data

    def duration(self):
        seconds = int(self.video()['duration'])
        return str(datetime.timedelta(seconds=seconds))

    def stream_url(self):
        return self.video()['formats'][0]['url']

    def audio_source(self):
        audio = discord.FFmpegPCMAudio(self.stream_url(), before_options=ffmpeg_opts)
        return audio


class scheduling():  # Class for managing queues for different guilds
    def __init__(self):
        self.queues = {}

    def add_queue(self, guild_id):
        self.queues[guild_id] = []

    def song_list(self, guild_id):
        try:
            return self.queues[guild_id]
        except KeyError:
            self.add_queue(guild_id)
            return self.queues[guild_id]

    def add_song(self, guild_id, song):
        self.song_list(guild_id).append(song)

    def remove_queue(self, guild_id):
        del self.queues[guild_id]


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
async def rename(ctx, *, name):
    if str(ctx.message.author) in admin_list:
        await bot.user.edit(username=name)
    else:
        await ctx.send('ur not allowed to do that...')


@bot.command()
async def play(ctx, *, url):  # Accept any arguments including spaces
    await connect(ctx)  # Connect to the user's voice channel

    song = music(url)
    voice_client = ctx.voice_client
    
    schedule.add_song(ctx.guild.id, song)

    if voice_client.is_playing():
        await ctx.send('`{}` added to queue.'.format(song.title))
    else:
        voice_client.play(song.audio_source(), after=lambda _: next_song(ctx))
        await ctx.send('Now playing: `{}`'.format(song.title))


@bot.command()
async def queue(ctx):
    embed = discord.Embed(color=0xf7ecb2, title='Queue')
    for index, song in enumerate(schedule.song_list(ctx.guild.id)):
        if index == 0:
            # Embed links in the title of each song
            embed.add_field(name='Now playing - use "np" for more info', value='[{}]({})'.format(song.title, song.webpage_url), inline=False)
        else:
            embed.add_field(name=index, value='[{}]({})'.format(song.title, song.webpage_url), inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def np(ctx):
    embed = discord.Embed(color=0xf7ecb2, title='Now Playing')
    embed.set_thumbnail(url=schedule.song_list(ctx.guild.id)[0].thumbnail_url)
    embed.add_field(name='Title', value=schedule.song_list(ctx.guild.id)[0].title, inline=False)
    embed.add_field(name='Length', value=schedule.song_list(ctx.guild.id)[0].duration(), inline=False)
    embed.add_field(name='URL', value=schedule.song_list(ctx.guild.id)[0].webpage_url, inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def remove(ctx, index :int):
    song_list = schedule.song_list(ctx.guild.id)
    del song_list[index]
    await ctx.send('Removed song #{} from the queue.'.format(index))


@bot.command()
async def clear(ctx):
    schedule.remove_queue(ctx.guild.id)
    await ctx.send('The queue has been cleared.')


@bot.command()
async def skip(ctx):
    ctx.voice_client.stop()
    await ctx.send('Skipped! (｡•̀ᴗ-)✧')

def next_song(ctx):
    del schedule.song_list(ctx.guild.id)[0]
    ctx.voice_client.play(schedule.song_list(ctx.guild.id)[0].audio_source(), after=lambda _: next_song(ctx))


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
    schedule.remove_queue(ctx.guild.id)
    ctx.voice_client.stop()


# Joins the voice channel if the user that sends the command
@bot.command()
async def connect(ctx):
    author_channel = ctx.author.voice.channel
    if ctx.voice_client:
        await ctx.voice_client.move_to(author_channel)
    else:
        voice_client = await author_channel.connect()


@bot.command()
async def disconnect(ctx):
    schedule.remove_queue(ctx.guild.id)
    await ctx.voice_client.disconnect()


@rename.error
async def rename_error(ctx, error):
    print(error)
    await ctx.send('```{}```'.format(error))

schedule = scheduling()

bot.run(TOKEN)

