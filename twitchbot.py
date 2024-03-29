from twitchio.ext import commands
import twitchio as tw
import config as cf
import inflect
import random as rd
import re
from alphagram import alphagram
from api import define, poll, predict, validate
from calculator import equity, evaluate
from cipher import cipher
import dictionary
from difflib import SequenceMatcher
from ety import origins
from pager import paginate, truncate

custom_commands = cf.custom_commands()
engine = inflect.engine()

class TwitchBot(commands.Bot):

    def __init__(self, config=cf.config()):
        super().__init__(api_token=config.api_token, token=config.irc_token,
                         client_id=config.client_id, nick=config.nick, prefix='!',
                         initial_channels=config.channels.keys())
        self.config = config

    def run(self):
        dictionary.open_files()
        super().run()

    async def event_ready(self):
        print(f'Wordsmith 0.33 by Danielle Barker | {self.nick}')

    async def event_message(self, ctx):
        if ctx.author and not ctx.author.name == self.nick:
            print(ctx.content)
            if SequenceMatcher(None, "Wanna become famous? Buy followers, primes and views on example*com (example . com)!", ctx.content).ratio() >= 0.8:
                if not ctx.author.is_mod:
                    message = f'/timeout {ctx.author.name}'
                    print(len(message))
                    await ctx.channel.send(message)
                message = '"If fame is only to come after death, I am in no hurry for it." - Martial'
                print(len(message))
                await ctx.channel.send(message)
            elif len(ctx.content) > 1 and ctx.content[0] == '!':
                if ctx.content[1:] in custom_commands.keys():
                    with open(custom_commands[ctx.content[1:]], 'r') as f:
                        messages = list(f)
                    message = rd.choice(messages).strip()
                    print(len(message))
                    await ctx.channel.send(message)
                else:
                    await self.handle_commands(ctx)

    @commands.command(name='poll')
    async def poll(self, ctx, tiles):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            msg = poll(self.config, ctx.channel.name, tiles)
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='predict')
    async def predict(self, ctx, player, opponent='Opponent'):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            msg = predict(self.config, ctx.channel.name, player, opponent)
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='check')
    async def check(self, ctx, *words):
        if words and len(words) > 0:
            results = []
            lexicon = self.config.channels[ctx.channel.name]['lexicon']
            entries = validate(lexicon, [word.upper() for word in words])
            for word in entries:
                if entries[word]['v']:
                    results.append(word + ' is valid VoteYea')
                else:
                    results.append(word + '* not found VoteNay')
            msg = truncate(' ', results)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='common')
    async def common(self, ctx, *words):
        if words and len(words) > 0:
            results = []
            entries = validate('ECWL', [word.upper() for word in words])
            for word in entries:
                if entries[word]['v']:
                    results.append(word + ' is common VoteYea')
                else:
                    results.append(word + ' is not common VoteNay')
            msg = truncate(' ', results)
        else:
            msg = 'Common English Lexicon, Copyright (c) 2021-2022 Fj00. Used with permission.';
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='wordnik')
    async def wordnik(self, ctx, *words):
        if words and len(words) > 0:
            lexicon = self.config.channels[ctx.channel.name]['lexicon']
            results = []
            for word in words:
                offensive, word, entry = dictionary.check(word.upper(), self.config.channels[ctx.channel.name]['lexicon'])
                if not offensive:
                    msg = ('%s%s' % dictionary.decorate(word, entry, lexicon, '')) if entry else ('%s*' % word)
                    results.append((msg + ' is open-source VoteYea') if dictionary.wordnik(word.lower()) else (msg + ' not open-source VoteNay'))
            msg = truncate(' ', results)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='yawl')
    async def yawl(self, ctx, *words):
        if words and len(words) > 0:
            lexicon = self.config.channels[ctx.channel.name]['lexicon']
            results = []
            for word in words:
                offensive, word, entry = dictionary.check(word.upper(), self.config.channels[ctx.channel.name]['lexicon'])
                if not offensive:
                    msg = ('%s%s' % dictionary.decorate(word, entry, lexicon, '')) if entry else ('%s*' % word)
                    results.append((msg + ' is open-source VoteYea') if dictionary.yawl(word.lower()) else (msg + ' not open-source VoteNay'))
            msg = truncate(' ', results)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='equity')
    async def equity(self, ctx, *racks):
        if racks and len(racks) > 0:
            lexicon = self.config.channels[ctx.channel.name]['lexicon']
            alphabet = self.config.channels[ctx.channel.name]['alphabet']
            results = []
            for rack in racks:
                if rack:
                    if len(rack) >= 2 and len(rack) <= 5:
                        result = equity(rack, lexicon)
                        if result[0] == '{':
                            msg = '%s: %s' % (alphagram(rack.upper(), alphabet), result)
                        else:
                            msg = '%s: %0.3f' % (alphagram(result[0], alphabet), result[1])
                    else:
                        msg = alphagram(rack.upper(), alphabet) + ': ?'
                    results.append(msg)
            msg = truncate('; ', results)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='sum')
    async def sum(self, ctx, *racks):
        if racks and len(racks) > 0:
            alphabet = self.config.channels[ctx.channel.name]['alphabet']
            results = []
            for rack in racks:
                if rack:
                    msg = '%s: %d' % (alphagram(rack.upper(), alphabet), evaluate(rack.upper()))
                    results.append(msg)
            msg = truncate('; ', results)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='define')
    async def define(self, ctx, *words):
        if words and len(words) > 0:
            definitions = []
            lexicon = self.config.channels[ctx.channel.name]['lexicon']
            entries = define(lexicon, [word.upper() for word in words])
            opposite = entries
            if self.config.channels[ctx.channel.name]['lexicon'] == 'csw#':
                opposite = validate('twl', [word.upper() for word in words])
            elif self.config.channels[ctx.channel.name]['lexicon'] == 'twl$':
                opposite = validate('csw', [word.upper() for word in words])
            for word in entries:
                if entries[word]['v']:
                    definition = entries[word]['d']
                    mark = ''
                    if self.config.channels[ctx.channel.name]['lexicon'] == 'csw#' and not opposite[word]['v']:
                        mark = '#'
                    elif self.config.channels[ctx.channel.name]['lexicon'] == 'twl$' and not opposite[word]['v']:
                        mark = '$'
                    definitions.append('%s%s - %s' % (word, mark, entries[word]['d']))
                else:
                    definitions.append(word + '* - not found')
            msg = truncate('; ', definitions)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='inflect')
    async def inflect(self, ctx, *words):
        if words and len(words) > 0:
            inflections = []
            for word in words:
                offensive, word, entry = dictionary.check(word.upper(), self.config.channels[ctx.channel.name]['lexicon'])
                if offensive:
                    pass
                elif entry:
                    inflections.append(dictionary.inflect(word.upper(), entry, self.config.channels[ctx.channel.name]['lexicon']))
                else:
                    inflections.append(word.upper() + '* - not found')
            msg = truncate('; ', inflections)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='lexicon')
    async def lexicon(self, ctx, word):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            self.config.channels[ctx.channel.name]['lexicon']=word.lower()
            cf.save(self.config)
            msg = f'Lexicon changed to {word.lower()}'
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
        await ctx.send(msg)

    @commands.command(name='timeout')
    async def timeout(self, ctx, user):
        if ctx.author.name == ctx.channel.name or ctx.author.is_mod:
            message = f'/timeout {user}'
        else:
            msg = f'Command can only be used by {ctx.channel.name} or moderators'
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='origin')
    async def origin(self, ctx, word):
        offensive, word, entry = dictionary.check(word.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        if not offensive:
            if entry:
                roots = origins(word.lower(), recursive=True)
                msg = '; '.join(root.pretty for root in roots) if roots else f'Origins not found for {word}'
            else:
                msg = f'{word.upper()}* not found'
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='rhymeswith')
    async def rhyme(self, ctx, word, page='1'):
        result = dictionary.rhyme(word.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='related')
    async def related(self, ctx, word, page='1'):
        result = dictionary.related(word.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='beginswith')
    async def beginswith(self, ctx, hook, page='1'):
        result = dictionary.begins_with(hook.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='startswith')
    async def startswith(self, ctx, hook, page='1'):
        result = dictionary.begins_with(hook.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='endswith')
    async def endswith(self, ctx, hook, page='1'):
        result = dictionary.ends_with(hook.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='finisheswith')
    async def finisheswith(self, ctx, hook, page='1'):
        result = dictionary.ends_with(hook.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='contains')
    async def contains(self, ctx, stem, page='1'):
        result = dictionary.contains(stem.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='pattern')
    async def pattern(self, ctx, pattern, page='1'):
        result = dictionary.pattern(pattern.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='regex')
    async def regex(self, ctx, pattern, page='1'):
        result = dictionary.find(pattern.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='hook')
    async def hook(self, ctx, stem):
        msg = dictionary.hook(stem.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='unhook')
    async def unhook(self, ctx, rack, page='1'):
        result = dictionary.unhook(rack.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='info')
    async def info(self, ctx, *stems):
        if stems and len(stems) > 0:
            lexicon = self.config.channels[ctx.channel.name]['lexicon']
            alphabet = self.config.channels[ctx.channel.name]['alphabet']
            results = []
            for stem in stems:
                if stem:
                    msg = dictionary.info(stem.upper(), lexicon, alphabet)
                    if len(stem) >= 2 and len(stem) <= 5:
                        result = equity(stem, lexicon)
                        if result[0] == '{':
                            msg += ' Equity: %s' % result
                        else:
                            msg += ' Equity: %0.3f' % result[1]
                    results.append(msg)
            msg = truncate('; ', results)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='anagram')
    async def anagram(self, ctx, *racks):
        if racks and len(racks) > 0:
            lexicon = self.config.channels[ctx.channel.name]['lexicon']
            results = []
            msg = None
            length = -2
            for rack in racks:
                if anagrams := dictionary.anagram(rack.upper(), lexicon):
                    count = len(anagrams)
                    msg = f'{count} %s' % engine.plural('result', count)
                    for n, element in enumerate(anagrams):
                        word, entry = element
                        if length + len(msg) + len(word) > 465:
                            msg += f' Limited to first {n} results'
                            break
                        msg += ' %s%s' % dictionary.decorate(word, entry, lexicon, '')
                else:
                    msg = 'No anagrams found'
                length += len(msg) + 2
                if length >= 500:
                    break
                results.append(msg)
            msg = truncate('; ', results)
            print(len(msg))
            await ctx.send(msg)

    @commands.command(name='bingo')
    async def bingo(self, ctx, length='7'):
        msg = dictionary.random_word(int(length), self.config.channels[ctx.channel.name]['lexicon'])
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='random')
    async def random(self, ctx, option='0'):
        lexicon = self.config.channels[ctx.channel.name]['lexicon']
        if option.isnumeric():
            msg = dictionary.random_word(int(option), lexicon)
        else:
            word, entry = rd.choice(dictionary.related(option.upper(), lexicon))
            word, _, definition, mark = dictionary.define(word, entry, lexicon, '')
            msg = '%s%s - %s' % (word, mark, definition)
        print(len(msg))
        await ctx.send(msg)

    @commands.command(name='pronounce')
    async def pronounce(self, ctx, stem):
        offensive, word, entry = dictionary.check(stem.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        if not offensive:
            if entry:
                await ctx.send(f'https://collinsdictionary.com/sounds/hwd_sounds/en_gb_{stem.lower()}.mp3')
            else:
                await ctx.send(f'{stem.upper()}* not found')

    @commands.command(name='crypto')
    async def crypto(self, ctx, text, page='1'):
        pattern = cipher(text.upper())
        result = dictionary.find(pattern, self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

    @commands.command(name='hidden')
    async def hidden(self, ctx, length, phrase='', page='1'):
        result = dictionary.hidden(int(length),phrase.upper(), self.config.channels[ctx.channel.name]['lexicon'])
        num, msg = paginate(result, self.config.channels[ctx.channel.name]['lexicon'], int(page))
        print(len(msg))
        await ctx.send(f'{num} %s:\n{msg}' % engine.plural('result', num))

def main():
    TwitchBot().run()

if __name__ == "__main__":
    main()

