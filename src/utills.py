import re
import os
import my_calendar

def special_request(text):
    
    if re.search(to_pattern(['logout']), text):
        pass
    
    return

def to_pattern(strings): # Regular expression from list of strings
    s = ''
    for string in strings:
        string = list(string)
        s += '[' + string[0].upper() + string[0] + ']' + ''.join(string[1:]) + "|"
    return s[:-1]

def check_login():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        print("Arvuti: Kahjuks Te ei ole sisse loginud, kas soovite seda teha praegu? [Y/n]")
        answ = input("Kasutaja: ")
        if re.match(to_pattern(['y']), answ):
            my_calendar.getNextTen()
            print('Arvuti: Olete edukalt sisse logitud.')
            return False
        else:
            print('Arvuti: Sisse logimiseks kirjutagi "!login".')
            return True