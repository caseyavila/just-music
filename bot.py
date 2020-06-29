import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from googletrans import Translator
import datetime
import random
import os


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

translator = Translator()


class Music():
    def __init__(self, url):
        self.url = url
        self.data = ytdl.extract_info(self.url, download=False)
        self.title = self.video()['title']
        self.webpage_url = self.video()['webpage_url']
        self.thumbnail_url = self.video()['thumbnail']
        self.loop = False

    def video(self):
        # Enable search compatibility with youtube_dl search
        if self.data['extractor'] == 'youtube:search':
            return self.data['entries'][0]
        else:
            return self.data

    def duration(self):
        if self.video()['is_live']:
            return '∞'
        else:
            seconds = int(self.video()['duration'])
            return str(datetime.timedelta(seconds=seconds))

    def stream_url(self):
        return self.video()['formats'][0]['url']

    def audio_source(self):
        audio = discord.FFmpegPCMAudio(self.stream_url(), before_options=ffmpeg_opts)
        return audio

    def set_loop(self, boolean):
        self.loop = boolean

    def is_loop(self):
        return self.loop


# Class for managing queues for different guilds
class Scheduling():
    def __init__(self):
        self.queues = {}

    def get_queue(self, guild_id):
        try:
            return self.queues[guild_id]
        except KeyError:
            self.add_queue(guild_id)
            return self.queues[guild_id]

    def add_queue(self, guild_id):
        self.queues[guild_id] = []

    def remove_queue(self, guild_id):
        del self.queues[guild_id]

    def add_song(self, guild_id, song):
        self.get_queue(guild_id).append(song)

# Construct Scheduling object
schedule = Scheduling()


@bot.command()
async def hello(ctx):
    await ctx.send('Hello there!')


@bot.command()
async def igger(ctx):
    embed = discord.Embed(color=0x693f1a)
    embed.set_author(name='Amanda O')
    embed.add_field(name='04/01/2020', value='Because it’s too close to the n word. \nIf you replace the underscore with an n, it’s a very offensive racial slur. \nIf you change the name to something more appropriate, I’d be glad to remove it.', inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def rng(ctx, max: int):
    await ctx.send(random.randint(1, max))

# Beginning of voice/music commands

# Accept any arguments including spaces
@bot.command()
async def play(ctx, *, url):  
    # Connect to the user's voice channel
    await connect(ctx)

    # If connection to the voice channel succedes
    if ctx.voice_client:
        # Construct Music object
        song = Music(url)
        
        # Add Music object to queue
        schedule.add_song(ctx.guild.id, song)

        if ctx.voice_client.is_playing():
            await ctx.send('`{}` added to queue.'.format(song.title))
        else:
            ctx.voice_client.play(song.audio_source(), after=lambda _: next_song(ctx))
            await ctx.send('Now playing: `{}`'.format(song.title))


@bot.command()
async def queue(ctx):
    embed = discord.Embed(color=0xf7ecb2, title='Queue')
    # If there is something in the queue
    if schedule.get_queue(ctx.guild.id):
        for index, song in enumerate(schedule.get_queue(ctx.guild.id)):
            if index == 0:
                # Embed links in the title of each song
                embed.add_field(name='Now playing:', value='[{}]({})'.format(song.title, song.webpage_url), inline=False)
            else:
                embed.add_field(name='{}:'.format(index), value='[{}]({})'.format(song.title, song.webpage_url), inline=False)
        await ctx.send(embed=embed)
     # If nothing is in the queue
    else:
        await ctx.send('There is nothing in the queue!')


@bot.command(aliases=['now', 'current', 'currentsong', 'playing'])
async def np(ctx):
    if schedule.get_queue(ctx.guild.id):
        song_list = schedule.get_queue(ctx.guild.id)
        embed = discord.Embed(color=0xf7ecb2, title='Now Playing')
        embed.set_thumbnail(url=schedule.get_queue(ctx.guild.id)[0].thumbnail_url)
        embed.add_field(name='Title', value=song_list[0].title, inline=False)
        embed.add_field(name='Length', value=song_list[0].duration(), inline=False)
        embed.add_field(name='URL', value=song_list[0].webpage_url, inline=False)
        embed.add_field(name='Looping', value=song_list[0].is_loop(), inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('There is nothing playing right now!')


@bot.command()
async def remove(ctx, index :int):
    # Prevent removing song number 0
    if index > 0:
        song_list = schedule.get_queue(ctx.guild.id)
        title = song_list[index].title
        del song_list[index]
        await ctx.send('Removed `{}` from the queue.'.format(title))


@bot.command()
async def clear(ctx):
    schedule.remove_queue(ctx.guild.id)
    await ctx.send('The queue has been cleared.')


@bot.command()
async def skip(ctx):
    # Remove loop
    schedule.get_queue(ctx.guild.id)[0].set_loop(False)
    # Stop playing music
    ctx.voice_client.stop()
    await ctx.send('Skipped! (｡•̀ᴗ-)✧')

def next_song(ctx):
    song_list = schedule.get_queue(ctx.guild.id)
    # If the song is set to loop
    if song_list[0].is_loop():
        pass
    else:
        del song_list[0]
    ctx.voice_client.play(song_list[0].audio_source(), after=lambda _: next_song(ctx))


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


@bot.command()
async def loop(ctx):
    song = schedule.get_queue(ctx.guild.id)[0]
    if song.is_loop():
        song.set_loop(False)
        await ctx.send('Stopped looping: `{}`'.format(song.title))
    else:
        song.set_loop(True)
        await ctx.send('Started looping: `{}`'.format(song.title))


@bot.command()
async def connect(ctx):
    # Joins the voice channel if the user that sends the command
    try:
        author_channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(author_channel)
        else:
            voice_client = await author_channel.connect()
    # If the command sender is not in a voice channel
    except AttributeError:
        await ctx.send('But you\'re not in a voice channel... ◑﹏◐')


@bot.command()
async def disconnect(ctx):
    schedule.remove_queue(ctx.guild.id)
    await ctx.voice_client.disconnect()

# End of voice/music commands
# Beginning of translation commands

@bot.command()
async def english(ctx, *, words):
    translation = translator.translate(words, dest='en')
    await ctx.send(translation.text)


@bot.command()
async def chinese(ctx, *, words):
    # Traditional chinese trnaslation
    translation = translator.translate(words, dest='zh-tw')
    # Send pinyin pronunciation
    await ctx.send('{} - {}'.format(translation.text, translation.pronunciation))


@bot.command()
async def spanish(ctx, *, words):
    translation = translator.translate(words, dest='es')
    await ctx.send(translation.text)


@bot.command()
async def french(ctx, *, words):
    translation = translator.translate(words, dest='fr')
    await ctx.send(translation.text)


@bot.command()
async def japanese(ctx, *, words):
    translation = translator.translate(words, dest='ja')
    # Send romaji pronunciation
    await ctx.send('{} - {}'.format(translation.text, translation.pronunciation))


@bot.command()
async def korean(ctx, *, words):
    translation = translator.translate(words, dest='ko')
    # Send latin pronunciation
    await ctx.send('{} - {}'.format(translation.text, translation.pronunciation))


bot.run(TOKEN)

