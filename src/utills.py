import re
import os
import my_calendar
import datetime
import dateutil.parser
import runpy
import arrow
import urllib.request
import json
import shutil

def to_pattern(strings): # Regular expression from list of strings
    s = ''
    for string in strings:
        string = list(string)
        s += '[' + string[0].upper() + string[0] + ']' + ''.join(string[1:]) + "|"
    return s[:-1]

FRAME = {"events": []}

DAYS = ["tana", "homme", "ulehomme", 
    "esmaspaev", "teisipaev", "kolmapaev", "neljapaev", "reede", "laupaev", "laupaeval", "puhapaev"]
DAYS_PATTERN = to_pattern(DAYS)

DAYS_DATETIME_RELATIONS = {
    "tana": datetime.datetime.now(),
    "homme": datetime.datetime.now() + datetime.timedelta(days=1),
    "ulehomme": datetime.datetime.now() + datetime.timedelta(days=2),
    "esmaspaev": arrow.utcnow().shift(weekday=0).naive,
    "teisipaev": arrow.utcnow().shift(weekday=1).naive,
    "kolmapaev": arrow.utcnow().shift(weekday=2).naive,
    "neljapaev": arrow.utcnow().shift(weekday=3).naive,
    "reede": arrow.utcnow().shift(weekday=4).naive,
    "laupaev": arrow.utcnow().shift(weekday=5).naive,
    "puhapaev": arrow.utcnow().shift(weekday=6).naive
}

DAYS_SPELL_RELATIONS = {
    "tana": [("ä", 1)],
    "homme": [('h', 0)],
    "ulehomme": [("ü", 0)],
    "paev": [("ä", -3)],
    "puhapaev": [("ü", 1), ("ä", 5)]
}

def special_request(text):
    response = ''
    if re.search(to_pattern(['logout']), text):
        if logout():
            response = "Olete edukalt välja logitud."
        else:
            response = "Välja logimine ebaõnnestus."
    elif re.search(to_pattern(['kabe', 'kabet', 'checkers']), text):
        runpy.run_path("./checkers.py")
        response = "Loodan, et sulle meeldis minuga mängida!"
    
    return response

def event_request(text):
    events = FRAME["events"]
    result = []
    day_of_interest = ''
    for day, obj in DAYS_DATETIME_RELATIONS.items():
        if re.search(to_pattern([day]), text):
            if day == 'homme' and re.search(to_pattern(['ulehomme']), text):
                continue
            day_of_interest = day
            for event in events:
                event_datetime = dateutil.parser.parse(event['start']['dateTime'])
                if event_datetime.day == obj.day and event_datetime.month == obj.month and event_datetime.year == obj.year:
                    result.append(event)
    return generate_response(result, day_of_interest)

def generate_response(events, day):
    response = ''
    if not events:
        return "Kalendris pole ühtegi plaani, yay :)"
    for event in events:
        event_datetime_start = dateutil.parser.parse(event['start']['dateTime'])
        event_datetime_end = dateutil.parser.parse(event['end']['dateTime'])
        event_summary = event["summary"]
        response += "Kell {0} toimub \"{1}\", mis kestab kuni {2}".format(
            str(event_datetime_start.hour)+":"+str(event_datetime_start.minute),
            event_summary,
            str(event_datetime_end.hour)+":"+str(event_datetime_end.minute),
        )
        try:
            response += ", aadressil {0}.\n".format(event["location"])
        except KeyError:
            response += ".\n"
    response = "{0} plaanis on järgmised üritused:\n".format(spell_day(day).capitalize()) + response
    return response[:-1]

def spell_day(day):
    trigger = ''
    res = ''
    if day == 'puhapaev':
        trigger = day
    elif re.search(to_pattern(['paev']), day):
        trigger = 'paev'
    else:
        trigger = day
    for k, v in DAYS_SPELL_RELATIONS[trigger]:
        day = list(day)
        day[v] = k
        res = ''.join(day)
    if 'paev' in trigger:
        res += "al"
        # data = getDictFromJson(u'http://prog.keeleressursid.ee/ws_etmrf/syntees.php?c=ad&s=' + res).encode('utf-8')
        # File "C:\Users\Andri\AppData\Local\Programs\Python\Python36-32\lib\http\client.py", line 1117, in putrequest
        # self._output(request.encode('ascii'))
        # UnicodeEncodeError: 'ascii' codec can't encode character '\xe4' in position 39: ordinal not in range(128)
    return res

def check_login():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        print("Arvuti: Kahjuks Te ei ole sisse loginud, kas soovite seda teha praegu? [Y/n]")
        answ = input("Kasutaja: ")
        if re.match(to_pattern(['y']), answ):
            service = my_calendar.open_connection()
            print('Arvuti: Olete edukalt sisse logitud.')
            if FRAME["events"] == []:
                FRAME["events"] = my_calendar.get_next(service, 10)
            return False
        else:
            print('Arvuti: Sisse logimiseks kirjutagi "!login".')
            return True
    elif FRAME["events"] == []:
        FRAME["events"] = my_calendar.get_next(my_calendar.open_connection(), 100)

def logout():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if os.path.exists(credential_dir):
        try:
            shutil.rmtree(credential_dir)
            return True
        except:
            return False

    
def getDictFromJson(url):
    file = urllib.request.urlopen(url)
    data = json.loads(file.read().decode())
    return data