#!/usr/bin/env python
# coding: utf-8

import re
import utills

NEED_TO_CHECK = True
FRAME = {'user_name' : ''}

GREETING = ["tere", "hallo", "hola", "tere paevast", "tsau"]
GREETING_PATTERN = utills.to_pattern(GREETING)
EVENT = ["plaanid", "plaan", "plan", "tegevus", "tegevused", "teen"]
EVENT_PATTERN = utills.to_pattern(EVENT)
INTRODUCTION = ["mina", "olen", "nimi"]
INTRODUCTION_PATTERN = utills.to_pattern(INTRODUCTION)

def getResponse(orig_text):
    ASKED_FOR_NAME = False
    text = standartize(orig_text)
    response = "?"
    utills.check_login()

    possible_name = re.findall("[A-ZÕÜŠŽÄÖ][\S]+", orig_text)
    if re.match("!.+", text):
        utills.special_request(text)
    elif re.search(GREETING_PATTERN, text):
        response = "Kuidas Teie nimi on?"
        ASKED_FOR_NAME = True
    elif re.search(INTRODUCTION_PATTERN, text):
        if len(possible_name) > 1:
            FRAME['user_name'] = possible_name[1]
        elif possible_name[0].lower() not in user_introduction:
            FRAME['user_name'] = possible_name[0]
        response = "Tere {0}, meeldiv tutvuda.".format(FRAME['user_name'])
    elif re.search(EVENT_PATTERN, text):
        response = utills.event_request(text)
    elif ASKED_FOR_NAME:
        FRAME['user_name'] = possible_name[0]
        ASKED_FOR_NAME = False
        response = "Tere {0}, meeldiv tutvuda.".format(FRAME['user_name'])
    
    return response

def standartize(text):
    letters = {"ä": "a", "ü": "u", "õ": "o", "ö": "o"}
    for key, value in letters.items():
        text = text.replace(key, value)
    return text
