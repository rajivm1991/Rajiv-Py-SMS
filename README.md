Rajiv-Py-SMS
============

An easy to use Python module for sending SMS.

This module currently supports sending sms through Way2Sms.

Usage:
======
    from RajivPySms import RajivSmsModule
    
    MyPager = RajivSmsModule() # create a object to use RajivSmsModule
    
    MyPager.login(UNAME='9876543210',PWD='way2smsPassword') # fill your way2sms login and password
    
    MyPager.set_signature(" ~ By Rajiv") # This signature will be appended with every sms you are sending
    
    MyPager.send(RECEIVER = "9952113011", MESSAGE = "Good Morning, Have a nice day...")
    
