#!/usr/bin/env python
# coding: utf-8
import random
from copy import deepcopy


def getTurn(tokens, player):
    allTurns = getAllTurns(tokens, player)
    response = getMiniMax(tokens, allTurns, player)
    return response
 
def getAllTurns(tokens, player):
    turns = []
    for button in tokens[player]:
        move = getPossMoves(tokens, button[0], button[1], player)
        if len(move) != 0:
            for i in move:
                turns.append(i)
    return turns

def minimax(player, board, allturns, depth, move):
    depth -= 1
    if len(allturns) > depth and depth >= 0:
        if player != move:
            bestturn, bestrate = minimizer(player, board, allturns, depth, move)
        elif player == move:
            bestturn, bestrate = maximizer(player, board, allturns, depth, move)
    return bestturn, bestrate

def getMiniMax(tokens, allturns, player):
    depth = 3
    if len(allturns) < depth:
        depth = len(allturns)
    if player == 1:
        opponent = 0
    else:
        opponent = 1
    turn, rate = minimax(player, tokens, allturns, depth, opponent)
    return turn

def getPossMoves(tokens, row, col, player):
    possMoves = []
    direct = 1
    opponent = 1
    
    if player == 1:
        direct = -1
        opponent = 0
    rightCol = col + 1
    leftCol = col - 1    
    newRow = row + direct
    
    if newRow in range(8):
        if [newRow, leftCol] not in tokens[player] and leftCol >= 0:
            if [newRow, leftCol] not in tokens[opponent]:
                possMoves.append([row, col, newRow, leftCol])
            elif [newRow + direct, leftCol - 1] not in tokens[player] + tokens[opponent] and leftCol - 1 >= 0 and (newRow + direct in range(8)):
                possMoves.append([row, col, newRow + direct, leftCol - 1])

        if [newRow, rightCol] not in tokens[player] and rightCol <= 7:
            if [newRow, rightCol] not in tokens[opponent]:
                possMoves.append([row, col, newRow, rightCol])
            elif [newRow + direct, rightCol + 1] not in tokens[player]+ tokens[opponent] and rightCol + 1 <= 7 and (newRow + direct in range(8)):
                possMoves.append([row, col, newRow + direct, rightCol + 1])

    return possMoves

def minimizer(player, board, allturns, depth, move):
    bestrate = 10
    bestturn= [-1,-1,-1,-1]
    for turn in allturns:
        cell = deepcopy(board)
        cell[1-move][cell[1-move].index(turn[:2])] = turn[2:]
        if turn[0] - turn[2] == 2:
            if turn[1] - turn[3] == 2:
                cell[move].remove([turn[0] - 1, turn[1] - 1])
            else:
                cell[move].remove([turn[0] - 1, turn[1] + 1])

        if depth > 0:
            _turn, rate = minimax(player, cell, getAllTurns(cell, move), depth, 1 - move)
        else:
            rate = 9 - len(board[1-move]) - len(board[move])
        if rate < bestrate:
            bestrate = rate
            bestturn = turn

    return bestturn, bestrate

def maximizer(player, board, allturns, depth, move):
    bestrate = 0
    bestturn= [-1,-1,-1,-1]
    for turn in allturns:
        cell = deepcopy(board)
        cell[1 - move][cell[1 - move].index(turn[:2])] = turn[2:]
        if turn[0] - turn[2] == 2:
            if turn[1] - turn[3] == 2:
                cell[move].remove([turn[0] - 1, turn[1] - 1])
            else:
                cell[move].remove([turn[0] - 1, turn[1] + 1])

        if depth > 0:
            _turn, rate = minimax(player, cell, getAllTurns(cell, move), depth, 1 - move)
        else:
            rate = len(board[1-move]) - len(board[move])
        if rate > bestrate:
            bestrate = rate
            bestturn = turn

    return bestturn, bestrate