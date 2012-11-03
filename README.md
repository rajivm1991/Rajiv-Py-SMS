Rajiv-Py-SMS
============

An easy to use Python module for sending SMS.

This module currently supports following sms services

- 160by2
- Way2Sms
- Site2sms (comming soon)
- FullOnSms (comming soon)

Pre-Requirements:
-----------------
we need a python package called "mechanize"

you can install it through **sudo pip install mechanize** or the other ways as shown here http://wwwsearch.sourceforge.net/mechanize/download.html

Easy Usage Steps:
-----------------
    from RajivPySms import RajivSmsModule
    
    MyPager = RajivSmsModule()                              # create a object to use RajivSmsModule
    
    MyPager.login(  UNAME    = '7411129611',
                    PWD      = 'way2smsPassword')           # fill your way2sms login and password
    
    MyPager.send(   RECEIVER = "9952113011",
                    MESSAGE  = "Have a nice day & night..."
                )                                           

    # Wow!!!, your sms has been sent...
    
for the above sending command, the message sent will be look like

    7411129611:
    Have a nice day and night...

Rajiv-Pearls-Addon
==================

This Pearls Addon provides awesome resources to the Rajiv-Py-SMS module.

Features of Rajiv-Pearls-Addon:
-------------------------------

- **Forex-Rates** of various country's Currencies up-to the current time lively from **XE.com**

    **Supported currencies:**
    *   INR - India Rupees
    *   USD - United States Dollars
    *   AUD - Australia Dollars
    *   CAD - Canada Dollars
    *   CHF - Switzerland Francs
    *   CNY - China Yuan Renminbi
    *   DKK - Denmark Kroner
    *   EUR - Euro
    *   GBP - United Kingdom Pounds
    *   HKD - Hong Kong Dollars
    *   HUF - Hungary Forint
    *   JPY - Japan Yen
    *   MXN - Mexico Pesos
    *   MYR - Malaysia Ringgits
    *   NOK - Norway Kroner
    *   NZD - New Zealand Dollars
    *   RUB - Russia Rubles
    *   SEK - Sweden Kronor
    *   SGD - Singapore Dollars
    *   THB - Thailand Baht
    *   USD - United States Dollars
    *   ZAR - South Africa Rand

- **Google Dictionary**

    To get the dict meaning of words online, using Google's Dictionary API.

- **Thoughts for Today**

    To start our day with positive vibrations, get the Brahmakumaris Thoughts for today from BKWSU.org Newyork.

- **Weather Forcast**

    Feel safety before going out of home by getting the latest updates of Weather forcast of your city from worldweatheronline.com

- **Gold Rates in India**

    To get the Daily variations in Gold rates in INR. 
    
    Includes Rates for 22-Caret and 24-Carets at Chennai, Mumbai, Delhi, Kolkata.

- **Random Post from your Wordpress blog**

    Will choose a random post from your Wordpress.com blog. (configured default with http://gulzarmanzil.wordpress.com - My Personal Blog)
    
    Retrives Title and URL of the post.
    
    The highlight is if Title + URL exeeds 130 charecters, the URL will automatically shortened using Optional Bitly library.

RajivPySms-Cron-Job(coming soon)
================================

This is automatic SMS notification sender. All you need to do is edit your cron-job file and point it to RajivPySms_cronjob.py script. 

You can configure the RECEIVERS, TIMINGS and Type of Message to send..

Automatic Twitter postings also available. It can be configured with TIMINGS and Type of Message to tweet..

Note:
-----

- for fast user experience fill all your accounts and API credentials in **RajivPySms_credentials.json**
- refer **sample_application.py** for more options and usages. sample_application.py is a stand-alone console app too :-)
- for more information refer the wiki page of the project( still not done! Need help to document.. )
- your Mobile-No will be prepended with your message text
- your Signature will be appended with your message text

- - -
