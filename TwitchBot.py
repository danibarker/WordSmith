
from twitchio.ext import commands
import dictionary
f = open('config.dat','r')
irct = f.readline()
clienti = f.readline()
nickn = f.readline().strip().lower()
initc = f.readline().split(',')
lexicon = f.readline()
f.close()
bot = commands.Bot(
    # set up the bot
    irc_token=irct,
    client_id=clienti,
    nick=f'{nickn}',
    prefix='!',
    initial_channels=initc
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print('it is online!')
@bot.event
async def event_message(ctx):
    await bot.handle_commands(ctx)


@bot.command(name='define')
async def define(ctx,word):
    msg = dictionary.define(word.upper())
    await ctx.send(msg)

@bot.command(name='related')
async def related(ctx,word):
    msg = dictionary.related(word.upper())
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='startswith')
async def startswith(ctx,word):
    msg = dictionary.starts_with(word.upper())
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='endswith')
async def endswith(ctx,word):
    msg = dictionary.ends_with(word.upper())
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='contains')
async def contains(ctx,word):
    msg = dictionary.contains(word.upper())
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='pattern')
async def pattern(ctx,word):
    msg = dictionary.pattern(word.upper())
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='regex')
async def regex(ctx,word):
    msg = dictionary.regex(word.upper())
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')

@bot.command(name='info')
async def info(ctx,word):
    msg = dictionary.info(word.upper())
    await ctx.send(msg)


@bot.command(name='anagram')
async def anagram(ctx,word):
    msg = dictionary.anagram_1(word.upper())
    num = msg[0]
    msg = msg[1]
    print(len(msg))
    await ctx.send(f'{num} results found:\n{msg}')


@bot.command(name='random')
async def random(ctx):
    msg = dictionary.random_word()
    await ctx.send(msg)

@bot.command(name='pronounce')
async def pronounce(ctx, word):
    if word.upper() in dictionary.wordlist:
        await ctx.send(f'https://www.collinsdictionary.com/sounds/hwd_sounds/en_gb_{word}.mp3')
    else:
        await ctx.send(f'{word} is not a valid word')
bot.run()