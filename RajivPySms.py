#!/usr/bin/python
from time import sleep
from textwrap import fill
import getpass
class RajivSmsModule:
    HIDDEN, ACTION, CATEGORY = "instantsms", "sa65sdf656fdfd", "Friendship+Day"
    SIGNATURE, USER = "", ""
    SPLIT_OR_TRUNCATE = True
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
        MESSAGE = MESSAGE.replace('&','and').strip() + self.SIGNATURE.replace('+',' ')
        parts = 1 if len(MESSAGE)<130 else ( (len(MESSAGE)/114) + (1 if len(MESSAGE)%114 else 0) )
        return len(MESSAGE),parts,MESSAGE

    def send(self,RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = False):
        RECEIVER, MESSAGE = RECEIVER.strip(), MESSAGE.strip()
        if self.Login_status:
            if MESSAGE != '':
                if len(RECEIVER) == 10:
                    length,parts,final_msg = self.check_message_size(MESSAGE)
                    if CONFIRM_BEFORE_SENDING and parts > 1:
                        allow = raw_input("your message will be splitted into %2d parts, do you want to proceed(y/n): "%(parts) if self.SPLIT_OR_TRUNCATE else "your message is %d long, it will be truncated to 130 chars, do you want to proceed sending(y/n): "%(length))
                        if allow == 'n':
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
                            self.browser.open("http://site2.way2sms.com/quicksms.action?MobNo="+RECEIVER+"&textArea="+MSG+"&HiddenAction="+self.HIDDEN+"&Action="+self.ACTION+"&catnamedis="+self.CATEGORY)
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
    print "+|","response: Success" if status else "response: Failure"
    print "+|",browser.geturl().split('/')[-1].split('.action?')[-1].split('&')[0].split('=')[-1].replace('+',' ').replace('%3A',':')
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return status

