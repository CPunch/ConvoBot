This was a project I threw together in like 3ish hours total. ConvoBot is a discord bot that can respond to converations, trained by your friends! aka, the "inside joke" bot.

![](demo.png?raw=true)

How this works is:
- clone the repo with "git clone https://github.com/CPunch/ConvoBot.git"
- Create a discord bot and put it's token in a file called "client-token"
- You add the bot to whatever servers/channels you want to simulate
- run setup.sh && run.sh
- run scrapeChannels.py to scrape the channels (this might take a while!)
- after that, run train.py (on your machine using tensorflow-gpu, or google's cloud compute service)
- finally run the bot, cause it to talk by pinging it.
> Mine took 10 hours to train before good results started showing

Like I said, I threw this together in like 3 hours, so please don't expect AAA python scripts. (they don't even accept params :[)