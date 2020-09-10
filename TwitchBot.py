
from twitchio.ext import commands
import twitchio as tw
import dictionary
import config as cf

config = cf.config()
initc = config.channels.keys()
bot = commands.Bot(
    # set up the bot
    irc_token=config.irc_token,
    client_id=config.client_id,
    nick=config.nick,
    prefix='!',
    initial_channels=initc
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print('Online')
@bot.event
async def event_message(ctx):
    await bot.handle_commands(ctx)
    

@bot.command(name='define')
async def define(ctx,word):
    msg = dictionary.define(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    await ctx.send(msg)

@bot.command(name='lexicon')
async def lexicon(ctx,word):
    if ctx.author.name == ctx.channel.name:
        config.channels[ctx.channel.name]["lexicon"]=word.lower()
        cf.save(config)
        msg = f'Lexicon changed to {word.lower()}'
    else:
        msg = f'Command can only be used by {ctx.channel.name}'
    await ctx.send(msg)

@bot.command(name='related')
async def related(ctx,word):
    msg = dictionary.related(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='startswith')
async def startswith(ctx,word):
    msg = dictionary.starts_with(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='endswith')
async def endswith(ctx,word):
    msg = dictionary.ends_with(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='contains')
async def contains(ctx,word):
    msg = dictionary.contains(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='pattern')
async def pattern(ctx,word):
    msg = dictionary.pattern(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='regex')
async def regex(ctx,word):
    msg = dictionary.regex(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='info')
async def info(ctx,word):
    msg = dictionary.info(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    await ctx.send(msg)


@bot.command(name='anagram')
async def anagram(ctx,word):
    msg = dictionary.anagram_1(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')


@bot.command(name='random')
async def random(ctx):
    msg = dictionary.random_word(config.channels[ctx.channel.name]["lexicon"])
    await ctx.send(msg)

@bot.command(name='pronounce')
async def pronounce(ctx, word):
    if word.upper() in dictionary.wordlist[config.channels[ctx.channel.name]["lexicon"]]:
        await ctx.send(f'https://www.collinsdictionary.com/sounds/hwd_sounds/en_gb_{word.lower()}.mp3')
    else:
        await ctx.send(f'{word} is not a valid word')
@bot.command(name='crypto')
async def crypto(ctx, word):
    msg = dictionary.crypto(word.upper(),config.channels[ctx.channel.name]["lexicon"])
    num = msg[0]
    msg = msg[1]
    await ctx.send(f'{num} results found:\n{msg}')
bot.run()