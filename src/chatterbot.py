#!/usr/bin/env python
# coding: utf-8

import chat_ai

print("Arvuti: Tere, mina olen juturobot-sekretär.")
while True:
    human = input("Kasutaja: ")
    # Programmi töö lõpetamine, kui kasutaja kirjutab "bye"
    if human == "bye":
        print("Arvuti: Dialoog on lõppenud.")
        break
    # Arvuti vastus lausele
    print("Arvuti:",chat_ai.getResponse(human))
    
