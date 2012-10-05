#!/usr/bin/python
from time import sleep
from textwrap import fill
import getpass

# global variables
BOT_BROWSER = { 
    'firefox' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/16.0.1-1.fc9 Firefox/13.0.1', # for Mozilla FireFox 13.0.1
    'chrome'  : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19', # for Google Chrome 18.0.1025.168
    'safari'  : 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25', # for Apple Safari 6.0 Mobile/10A5355d
}
SERVICE_URL = {
    'way2sms' : {   
        'login' : "'http://site2.way2sms.com/Login1.action?username=%s&password=%s'%(UNAME,PWD)",
        'send'  : "'http://site2.way2sms.com/quicksms.action?MobNo=%s&textArea=%s&HiddenAction=%s&Action=%s&catnamedis=%s'%(RECEIVER,MSG,HIDDEN,ACTION,CATEGORY)",
    },
    '160by2'  : {
        'login' : "'http://www.160by2.com/re-login?username=%s&password=%s&button=Login'%(UNAME,PWD)",
        'send'  : "'http://www.160by2.com/SendSMSAction?hid_exists=no&action1=%s&mobile1=%s&msg1=%s&btnsendsms=Send+Now'%(ACTION,RECEIVER,MSG)",
    },
}
class RajivSmsModule:
    USER                = "No Logged in user"
    SPLIT_OR_TRUNCATE   = True  # True - split-mode ; False - truncate-mode
    SIGNATURE           = ""
    Login_status        = False
    SERVICE             = "way2sms"

    def __init__(self):
        from mechanize import Browser
        self.browser = Browser()
        # This is really Cheating with Bot Browser as (firefor/chrome/safari)
        self.browser.addheaders = [('User-agent', BOT_BROWSER['safari'] )]
        self.browser.method = "POST"
        
    def login(self,UNAME='',PWD=''):
        if not UNAME: UNAME = raw_input("Enter Your Mobile number: ")
        if not PWD:   PWD   = getpass.getpass("Enter Your Password: ")
        UNAME, PWD = UNAME.strip(), PWD.strip()
        print "Attempting to Login..."
        self.browser.open( generate_url( 
                SERVICE = self.SERVICE, 
                TYPE    = 'login', 
                UNAME   = UNAME,
                PWD     = PWD
            )
        )
        response = self.browser.response().info()
        #self.Login_status = 'pragma' not in response
        self.Login_status = True
        self.USER = self.Login_status and UNAME or 'No Logged in user'
        print "+++++++++++++ browser response ++++++++++++"
        #print "+|","Login Successful" if self.Login_status else "Login Failed, check your mobile number & password."
        print "+|",self.browser.geturl().split('/')[-1].split('action;')[-1].replace('?','\n+| ').replace('=',' : ')
        print "+++++++++++++++++++++++++++++++++++++++++++"
        return self.Login_status
        
    
    def config(self, SIGNATURE=None, SPLIT_OR_TRUNCATE=None, SERVICE=None):
        if SIGNATURE != None:          self.SIGNATURE = SIGNATURE.replace(' ','+')
        if SPLIT_OR_TRUNCATE != None:  self.SPLIT_OR_TRUNCATE = SPLIT_OR_TRUNCATE
        if SERVICE != None:
            if SERVICE in SERVICE_URL: self.SERVICE = SERVICE

        data = { 'SIGNATURE'         : self.SIGNATURE,
                 'SPLIT_OR_TRUNCATE' : self.SPLIT_OR_TRUNCATE,
                 'Login_status'      : self.Login_status,
                 'USER'              : self.USER,
                 'SERVICE'           : self.SERVICE,
                 'AVAILABLE_SERVICES': SERVICE_URL.keys(),
                 }
        
        return data

    def check_message_size(self, MESSAGE):
        MESSAGE = MESSAGE.replace('&','and').strip() + self.SIGNATURE.replace('+',' ')
        parts = 1 if len(MESSAGE)<130 else ( (len(MESSAGE)/114) + (1 if len(MESSAGE)%114 else 0) )
        return len(MESSAGE),parts,MESSAGE

    def send(self,RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = False):
        RECEIVER, MESSAGE = RECEIVER.strip(), MESSAGE.strip()
        if self.Login_status:
            if MESSAGE != '':
                if len(RECEIVER) == 10:
                    length,parts,final_msg = self.check_message_size(MESSAGE)
                    if CONFIRM_BEFORE_SENDING:
                        if get_conformation(length,parts,final_msg,self.SPLIT_OR_TRUNCATE) == 'n':
                            print "! sending process stopped.."
                            return False
                    print "sending msg to %s..."%(RECEIVER)
                    MESSAGE = final_msg.replace(' ','+')
                    MSG_list = []
                    if parts == 1:
                        MSG_list.append( MESSAGE )
                    else:
                        if self.SPLIT_OR_TRUNCATE:
                            MESSAGE = fill(MESSAGE, width=114, fix_sentence_endings=True).split('\n')
                            MSG_list = [ (MESSAGE[i]+' [part %0.2d of %0.2d]'%(i+1,len(MESSAGE))).replace(' ','+') for i in range(len(MESSAGE)) ]
                        else:
                            MSG_list.append( MESSAGE[:130].replace(' ','+') )
                    try:
                        part,total = 1,len(MSG_list)
                        for MSG in MSG_list:
                            self.browser.open(  generate_url( 
                                    SERVICE  = self.SERVICE, 
                                    TYPE     = 'send', 
                                    RECEIVER = RECEIVER,
                                    MSG      = MSG
                                )
                            )
                            if total>1:
                                print '\tpart',part,'of',total,'sent'
                                part += 1
                            sleep(1)
                        status = print_browser_response(self.browser)
                        return status
                    except:
                        print "!Unable to send your message :P"
                        return False
                else:
                    print "!Message cannot be sent to this receiver %s :P"%(RECEIVER)
                    return False
            else:
                print "!No content in your message.."
                return False
        else:
            print "!Please login first :P"
            return False

def print_browser_response(browser):
    print "++++++++++++++++++++ browser response +++++++++++++++++++"
    response = browser.response().info()
    status   = False if 'pragma' in response else True
    #print "+|",["response: Failure","response: Success"][status]
    print "+|",browser.geturl().split('/')[-1].split('.action?')[-1]#.split('&')[0].split('=')[-1].replace('+',' ').replace('%3A',':')
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return status

def generate_url(SERVICE, TYPE, UNAME='', PWD='', RECEIVER='', MSG=''):
    HIDDEN      = "instantsms"
    CATEGORY    = "Friendship+Day"
    ACTION      = "sa65sdf656fdfd"
    URL = eval(SERVICE_URL[ SERVICE ][ TYPE ])
    return URL

def get_conformation(length,parts,final_msg,SPLIT_OR_TRUNCATE):
    print "********* your message is ********"
    print final_msg
    print "**********************************"
    allow = 'n'
    if parts > 1:
        allow = raw_input("your message will be splitted into %2d parts, do you want to proceed(y/n): "%(parts) if SPLIT_OR_TRUNCATE else "your message is %d long, it will be truncated to 130 chars, do you want to proceed sending(y/n): "%(length))
    else:
        allow = raw_input("do you want to proceed sending(y/n): ")
    if allow != 'y': allow = 'n'
    return allow

