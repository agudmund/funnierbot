#!/usr/bin/env python
# *-* coding:utf-8 *-*

def keys():
	with open('keys.txt') as data:
		result = data.read()

	return [n.rstrip('\r') for n in result.split('\n')]