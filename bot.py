'''
    Demo Discord Bot using gpt-2 to make a bot-friend that should engage in conversations and stay on-topic (theoretically)
    Author: CPunch
    
    I wrote this in 2 Hours, I originally planned to use tensorflow myself but gpt-2-simple already existed and that was pretty sweet of them :)
'''
import os
import gpt_2_simple as gpt2
import discord

# loads our trained model
sess = None
if not logMode:
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)

activeChannels = []

client = discord.Client()
class Conversation:
    """Each channel has it's own Conversation. Trigger the bot by pinging it, it'll read the conversation in the channel and try to predict a response. """

    def __init__(self):
        self.conversation = []

    def add(self, text):
        self.conversation.append(text.replace("\n", ""))

    def grabText(self, nspace = 1):
        output = ""
        for reply in reversed(self.conversation):
            output = output + (reply + ("\n" * nspace))
        return output

    def buildResponse(self):
        rawresponse = gpt2.generate(sess, prefix=self.grabText(), include_prefix=False, length=10, return_as_list=True)
        return rawresponse[0].split('\n', 1)[0]

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
            # start "typing" to let the users know we're running the model
            print("crafting response...")
            async with message.channel.typing():
                # build conversation, then use gpt-2 on convo to extract response
                convo = Conversation()
                async for msg in message.channel.history(limit=15):
                    convo.add(msg.clean_content)
                predictedResponse = convo.buildResponse()
                await message.channel.send(predictedResponse)
        break

client.run(open("client-token", "r").readline())