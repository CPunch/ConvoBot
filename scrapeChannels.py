# this file will grab chat logs from all of the channels it's connected too. easy way to grab training data to use

import os
import sys
import discord

import blacklist as bl

chat_dir = "chats"
main_dataset = "complete-data"

client = discord.Client()

use_whitelist = True
whitelist = [646807091012435981, 502289648551329793, 502296284556951563]

def deleteIfExist(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

async def scrapeChannel(channel):
    # if we already have a log for that channel, remove it!
    file_path = os.path.join(chat_dir, channel.name + str(channel.id))
    deleteIfExist(file_path)

    try:
        with open(file_path, "a") as cLog:
            rawData = []

            # add channel histroy to raw data
            lastMessage = None
            async for message in channel.history(limit=10000): # should i limit more?? hmm
                msg = message.clean_content.encode('ascii', 'ignore').decode('ascii')
                if bl.passFilter(msg): 

                    # combine messages from people onto the same line
                    if lastMessage != None and lastMessage.author.id == message.author.id:
                        rawData[-1] = rawData[-1] + " " + msg
                    else:
                        rawData.append(msg)
                    lastMessage = message

            # raw data is reversed becasue discord api moment, so fix it and write to file
            for msg in reversed(rawData):
                cLog.write(msg + '\n')
    except e:
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
    deleteIfExist(main_dataset)
    newfile = open(main_dataset, "a")

    for log in os.listdir(chat_dir):
        with open(os.path.join(chat_dir, log), "r") as file:
            for line in reversed(file.readlines()):
                newfile.write(line)

    newfile.close()
    print("done!")

    await client.close()

client.run(open("client-token", "r").readline())