Rajiv-Py-SMS
============

An easy to use Python module for sending SMS.

This module currently supports following sms services

- 160by2
- Way2Sms

Pre-Requirements:
-----------------
we need a python package called "mechanize"

you can install it through **sudo pip install mechanize** or the other ways as shown here http://wwwsearch.sourceforge.net/mechanize/download.html

Simple Usage steps:
-------------------
    from RajivPySms import RajivSmsModule
    
    MyPager = RajivSmsModule()                              # create a object to use RajivSmsModule
    
    MyPager.login(  UNAME    = '7411129611',
                    PWD      = 'way2smsPassword')           # fill your way2sms login and password
    
    MyPager.send(   RECEIVER = "9952113011", 
                    MESSAGE  = "Have a nice day & night..."
                )                                           
    # That's all, your sms has been sent...
    
for the above sending command, the message sent will be look like

    7411129611:
    Have a nice day and night...

Note:
-----
- refer **sample_application.py** for more options and usages. sample_application.py is a stand-alone console app too :-)
- for more information refer the wiki page of the project
- your mobile number will be prepended with your message text
- the '&' symbol will be changed to 'and'
- - -
