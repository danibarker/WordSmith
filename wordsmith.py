
from twitchio.ext import commands
import twitchio as tw
import dictionary
import config as cf
import random as rd

config = cf.config()
dictionary.open_files()
initc = config.channels.keys()
custom_commands = cf.custom_commands()

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=config.irc_token, client_id=config.client_id, nick=config.nick, prefix='!',
                         initial_channels=initc)

    async def event_ready(self):
        print(f'Wordsmith 0.2 by Danielle Barker | {self.nick}')

    async def event_message(self, ctx):
        if len(ctx.content) > 1 and ctx.content[0] == '!' and ctx.content[1:] in custom_commands.keys():
            print(ctx.content)
            f = open(custom_commands[ctx.content[1:]], 'r')
            messages = f.read().split('\n')
            message = rd.choice(messages)
            print(len(message))
            await ctx.channel.send(message)
        else:
            await self.handle_commands(ctx)

    @commands.command(name='check')
    async def check(self, ctx, word):
        msg = dictionary.check(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        await ctx.send(msg)

    @commands.command(name='define')
    async def define(self, ctx, word):
        msg = dictionary.define(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        await ctx.send(msg)

    @commands.command(name='lexicon')
    async def lexicon(self, ctx, word):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            config.channels[ctx.channel.name]["lexicon"]=word.lower()
            cf.save(config)
            msg = f'Lexicon changed to {word.lower()}'
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
        await ctx.send(msg)

    @commands.command(name='so')
    async def shoutout(self, ctx, word):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            msg = f'Welcome http://twitch.tv/{word.lower()} !'
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
        await ctx.send(msg)

    @commands.command(name='related')
    async def related(self, ctx, word):
        msg = dictionary.related(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} results found:\n{msg}')

    @commands.command(name='startswith')
    async def startswith(self, ctx, word):
        msg = dictionary.starts_with(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} results found:\n{msg}')

    @commands.command(name='endswith')
    async def endswith(self, ctx, word):
        msg = dictionary.ends_with(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} results found:\n{msg}')

    @commands.command(name='contains')
    async def contains(self, ctx, word):
        msg = dictionary.contains(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} results found:\n{msg}')

    @commands.command(name='pattern')
    async def pattern(self, ctx, word):
        msg = dictionary.pattern(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} results found:\n{msg}')

    @commands.command(name='regex')
    async def regex(self, ctx, word):
        msg = dictionary.regex(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} results found:\n{msg}')

    @commands.command(name='info')
    async def info(self, ctx, word):
        msg = dictionary.info(word.upper(),config.channels[ctx.channel.name]["lexicon"],config.channels[ctx.channel.name]["alphabet"])
        await ctx.send(msg)

    @commands.command(name='anagram')
    async def anagram(self, ctx, word):
        msg = dictionary.anagram_1(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} results found:\n{msg}')

    @commands.command(name='random')
    async def random(self, ctx):
        msg = dictionary.random_word(config.channels[ctx.channel.name]["lexicon"])
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='pronounce')
    async def pronounce(ctx, word):
        if word.upper() in dictionary.wordlist[config.channels[ctx.channel.name]["lexicon"]]:
            await ctx.send(f'https://www.collinsdictionary.com/sounds/hwd_sounds/en_gb_{word.lower()}.mp3')
        else:
            await ctx.send(f'{word} is not a valid word')

    @commands.command(name='crypto')
    async def crypto(ctx, word):
        msg = dictionary.crypto(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        await ctx.send(f'{num} results found:\n{msg}')

bot = Bot()
bot.run()
