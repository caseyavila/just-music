# just-music
An open-source Discord bot for you and your greatest of friends.

Intended to be run with Heroku. However, it can be run locally.

## Features
- [x] Youtube Music
- [x] Queing
- [x] Looping
- [x] Other basic music commands: np, stop, pause, resume, clear, etc.
- [x] Translation to English, Spanish, French, Chinese (traditional and simplified), and Japanese
- [ ] Soundcloud
- [ ] Spotify
- [ ] Bandcamp
- [ ] Other stuff... Open an issue to let me know of anything you want added!

## How to Use 

### Adding the bot
To add the bot to your own discord server, simply click [here](https://discord.com/api/oauth2/authorize?client_id=621598762657120256&permissions=238550848&scope=bot) and authorize!

### Commands
This bot uses the `_` prefix for its commands

#### Music
- `_play <query>` or `_play <youtube url>`: Search youtube for a song and stream it to the voice channel you are currently in. (This will also add songs to the queue if there is already one playing)
- `_pause`: Pause the current song
- `_resume`: Resume the current song
- `_skip`: Skip the current song and move to the next in queue
- `_queue`: View the contents of the queue
- `_clear`: Clear the song queue
- `_reset`: Clear the song queue, including the current song (This can break some things)
- `_remove <number>`: Remove a specific song from the queue
- `_np`, `_now`, `_current`, `_currentsong`, `_playing`: View information about the current song
- `_loop`: Toggle looping of the current song
- `_stop`: Stop playing music
- `_connect`: Summon the bot to your current voice channel
- `_disconnect`: Remove the bot from your channel

#### Translation
Through use of the Google Translate API, this discord bot can translate messages into different languages! The language from which text is translated is automatically detected, though the target langugage must be specified through the command.

- `_english <phrase>`: Translate something to english
- `_simplified <phrase>`: Translate something to simplified chinese
- `_traditional <phrase>`: Translate something to traditional chinese
- `_spanish <phrase>`
- `_french <phrase>`
- `_japanese <phrase>`
- `_korean <phrase>`

#### Miscellaneous
- `_hello`: Hello there!
- `_servercount`: View how many servers this bot is in
- `_rng <integer>`: Generate a random integer between 1 and any number

