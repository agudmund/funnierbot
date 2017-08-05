#!/usr/bin/env python
# *-* coding: utf-8  *-*
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

funny = 'https://api.telegram.org/bot333486385:AAFGYg14V7hJJqRKyTx5tF2sb2beEu07MCg'

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

def wiki(text):
    '''Checks wikipedia for generic descriptions'''
    
    query = text.lstrip('What is')
    
    rez = wikipedia.search(query)
    that = (random.choice(rez))
    something = wikipedia.summary(that)

    return something

if __name__ == '__main__':

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
        if args.say == 'image':
            sendImage()
        else:
            text = urllib.parse.quote_plus(args.say)
            r.post(r'%s/sendMessage?text=%s&chat_id=339387792'%(funny,text))
    
    if args.twit:
        twitter.stream.filter(track='sexy')

    if args.listen:
        listen()
    if args.audio:
        sendAudio()
    if args.image:
        sendImage()