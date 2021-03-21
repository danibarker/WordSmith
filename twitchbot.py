
from twitchio.ext import commands
import twitchio as tw
import config as cf
import inflect
import random as rd

config = cf.config()
initc = config.channels.keys()
custom_commands = cf.custom_commands()
engine = inflect.engine()

class TwitchBot(commands.Bot):

    def __init__(self, dictionary):
        super().__init__(irc_token=config.irc_token, client_id=config.client_id, nick=config.nick, prefix='!',
                         initial_channels=initc)
        self.dictionary = dictionary

    async def event_ready(self):
        print(f'Wordsmith 0.3 by Danielle Barker | {self.nick}')

    async def event_message(self, ctx):
        if len(ctx.content) > 1 and ctx.content[0] == '!' and ctx.content[1:] in custom_commands.keys():
            print(ctx.content)
            with open(custom_commands[ctx.content[1:]], 'r') as f:
                messages = list(f)
            message = rd.choice(messages).strip()
            print(len(message))
            await ctx.channel.send(message)
        else:
            await self.handle_commands(ctx)

    @commands.command(name='check')
    async def check(self, ctx, word):
        msg = self.dictionary.check(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        await ctx.send(msg)

    @commands.command(name='define')
    async def define(self, ctx, *words):
        if words and len(words) > 0:
            definitions = []
            msg = None
            length = -2
            for word in words:
                definition = self.dictionary.define(word.upper(),config.channels[ctx.channel.name]["lexicon"])
                length += len(definition) + 2
                if length >= 500:
                    break
                definitions.append(definition)
            msg = '; '.join(definitions)
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
    async def shoutout(self, ctx, name):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            msg = f'Check {name} out at http://twitch.tv/{name.lower()} !'
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
        await ctx.send(msg)

    @commands.command(name='related')
    async def related(self, ctx, word):
        msg = self.dictionary.related(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='startswith')
    async def startswith(self, ctx, word):
        msg = self.dictionary.starts_with(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='endswith')
    async def endswith(self, ctx, word):
        msg = self.dictionary.ends_with(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='contains')
    async def contains(self, ctx, word):
        msg = self.dictionary.contains(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='pattern')
    async def pattern(self, ctx, word):
        msg = self.dictionary.pattern(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='regex')
    async def regex(self, ctx, word):
        msg = self.dictionary.regex(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='hook')
    async def hook(self, ctx, word):
        msg = self.dictionary.hook(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        await ctx.send(msg)

    @commands.command(name='info')
    async def info(self, ctx, word):
        msg = self.dictionary.info(word.upper(),config.channels[ctx.channel.name]["lexicon"],config.channels[ctx.channel.name]["alphabet"])
        await ctx.send(msg)

    @commands.command(name='anagram')
    async def anagram(self, ctx, *words):
        if words and len(words) > 0:
            results = []
            msg = None
            length = -2
            for word in words:
                result = self.dictionary.anagram_1(word.upper(),config.channels[ctx.channel.name]["lexicon"])
                count, words = result
                msg = f'{count} %s:\n{words}' % engine.plural('result', count)
                print(len(msg))
                length += len(msg) + 2
                if length >= 500:
                    break
                results.append(msg)
            msg = '; '.join(results)
            await ctx.send(msg)

    @commands.command(name='bingo')
    async def bingo(self, ctx, length='7'):
        msg = self.dictionary.random_word(int(length), config.channels[ctx.channel.name]["lexicon"])
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='random')
    async def random(self, ctx, length='0'):
        msg = self.dictionary.random_word(int(length), config.channels[ctx.channel.name]["lexicon"])
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='pronounce')
    async def pronounce(self, ctx, word):
        if word.upper() in self.dictionary.wordlist[config.channels[ctx.channel.name]["lexicon"]]:
            await ctx.send(f'https://www.collinsdictionary.com/sounds/hwd_sounds/en_gb_{word.lower()}.mp3')
        else:
            await ctx.send(f'{word} is not a valid word')

    @commands.command(name='crypto')
    async def crypto(self, ctx, word):
        msg = self.dictionary.crypto(word.upper(),config.channels[ctx.channel.name]["lexicon"])
        num = msg[0]
        msg = msg[1]
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

