#!/usr/bin/env python
# coding: utf-8

# Fail, mida võib muuta ja mis tuleb esitada koduse töö lahendusena
# Faili nime peab jätma samaks
# Faili võib muuta suvaliselt, kuid see peab sisaldama funktsiooni getResponse(),
# millele antakse argumendina ette kasutajalt sisendiks saadud tekst (sõnena)
# ja mis tagastab sobiva vastuse (samuti sõnena)
import urllib.request
import json

def getResponse(text):
    response = "?"
    # Siia tuleb vastuste genereerimise loogika, kasutada võib ka siia faili loodud funktsioone
    # Momendi ilmateade
    weather = getDictFromJson('http://api.openweathermap.org/data/2.5/weather?q=tartu&units=metric&APPID=' + APPID)
    # Ilmaennustus
    #weather = getDictFromJson('http://api.openweathermap.org/data/2.5/forecast?q=tartu&units=metric&APPID=' + APPID)
    return response

def getDictFromJson(url):
    # Testimiseks näidisfail Tartu ilmateatega, kodutööna esitatavas versioonis neid ei kasutata
    file = open("weatherSample.txt", 'r')
    #file = open("forecastSample.txt", 'r')
    data = json.loads(file.read())
    # Veebist ilmainfo lugemine, kodutööna esitatavas versioonis peab olema just järgmised kaks rida kasutuses!!!
    #file = urllib.request.urlopen(url)
    #data = json.loads(file.read().decode())
    return data

def getCountryByIso(iso):
    country = "teave puudub"
    # Päring: http://prog.keeleressursid.ee/ws_riigid/index.php?iso=<ISO kood>
    # ISO kahetähelised koodid: https://en.wikipedia.org/wiki/ISO_3166-1
    # Vastus: riigi nimi (eesti keeles)
    country = file.read().decode()
    return country

# Registreerige ennast http://openweathermap.org/ kasutajaks (ei pea kasutama oma kõige olulisemat e-posti aadressi)
# API Key leiate https://home.openweathermap.org/api_keys, kopeerige see sõnena APPID muutuja väärtuseks
APPID = '<API Key tuleb siia>'
