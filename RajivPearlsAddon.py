from datetime import datetime
from RajivPySms import BOT_BROWSER
from mechanize import Browser

browser = Browser()
browser.addheaders = [('User-agent', BOT_BROWSER['safari'] )]
date = datetime.strftime(datetime.now(),"%B %d, %I:%M %p")

def get_forex_rate(From = 'USD', To = 'INR'):
    msg = "Rajiv-Pearl-Forex%0a"+date+"%0a----------%0a"
    data = browser.open("http://www.xe.com/ucc/convert.cgi?template=mobile&Amount=1&From="+From+"&To="+To).read()
    n = data.index('1 '+From+' =')
    m = data[n:].index(' '+To)
    msg += "" + data[n:n+m+4] + '%0a'
    n = data.index('1 '+To+' =')
    m = data[n:].index(' '+From)
    msg += data[n:n+m+4]
    msg += "%0a----------"
    
    print "+--+----+--Pearl Response---+----+----+"
    print msg.replace('%0a','\n')
    print "+--+----+----+----+----+----+----+----+"
    
    return msg

