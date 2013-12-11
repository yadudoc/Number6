#!/usr/bin/env python
import os
import time
import datetime
import json
import string
import csv
import sys
import ast
import thread, itertools
import math
import sys
import pynotify
import subprocess

capabilities = {'actions':             False,
        'body':                False,
        'body-hyperlinks':     False,
        'body-images':         False,
        'body-markup':         False,
        'icon-multi':          False,
        'icon-static':         False,
        'sound':               False,
        'image/svg+xml':       False,
        'private-synchronous': False,
        'append':              False,
        'private-icon-only':   False}

def initCaps ():
    caps = pynotify.get_server_caps ()
    if caps is None:
        print "Failed to receive server caps."
        sys.exit(1)

    for cap in caps:
        capabilities[cap] = True

def printCaps ():
    info = pynotify.get_server_info ()
    print "Name:          " + info["name"]
    print "Vendor:        " + info["vendor"]
    print "Version:       " + info["version"]
    print "Spec. Version: " + info["spec-version"]

    caps = pynotify.get_server_caps ()
    if caps is None:
        print "Failed to receive server caps."
        sys.exit (1)

    print "Supported capabilities/hints:"
    if capabilities['actions']:
        print "tactions"
    if capabilities['body']:
        print "tbody"
    if capabilities['body-hyperlinks']:
        print "tbody-hyperlinks"
    if capabilities['body-images']:
        print "tbody-images"
    if capabilities['body-markup']:
        print "tbody-markup"
    if capabilities['icon-multi']:
        print "ticon-multi"
    if capabilities['icon-static']:
        print "ticon-static"
    if capabilities['sound']:
        print "tsound"
    if capabilities['image/svg+xml']:
        print "timage/svg+xml"
    if capabilities['private-synchronous']:
        print "tprivate-synchronous"
    if capabilities['append']:
        print "tappend"
    if capabilities['private-icon-only']:
        print "tprivate-icon-only"

    print "Notes:"
    if info["name"] == "notify-osd":
        print "tx- and y-coordinates hints are ignored"
        print "texpire-timeout is ignored"
        print "tbody-markup is accepted but filtered"
    else:
        print "tnone"

def coinbase():
	p = os.popen("curl https://coinbase.com/api/v1/currencies/exchange_rates 2>/dev/null")

	all_currencies = p.read()
	all_currencies = string.replace(all_currencies,'{','')
	all_currencies = string.replace(all_currencies,'}','')
	all_currencies = string.replace(all_currencies,'"','')

	for conversion in string.split(all_currencies, ','):
		[currency, rate] = string.split(conversion, ':')
		if ( currency == "btc_to_usd" ):
			return float(rate)

def mtgox():
	p = os.popen("curl https://data.mtgox.com/api/2/BTCUSD/money/ticker 2>/dev/null")
	info = ast.literal_eval(p.read())
	return float(info['data']['last']['value'])

def alert_rule(old, current):
	delta = math.fabs(old-current)
	if current > old :
		direction = "^"
	elif current < old :
		direction = "V"
	else:
		direction = "-"
	if ( delta > 20 ):
		print "delta : ",delta," direction : ", direction
		return -1

def notify(mt, cb):
	print "in notify"
	n = pynotify.Notification ("BitCoin Alert",
							   "MtGox   : " + str(mt[2]) + " (" + str(round(mt[3],2)) + "%) \n"
							   "Coinbase: " + str(cb[2]) + " (" + str(round(cb[3],2)) + "%) \n",
							   "notification-message-im")
	n.show()

def server():
	prev_cb=90
	prev_mt=90
	counter = 0
	while True:
		time.sleep(60)
		counter += 1
		cb = coinbase()
		mt = mtgox()
		percent_cb = round ((((cb - prev_cb)/prev_cb)*100), 2)
		percent_mt = round ((((mt - prev_mt)/prev_mt)*100), 2)
		print "percent_cb : ", percent_cb
		print "percent_mt : ", percent_mt

		if (math.fabs(percent_cb) > 1.0) or (math.fabs(percent_mt) > 1.0) or (counter > 5):
			print "Notifying"
			notify(["MtGox   ", prev_mt, mt, percent_mt],
				   ["Coinbase", prev_cb, cb, percent_cb])
			prev_cb = cb
			prev_mt = mt
			counter = 0


if __name__ == "__main__":
	pynotify.init("icon-summary-body")
	initCaps()
	printCaps()
	print "Price at Coinbase : ",coinbase()
	print "Price at MtGox    : ",mtgox()
	server()

