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

def sendImage(path='', chat_id=0, debug=False ):
    '''Sends a random image from the gallery'''

    url = "%s/sendPhoto" % funny
    if path='':
        path =  os.getenv('ICONIC_IMAGES')
    images = os.listdir( path )
    target_image = os.path.join( path,random.choice(images) )
    files = {'photo': open( target_image, 'rb')}
    data = {'chat_id' : chat_id }
    rez= r.post(url, files=files, data=data)

    if debug:
        print(rez.status_code, rez.reason, rez.content)

def sendAudio():
    url = "%s/sendAudio" % funny
    path = os.getenv('ICONIC_AUDIO')
    selected = random.choice(os.listdir(path))
    files = {'audio': open(os.path.join(path,selected), 'rb')}
    data = {'chat_id' : "339387792"}
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

def listen():
    last = None
    while True:
        text = latest()
        if text != last:
            print (text)
            print (last)
            if last != None:

                if text.startswith('What is'):
                    rez = wiki(text)
                    this = urllib.parse.quote_plus(rez)
                    r.post(r'%s/sendMessage?text=%s&chat_id=339387792'%(funny,str(this)))
                else:
                    r.post(r'%s/sendMessage?text=%s&chat_id=339387792'%(funny,'yes'))

                if text.startswith('+audio'):
                    sendAudio()

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

    twitter = Base()

    parser = argparse.ArgumentParser(description='Funny bot and friends')
    parser.add_argument('--info', help='Basic Information',action="store_true")
    parser.add_argument('--new', help='Latest Messages',action="store_true")
    parser.add_argument('--say', type=str, help='Speak',action="store")
    parser.add_argument('--twit', help='Twit',action="store_true")
    parser.add_argument('--listen', help='Listening daemon',action="store_true")
    parser.add_argument('--audio', help='Responds with an audio file',action="store_true")
    parser.add_argument('--image', help='Responds with an image file',action="store_true")
    args = parser.parse_args()

    if args.new:
        print ( latest() )
    if args.info:
        info()
    if args.say:
        text = urllib.parse.quote_plus(args.say)
        r.post(r'%s/sendMessage?text=%s&chat_id=339387792'%(funny,text))
    if args.twit:
        twitter.stream.filter(track='sexy')
    if args.listen:
        listen()
    if args.audio:
        sendAudio()
    if args.image:
        sendImage(chat_id="339387792")