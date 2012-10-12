from datetime import datetime
from RajivPySms import BOT_BROWSER
from mechanize import Browser
from textwrap import fill,wrap

browser = Browser()
browser.addheaders = [('User-agent', BOT_BROWSER['safari'] )]
date = datetime.strftime(datetime.now(),"%B %d, %I:%M %p")

def get_forex_rate(From = 'USD', To = 'INR'):
    msg = "Forex Rate Live:%0a"+date+"%0a- - - - - - - - - -%0a"
    data = browser.open("http://www.xe.com/ucc/convert.cgi?template=mobile&Amount=1&From="+From+"&To="+To).read()
    n = data.index('1 '+From+' =')
    m = data[n:].index(' '+To)
    msg += "" + data[n:n+m+4] + '%0a'
    n = data.index('1 '+To+' =')
    m = data[n:].index(' '+From)
    msg += data[n:n+m+4]
    msg += "%0a- - - - - - - - - -"
    return msg

def find_in_gdict(Word = 'Error'):
    if Word:
        msg, null = 'Dictionary:'+Word+'\n', None
        data = browser.open("http://www.google.com/dictionary/json?callback=dict_api.callbacks.id100&q="+Word+"&sl=en&tl=en&restrict=pr%2Cde&client=te").read()[25:-1]
        result = eval('('+data+')')[0]
        for primary in result.get('primaries',[]):
            for term in primary.get('terms'):
                for label in term.get('labels',[]):
                    if label['title'] == 'Part-of-speech' and label['text'] not in msg: 
                        msg += '~'+label['text']+'\n'
                        get_eg = True
            for entry in primary.get('entries'):
                for term in entry.get('terms'):
                    if not term.get('labels',[{}])[0].get('text') and get_eg:
                        msg += term.get('text','').replace('<em>','').replace('</em>','') + '\n'
                        get_eg = False
                    for eentry in entry.get('entries',[]):
                        for eterm in eentry.get('terms'):
                            if get_eg:
                                msg += '-'+eterm.get('text','').replace('<em>','').replace('</em>','').replace('<b>','').replace('</b>','')+'\n'
                                get_eg = False
        empty = len(msg.strip()) == 0
        for entry in result.get('webDefinitions',[{}])[0].get('entries',[]):
            if empty:
                msg = entry.get('terms',[{}])[0].get('text').replace('&quot;','"').replace('&#39;',"'")
                empty = False
        return unicode(msg.strip().replace("\n","%0a"),errors='ignore')
    else: 
        return False

