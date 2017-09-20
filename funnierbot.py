#!/usr/bin/env python
#
#  Very minimal Telegram chat bot client
# only echos back positive reinforcement and wikipedia things
#
# -aeVar 2017

import requests as r
import wikipedia
import argparse
import urllib
import random
import json
import read
import os
from time import sleep
from tweepy import OAuthHandler,API,Stream
from tweepy.streaming import StreamListener

funny = 'https://api.telegram.org/bot333486385:AAFGYg14V7hJJqRKyTx5tF2sb2beEu07MCg'
keys = read.keys()

class Base:
    '''Twitter Base'''
    def __init__(self, name=None, keyfile=None):
        self.name = 'Iconic'
        self.auth = OAuthHandler(keys[0], keys[1])
        self.auth.set_access_token(keys[2], keys[3] )
        self.api = API(self.auth)
        self.me = self.api.me()
        self.listen = StdOutListener()
        self.stream = Stream(self.auth, self.listen)

class StdOutListener(StreamListener):

    def on_data(self, data):
        result = json.loads(data)

        text = urllib.parse.quote_plus(result['text'])
        r.post(r'%s/sendMessage?text=%s&chat_id=339387792'%(funny,text))
        sleep(3)

        return True

    def on_error(self, status):
        print (status)

        return False

class Iconic:
    def __init__(self):
        self.name = 'Iconic'
        self.id = 'https://api.telegram.org/bot333486385:AAFGYg14V7hJJqRKyTx5tF2sb2beEu07MCg'
        self.chat_id = '339387792'

        # Math Quiz things
        self.x = 0
        self.y = 0
        self.z = 0

    def getChatID(self):
        try:
            chat_id = self.getUpdates()[-1]['message']['chat']['id']
        except KeyError as e:
            print ('--[ No new messages')
            chat_id = self.chat_id

        return chat_id

    def getUpdates(self):
        '''Retrieves conversation updates'''

        rez = r.get( '%s/getUpdates' % self.id )
        z = json.loads( rez.text )['result']

        return z

    def mathQuiz(self):
        "Simple addition test"

        self.x = random.randint(0,9)
        self.y = random.randint(0,9)
        self.z = self.x + self.y

        this = "What do you get if you add %s and %s?" % (self.x,self.y)

        r.post(r'%s/sendMessage?text=%s&chat_id=%s'%(funny,str(this),iconic.getChatID()))

    def wiki(self, text):
        '''Checks wikipedia for generic descriptions'''
   
        text = text.replace('?','')
        prefix = text[0:7].lower()
        query = text[7:].lstrip()
        rez = wikipedia.search(query)
        if rez ==[]:
            something = "Not something I've heard of"
            return something
        that = (random.choice(rez))
        try:
            something = wikipedia.summary(that)
        except wikipedia.exceptions.DisambiguationError as e:
            rex = random.choice(e.args)
            if len(rex)==1:
                something = self.wiki('what is %s' % rex)
            else:
                something = self.wiki('what is %s' % random.choice(rex))

        return something

def reply():
    with open('generic.txt') as data:
        rez = data.readlines()
    return random.choice(rez).rstrip('\n')

def sendImage(path='', chat_id=0, debug=False, loop=False ):
    '''Sends a random image from the gallery'''

    url = "%s/sendPhoto" % funny
    if path=='':
        path =  os.getenv('ICONIC_IMAGES')

    targets = []

    for x,y,z in os.walk(path):
        for n in z:
            targetpath = os.path.join(x,n)
            targets.append(targetpath)

    target_image = random.choice(targets)
    files = {'photo': open( target_image, 'rb')}
    data = {'chat_id' : chat_id }
    rez= r.post(url, files=files, data=data)

    if debug:
        print(rez.status_code, rez.reason, rez.content)

    if loop:
        wait = random.randint(7200,18000)
        print ("Waiting %s seconds until next image " % wait )
        sleep(wait)
        sendImage(path=path,chat_id=chat_id,debug=debug,loop=loop)


def sendAudio():
    url = "%s/sendAudio" % funny
    path = os.getenv('ICONIC_AUDIO')
    selected = random.choice(os.listdir(path))
    files = {'audio': open(os.path.join(path,selected), 'rb')}
    data = {'chat_id' : iconic.getChatID()}
    rez= r.post(url, files=files, data=data)
    print(rez.status_code, rez.reason, rez.content)

def info():
    '''Returns basic information about self'''

    rez = r.get( '%s/getme' % funny )
    z = json.loads(rez.text)['result']
    
    print( 'My name is: %s' % z['username'])
    print( '\tbut you can call me %s....' % z['first_name'])
    print( 'if you then want to be really beurocratic about it, my ID is %s' % z['id'])

    return True

def latest():
    '''Returns latest messages sent to the bot'''

    rez = r.get( '%s/getUpdates' % funny )
    z = json.loads( rez.text )['result']

    for n in z:
        t = n['message']

    try:
        text = t['text']
    except UnboundLocalError as e:
        text = "No new messages..... "

    return text

def smallTalk(text):
    if text.startswith('what is'):
        rez = iconic.wiki(text)
        this = urllib.parse.quote_plus(rez)
        r.post(r'%s/sendMessage?text=%s&chat_id=%s'%(funny,str(this),iconic.getChatID()))
        return
    else:
        r.post(r'%s/sendMessage?text=%s&chat_id=%s'%(funny,reply(),iconic.getChatID()))
        return

def math():
    this = "ok, lets play a game, I'll give you numbers you tell me the answer."
    r.post(r'%s/sendMessage?text=%s&chat_id=%s'%(funny,str(this),iconic.getChatID()))
    sleep(1)
    this = "if you want to stop the game and return to small talk just tell me 'stop' and I will stop"    
    r.post(r'%s/sendMessage?text=%s&chat_id=%s'%(funny,str(this),iconic.getChatID()))

    sleep(1)
    iconic.mathQuiz()


def listen():
    last = None
    while True:
        text = latest()
        if text != last:
            print (text)
            print (last)
            if last != None:
                text = text.lower()

                if text.lower() == 'play math':
                    math()
                    last = None
                    continue

                if text.lower() == 'stop':
                    smallTalk(text)
                    last = None
                    continue

                if text[0].isdigit():
                    if text == str(iconic.z):
                        this = 'perhaps'
                        r.post(r'%s/sendMessage?text=%s&chat_id=%s'%(funny,str(this),iconic.getChatID()))
                        sleep(3)
                        iconic.mathQuiz()
                    else:
                        this = 'not quite, try again'
                        r.post(r'%s/sendMessage?text=%s&chat_id=%s'%(funny,str(this),iconic.getChatID()))
                    last = None
                    continue

            
                smallTalk(text)
                last = None
                continue

            last = text

        sleep(0.5)

def wiki(text):
    '''Checks wikipedia for generic descriptions'''
    
    query = text.lstrip('What is')
    
    rez = wikipedia.search(query)
    that = (random.choice(rez))
    something = wikipedia.summary(that)

    return something

if __name__ == '__main__':
    iconic = Iconic()
    twitter = Base()

    parser = argparse.ArgumentParser(description='Funny bot and friends')
    parser.add_argument('--info', help='Basic Information',action="store_true")
    parser.add_argument('--new', help='Latest Messages',action="store_true")
    parser.add_argument('--say', type=str, help='Speak',action="store")
    parser.add_argument('--twit', help='Twit',action="store_true")
    parser.add_argument('--listen', help='Listening daemon',action="store_true")
    parser.add_argument('--audio', help='Responds with an audio file',action="store_true")
    parser.add_argument('--image', help='Responds with an image file',action="store_true")
    parser.add_argument('--loop', help='loop command',action="store_true")

    args = parser.parse_args()

    if args.new:
        print ( latest() )
    if args.info:
        info()
    if args.say:
        text = urllib.parse.quote_plus(args.say)
        r.post(r'%s/sendMessage?text=%s&chat_id=%s'%(funny,text,iconic.getChatID()))
    if args.twit:
        twitter.stream.filter(track='sexy')
    if args.listen:
        listen()
    if args.audio:
        sendAudio()

    if args.image:
        if args.loop:
            sendImage(chat_id=iconic.getChatID(),loop=True)
        else:
            sendImage(chat_id=iconic.getChatID())