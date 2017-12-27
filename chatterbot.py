#!/usr/bin/env python
# coding: utf-8

# LTAT.01.003 Tehisintellekt (2017 sügis)
# Kodutöö nr 5. Dialoogsüsteem

# Fail, millest käivitatakse dialoogsüsteem konsooliaknas 
# Seda faili muuta pole mõtet ning seda koduse töö esitamisel EI SAADETA

import chat_ai

print("Arvuti: Tere, mina olen juturobot.")
while True:
    human = input("Kasutaja: ")
    # Programmi töö lõpetamine, kui kasutaja kirjutab "bye"
    if human == "bye":
        print("Arvuti: Dialoog on lõppenud.")
        break
    # Arvuti vastus lausele
    print("Arvuti:",chat_ai.getResponse(human))
    
