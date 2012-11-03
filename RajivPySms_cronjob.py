#!/usr/bin/python
import RajivPySms, bitly
from RajivPearlsAddon import get_forex_rate, bk_thought_for_today, gold_rate_india, random_blog, get_weather
from twitter import Api as TwitterApi
from mechanize import Browser
from BeautifulSoup import BeautifulSoup,BeautifulStoneSoup
from datetime import datetime

date = datetime.now()

browser = Browser()
browser.addheaders = [('User-agent', RajivPySms.BOT_BROWSER['chrome'] )]
browser.method = "POST"
global Twitter,T_status
Twitter,T_status = None, False

# ============================================================= Control Panel ========================

contacts = open('RajivPySms_contacts.csv').readlines()
titles = [ msg_title.strip() for msg_title in contacts[0].split(',')[2:] ]
RECEIVERS = { title:[] for title in titles }
for line in contacts[1:]:
    contact     = line.split(',')
    number      = contact[1]
    permission  = [ eval("("+permission.strip()+")") for permission in contact[2:] ]
    for i in range(len(titles)):
        if permission[i]:
            RECEIVERS[titles[i]].append(number)

TIMINGS   = eval('('+open('RajivPySms_timings.json').read()+')')
SIGNATURE = '~ SMS Seva Rajiv-Py-SMS'
SERVICE   = '160by2'

# ============================================================= Engine Section ========================

MyPager = RajivPySms.RajivSmsModule()
MyPager.config(SIGNATURE = SIGNATURE, SERVICE = SERVICE)

def get_pager_ready():
    if not MyPager.config()['Login_status']: MyPager.login()

def get_twitter_ready():
    global Twitter,T_status
    if not T_status:
        print "Twitter Login attempt..."
        Twitter = TwitterApi(
            consumer_key        = RajivPySms.CREDENTIALS['twitter']['consumer_key'],
            consumer_secret     = RajivPySms.CREDENTIALS['twitter']['consumer_secret'], 
            access_token_key    = RajivPySms.CREDENTIALS['twitter']['access_token_key'], 
            access_token_secret = RajivPySms.CREDENTIALS['twitter']['access_token_secret']
        )
        T_status = True
def shoot_forex():
        print "Sending Forex Updates"
        # Get ready
        get_pager_ready()
        # Load Bullet
        forex = get_forex_rate()
        # Shoot
        for RECEIVER in RECEIVERS['ForexSms']: MyPager.send(RECEIVER,MESSAGE=forex)
def shoot_gold():
        print "Sending Gold Updates"
        # Get ready
        get_pager_ready()
        # Load Bullet
        gold = gold_rate_india()
        # Shoot
        for RECEIVER in RECEIVERS['GoldSms']: MyPager.send(RECEIVER,MESSAGE=gold)
def shoot_bk():
        print "Sending BK Updates"
        # Get ready
        get_pager_ready()
        get_twitter_ready()
        # Load Bullet
        thought = bk_thought_for_today()
        # Shoot
        Twitter.PostUpdate(thought)
        for RECEIVER in RECEIVERS['BkSms']: MyPager.send(RECEIVER,MESSAGE=thought)
def shoot_blog():
        print "Sending Blog Updates"
        # Get ready
        get_pager_ready()
        get_twitter_ready()
        # Load Bullet
        random_blog_post = random_blog()
        # Shoot
        Twitter.PostUpdate(random_blog_post)
        for RECEIVER in RECEIVERS['BlogSms']: MyPager.send(RECEIVER,MESSAGE=random_blog_post)
def shoot_weather():
        print "Sending Weather Updates"
        # Get ready
        get_pager_ready()
        # Load Bullet
        weather = get_weather()
        # Shoot
        for RECEIVER in RECEIVERS['WeatherSms']: MyPager.send(RECEIVER,MESSAGE=weather)
if date.minute == 0:
    if date.hour in TIMINGS['ForexSms']:     shoot_forex()
    if date.hour in TIMINGS['GoldSms']:      shoot_gold()
    if date.hour in TIMINGS['BkSms']:        shoot_bk()
    if date.hour in TIMINGS['BlogSms']:      shoot_blog()
    if date.hour in TIMINGS['WeatherSms']:   shoot_weather()

