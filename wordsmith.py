
import dictionary
from twitchbot import TwitchBot

dictionary.open_files()
bot = TwitchBot(dictionary)
bot.run()
