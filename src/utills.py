import re
import os
import my_calendar
import datetime
import dateutil.parser
import runpy

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
## TODO add a solution to have dynamical datetime objects for every next day of week. Ex:
## "esmaspaev": datetime.datetime.now() +/- smth 
## or any other way
DAYS_DATETIME_RELATIONS = {
    "tana": datetime.datetime.now(),
    "homme": datetime.datetime.now() + datetime.timedelta(days=1),
    "ulehomme": datetime.datetime.now() + datetime.timedelta(days=2)
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
        pass
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
        trigger = 'puhapaev'
    elif re.search(to_pattern(['paev']), day):
        trigger = 'paev'
    else:
        trigger = day
    for k, v in DAYS_SPELL_RELATIONS[trigger]:
        day = list(day)
        day[v] = k
        res = ''.join(day)
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
