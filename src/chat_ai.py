#!/usr/bin/env python
# coding: utf-8

import re
import utills

NEED_TO_CHECK = True

GREETING = ["tere", "hallo", "hola", "tere paevast", "tsau"]
GREETING_PATTERN = utills.to_pattern(GREETING)
EVENT = ["plaanid", "plaan", "plan", "tegevus", "tegevused", "teen"]
EVENT_PATTERN = utills.to_pattern(EVENT)

def getResponse(orig_text):
    text = standartize(orig_text)
    response = "?"
    utills.check_login()

    if re.match("!.+", text):
        utills.special_request(text)
    elif re.search(GREETING_PATTERN, text):
        pass
    elif re.search(EVENT_PATTERN, text):
        pass

    
    return response

def standartize(text):
    letters = {"ä": "a", "ü": "u", "õ": "o", "ö": "o"}
    for key, value in letters.items():
        text = text.replace(key, value)
    return text
