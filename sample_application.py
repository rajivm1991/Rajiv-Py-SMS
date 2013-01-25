#!/usr/bin/python
from RajivPySms import RajivSmsModule, get_conformation, DATA_DIR
import RajivPearlsAddon
#import pynotify
import os
"""def notify_me(status,message):
    pynotify.init("Rajiv-Py-Sms")
        notification=pynotify.Notification (status,message,"dialog-information")
        notification.show()"""


def multiline_input(query=None):
    print "Note: An empty line input will conclude getting input from user. Now start typing..."
    if query:
        print query
    Buffer = ''
    while True:
        line = raw_input()
        if not line:
            break
        if Buffer:
            Buffer += '\n'
        Buffer += line
    return Buffer


def send_instant_sms(MyPager, RECEIVER=False, MESSAGE=False):
    'instant sms to a receiver'
    if not MyPager.config()['Login_status']:
        print '+++++++++++++++++++++++++'
        print '+| Please login first  |+'
        print '+++++++++++++++++++++++++'
        return False
    if RECEIVER and MESSAGE:
        MyPager.send(RECEIVER,MESSAGE)
    else:
        RECEIVER    = raw_input("Receiver no: ")
        MESSAGE     = multiline_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = True)
        #notify_me("Woa!!","Cool.. You did a great job..\n~ Rajiv-Py-Sms")


def start_one_to_one_chat(MyPager, RECEIVER=False):
    'Its like sms chat, simultaneous message to single person'
    if not MyPager.config()['Login_status']:
        print '+++++++++++++++++++++++++'
        print '+| Please login first  |+'
        print '+++++++++++++++++++++++++'
        return False
    if not RECEIVER: RECEIVER = raw_input("Receiver no: ")
    begun = 'y'
    while begun == 'y':
        MESSAGE = multiline_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = True)
        #notify_me("Woa!!","Cool.. You did a great job..\n~ Rajiv-Py-Sms")
        begun = raw_input("Want send another sms(y/n): ")


def send_group_sms(MyPager, RECEIVERS=False, CONTACT_CSV_FILE=False, MESSAGE=False):
    if not MyPager.config()['Login_status']:
        print '+++++++++++++++++++++++++'
        print '+| Please login first  |+'
        print '+++++++++++++++++++++++++'
        return False
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
            RECEIVERS = [ contact.split(',')[1] for contact in open(os.path.join(DATA_DIR,CONTACT_CSV_FILE)) ]

    elif RECEIVERS: RECEIVERS = RECEIVERS.split(',')

    elif CONTACT_CSV_FILE: RECEIVERS = [ contact.split(',')[1] for contact in open(CONTACT_CSV_FILE,'r') ]

    if not MESSAGE: MESSAGE = multiline_input("Your msg: ")

    MyPager.check_message_size(MESSAGE)
    if get_conformation() == 'n':
        print "! sending process stopped.."
        return False

    for RECEIVER in RECEIVERS: MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = False)
    #notify_me("Woa!!","Cool.. You did a great job..\n~ Rajiv-Py-Sms")
    return True


def rajivpearl_sms(MyPager):
    print """
+---+------+------+------+------+------+
|            Pearl SMS options         |
| f - Current Forex Rates (XE rates)   |
| w - Weather Forcast (Bangalore)      |
| d - Dict Word search (Google Dict)   |
| g - Gold Rate Today (India - Rs/1gm) |
| o - Thought For Today (BKWSU-Newyork)|
| r - Random blog from GulzarManzil    |
| b - back                             |
+---+------+------+------+------+------+
"""
    myoption = raw_input("Select your option: ")
    MESSAGE = ''
    if   myoption == 'f':   MESSAGE = RajivPearlsAddon.get_forex_rate(From = 'USD', To = 'INR')
    elif myoption == 'w':   MESSAGE = RajivPearlsAddon.get_weather()
    elif myoption == 'd':   MESSAGE = RajivPearlsAddon.find_in_gdict(Word = raw_input("Word to search: "))
    elif myoption == 'g':   MESSAGE = RajivPearlsAddon.gold_rate_india()
    elif myoption == 'o':   MESSAGE = RajivPearlsAddon.bk_thought_for_today()
    elif myoption == 'r':   MESSAGE = RajivPearlsAddon.random_blog()
    else: return 1
    RECEIVER = raw_input('Enter receiver number: ')
    MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = True)
    #notify_me("Woa!!","Cool.. You did a great job..\n~ Rajiv-Py-Sms")


def main():
    #======================= You can Run this program as a Stand Alone Console App ===========================
    #notify_me("Hey!!","Rajiv-Py-Sms sample application has been started, enjoy sending FREE sms. Check out special messages option for more available features sms.\n~ Rajiv M")
    MyPager = RajivSmsModule()
    option = '0'
    while option != 'x':
        conf_data = MyPager.config()
        print """
+---+------+------+------+------+------+------+
|              Main Menu Options              |
| r - Rajiv Pearl - Special messages          |     +---+---+---+---+---Pager Status:---+---+---+---+---+
| i - Instant SMS                             |     SMS Service    : %s
| c - Chat                                    |     Allowed        : %d chars per sms
| g - Group SMS                               |     Sending method : Sms > %d chars will be - %s
| a - Sms to all contacts in sms_contact.csv  |     Current USER   : %s
| d - Change Service                          |     Signature text : %s
| t - Change Sending method                   |     Login Status   : %s
| s - set/change signature                    |     +---+---+---+---+---+---+---+---+---+---+---+---+---+
| l - login/re-login                          |
| x - Exit                                    |
+---+------+------+------+------+------+------+
"""%(   conf_data['SERVICE'],
        conf_data['allowed_chars'],
        conf_data['allowed_chars'],
        'Split and send as multiple sms' if conf_data['SPLIT_OR_TRUNCATE'] else 'Truncate to %d chars'%(conf_data['allowed_chars']),
        conf_data['USER'],
        conf_data['SIGNATURE'],
        'Logged in' if conf_data['Login_status'] else 'Logged out',
)
        option = raw_input('Select your option: ')
        if   option == 'r': rajivpearl_sms(MyPager)
        elif option == 'i': send_instant_sms(MyPager)
        elif option == 'c': start_one_to_one_chat(MyPager)
        elif option == 'g': send_group_sms(MyPager)
        elif option == 'a': send_group_sms(MyPager,CONTACT_CSV_FILE=os.path.join(DATA_DIR,"sms_contact.csv"))
        elif option == 's': MyPager.config(SIGNATURE = raw_input("enter your new sign: "));print "done!!"
        elif option == 'd':
            AVAILABLE_SERVICES = MyPager.config()['AVAILABLE_SERVICES']
            print "+---+------+------+------+-----+"
            print "    Available SMS Services:     "
            for service in AVAILABLE_SERVICES:
                print "%d - %s"%( AVAILABLE_SERVICES.index(service)+1, service )
            print "+---+------+------+------+-----+"
            my_selection = raw_input("select your favourite service: ")
            MyPager.config(SERVICE = AVAILABLE_SERVICES[ int(my_selection)-1 ])
            print "Service changed!. Attempting Login into current service..."
            MyPager.login()
        elif option == 't':
            print """
+---+------+------+------+-----+
| If sms > allowed characters: |
| s - split and send           |
| t - truncate and send        |
| b - back                     |
+---+------+------+------+-----+"""
            my_sending_method = raw_input("select your sending method: ")
            if   my_sending_method == 's': MyPager.config( SPLIT_OR_TRUNCATE = True )
            elif my_sending_method == 't': MyPager.config( SPLIT_OR_TRUNCATE = False )
        elif option == 'l': MyPager.login()
        elif option != 'x': print 'invalid option'
    #notify_me("You're welcome","Thanks for using Rajiv-Py-Sms sample application")


if __name__ == "__main__":
    main()
