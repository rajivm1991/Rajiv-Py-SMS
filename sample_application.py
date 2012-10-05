#!/usr/bin/python
from RajivPySms import RajivSmsModule,get_conformation

def send_instant_sms(MyPager, RECEIVER=False, MESSAGE=False):
    'instant sms to a receiver'
    if not MyPager.config()['Login_status']: 
        print '+++++++++++++++++++++++++'
        print '+| Please login first  |+'
        print '+++++++++++++++++++++++++'
        return False
    if RECEIVER and MESSAGE: MyPager.send(RECEIVER,MESSAGE)
    else:
        RECEIVER    = raw_input("Receiver no: ")
        MESSAGE     = raw_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = True)

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
        MESSAGE = raw_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = True)
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
            RECEIVERS = [ contact.split(',')[1] for contact in open(CONTACT_CSV_FILE,'r') ]

    elif RECEIVERS: RECEIVERS = RECEIVERS.split(',')

    elif CONTACT_CSV_FILE: RECEIVERS = [ contact.split(',')[1] for contact in open(CONTACT_CSV_FILE,'r') ]

    if not MESSAGE: MESSAGE = raw_input("Your msg: ")
    
    length,parts,final_msg = MyPager.check_message_size(MESSAGE)
    if get_conformation(length, parts, final_msg,SPLIT_OR_TRUNCATE = MyPager.config()['SPLIT_OR_TRUNCATE'] ) == 'n':
        print "! sending process stopped.."
        return False

    for RECEIVER in RECEIVERS: MyPager.send(RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = False)
    return True

def main():
    #======================= You can Run this program as a Stand Alone App ===========================
    MyPager = RajivSmsModule()
    option = '0'
    while option != 'x':
        conf_data = MyPager.config()
        print """
+---+------+------+------+------+------+------+     
|              Main Menu Options              |     +---+---+---+---+---Pager Status:---+---+---+---+---+
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
        if   option == 'i': send_instant_sms(MyPager)
        elif option == 'c': start_one_to_one_chat(MyPager)
        elif option == 'g': send_group_sms(MyPager)
        elif option == 'a': send_group_sms(MyPager,CONTACT_CSV_FILE="sms_contact.csv")
        elif option == 's': MyPager.config(SIGNATURE = raw_input("enter your new sign: "));print "done!!"
        elif option == 'd':
            AVAILABLE_SERVICES = MyPager.config()['AVAILABLE_SERVICES']
            print "+---+------+------+------+-----+"
            print "    Available SMS Services:     "
            for service in AVAILABLE_SERVICES:
                print "%d - %s"%( AVAILABLE_SERVICES.index(service)+1, service )
            print "+---+------+------+------+-----+"
            my_selection = raw_input("select your favourite service: ")
            MyPager.config(SERVICE = AVAILABLE_SERVICES[ int(my_selection)-1 ]);print "done!!"
        elif option == 't':
            print """
+---+------+------+------+-----+
| If sms > allowed characters: |
| s - split and send           |
| t - truncate and send        |
+---+------+------+------+-----+"""
            my_sending_method = raw_input("select your sending method: ")
            if   my_sending_method == 's': MyPager.config( SPLIT_OR_TRUNCATE = True )
            elif my_sending_method == 't': MyPager.config( SPLIT_OR_TRUNCATE = False )
        elif option == 'l': MyPager.login()
        elif option != 'x': print 'invalid option'


if __name__ == "__main__":
    main()
