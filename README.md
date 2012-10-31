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

- **Gold Rates in India**

    To get the Daily variations in Gold rates in INR. 
    Includes Rates for 22-Caret and 24-Carets at Chennai, Mumbai, Delhi, Kolkata.


Note:
-----

- refer **sample_application.py** for more options and usages. sample_application.py is a stand-alone console app too :-)
- for more information refer the wiki page of the project
- your mobile number will be prepended with your message text
- the '&' symbol will be changed to 'and'

- - -
