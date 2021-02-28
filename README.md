# Wordsmith
`A Twitch bot for OMGWords`

## Files you need on your local version

  `csw.dat` `twl.dat` `mw.dat`
   These are the dictionary files, plain text, each word on one line following this example (will work with only one or two of these files, a warning will just be shown for the missing files):
      
      AA	(Hawaiian) a volcanic rock consisting of angular blocks of lava with a very rough surface [n -S]	bcfm	hls	46	AA
      
      word (tab \t) definition (tab \t) front_hooks (tab \t) back_hooks (tab \t) probability (tab \t) alphagram

      also for csw.dat if you add another tab and a # at the end of the line for collins only words, the bot will display the # at the end of the word, this is optional though
      
      
  `config.json`
   This is the configuration file to connect the bot to a twitch account and have it join channels, it has the following 5 lines only (made up info) instructions on how to set up your own bot found below:
    
      {
        "irc_token": "oauth:2cw2mrjef8fd8fdoyd95fbi2ajnwpvy1",
        "client_id": "oe08ff8dfds8fdfjd99fda68g6pt",
        "nick": "BotsTwitchAccountName",
        "channels": {
            "somestreamer": {
                "alphabet": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "lexicon": "twl",
                "command_blacklist": []
            },
            "anotherstreamer": {
                "alphabet": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "lexicon": "csw",
                "command_blacklist": []
            }
      }

}
      
    
## Setting up your own bot 
### You can run wordsmith.py, or if you don't have python or just want to run the exe that works too

  	1. Create a new twitch account with the username you want the bot to have

  	2. Go to https://twitchapps.com/tmi/ and click Connect, copy what is in the text box including "oauth:"

  	3. Sign in as that account and go here: https://dev.twitch.tv/console/apps/create

  	4. Register a new application, Name is not important, it isn't shown anywhere except in your applications list

  	5. Paste the oauth you got earlier, you'll also need to put this into config.json (just open in notepad or similar)

  	6. Choose Chat Bot for Category

  	7. Click Create

  	8. You will be brough to a page called Console, where you will see your App, click on Manage

  	9. Copy your Client ID, you will need to put this in config.json

  	10. Open config.json and replace the lines with your information, be sure to leave the variables in quotes:
	  	
		irc_token is the oauth, make sure it includes the text "oauth:" and not just the rest of the string
	  	client_id is your client id
	  	nick is your bot's username
	  	channels is the channels you want it to join and their initial lexicon

  	11. Save this file

  	12. That's it, run wordsmith.py and it should connect and show a message saying "it is online"
    
    13. To run wordsmith.py you will need to have the twitchio package installed, instructions can be found in the readme at https://github.com/TwitchIO/TwitchIO

## Commands for the bot

Some commands will return a list of results, if there are more than 30, it will be concatenated in order to fit Twitch's 500 character message limit

	!check - checks if a word is valid, e.g. !check cat
	!define - returns the definition, e.g. !define cat
	!related - searches all definitions for the key word and returns the list, e.g. !related cat (for searching multiple consecutive words in a string, use . to separate words, e.g. !related star.wars will return JEDI and JEDIS
	!hook - returns front hooks, back hooks, and middle hooks, e.g. !hook cat
	!startswith -returns a list of words that start with the given string, e.g. !startswith cat
	!endswith - same as above but words ending in the string, e.g. !endswith cat
	!contains - returns a list of words that contain the given string anywhere in the word, e.g. !contains cat
	!pattern - ? for single blank, * for multiple
	!regex - !regex ^[abc]at$ will return BAT and CAT.
	!info - returns the definition, front hooks, back hooks, middle hooks, probability, alphagram sorted by alphabet, e.g. !info cat
	!anagram - returns a list of words that fit the letters given, e.g. !anagram ?aeinst
	!random - returns a single word and definition chosen at random
    !lexicon - only usable by the stream owner, changes to one of the other lexicons, e.g. !lexicon csw, csw# is for csw with octothorps.
