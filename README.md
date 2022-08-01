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
        "api_token": "REDACTED",
        "irc_token": "REDACTED",
        "client_id": "oe08ff8dfds8fdfjd99fda68g6pt",
        "nick": "BotsTwitchAccountName",
        "channels": {
            "somestreamer": {
                "alphabet": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "lexicon": "csw",
                "command_blacklist": []
            }
        }
      }
      
    
## Setting up your own bot 

  	1. Create a new twitch account with the username you want the bot to have

  	2. Sign in as that account and go here: https://dev.twitch.tv/console/apps/create

  	3. Register a new Chat Bot application. Name is not important, it isn't shown anywhere except in your applications list

 	4. During registration set the callback URL to token generator https://twitchapps.com/tokengen/

 	5. Copy your client ID from your new Twitch application into config.json

  	6. Generate an API token with scope channel:manage:polls channel:manage:predictions and an IRC token with scope chat:edit chat:read
           API specification: https://dev.twitch.tv/docs/authentication/scopes
           TwitchIO usage:
               https://twitchio.dev/en/latest/twitchio.html
               https://twitchio.dev/en/latest/reference.html#twitchio.PartialUser.create_poll
               https://twitchio.dev/en/latest/reference.html#twitchio.PartialUser.create_prediction

  	7. Open config.json and replace the lines with your information, be sure to leave the variables in quotes:
	  	
		api_token is the API token (TwitchIO supplies an oauth: prefix, so omit "oauth:")
		irc_token is the IRC token
	  	client_id is your Twitch Application ID
	  	nick is your bot's username
	  	channels is the channels you want it to join and their initial lexicon

  	8. Save this file

  	9. That's it, run wordsmith.exe and it should connect and show a message saying "Wordsmith [version] by Danielle Barker | [nick]"
    
 	10. To run "python wordsmith.py" you will need to have the twitchio package installed, instructions can be found in the readme at https://github.com/TwitchIO/TwitchIO or try your luck with installing Python and `pip install -r requirements.txt`.

## Commands for the bot

Some commands will return a list of results, if there are more than 30, it will be concatenated in order to fit Twitch's 500 character message limit

	!check - checks if a word is valid, e.g. !check cat
	!define - returns word definitions, e.g. !define cat dog
	!inflect - returns word inflections, e.g. !define cat dog
	!related - searches all definitions for the key word and returns the list, e.g. !related cat (for searching multiple consecutive words in a string, use . to separate words, e.g. !related star.wars will return JEDI and JEDIS
	!hook - returns front hooks, back hooks, and middle hooks, e.g. !hook cat
	!startswith -returns a list of words that start with the given string, e.g. !startswith cat
	!endswith - same as above but words ending in the string, e.g. !endswith cat
	!contains - returns a list of words that contain the given string anywhere in the word, e.g. !contains cat
	!pattern - ? for single blank, 1-9 or * for multiple, e.g. !pattern fat7
	!regex - !regex ^[abc]at$ will return BAT and CAT.
	!info - returns the definition, front hooks, back hooks, middle hooks, probability, alphagram sorted by alphabet, e.g. !info cat
	!anagram - returns a list of words that fit the letters given, e.g. !anagram ?aeinst
	!random [length] - returns a single word and definition chosen at random, e.g. !random 7
	!lexicon - only usable by the stream owner, changes to one of the other lexicons, e.g. !lexicon csw, csw# is for csw with octothorps.
