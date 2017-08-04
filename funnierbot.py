#!/usr/bin/env python
# *-* coding: utf:8  *-*
#
#  Very minimal Telegram chat bot client
# only echos back positive reinforcement and wikipedia things
#
# -aeVar 2017

import requests as r
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

if __name__ == '__main__':
    info()