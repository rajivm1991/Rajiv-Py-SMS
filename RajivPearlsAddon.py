from datetime import datetime
from RajivPySms import BOT_BROWSER, CREDENTIALS
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import bitly

browser = Browser()
browser.addheaders = [('User-agent', BOT_BROWSER['chrome'] )]
date = datetime.strftime(datetime.now(),"%B %d, %I:%M %p")

def get_forex_rate(From = 'USD', To = 'INR'):
    msg = "Dollar Rate: "+date+"; "
    data = browser.open("http://www.xe.com/ucc/convert.cgi?template=mobile&Amount=1&From="+From+"&To="+To).read()
    n = data.index('1 '+From+' =')
    m = data[n:].index(' '+To)
    msg += "" + data[n:n+m+4] + '; '
    n = data.index('1 '+To+' =')
    m = data[n:].index(' '+From)
    msg += "" + data[n:n+m+4]
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
                        msg += term.get('text','')+ '\n'
                        for cut in ['<em>', '</em>', '<i>', '</i>', '<b>', '</b>']: msg = msg.replace(cut,'')
                        get_eg = False
                    for eentry in entry.get('entries',[]):
                        for eterm in eentry.get('terms'):
                            if get_eg:
                                msg += '-'+eterm.get('text','')+'\n'
                                for cut in ['<em>', '</em>', '<i>', '</i>', '<b>', '</b>']: msg = msg.replace(cut,'')
                                get_eg = False
        empty = len(msg.strip()) == 0
        for entry in result.get('webDefinitions',[{}])[0].get('entries',[]):
            if empty:
                msg = entry.get('terms',[{}])[0].get('text').replace('&quot;','"').replace('&#39;',"'")
                empty = False
        return unicode(msg.strip(),errors='ignore')
    else: 
        return False

def gold_rate_india():
    data = browser.open("http://www.sify.com/finance/gold_rates/").read()
    soup = BeautifulSoup(data)
    gold = soup.find('div', attrs={"class":"rates-outer-wrapper"})
    g_list = []
    msg = 'Gold ('+datetime.strftime(datetime.now(),"%b %d")+') 22C 24C\n'
    for tag in gold.findAll('td', attrs={"align":"center"}):
        t = tag.findAll(text=True)
        rem = [u'Company', u'Jet Airways', u'India Cements', u'Cipla', u'Century Textiles', u' ', u'\n']
        if t and not [ item for item in rem if item in t ]: g_list.append(t[0])
    city_code = ["Chn","Mum","Del","Kol"]
    for i in range(4,16,3): msg += '%s\n%.2f, %.2f'%(city_code[((i-1)/3)-1],float(g_list[i].replace('Rs. ',''))/10,float(g_list[i+1].replace('Rs. ',''))/10) + '\n'
    return msg.strip()

def bk_thought_for_today():
    data = browser.open("http://www.bkwsu.org/us/newyork/thoughts").read()
    soup = BeautifulSoup(data)
    thought = soup.find('div', attrs={"id":"thoughtForToday"}).findAll(text=True)
    for rem in [u'\n',u'&nbsp;']: 
        while rem in thought: thought.remove(rem)
    return 'Om Shanti:\n'+''.join(thought)+"\n~ Brahmakumaris"

def random_blog():
    data = browser.open("http://gulzarmanzil.wordpress.com/?random").read()
    soup = BeautifulSoup(data)
    title = soup.find('title').findAll(text=True)[0].split('|')[0].strip()
    link = browser.geturl()
    rep_with = {
        "&lsquo;" : "'",
        "&rsquo;" : "'",
        "&#8217;" : "'",
        "&#8211;" : "-",
        "&#8230;" : "...",
        "&hellip;": "...",
    }
    for rem in rep_with.keys():
        while rem in title:
            title.replace(rem,rep_with[rem])
    if len(title+' '+link) > 130:
        try:
            # Fill your BITLY api credentials here
            bittifier = bitly.Api(login=CREDENTIALS['bitly']['login'], apikey=CREDENTIALS['bitly']['key'])
            link = str(bittifier.shorten(link))
        except:pass
    return title + ' ' + link

def get_weather(city = 'Bangalore,India'): # "rajapalayam,India"
    data = browser.open("http://free.worldweatheronline.com/feed/weather.ashx?q=" + city + "&format=json&num_of_days=5&key=" + CREDENTIALS['wwo']['key']).read()
    x = eval('('+data+')')
    cc = x['data']['current_condition'][0]
    wc = cc['weatherCode']
    for line in browser.open("http://www.worldweatheronline.com/feed/wwoConditionCodes.txt").read().split('\n'):
        if line[:3] == wc:
            wc = line.split('\t')[1]
            break
    weather = "Weather Today:\n"+x['data']['request'][0]['query']+' '+cc['observation_time']+'\n'
    weather += wc+'\n'
    weather += "Temp: "+cc['temp_C']+'C, '+cc['temp_F']+'F\n'
    weather += "Wind: "+cc['windspeedKmph']+'Kmph > '+cc['winddir16Point']+'\n'
    weather += "Humidity: "+cc['humidity']+"\n"
    weather += 'Visibility: '+cc['visibility']+'km'
    return weather
