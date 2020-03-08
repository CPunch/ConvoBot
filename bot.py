'''
    Demo Discord Bot using gpt-2 to make a bot-friend that should engage in conversations and stay on-topic (theoretically)
    Author: CPunch
    
    I wrote this in 2 Hours, I originally planned to use tensorflow myself but gpt-2-simple already existed and that was pretty sweet of them :)
'''
import os
import gpt_2_simple as gpt2
import discord

import blacklist as bl

# loads our trained model
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

activeChannels = {}

def checkActiveChannel(id):
    if id in activeChannels:
        return True
    activeChannels[id] = True
    return False

def removeActiveChannel(id):
    del activeChannels[id]

client = discord.Client()
class Conversation:
    """Each channel has it's own Conversation. Trigger the bot by pinging it, it'll read the conversation in the channel and try to predict a response. """

    def __init__(self):
        self.conversation = []

    def add(self, text):
        self.conversation.append(text.replace("\n", ""))

    def continued(self, text):
        self.conversation[-1] = self.conversation[-1] + ". " + text

    def grabText(self):
        output = ""
        for reply in reversed(self.conversation):
            output = output + reply + "\n"
        return output

    def getUnique(self, results):
        for res in results:
            if not res in self.conversation:
                return res

    def buildResponse(self):
        rawresponse = gpt2.generate(sess, prefix=self.grabText(), include_prefix=False, length=75, return_as_list=True)
        print(rawresponse)
        chats = rawresponse[0].split('\n')
        return getUnique(chats)

@client.event
async def on_ready():
    print(client.user.name + ' is ready!')

@client.event
async def on_message(message):
    if len(message.clean_content) <= 0 or "http" in message.clean_content:
        return

    # don't do anything if we sent the message
    if message.author == client.user:
        return

    mentions = message.mentions
    for usr in mentions:
        if usr.id == client.user.id: # if bot was mentioned
            # we're already typing in that channel
            if (checkActiveChannel(message.channel.id)):
                print("busy!")
                return
            # start "typing" to let the users know we're running the model
            print("crafting response...")
            async with message.channel.typing():
                # build conversation, then use gpt-2 on convo to extract response
                convo = Conversation()
                lastMessage = None
                async for messg in message.channel.history(limit=10):
                    msg = messg.clean_content.encode('ascii', 'ignore').decode('ascii')
                    if bl.passFilter(msg): 

                        # combine messages from people onto the same line
                        if lastMessage != None and lastMessage.author.id == messg.author.id:
                            convo.continued(msg)
                        else:
                            convo.add(msg)
                        lastMessage = messg

                predictedResponse = convo.buildResponse()
                removeActiveChannel(message.channel.id)
                await message.channel.send(predictedResponse)
        break

client.run(open("client-token", "r").readline())