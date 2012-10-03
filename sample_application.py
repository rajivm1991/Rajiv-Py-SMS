#!/usr/bin/python
from RajivPySms import *

if __name__ == "__main__":
    #======================= You can Run this program as a Stand Alone App ===========================
    MyPager = RajivSmsModule()
    option = '0'
    while option != 'x':
        print """
+---+------+------+------+------+------+------+
|                    Options                  |
| i - Instant SMS                             |
| c - Chat                                    |
| g - Group SMS                               |
| a - Sms to all contacts in sms_contact.csv  |
| s - set/change signature                    | (current sign: %s)
| l - login/re-login                          | (current user: %s)
| x - Exit                                    |
+---+------+------+------+------+------+------+
"""%(MyPager.get_signature(),MyPager.get_user())
        option = raw_input('Select your option: ')
        if   option == 'i': send_instant_sms(MyPager)
        elif option == 'c': start_one_to_one_chat(MyPager)
        elif option == 'g': send_group_sms(MyPager)
        elif option == 'a': send_group_sms(MyPager,CONTACT_CSV_FILE="sms_contact.csv")
        elif option == 's': MyPager.set_signature(raw_input("enter your new sign: "));print "success!!"
        elif option == 's': MyPager.set_signature(raw_input("enter your new sign: "));print "success!!"
        elif option == 'l': MyPager.login()
        elif option != 'x': print 'invalid option'
        
