
from twitchio.ext import commands
import twitchio as tw
import config as cf
import inflect
import random as rd
import re
from api import equity, predict

config = cf.config()
print(config)
initc = config.channels.keys()
custom_commands = cf.custom_commands()
engine = inflect.engine()

class TwitchBot(commands.Bot):

    def __init__(self, dictionary):
        super().__init__(api_token=config.api_token, irc_token=config.irc_token,
                         client_id=config.client_id, nick=config.nick, prefix='!',
                         initial_channels=initc)
        self.dictionary = dictionary

    async def event_ready(self):
        print(f'Wordsmith 0.7 by Danielle Barker | {self.nick}')

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

    def paginate(self, my_result, page='1'):
        num_results = len(my_result)
        msg = ''
        p = int(page)
        for n, word in enumerate(my_result):
            if len(msg) > 450 - len(my_result[n]):
                if p > 1:
                    msg = ''
                    p = p - 1
                else:
                    msg += f'Limited to first {n} results'
                    break
            msg += word + ' '
        return num_results, msg

    @commands.command(name='predict')
    async def predict(self, ctx, opponent):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            msg = predict(config, ctx.channel.name, opponent)
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
        await ctx.send(msg)

    @commands.command(name='check')
    async def check(self, ctx, stem):
        if re.search('[/!]', stem):
            return await ctx.send('Words must not contain / or !')
        offensive, valid = self.dictionary.check(stem.upper(),config.channels[ctx.channel.name]["lexicon"])
        if not offensive:
            if valid:
                msg = stem.upper() + ' is valid VoteYea'
            else:
                msg = stem.upper() + '* not found VoteNay'
            print(len(msg))
            await ctx.send(msg[0:500])

    @commands.command(name='common')
    async def common(self, ctx, stem):
        if re.search('[/!]', stem):
            return await ctx.send('Words must not contain / or !')
        offensive, common = self.dictionary.common(stem.upper(),config.channels[ctx.channel.name]["lexicon"])
        if not offensive:
            if common:
                msg = stem.upper() + ' is common VoteYea'
            else:
                msg = stem.upper() + '* not found VoteNay'
            print(len(msg))
            await ctx.send(msg[0:500])

    @commands.command(name='equity')
    async def equity(self, ctx, *racks):
        if racks and len(racks) > 0:
            lexicon = config.channels[ctx.channel.name]["lexicon"]
            alphabet = config.channels[ctx.channel.name]["alphabet"]
            results = []
            for rack in racks:
                if rack:
                    if re.search('[/!]', rack):
                        return await ctx.send('Racks must not contain / or !')
                    if len(rack) >= 2 and len(rack) <= 5:
                        msg = equity(rack, lexicon)
                    else:
                        msg = rack.upper() + ': ?'
                    results.append(msg)
            msg = '; '.join(results)
            print(len(msg))
            await ctx.send(msg[0:500])

    @commands.command(name='define')
    async def define(self, ctx, *stems):
        if stems and len(stems) > 0:
            definitions = []
            for stem in stems:
                if stem:
                    if re.search('[/!]', stem):
                        return await ctx.send('Words must not contain / or !')
                    definition = self.dictionary.define(stem.upper(),config.channels[ctx.channel.name]["lexicon"])
                    definitions.append(definition)
            msg = '; '.join(definitions)
            print(len(msg))
            await ctx.send(msg[0:500])

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
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='timeout')
    async def timeout(self, ctx, user):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            await ctx.timeout(user)
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='related')
    async def related(self, ctx, stem, page='1'):
        result = self.dictionary.related_command(stem.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='beginswith')
    async def beginswith(self, ctx, hook, page='1'):
        result = self.dictionary.begins_with(hook.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='startswith')
    async def startswith(self, ctx, hook, page='1'):
        result = self.dictionary.begins_with(hook.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='endswith')
    async def endswith(self, ctx, hook, page='1'):
        result = self.dictionary.ends_with(hook.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='finisheswith')
    async def finisheswith(self, ctx, hook, page='1'):
        result = self.dictionary.ends_with(hook.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='contains')
    async def contains(self, ctx, stem, page='1'):
        result = self.dictionary.contains(stem.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='pattern')
    async def pattern(self, ctx, pattern, page='1'):
        result = self.dictionary.pattern(pattern.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='regex')
    async def regex(self, ctx, pattern, page='1'):
        result = self.dictionary.regex(pattern.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='hook')
    async def hook(self, ctx, stem):
        msg = self.dictionary.hook(stem.upper(),config.channels[ctx.channel.name]["lexicon"])
        await ctx.send(msg)

    @commands.command(name='info')
    async def info(self, ctx, *stems):
        if stems and len(stems) > 0:
            lexicon = config.channels[ctx.channel.name]["lexicon"]
            alphabet = config.channels[ctx.channel.name]["alphabet"]
            results = []
            for stem in stems:
                if stem:
                    msg = self.dictionary.info(stem.upper(), lexicon, alphabet)
                    if len(stem) >= 2 and len(stem) <= 5:
                        msg += equity(stem, lexicon)[len(stem):]
                    results.append(msg)
            msg = '; '.join(results)
            print(len(msg))
            await ctx.send(msg[0:500])

    @commands.command(name='anagram')
    async def anagram(self, ctx, *racks):
        if racks and len(racks) > 0:
            results = []
            msg = None
            length = -2
            for rack in racks:
                if rack:
                    result = self.dictionary.anagram_1(rack.upper(),config.channels[ctx.channel.name]["lexicon"])
                    count, words = result
                    msg = f'{count} %s:\n{words}' % engine.plural('result', count)
                    length += len(msg) + 2
                    if length >= 500:
                        break
                    results.append(msg)
            msg = '; '.join(results)
            print(len(msg))
            await ctx.send(msg[0:500])

    @commands.command(name='bingo')
    async def bingo(self, ctx, length='7'):
        msg = self.dictionary.random_word(int(length), config.channels[ctx.channel.name]["lexicon"],"")
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='random')
    async def random(self, ctx, option='0'):
        if option.isnumeric():
            msg = self.dictionary.random_word(int(option), config.channels[ctx.channel.name]["lexicon"], "")
        else:
            msg = self.dictionary.random_word(0,config.channels[ctx.channel.name]["lexicon"],option)
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='pronounce')
    async def pronounce(self, ctx, stem):
        if re.search('[/!]', stem):
            return await ctx.send('Words must not contain / or !')
        offensive, valid = self.dictionary.check(stem.upper(),config.channels[ctx.channel.name]["lexicon"])
        if not offensive:
            if valid:
                await ctx.send(f'https://collinsdictionary.com/sounds/hwd_sounds/en_gb_{stem.lower()}.mp3')
            else:
                await ctx.send(f'{stem.upper()}* not found')

    @commands.command(name='crypto')
    async def crypto(self, ctx, cipher, page='1'):
        result = self.dictionary.crypto(cipher.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='hidden')
    async def hidden(self, ctx, length, phrase='', page='1'):
        result = self.dictionary.hidden(int(length),phrase.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

