from twitchio.ext import commands
import twitchio as tw
import config as cf
import inflect
import random as rd
import re
from alphagram import alphagram
from api import predict
from calculator import equity, evaluate
from cipher import cipher

config = cf.config()
print(config)
initc = config.channels.keys()
custom_commands = cf.custom_commands()
engine = inflect.engine()

class TwitchBot(commands.Bot):

    def __init__(self, dictionary):
        super().__init__(api_token=config.api_token, token=config.irc_token,
                         client_id=config.client_id, nick=config.nick, prefix='!',
                         initial_channels=initc)
        self.dictionary = dictionary

    async def event_ready(self):
        print(f'Wordsmith 0.14 by Danielle Barker | {self.nick}')

    async def event_message(self, ctx):
        if len(ctx.content) > 1 and ctx.content[0] == '!':
            print(ctx.content)
            if ctx.content[1:] in custom_commands.keys():
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
        lastmark = ''
        lastword = ''
        p = int(page)
        for n, element in enumerate(my_result):
            word, mark = element
            if lastword and mark == lastmark and word == lastword + 'S':
                msg = msg[:(-2 if mark else -1)] + '[-S]'
            elif len(msg) + len(word) > 455:
                if p > 1:
                    msg = ''
                    p = p - 1
                else:
                    msg += f' Limited to first {n} results '
                    break
            else:
                msg += word 
                lastmark = mark
                lastword = word
            msg += (mark if mark else '') + ' '
        print(len(msg))
        return num_results, msg[:-1]

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

    @commands.command(name='wordnik')
    async def wordnik(self, ctx, stem):
        if re.search('[/!]', stem):
            return await ctx.send('Words must not contain / or !')
        offensive, common = self.dictionary.common(stem.upper(),config.channels[ctx.channel.name]["lexicon"])
        if not offensive:
            if common:
                msg = stem.upper() + ' is open-source VoteYea'
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
                        result = equity(rack, lexicon)
                        if result[0] == '{':
                            msg = '%s: %s' % (alphagram(rack.upper(), alphabet), result)
                        else:
                            msg = '%s: %0.3f' % (alphagram(result[0], alphabet), result[1])
                    else:
                        msg = alphagram(rack.upper(), alphabet) + ': ?'
                    results.append(msg)
            msg = '; '.join(results)
            print(len(msg))
            await ctx.send(msg[0:500])

    @commands.command(name='sum')
    async def sum(self, ctx, *racks):
        if racks and len(racks) > 0:
            alphabet = config.channels[ctx.channel.name]["alphabet"]
            results = []
            for rack in racks:
                if rack:
                    if re.search('[/!]', rack):
                        return await ctx.send('Racks must not contain / or !')
                    msg = '%s: %d' % (alphagram(rack.upper(), alphabet), evaluate(rack.upper()))
                    results.append(msg)
            msg = '; '.join(results)
            print(len(msg))
            await ctx.send(msg[0:500])

    @commands.command(name='define')
    async def define(self, ctx, *words):
        if words and len(words) > 0:
            definitions = []
            for word in words:
                if re.search('[/!]', word):
                    return await ctx.send('Words must not contain / or !')
                offensive, valid = self.dictionary.check(word.upper(),config.channels[ctx.channel.name]["lexicon"])
                if offensive:
                    pass
                elif valid:
                    lexicon = config.channels[ctx.channel.name]["lexicon"]
                    word, definition = self.dictionary.define(word.upper(), lexicon)
                    definitions.append('%s%s - %s' % (word, self.dictionary.decorate(word, lexicon, '')[1], definition))
                    while match := re.match(rf'(?:characterized by |not |one that |one who |somewhat |the state of being )?([a-z]+)(?:,| \[)', definition):
                        word, definition = self.dictionary.define(match.group(1).upper(), lexicon)
                        definitions.append('%s%s - %s' % (word, self.dictionary.decorate(word, lexicon, '')[1], definition))
                else:
                    definitions.append(word.upper() + '* - not found')
            msg = '; '.join(definitions)
            print(len(msg))
            await ctx.send(msg[0:500])

    @commands.command(name='inflect')
    async def inflect(self, ctx, *words):
        if words and len(words) > 0:
            inflections = []
            for word in words:
                if re.search('[/!]', word):
                    return await ctx.send('Words must not contain / or !')
                offensive, valid = self.dictionary.check(word.upper(),config.channels[ctx.channel.name]["lexicon"])
                if offensive:
                    pass
                elif valid:
                    inflections.append(self.dictionary.inflect(word.upper(),config.channels[ctx.channel.name]["lexicon"]))
                else:
                    inflections.append(word.upper() + '* - not found')
            msg = '; '.join(inflections)
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
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='stem')
    async def stem(self, ctx, rack):
        msg = self.dictionary.stem(rack.upper(),config.channels[ctx.channel.name]["lexicon"])
        print(len(msg))
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
            msg = self.dictionary.random_word(int(option), config.channels[ctx.channel.name]["lexicon"], '')
        else:
            msg = self.dictionary.random_word(0, config.channels[ctx.channel.name]["lexicon"], option)
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
    async def crypto(self, ctx, text, page='1'):
        pattern = '^%s$' % cipher(text.upper())
        result = self.dictionary.regex(pattern,config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='hidden')
    async def hidden(self, ctx, length, phrase='', page='1'):
        result = self.dictionary.hidden(int(length),phrase.upper(),config.channels[ctx.channel.name]["lexicon"])
        num, msg = self.paginate(result, page)
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

