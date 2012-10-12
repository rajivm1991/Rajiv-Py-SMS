#!/usr/bin/python
from time import sleep
from textwrap import fill,wrap
import getpass
from BeautifulSoup import BeautifulSoup

# global variables
BOT_BROWSER = { 
    'firefox' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/16.0.1-1.fc9 Firefox/13.0.1', # for Mozilla FireFox 13.0.1
    'chrome'  : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19', # for Google Chrome 18.0.1025.168
    'safari'  : 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25', # for Apple Safari 6.0 Mobile/10A5355d
}
SERVICE_DATA = {
    'way2sms' : {   
        'login'         : "'http://site2.way2sms.com/Login1.action?username=%s&password=%s'%(UNAME,PWD)",
        'send'          : "'http://site2.way2sms.com/quicksms.action?MobNo=%s&textArea=%s&HiddenAction=%s&Action=%s&catnamedis=%s'%(RECEIVER,MSG,HIDDEN,ACTION,CATEGORY)",
        'allowed_chars' : 130,
    },
    '160by2'  : {
        'login'         : "'http://www.160by2.com/re-login?username=%s&password=%s&button=Login'%(UNAME,PWD)",
        'send'          : "'http://www.160by2.com/SendSMSAction?hid_exists=no&action1=%s&mobile1=%s&msg1=%s&btnsendsms=Send+Now'%(ACTION,RECEIVER,MSG)",
        'allowed_chars' : 140,
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
        htmldata = self.browser.open( generate_url( 
                SERVICE = self.SERVICE, 
                TYPE    = 'login', 
                UNAME   = UNAME,
                PWD     = PWD
            )
        )
        self.Login_status = Soup_check(htmldata.read())
        print_browser_response(self.browser)
        self.USER = self.Login_status and UNAME or 'No Logged in user'
        return self.Login_status
        
    
    def config(self, SIGNATURE=None, SPLIT_OR_TRUNCATE=None, SERVICE=None):
        if SIGNATURE != None:          self.SIGNATURE = SIGNATURE.strip()
        if SPLIT_OR_TRUNCATE != None:  self.SPLIT_OR_TRUNCATE = SPLIT_OR_TRUNCATE
        if SERVICE != None:
            if SERVICE in SERVICE_DATA: self.SERVICE = SERVICE

        data = { 'SIGNATURE'         : self.SIGNATURE,
                 'SPLIT_OR_TRUNCATE' : self.SPLIT_OR_TRUNCATE,
                 'Login_status'      : self.Login_status,
                 'USER'              : self.USER,
                 'SERVICE'           : self.SERVICE,
                 'allowed_chars'     : SERVICE_DATA[ self.SERVICE ][ 'allowed_chars' ],
                 'AVAILABLE_SERVICES': SERVICE_DATA.keys(),
                 }
        
        return data

    def check_message_size(self, MESSAGE):
        allowed_chars = SERVICE_DATA[ self.SERVICE ][ 'allowed_chars' ]
        MESSAGE = MESSAGE.strip()
        if self.SIGNATURE: MESSAGE += '\n' + self.SIGNATURE
        length = len(MESSAGE.replace('%0a','\n'))
        parts = 1
        if length > allowed_chars: 
            parts = len ( wrap(MESSAGE.replace('%0a','\n'), width=(allowed_chars-16), fix_sentence_endings=True) )
        return length,parts,MESSAGE

    def send(self,RECEIVER,MESSAGE,CONFIRM_BEFORE_SENDING = False):
        RECEIVER, MESSAGE = RECEIVER.strip(), MESSAGE.strip()
        allowed_chars = SERVICE_DATA[ self.SERVICE ][ 'allowed_chars' ]
        if self.Login_status:
            if MESSAGE != '':
                if len(RECEIVER) == 10:
                    length,parts,final_msg = self.check_message_size(MESSAGE)
                    if CONFIRM_BEFORE_SENDING:
                        if get_conformation(length,parts,final_msg,self.SPLIT_OR_TRUNCATE) == 'n':
                            print "! sending process stopped.."
                            return False
                    print "sending msg to %s..."%(RECEIVER)
                    MESSAGE = final_msg
                    MSG_list = []
                    if parts == 1:
                        MSG_list.append( MESSAGE )
                    else:
                        if self.SPLIT_OR_TRUNCATE:
                            MESSAGE = wrap(MESSAGE, width=(allowed_chars-16), fix_sentence_endings=True,  replace_whitespace=False)
                            #multipart sms append text like --> ' [part 01 of 03]' with every part of sms
                            MSG_list = [ (MESSAGE[i] + '\n[part %0.2d of %0.2d]'%(i+1,len(MESSAGE))) for i in range(len(MESSAGE)) ]
                        else:
                            MSG_list.append( MESSAGE[:allowed_chars] )
                    try:
                        part = 1
                        htmldata = ''
                        for MSG in MSG_list:
                            htmldata = self.browser.open(  generate_url( 
                                    SERVICE  = self.SERVICE, 
                                    TYPE     = 'send', 
                                    RECEIVER = RECEIVER,
                                    MSG      = MSG
                                )
                            )
                            if parts > 1:
                                print '\tpart',part,'of',parts,'sent'
                                part += 1
                            sleep(1)
                        status = print_browser_response(self.browser)
                        Soup_check(htmldata.read())
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
    print "+++++++++++++++ Browser Response +++++++++++++++++"
    response = browser.response().info()
    status   = False if 'pragma' in response else True
    #print "+|",["response: Failure","response: Success"][status]
    #print "+|",browser.geturl().split('/')[-1].split('.action?')[-1]#.split('&')[0].split('=')[-1].replace('+',' ').replace('%3A',':')
    print "+|",browser.geturl().split('/')[-1]
    print "++++++++++++++++++++++++++++++++++++++++++++++++++"
    return status

def generate_url(SERVICE, TYPE, UNAME='', PWD='', RECEIVER='', MSG=''):
    HIDDEN   = "instantsms"
    CATEGORY = "Friendship+Day"
    ACTION   = "sa65sdf656fdfd"
    UNAME, PWD, RECEIVER, MSG = UNAME.replace(' ','').strip(), PWD.replace(' ','').strip(), RECEIVER.replace(' ','').strip(), MSG.strip()
    replace_chars = [
        ('\n','%0a'),        ('"', '%22'),        ('<', '%3c'),        ('>', '%3e'),
        ('{', '%7b'),        ('}', '%7d'),        ('|', '%7c'),        ('\\', '%5c'),
        ('^', '%5e'),        ('~', '%7e'),        ('[', '%5b'),        (']', '%5d'),
        ('`', '%60'),        ('$', '%24'),        ('&', '%26'),        ('+', '%2b'),
        (',', '%2c'),        ('/', '%2f'),        (':', '%3a'),        (';', '%3b'),
        ('=', '%3d'),        ('?', '%3f'),        ('@', '%40'),        (' ', '%20'),
        ('#', '%23'),
    ]
    for From,To in replace_chars:
        MSG = MSG.replace(From, To)
    URL      = eval(SERVICE_DATA[ SERVICE ][ TYPE ])
    return URL

def get_conformation(length,parts,final_msg,SPLIT_OR_TRUNCATE):
    print "********* your message is ********"
    print final_msg.replace('%0a','\n')
    print "**********************************"
    allow = 'n'
    print "message length: %d, "%(length),
    if parts > 1:
        allow = raw_input("your message will be splitted into %2d parts, do you want to proceed(y/n): "%(parts) if SPLIT_OR_TRUNCATE else "your message is %d long, it will be truncated to 130 chars, do you want to proceed sending(y/n): "%(length))
    else:
        allow = raw_input("do you want to proceed sending(y/n): ")
    if allow != 'y': allow = 'n'
    return allow

def Soup_check(html):
    soup = BeautifulSoup(html)
    
    confirmation160 = soup.find('div', attrs={"class":"h-sta"})
    if confirmation160: 
        print "+++++++++++++++ Service Response +++++++++++++++++"
        print "+|",confirmation160.find('h2').findAll(text=True)[0].strip().replace('\r','')
        print "++++++++++++++++++++++++++++++++++++++++++++++++++"

    w2s_Confirmation = soup.find('div', attrs={"class":"confirm"})
    if w2s_Confirmation:
        print "+++++++++++++++ Service Response +++++++++++++++++"
        print "+|",w2s_Confirmation.find('h2').findAll(text=True)[0]
        print "++++++++++++++++++++++++++++++++++++++++++++++++++"

    w2sms_mobile_no = soup.find('div', attrs={"class" : "mobile-in"})
    if w2sms_mobile_no:
        print "+++++++++++++ Way2Sms Login Detail +++++++++++++++"
        name = soup.find('span', attrs={"onmouseover":"dismouout();"})
        print "+| Name:",name.findAll(text=True)[0]
        
        Text_list = w2sms_mobile_no.findAll(text=True)
        cut = ['\t','\n','\r','  ','.']
        for text in Text_list[:]:
            i = Text_list.index(text)
            for s in cut: 
                text = text.replace(s,'')
            Text_list[i] = text
            if not text: 
                Text_list.remove(text)
        print "+|",': '.join(Text_list)
        
        email = str(soup.find('input', attrs={"id":"logemail"}))
        print "+| Email:",email[email.index('value=')+7:email.index('>')-3]

        ips = soup.find('div', attrs={"class" : "item1 flt ip"})
        Text_list = ips.findAll(text=True)
        cut = ['&nbsp;', '\n', ' ']
        for text in Text_list[:]:
            i = Text_list.index(text)
            for s in cut: 
                text = text.replace(s,'')
            Text_list[i] = text
            if not text: 
                Text_list.remove(text)
        for i in range(0,len(Text_list),2): print "+|",Text_list[i],Text_list[i+1] if i+1 < len(Text_list) else ''
        return True

    acc_details = soup.find('div',attrs={"class" : "mad"} )
    if acc_details:
        print "++++++++++++++ 160by2 Login Detail +++++++++++++++"
        Text_list = acc_details.findAll(text=True)
        rem = [u'Change Password', u'(Change)', u'\n' ]
        cut = ['&nbsp;',]
        for text in Text_list[:]:
            if [x for x in rem if x in text]: 
                Text_list.remove(text)
            else:
                i = Text_list.index(text)
                for s in cut: 
                    text = text.replace(s,'')
                Text_list[i] = text
                    
        print "$|",Text_list[0]
        for i in range(1,len(Text_list),3): print "+| %s%s %s"%(Text_list[i], Text_list[i+1] if i+1 < len(Text_list) else '' , Text_list[i+2] if i+2 < len(Text_list) else '' )

        last_login = soup.find('div',attrs={"class" : "lh"} )
        Text_list = last_login.findAll(text=True)
        rem = [u'\n', u'about', u'view', u'button']
        for text in Text_list[:]:
            if [x for x in rem if x in text]: 
                Text_list.remove(text)
            else:
                i = Text_list.index(text)
                for s in cut: 
                    text = text.replace(s,'')
                Text_list[i] = text
        print "$|",Text_list[0]
        for i in range(1,len(Text_list),3): print "+| %s%s %s"%(Text_list[i], Text_list[i+1] if i+1 < len(Text_list) else '' , Text_list[i+2] if i+2 < len(Text_list) else '' )
        return True
        
    return False
