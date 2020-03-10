import discord

def passFilter(msg):
    # lets make sure it isn't an empty message or a shitpost
    return len(msg) > 0 and not 'http' in msg

# used to remove pings, bad words, etc.
# expects a discord.py Message object
def filterMessageToText(msg):
    rawMsg = msg.clean_content.encode('ascii', 'ignore').decode('ascii')

    # removes mentions,  we don't want the bot to train on mentions :(
    for usr in msg.mentions:
        rawMsg.replace("@" + usr.name, "")

    # removes mentions we didn't catch
    rawMsg = " ".join(filter(lambda x:x[0]!='@', rawMsg.split()))

    return rawMsg
    
