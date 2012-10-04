#!/usr/bin/python
from RajivPySms import RajivSmsModule

def send_instant_sms(MyPager, RECEIVER=False, MESSAGE=False):
    'instant sms to a receiver'
    if RECEIVER and MESSAGE: MyPager.send(RECEIVER,MESSAGE)
    else:
        RECEIVER    = raw_input("Receiver no: ")
        MESSAGE     = raw_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = True)

def start_one_to_one_chat(MyPager, RECEIVER=False):
    'Its like sms chat, simultaneous message to single person'
    if not RECEIVER: RECEIVER = raw_input("Receiver no: ")
    begun = 'y'
    while begun == 'y':
        MESSAGE = raw_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = True)
        begun = raw_input("Want send another sms(y/n): ")

def send_group_sms(MyPager, RECEIVERS=False, CONTACT_CSV_FILE=False, MESSAGE=False):
    'Its like group sms: Send a message to "comma seperated numbers" OR "all contacts in a csv file"'
    if not CONTACT_CSV_FILE and not RECEIVERS:
        print """
+---+------+------+------+------+------+------+------+-----+
|                     Group SMS option:                    |
| m - manually enter some comma seperated receiver numbers |
| c - csv file name containing list of contacts            |
+---+------+------+------+------+------+------+------+-----+
"""
        option = raw_input('Select your option: ')
        if option == 'm':
            RECEIVERS = raw_input("Receivers numbers(comma seperated): ")
            RECEIVERS = RECEIVERS.split(',')
        elif option == 'c':
            CONTACT_CSV_FILE = raw_input("Contact csv file name: ")
            RECEIVERS = [ contact.split(',')[1] for contact in open(CONTACT_CSV_FILE,'r') ]

    elif RECEIVERS: RECEIVERS = RECEIVERS.split(',')

    elif CONTACT_CSV_FILE: RECEIVERS = [ contact.split(',')[1] for contact in open(CONTACT_CSV_FILE,'r') ]

    if not MESSAGE: MESSAGE = raw_input("Your msg: ")
    
    for RECEIVER in RECEIVERS: MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = True)

    return True

def main():
    #======================= You can Run this program as a Stand Alone App ===========================
    MyPager = RajivSmsModule()
    option = '0'
    while option != 'x':
        print """
+---+------+------+------+------+------+------+
|              Main Menu Options              |
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


if __name__ == "__main__":
    main()
