import sqlite3

def initialize_db(cursor):
    table_names = cursor.execute("SELECT name FROM SQLITE_MASTER where type='table'").fetchall()
    if (u'contact',) not in table_names:
        print "CREATE TABLE contact"
        cursor.execute("""CREATE TABLE contact
(
    person_name     TEXT NOT NULL,
    mobile_number   TEXT PRIMARY KEY,
    email           TEXT
)
""")

    if (u'subscription',) not in table_names:
        print "CREATE TABLE subscription"
        cursor.execute("""CREATE TABLE subscription
(
    subscriber_number TEXT UNIQUE,
    forex_service INTEGER NOT NULL DEFAULT 0,
    gold_service INTEGER NOT NULL DEFAULT 0,
    bk_service INTEGER NOT NULL DEFAULT 0,
    blog_service INTEGER NOT NULL DEFAULT 0,
    weather_service INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(subscriber_number) REFERENCES contacts (mobile_number)
)
""")

    if (u'timing',) not in table_names:
        print "CREATE TABLE timing"
        cursor.execute("""CREATE TABLE timing
(
    subscriber_number TEXT UNIQUE,
    forex_timing TEXT NOT NULL DEFAULT '',
    gold_timing TEXT NOT NULL DEFAULT '',
    bk_timing TEXT NOT NULL DEFAULT '',
    blog_timing TEXT NOT NULL DEFAULT '',
    weather_timing TEXT NOT NULL DEFAULT '',
    FOREIGN KEY(subscriber_number) REFERENCES contacts (mobile_number)
)
""")

class RajivContactStore:
    def __init__(self, db_name='RajivPySMS_contacts.db'):
        "Initialize RajivConactStore database conection"
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        initialize_db(self.cursor)

    def get_contact_list(self, time=None, service=None):
        "Returns list of tuples containing (person_name, mobile_number, email)"
        q_string_template = '"SELECT person_name, mobile_number, email'
        SERVICE, TIME = service, time
        if service is not None:
            q_string_template += ", %s_timing FROM contact, subscription, timing WHERE mobile_number=subscription.subscriber_number AND contact.mobile_number=timing.subscriber_number AND %s_service=1"
            if time is not None:
                q_string_template += """ AND %s_timing LIKE \\'%s\\'"%(SERVICE, SERVICE, SERVICE, TIME)"""
                TIME = "%" + str(time) + "%"
            else:
                q_string_template += """"%(SERVICE, SERVICE)"""
        else:
            q_string_template += ' FROM contact, subscription, timing WHERE mobile_number=subscription.subscriber_number AND contact.mobile_number=timing.subscriber_number"'
        q_string = eval('(' + q_string_template + ')')
        if time is not None and service is not None:
            return [contact[:3] for contact in self.cursor.execute(q_string).fetchall() if time in eval('('+contact[3]+')')]
        else:
            return [contact[:3] for contact in self.cursor.execute(q_string).fetchall()]

    def add_contact(self,
        name, number, email='',
        forex_service=False, forex_timing='',
        gold_service=False, gold_timing='',
        bk_service=False, bk_timing='',
        blog_service=False, blog_timing='',
        weather_service=False, weather_timing='',
        ):
        "Add new contact to database"
        forex_timing, gold_timing, bk_timing, blog_timing, weather_timing = (str(eval('(' + timing + ')')) for timing in (forex_timing, gold_timing, bk_timing, blog_timing, weather_timing))
        try:
            self.cursor.execute('INSERT INTO contact VALUES(?,?,?)', (name, number, email))
            self.cursor.execute('INSERT INTO subscription VALUES(?,?,?,?,?,?)', (number, forex_service, gold_service, bk_service, blog_service, weather_service))
            self.cursor.execute('INSERT INTO timing VALUES(?,?,?,?,?,?)', (number, forex_timing, gold_timing, bk_timing, blog_timing, weather_timing))
            self.connection.commit()
            print 'contact added'
            return True
        except:
            print 'error in contact adding'
            return False

    def delete_contact(self, number):
        "Delete a contact from database"
        self.cursor.execute('DELETE FROM contacts WHERE mobile_number=?',(number))
        self.cursor.execute('DELETE FROM subscription WHERE subscriber_number=?',(number))
        self.cursor.execute('DELETE FROM timing WHERE subscriber_number=?',(number))
        self.connection.commit()

x = RajivContactStore()
for l in x.get_contact_list(service='weather', time=13):
    print l

print help(RajivContactStore)
#~ print help(list)
#~ contacts = open('RajivPySms_contacts.csv')
#~ contacts.readline()

#~ for l in contacts.readlines():
    #~ name, number, ForexSms, GoldSms, BkSms, BlogSms, WeatherSms = ( x.strip() for x in l.split(','))
    #~ ForexSms, GoldSms, BkSms, BlogSms, WeatherSms = (eval('(' + x + ')') for x in (ForexSms, GoldSms, BkSms, BlogSms, WeatherSms))
    #~ print name, number, ForexSms, GoldSms, BkSms, BlogSms, WeatherSms
    #~ x.add_contact(
        #~ name, number,
        #~ forex_service=ForexSms,
        #~ gold_service=GoldSms,
        #~ bk_service=BkSms,
        #~ blog_service=BlogSms,
        #~ weather_service=WeatherSms,
        #~ #                   8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22
        #~ forex_timing   = '  8,      11,      14,      17,      20,      ',
        #~ weather_timing = '       10,      13,      16,      19,         ',
        #~ blog_timing    = '             12,      15,      18,            ',
        #~ gold_timing    = '          12,                                 ',
        #~ bk_timing      = '                13,                           ',
    #~ )
