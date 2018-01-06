#!/usr/bin/env python
# coding: utf-8
import random
from copy import deepcopy


def getTurn(tokens, player):
    allTurns = getAllTurns(tokens, player)
    response = getTurnMinimax(tokens, allTurns, player)
    return response


# Make a list of all turns 
def getAllTurns(tokens, player):
    allturns = []
    for nupp in tokens[player]:
        move = getPossMoves(tokens, nupp[0], nupp[1], player)
        if len(move) != 0:
            for i in move:
                allturns.append(i)
    return allturns

# Make a list of player possible moves
def getPossMoves(tokens, row, col, player):
    possMoves = []
    direction = 1
    opponent = 1
    if player == 1:
        direction = -1
        opponent = 0

# Possible moves
    newRow = row + direction
    rightCol = col + 1
    leftCol = col - 1

    if newRow in range(8):
        if [newRow, leftCol] not in tokens[player] and leftCol >= 0:
            if [newRow, leftCol] not in tokens[opponent]:
                possMoves.append([row, col, newRow, leftCol])
            # Checking if it is possible to eat
            elif [newRow + direction, leftCol - 1] not in tokens[player] and [newRow + direction, leftCol - 1] not in \
                    tokens[opponent] and leftCol - 1 >= 0 and (newRow + direction in range(8)):
                possMoves.append([row, col, newRow + direction, leftCol - 1])

        if [newRow, rightCol] not in tokens[player] and rightCol <= 7:
            if [newRow, rightCol] not in tokens[opponent]:
                possMoves.append([row, col, newRow, rightCol])
            # Checking if it is possible to eat
            elif [newRow + direction, rightCol + 1] not in tokens[player] and [newRow + direction, rightCol + 1] not in \
                    tokens[opponent] and rightCol + 1 <= 7 and (newRow + direction in range(8)):
                possMoves.append([row, col, newRow + direction, rightCol + 1])

    return possMoves

# Using minimax algorithm
def getTurnMinimax(tokens, allturns, player):
    depth = 3
    if len(allturns) < depth:
        depth = len(allturns)
    if player == 1: opponent = 0
    else: opponent = 1
    turn, rate = minimax(player, tokens, allturns, depth, opponent)
    return turn


def minimax(player, board, allturns, depth, move):
    # player - player atm, who is using the algorithm
    # move - player, who will make a move
    depth -= 1
    bestturn = [-1,-1,-1,-1]
    bestrate = 0
    if depth >= 0 and len(allturns) > depth:
        if player == move:
            # If player is the same guy as move-player, when use maximization
            bestturn, bestrate = maximizer(player, board, allturns, depth, move)
        else:
            bestturn, bestrate = minimizer(player, board, allturns, depth, move)
    return bestturn, bestrate


# Max
def maximizer(player, board, allturns, depth, move):
    bestturn = [-1,-1,-1,-1]
    bestrate = 0
    # If max depth is not reached yet
    for turn in allturns:
        b = deepcopy(board)
        # Changing the old moves with a new ones
        b[1 - move][b[1 - move].index(turn[:2])] = turn[2:]
        # Checking if it was eaten
        if turn[0] - turn[2] == 2:
            if turn[1] - turn[3] == 2:
                b[move].remove([turn[0]-1, turn[1]-1])
            else:
                b[move].remove([turn[0] - 1, turn[1] + 1])

        if depth > 0:
            _turn, rate = minimax(player, b, getAllTurns(b, move), depth, 1 - move)
        else:
            rate = len(board[1-move]) - len(board[move])
        if rate > bestrate:
            bestrate = rate
            bestturn = turn

    return bestturn, bestrate


# Min
def minimizer(player, board, allturns, depth, move):
    bestturn = [-1,-1,-1,-1]
    bestrate = 10

    # If max depth is not reached yet
    for turn in allturns:
            b = deepcopy(board)
            
            # Changing the old moves with a new ones
            b[1-move][b[1-move].index(turn[:2])] = turn[2:]
            # Checking if it was eaten
            if turn[0] - turn[2] == 2:
                if turn[1] - turn[3] == 2:
                    b[move].remove([turn[0] - 1, turn[1] - 1])
                else:
                    b[move].remove([turn[0] - 1, turn[1] + 1])

            if depth > 0:
                _turn, rate = minimax(player, b, getAllTurns(b, move), depth, 1 - move)
            else:
                rate = 9 - len(board[1-move]) - len(board[move])
            if rate < bestrate:
                bestrate = rate
                bestturn = turn

    return bestturn, bestrate
