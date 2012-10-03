#!/usr/bin/python
from RajivPySms import RajivSmsModule

def send_instant_sms(MyPager, RECEIVER=False, MESSAGE=False):
    'instant sms to a receiver'
    if RECEIVER and MESSAGE: MyPager.send(RECEIVER,MESSAGE)
    else:
        RECEIVER    = raw_input("Receiver no: ")
        MESSAGE     = raw_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE)

def start_one_to_one_chat(MyPager, RECEIVER=False):
    'Its like sms chat, simultaneous message to single person'
    if not RECEIVER: RECEIVER = raw_input("Receiver no: ")
    begun = 'y'
    while begun == 'y':
        MESSAGE = raw_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE)
        begun = raw_input("Want send another sms(y/n): ")

def send_group_sms(MyPager, RECEIVERS=False, CONTACT_CSV_FILE=False, MESSAGE=False):
    'Its like group sms: Send a message to "comma seperated numbers" OR "all contacts in a csv file"'
    if not CONTACT_CSV_FILE:
        if not RECEIVERS:
            RECEIVERS = raw_input("Receivers no(comma seperated): ")
    else:
        RECEIVERS = ''
        for contact in open(CONTACT_CSV_FILE,'r'):
            RECEIVERS += contact.split(',')[1]+','

    if not MESSAGE:
        MESSAGE = raw_input("Your msg: ")
    #======================= confirm before sending  ================
    size,parts,msg = MyPager.check_message_size(MESSAGE)
    print "message size: %d chars"%(size)
    if parts != 1:
        print "split into: %d parts"%(parts)
    print "your message: %s"%(msg)
    permit = raw_input("continue?(y/n) :")
    if permit == 'n':
        print "! sending process stopped.."
        return False
    #================================================================

    for RECEIVER in RECEIVERS.split(','):
        MyPager.send(RECEIVER,MESSAGE)
    return True

def main():
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


if __name__ == "__main__":
    main()
