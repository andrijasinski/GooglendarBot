#!/usr/bin/env python
# coding: utf-8

# LTAT.01.003 Tehisintellekt (2017 sügis)
# Kodutöö nr 5. Dialoogsüsteem

# Graafiline kasutajaliides
# Fail, millest käivitatakse dialoogsüsteem graafilises vaates 
# Seda faili muuta pole mõtet ning seda koduse töö esitamisel EI SAADETA

import chat_ai
from tkinter import *

def saadaDialoogi():
    global tkTurnNr
    human = user.get()
    dialogueList.insert(END, "Kasutaja: " + human)
    dialogueList.itemconfig(tkTurnNr*2-1, {'bg':tkColor2})
    if human == "bye":
        dialogueList.insert(END, "Arvuti: Dialoog on lõppenud.")
        dialogueList.itemconfig(tkTurnNr*2, {'bg':tkColor1})
        finish()
        return
    dialogueList.insert(END, "Arvuti: " + str(chat_ai.getResponse(human)))
    dialogueList.yview(END)
    dialogueList.itemconfig(tkTurnNr*2, {'bg':tkColor1})
    userInput.set("")
    user.focus()
    tkTurnNr += 1

def sendEnter(event):
    if endDial == False:
        saadaDialoogi()

def finish():
    global endDial
    endDial = True
    user.configure(state="disabled")
    button.configure(state="disabled")
    
# Disain
tkColor1 = 'light sky blue'
tkColor2 = 'White'
tkColor3 = 'midnight blue'
tkTurnNr = 1
tkDialogueWidth = 160
tkDialogueHeight = 30

endDial = False

# Akna loomine
root = Tk() 
root.wm_title("Dialoogsüsteem")
root.configure(background=tkColor2)

# Pealkiri
title = Label(root, text="Dialoogsüsteem", fg=tkColor3, font=("Helvetica", 20), background=tkColor2)

# Dialoogi listi loomine
dialogueList = Listbox(root, width=tkDialogueWidth, height=tkDialogueHeight)
dialogueList.insert(END, "Arvuti: Tere, mina olen juturobot.")
dialogueList.itemconfig(0, {'bg':tkColor1})

# Saatmisnupu loomine
button = Button(root, text ="Saada!", command = saadaDialoogi)

# Vastuselahtri loomine
userInput = StringVar()
user = Entry(root, textvariable = userInput, width=150)
user.focus()
# Saatmiseks piisab ka Enter-klahvi vajutusest
root.bind('<Return>', sendEnter)

title.pack(fill=X, padx=10, pady=10)
dialogueList.pack(fill=X, padx=10, pady=10)
user.pack(side=LEFT, fill=X, padx=10, pady=10)
button.pack(side=RIGHT, fill=X, padx=10, pady=10)

# Tsükkel, mis hoiab akna avatuna
root.mainloop()
