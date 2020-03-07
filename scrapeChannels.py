# this file will grab chat logs from all of the channels it's connected too. easy way to grab training data to use

import os
import sys
import discord

chat_dir = "chats"
main_dataset = "complete-data"

client = discord.Client()

use_whitelist = True
whitelist = [646807091012435981, 502296284556951563]

def passFilter(msg):
    return len(msg) > 0

async def scrapeChannel(channel):
    try:
        with open(os.path.join(chat_dir, channel.name + str(channel.id)), "a") as cLog:
            rawData = []

            # add channel histroy to raw data
            async for message in channel.history(limit=10000): # should i limit more?? hmm
                if passFilter(message.clean_content): 
                    rawData.append(message.clean_content)

            # raw data is reversed becasue discord api moment, so fix it and write to file
            for msg in reversed(rawData):
                cLog.write(str(msg.encode('utf-8')))
    except:
        print("failed!")

@client.event
async def on_ready():
    # if we're going to use a whitelist, do that
    if use_whitelist:
        for id in whitelist:
            channel = client.get_channel(id)
            if channel == None:
                continue
            server = channel.guild

            print("Scraping " + server.name + " : " + channel.name)
            await scrapeChannel(channel)
    else:
        # for every server, go to every channel
        for server in client.guilds:
            for channel in server.channels:
                print("Scraping " + server.name + " : " + channel.name)

                if (channel.type == discord.ChannelType.text or 
                    channel.type == discord.ChannelType.private or 
                    channel.type == discord.ChannelType.group and 
                    not channel.is_nsfw()): # now do some sanity checks
                    # scrape the chat history into a file 
                    await scrapeChannel(channel)
    
    # after scraping, combine all data into one file for training
    newfile = open(main_dataset, "a")

    for log in os.listdir(chat_dir):
        with open(os.path.join(chat_dir, log), "r") as file:
            for line in reversed(file.readlines()):
                newfile.write(line)

    newfile.close()
    print("done!")

client.run(open("client-token", "r").readline())