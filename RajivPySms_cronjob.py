#!/usr/bin/python
import RajivPySms
import bitly
import RajivPearlsAddon
#import pynotify
import os

from twitter import Api as TwitterApi
from mechanize import Browser
from BeautifulSoup import BeautifulSoup,BeautifulStoneSoup
from datetime import datetime

browser = Browser()
browser.addheaders = [('User-agent', RajivPySms.BOT_BROWSER['chrome'] )]
browser.method = "POST"
date = datetime.now()
global Twitter,T_status
Twitter,T_status = None, False

contacts = open(os.path.join(RajivPySms.DATA_DIR,'RajivPySms_contacts.csv')).readlines()

titles = [ msg_title.strip() for msg_title in contacts[0].split(',')[2:] ]
RECEIVERS = { title:[] for title in titles }
for line in contacts[1:]:
    contact     = line.split(',')
    number      = contact[1]
    permission  = [ eval("("+permission.strip()+")") for permission in contact[2:] ]
    for i in range(len(titles)):
        if permission[i]:
            RECEIVERS[titles[i]].append(number)

TIMINGS         = eval('('+open(os.path.join(RajivPySms.DATA_DIR,'RajivPySms_timings.json')).read()+')')
SMS_TIMINGS     = TIMINGS['sms_timings']
TWITTER_TIMINGS = TIMINGS['twitter_timings']

SIGNATURE = '~ SMS Seva Rajiv-Py-SMS'
SERVICE   = '160by2'

DATA = {}
def prepare_data(Type=None):
    if Type not in DATA:
        print "preparing data:",Type
        if   Type == "ForexSms":    DATA["ForexSms"]    = RajivPearlsAddon.get_forex_rate()
        elif Type == "GoldSms":     DATA["GoldSms"]     = RajivPearlsAddon.gold_rate_india()
        elif Type == "BkSms":       DATA["BkSms"]       = RajivPearlsAddon.bk_thought_for_today()
        elif Type == "BlogSms":     DATA["BlogSms"]     = RajivPearlsAddon.random_blog()
        elif Type == "WeatherSms":  DATA["WeatherSms"]  = RajivPearlsAddon.get_weather()

MyPager = RajivPySms.RajivSmsModule()
MyPager.config(SIGNATURE = SIGNATURE, SERVICE = SERVICE)

#def notify_me(status,message):
#	pynotify.init("Rajiv-Py-Sms")
#        notification=pynotify.Notification (status,message,"dialog-information")
#        notification.show()

def send_sms(Type=None):
    if not MyPager.config()['Login_status']: MyPager.login()
    prepare_data(Type)
    print "sending",Type
    status = ''
    for RECEIVER in RECEIVERS[Type]: status = MyPager.send(RECEIVER,MESSAGE=DATA[Type])
    return status
    
def send_tweets(Type=None):
    global Twitter,T_status
    if not T_status:
        print "Twitter login attempt.."
        Twitter = TwitterApi(
            consumer_key        = RajivPySms.CREDENTIALS['twitter']['consumer_key'],
            consumer_secret     = RajivPySms.CREDENTIALS['twitter']['consumer_secret'], 
            access_token_key    = RajivPySms.CREDENTIALS['twitter']['access_token_key'], 
            access_token_secret = RajivPySms.CREDENTIALS['twitter']['access_token_secret']
        )
        T_status = True
    prepare_data(Type)
    print "tweeting",Type
    Twitter.PostUpdate(DATA[Type])


# ==========================================================================================
if date.minute == 0:
    for Type in SMS_TIMINGS:
        if date.hour in SMS_TIMINGS[Type]: 
            #notify_me("Rajiv-Py-Sms:","Sending Alerts for "+Type)
            send_sms(Type)
    for Type in TWITTER_TIMINGS: 
        if date.hour in TWITTER_TIMINGS[Type]: 
            #notify_me("Rajiv-Py-Sms:","Posting tweets @rajivm1991 "+Type)
            send_tweets(Type)
#send_tweets("BlogSms")
#send_sms("BlogSms")
#else:
#    notify_me("Hey Idiot...","Don't you have brain?")
