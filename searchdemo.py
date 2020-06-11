from youtube_dl import YoutubeDL

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

def extract(url):
    data = ytdl.extract_info(url, download=False)
    file = open('output.txt', 'w')
    file.write(str(data))
    # print(data['entries'][0]['formats'][0]['url'])
    print("file written")

extract('https://www.youtube.com/playlist?list=PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10')
