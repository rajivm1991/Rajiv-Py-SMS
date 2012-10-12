from datetime import datetime
from RajivPySms import BOT_BROWSER
from mechanize import Browser
from textwrap import fill,wrap
from BeautifulSoup import BeautifulSoup

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

def gold_rate_india():
    data = browser.open("http://www.sify.com/finance/gold_rates/").read()
    soup = BeautifulSoup(data)
    gold = soup.find('div', attrs={"class":"rates-outer-wrapper"})
    g_list = []
    msg = 'Gold(1g) '+datetime.strftime(datetime.now(),"%d/%m/%Y")+'\n     22-Car  24-Car\n'
    for tag in gold.findAll('td', attrs={"align":"center"}):
        t = tag.findAll(text=True)
        rem = [u'Company', u'Jet Airways', u'India Cements', u'Cipla', u'Century Textiles', u' ', u'\n']
        if t and not [ item for item in rem if item in t ]: g_list.append(t[0])
    city_code = ["Chn","Mum","Del","Kol"]
    for i in range(4,16,3): msg += '%s|%.2f|%.2f'%(city_code[((i-1)/3)-1],float(g_list[i].replace('Rs. ',''))/10,float(g_list[i+1].replace('Rs. ',''))/10) + '\n'
    return msg.strip()

