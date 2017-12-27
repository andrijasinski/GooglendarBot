#!/usr/bin/env python
# coding: utf-8

# MTAT.06.008 Tehisintellekt I (2017 sügis)
# Koduülesanne 3. Kabe

# Graafiline kasutajaliides
# Fail, mida koduse töö esitamisel EI SAADETA

from tkinter import *

import checkers_ai

# Muutujate algväärtustamine ========================================================================================
# Nuppude asukohad kujul 
# [[Mustade nuppude asukohad listidena [rida, veerg]][Valgete nuppude asukohad listidena [rida, veerg]]]
tokens = []
for i in [0,6]:
    tokenscol = []
    for j in range(2):
        for k in range(4):
            tokenscol.append([i+j, 2*k-j+1])
    tokens.append(tokenscol)

boardWidth = 8 # Laua suurus
players = ["Must", "Valge"] # Mängijad
buttons = {} # Nupud 
chosen = [0, 0] # Valitud nupu aadressi säilitamine
tkTokenDown = True # Kas järgmine nupuvajutus on nupu valik käimiseks?
player = 0 # Käiku tegev mängija (alustab 0 ehk must)

# Tehisintellekti vastu mängimine (True või False)
playAI = True
# Kas AI mängib mustade (0) või valgete (1) nuppudega (alati alustavad mustad)
AIPlayer = 1

# Funktsioonid ======================================================================================================

# Laua algseisu loomine
def createBoard():
    for i in range(boardWidth):
        for j in range(boardWidth):
            button = Button(root, text = "", font="Helvetica 13", height=3, width=6, background=tkColorButton)
            button.grid(row=j+1, column=i, padx=0, pady=0)
            # Ruudud, mille rea- ja veeruindeksi summa on paaritu, on valged, mitteaktiivsed, neisse "ei käida"
            if (j + i) % 2 == 1:
                button.configure(command = lambda i=i, j=j: pressButton(j, i))
            else:
                button.configure(background = tkColor1, state="disabled")
            buttons[str(j)+str(i)] = button
    tokensOnBoard()

# Nuppude asetamine mängulauale
def tokensOnBoard():
    for i in range(2):
        for j in range(len(tokens[i])):
            buttons[str(tokens[i][j][0])+str(tokens[i][j][1])].configure(text=players[i])

# Mängulaua tühjendamine       
def drawBoard():
    for button in buttons:
        buttons[button].configure(text="")
    tokensOnBoard()

# Nupuvajutusele (ruudu valimisele) reageerimine
def pressButton(row, col):
    global tkTokenDown, chosen, player, tokens
    # Esimese vajutusega valitakse ruut, millel on mängija nupp, ja muudetakse selle värvi
    if tkTokenDown:
        if [row, col] in tokens[player]:
            buttons[str(row)+str(col)].configure(state="disabled", background=tkColor2)
            chosen = [row, col]
            tkTokenDown = False
    # Teise vajutusega pannakse see õigesse kohta
    else:
        possMoves = getPossMoves(chosen[0], chosen[1], player)
        # Kui tehtud käik on üks võimalikest käikudest, siis teeme selle
        if [row, col] in possMoves:
            tokens[player].remove([chosen[0], chosen[1]])
            tokens[player].append([row, col])
            buttons[str(chosen[0])+str(chosen[1])].configure(state="normal", background=tkColorButton)
            drawBoard()
            # Vajadusel eemaldame ka vastase mängunupu
            if abs(chosen[0]-row) == 2:
                opponent = 1
                if player == 1:
                    opponent = 0
                tokens[opponent].remove([min(chosen[0], row)+1, min(chosen[1], col)+1])
            # Kontrollime, kas mäng on lõppenud ehk kas järgmisel mängijal pole enam käiguvõimalusi
            tkTokenDown = True
            if player == 0:
                player = 1
            else:
                player = 0
            end = False
            # Kui mäng pole veel lõppenud, siis teavitame, kes järgmisena käib
            if not isEnd(player):
                tkMessage.configure(text = "Järgmise käigu teeb " + players[player].lower() + ".")
                # Kui tehisintellekti abil mängimine on sisse lülitatud
                if playAI and player == AIPlayer:
                    drawBoard()
                    getAIMove()
            # Kui järgmisel mängijal enam käiguvõimalusi pole, teatame, kes võitis või jäi mäng viiki
            else:
                winner = getWinner()
                if winner < 0:
                    tkMessage.configure(text = "Mäng on lõppenud viigiga.")
                else:
                    tkMessage.configure(text = "Mäng on lõppenud, võitis " + players[winner] + ".")
        # Kui tehtud käik polnud üks võimalikest, tühistame valiku ja lubame samal mängijal uuesti käia
        else:
            tkTokenDown = True
        buttons[str(chosen[0])+str(chosen[1])].configure(state="normal", background=tkColorButton)
        drawBoard()

# Kasutab käiguks tehisintellekti mooduli checkers_ai meetodit getTurn(tokens, player),
# kus tokens on nuppude asukohad momendi mänguseisus kujul
# [[Mustade nuppude asukohad listidena [rida, veerg]][Valgete nuppude asukohad listidena [rida, veerg]]]
# ja muutuja player tähistab mängijat (0 - must, 1 - valge)
def getAIMove():
    move = checkers_ai.getTurn(tokens, player)
    # Nupu algne asukoht
    pressButton(move[0], move[1])
    # Nupu lõppasukoht
    pressButton(move[2], move[3])
    drawBoard()
    
# Tagastab mängija nupu võimalike käikude listi vastavalt etteantud mänguruudule
# kujul [[<käiguvariant1 reaaadress>, <käiguvariant1 veeruaadress>], [<käiguvariant2 reaaadress>, <käiguvariant2 veeruaadress>]...]
# Kui võimalikud käigud puuduvad, tagastab tühja listi
def getPossMoves(row, col, player):
    possMoves = []
    # Mustad liiguvad ainult allapoole (reaindeks saab ainult suureneda), valged vastupidi
    direction = 1
    opponent = 1
    if player == 1:
        direction = -1
        opponent = 0
    # Naaberruut
    if str(row+1*direction)+str(col+1) in buttons.keys() and [row+1*direction, col+1] not in tokens[0] and [row+1*direction, col+1] not in tokens[1]:
        possMoves.append([row+1*direction, col+1])
    if str(row+1*direction)+str(col-1) in buttons.keys() and [row+1*direction, col-1] not in tokens[0] and [row+1*direction, col-1] not in tokens[1]:
        possMoves.append([row+1*direction, col-1])
    # Vastase nupu võtmine ja seega kahe ruudu võrra liikumine
    if str(row+2*direction)+str(col+2) in buttons.keys() and [row+2*direction, col+2] not in tokens[0] and [row+2*direction, col+2] not in tokens[1] and [row+1*direction, col+1] in tokens[opponent] and [row+1*direction, col+1] not in tokens[player]:
        possMoves.append([row+2*direction, col+2])
    if str(row+2*direction)+str(col-2) in buttons.keys() and [row+2*direction, col-2] not in tokens[0] and [row+2*direction, col-2] not in tokens[1] and [row+1*direction, col-1] in tokens[opponent] and [row+1*direction, col-1] not in tokens[player]:
        possMoves.append([row+2*direction, col-2])
    return possMoves

# Kontroll, kas mäng on lõppenud ehk kas järgmisel mängijal on võimalik kuhugi käia
def isEnd(player):
    answer = False
    possMoves = []
    for token in tokens[player]:
        possMoves1 = getPossMoves(token[0], token[1], player)
        for pM in possMoves1:
            possMoves.append(pM)
    if len(possMoves) < 1:
        answer = True
    return answer

# Võitja tagastamine: -1 - viik, 0 - must, 1 - valge
# Võidab see, kellel jääb mängulauale rohkem nuppe, võrdse nuppude arvu puhul on viik
def getWinner():
    result = -1
    if len(tokens[0]) != len(tokens[1]):
        result = [len(tokens[0]), len(tokens[1])].index(max([len(tokens[0]), len(tokens[1])]))
    return result

# Disain ============================================================================================================
tkColorBg = 'LightSkyBlue1'
tkColorTitle = 'SlateBlue4'
tkColor1 = 'White'
tkColor2 = 'PaleGreen1'
tkColorButton = 'gray75'

# Mängu käivitamine =================================================================================================

# Akna loomine
root = Tk() 
root.wm_title("Kabe")
root.resizable(0,0)
root.configure(background=tkColorBg)
title = Label(root, text="Kabe", fg=tkColorTitle, font="Helvetica 18 bold", background=tkColorBg).grid(row=0, column=0, padx=10, pady=8, columnspan=8)

# Laua loomine
createBoard()

# Info kuvamine
tkMessage = Label(root, text="Alustab mustade nuppudega mängija.", font="Helvetica 13 bold", fg=tkColorTitle, background=tkColorBg)
tkMessage.grid(row=9, column=0, padx=10, pady=8, columnspan=8)

# Kui valitud on tehisintellektiga mängimine ja tehisintellektile on määratud mustad nupud, siis lase esimene käik teha tehisintellektil
if playAI and player == AIPlayer:
    getAIMove()

# Tsükkel, mis hoiab akna avatuna
root.mainloop()
