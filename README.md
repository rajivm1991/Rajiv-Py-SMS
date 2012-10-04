Rajiv-Py-SMS
============

An easy to use Python module for sending SMS.

This module currently supports sending sms through Way2Sms.

Usage:
======
    from RajivPySms import RajivSmsModule
    
    MyPager = RajivSmsModule()                              # create a object to use RajivSmsModule
    
    MyPager.login(UNAME='7411129611',PWD='way2smsPassword') # fill your way2sms login and password
    
    MyPager.set_signature(" ~ By Rajiv")                    # Signature will be appended with every sms
    
    MyPager.send(   RECEIVER = "9952113011", 
                    MESSAGE  = "Have a nice day & night..."
                )                                           
    

for the above sending command, the message sent will be look like

    7411129611:
    Have a nice day and night... ~ By Rajiv

Note:
    1. your mobile number will be prepended with your message text
    2. the '&' symbol will be changed to 'and'
    3. the signature text will be appended with your message text


