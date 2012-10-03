#!/usr/bin/python
from time import sleep
from textwrap import fill
import getpass
class RajivSmsModule:
    HIDDEN, ACTION, CATEGORY = "instantsms", "sa65sdf656fdfd", "Friendship+Day"
    SIGNATURE, USER = "", ""
    Login_status = False
    def __init__(self):
        from mechanize import Browser
        self.browser = Browser()
        # =============== Cheating with Bot Browser as =================
        # 1.) Mozilla FireFox 13.0.1 
        #self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/16.0.1-1.fc9 Firefox/13.0.1')]
        
        # 2.) Google Chrome 18.0.1025.168 
        #self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19')]
        
        # 3.) Apple Safari 6.0 Mobile/10A5355d 
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25')]
        
        # 4.) Apple Safari 5.1.3
        #self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10')]
        
        self.browser.method = "POST"
    def login(self,UNAME='',PWD=''):
        if not UNAME: UNAME = raw_input("Enter Your Mobile number: ")
        if not PWD:   PWD   = getpass.getpass("Enter Your Password: ")
        UNAME, PWD = UNAME.strip(), PWD.strip()
        print "Attempting to Login..."
        self.browser.open("http://site2.way2sms.com/Login1.action?username="+UNAME+"&password="+PWD)
        response = self.browser.response().info()
        self.Login_status = False if 'pragma' in response else True
        self.USER = UNAME if self.Login_status else "Please login again"
        print "+++++++++++++ browser response ++++++++++++"
        print "+|","Login Successful" if self.Login_status else "Login Failed, check your mobile number & password."
        print "+|",self.browser.geturl().split('/')[-1].split('action;')[-1].replace('?','\n+| ').replace('=',' : ')
        print "+++++++++++++++++++++++++++++++++++++++++++"
        return self.Login_status
    def set_signature(self, SIGNATURE):
        self.SIGNATURE = SIGNATURE.replace(' ','+')
    def get_signature(self):
        return self.SIGNATURE.replace('+',' ')
    def get_user(self):
        return self.USER if self.USER else "Nobody logged in"
    def check_message_size(self, MESSAGE):
        MESSAGE = MESSAGE + self.SIGNATURE.replace('+',' ')
        parts = 1 if len(MESSAGE)<130 else ( (len(MESSAGE)/114) + (1 if len(MESSAGE)%114 else 0) )
        return len(MESSAGE),parts,MESSAGE
    def send(self,RECEIVER,MESSAGE):
        RECEIVER, MESSAGE = RECEIVER.strip(), MESSAGE.strip()
        if self.Login_status:
            if len(RECEIVER) == 10:
                print "sending msg to %s..."%(RECEIVER)
                MESSAGE = MESSAGE.replace('&','and') + self.SIGNATURE
                MSG_list = []
                if len(MESSAGE) > 130:
                    MESSAGE = fill(MESSAGE, width=114, fix_sentence_endings=True).split('\n')
                    MSG_list = [ (MESSAGE[i]+' [part %0.2d of %0.2d]'%(i+1,len(MESSAGE))).replace(' ','+') for i in range(len(MESSAGE)) ]
                else:
                    MSG_list.append( MESSAGE.replace(' ','+') )
                try:
                    part,total = 1,len(MSG_list)
                    for MSG in MSG_list:
                        self.browser.open("http://site2.way2sms.com/quicksms.action?MobNo="+RECEIVER+"&textArea="+MSG+"&HiddenAction="+self.HIDDEN+"&Action="+self.ACTION+"&catnamedis="+self.CATEGORY)
                        if total>1:
                            print '\tpart',part,'of',total,'sent'
                            part += 1
                        sleep(1)
                    status = print_browser_response(self.browser)
                    return status
                except:
                    print "Unable to send your message :P"
                    return False
            else:
                print "Message cannot be sent to this receiver %s :P"%(RECEIVER)
                return False
        else:
            print "Your message cannot be sent. Please login first :P"
            return False
def print_browser_response(browser):
    print "++++++++++++++++++++ browser response +++++++++++++++++++"
    response = browser.response().info()
    status   = False if 'pragma' in response else True
    print "+|","response: Success" if status else "response: Failure"
    print "+|",browser.geturl().split('/')[-1].split('.action?')[-1].split('&')[0].split('=')[-1].replace('+',' ').replace('%3A',':')
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return status

def send_instant_sms(MyPager, RECEIVER=False, MESSAGE=False):
    'instant sms to a receiver'
    if RECEIVER and MESSAGE: MyPager.send(RECEIVER,MESSAGE)
    else:
        RECEIVER    = raw_input("Receiver no: ")
        MESSAGE     = raw_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE)

def start_one_to_one_chat(MyPager, RECEIVER=False):
    'Its like chat with single person'
    if not RECEIVER: RECEIVER = raw_input("Receiver no: ")
    begun = 'y'
    while begun == 'y':
        MESSAGE = raw_input("Your msg: ")
        MyPager.send(RECEIVER,MESSAGE)
        begun = raw_input("Want send another sms(y/n): ")

def send_group_sms(MyPager, RECEIVERS=False, CONTACT_CSV_FILE=False, MESSAGE=False):
    'Its like group sms'
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

if __name__ == "__main__":
    #======================= If run as Stand Alone App ===========================
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


