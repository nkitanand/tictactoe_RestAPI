# This file contains all the game logic and functions 

import json
import random
import copy

'''
# This library works with the following master json

{
    "Game": "Tic Tac Toe",
    "Status": ["In Progress", "Game over"],
    "Winner": ["Human", "Bot", "None", null],
    "GameBoardState": {
        "Box 1": ["Human", "Bot", null],
        "Box 2": ["Human", "Bot", null],
        "Box 3": ["Human", "Bot", null],
        "Box 4": ["Human", "Bot", null],
        "Box 5": ["Human", "Bot", null],
        "Box 6": ["Human", "Bot", null],
        "Box 7": ["Human", "Bot", null],
        "Box 8": ["Human", "Bot", null],
        "Box 9": ["Human", "Bot", null]
    }
}
'''

# initialJSON() - creates initial JSON and return it
def initialJSON():
    data = {
        "Game": "Tic Tac Toe",
        "Status": "In Progress",
        "Winner": None,
        "GameBoardState": {
            "Box 1": None,
            "Box 2": None,
            "Box 3": None,
            "Box 4": None,
            "Box 5": None,
            "Box 6": None,
            "Box 7": None,
            "Box 8": None,
            "Box 9": None
        }
    }
    
    # convert into JSON
    jsonData = json.dumps(data)

    return jsonData

def updateGameState(currentState):

    tempData = currentState
    board = jsonToBoard(tempData)
    
    human = 1
    bot   = 0
    # Check if Human Player's move ended in win
    if (isGameOver(human, board, 3, 3)):
        winner = "Human"
        jsonGameOver = createJsonGameOver(tempData, winner)
        return jsonGameOver
    
    # make bot play next move if game not over
    choices = choicesLeftToPlay(board)
    if (len(choices) == 0):
        winner = "None"
        jsonGameOver = createJsonGameOver(tempData, winner)
        return jsonGameOver
    #print(choices)
    #botMoveChoice = random.choice(choices) # replace with smart Bot
    botMoveChoice = playBot(bot, choices, board, 3, 3)
    #print(botMoveChoice)
    updatedJsonBotData = updateJsonForBotMove(tempData, botMoveChoice)
    #print(updatedJsonBotData)

    # update board
    board = jsonToBoard(updatedJsonBotData)
    # Check if Bot's move ended in win
    if (isGameOver(bot, board, 3, 3)):
        winner = "Bot"
        jsonGameOver = createJsonGameOver(updatedJsonBotData, winner)
        return jsonGameOver
    
    return updatedJsonBotData

# Convert input to location
def gameInput(key):
    if (key == 1):
        return [0,0]
    if (key == 2):
        return [0,1]
    if (key == 3):
        return [0,2]
    if (key == 4):
        return [1,0]
    if (key == 5):
        return [1,1]
    if (key == 6):
        return [1,2]
    if (key == 7):
        return [2,0]
    if (key == 8):
        return [2,1]
    if (key == 9):
        return [2,2]


# get all location of players input - 0/1
# 1 = Human player
# 0 = Computer bot
def getLocation(player, board, w, h):
    locs = []

    for i_h in range(h):
        for i_w in range(w):
            if board[i_h][i_w] == player:
                locs += [[i_h, i_w]]

    return locs


def getLocs(locs, index):
    locList = []

    for x in range(len(locs)):
        locList.append(locs[x][index])

    return locList


# Checks the conditions of game over
# function returns 1 if the player has win else return 0
def isGameOver(player, board, w, h):
    # get all current locations of player
    locs = getLocation(player, board, w, h)

    if (len(locs) <= 2):    # only a combination of three locations can end the game
        return 0

    else:
        x_locs = getLocs(locs, 0)   # get all row co-ordinates
        y_locs = getLocs(locs, 1)   # get all column co-ordinates

        x_locs.sort()
        y_locs.sort()

        # check if player has any combination in same row/column
        for x in range(3):
            x_count = x_locs.count(x)
            if (x_count >= 3):
                return 1

            y_count = y_locs.count(x)
            if y_count >= 3:
                return 1

        # check for diagonal combination (left-top to right-bottom)
        if [0,0] in locs and [1,1] in locs and [2,2] in locs:
            return 1

        # check for diagonal combination (left-bottom to right-top)
        if [0,2] in locs and [1,1] in locs and [2,0] in locs:
            return 1

        return 0

# Recurse to check for the optimal move
def check(player, choices, board, w, h):
    if isGameOver(0, board, w, h):
        return 10
    elif isGameOver(1, board, w, h):
        return -10
    elif len(choices) == 0:
        return 0

    (WIN, LOSE, DRAW) = (-1, -1, -1)
    if (player == 0):   # For BOT
        (WIN, LOSE, DRAW) = (10, -10, 0)
    if (player == 1):   # For HUMAN
        (WIN, LOSE, DRAW) = (-10, 10, 0)

    # Check if opponent's next move finish the game
    nextPlayer = -1
    bufferChoices = list(choices)
    bufferBoard = copy.deepcopy(board)
    for step in choices:
        loc = gameInput(step)
        if (player == 1):
            nextPlayer = 0
        elif (player == 0):
            nextPlayer = 1
        bufferBoard[loc[0]][loc[1]] = nextPlayer
        if isGameOver(player, bufferBoard, w, h):
            return WIN
        elif isGameOver(nextPlayer, bufferBoard, w, h):
            return LOSE
        bufferBoard[loc[0]][loc[1]] = '-'
    
    nextPlayer = -1
    loseFlag = False
    bufferChoices = list(choices)
    bufferBoard = copy.deepcopy(board)
    resultList = []
    for step in choices:
        loc = gameInput(step)
        stepIndex = bufferChoices.index(step)
        bufferChoices.remove(step)
        if (player == 1):
            nextPlayer = 0
        elif (player == 0):
            nextPlayer = 1
        bufferBoard[loc[0]][loc[1]] = nextPlayer
        result = check(nextPlayer, bufferChoices, bufferBoard, w, h)
        resultList.append([step, result])
        bufferChoices.insert(stepIndex, step)
        bufferBoard[loc[0]][loc[1]] = '-'

    '''print str(player) + str(resultList)'''
    # look for win
    (winStep, drawStep, loseStep) = ('', '', '')
    for x in resultList:
        if x[1] == WIN:
            winStep = x[0]
        elif x[1] == DRAW:
            drawStep = x[0]
        elif x[1] == LOSE:
            loseStep = x[0]

    if (winStep != ''):
        return WIN
    elif (drawStep != ''):
        return DRAW
    elif (loseStep != ''):
        return LOSE
    return LOSE

def playBot(player, choices, board, w, h):
    
    (WIN, LOSE, DRAW) = (-1, -1, -1)
    if (player == 0):   # For BOT
        (WIN, LOSE, DRAW) = (10, -10, 0)
    if (player == 1):   # For HUMAN
        (WIN, LOSE, DRAW) = (-10, 10, 0)
        
    winStep  = -1;
    loseStep = -1;
    drawStep = -1;
    bufferChoices = list(choices)
    bufferBoard = copy.deepcopy(board)
    for step in choices:
        loc = gameInput(step)
        stepIndex = bufferChoices.index(step)
        bufferChoices.remove(step)
        bufferBoard[loc[0]][loc[1]] = player
        result = check(player, bufferChoices, bufferBoard, w, h)
        bufferChoices.insert(stepIndex, step)
        bufferBoard[loc[0]][loc[1]] = '-'
        if (result == WIN):
            winStep = step
            return winStep
        elif (result == DRAW):
            drawStep = step
        elif (result == LOSE):
            loseStep = step

    if (drawStep != -1):
        return drawStep
    
    return loseStep


def jsonToBoard(jsonData):
    # Wrong approach since I assumed jsonData to be JSON
    # where as it automatically changed to dict by python
    # pyObj = json.loads(str(jsonData))

    # pyObj = json.loads(json.dumps(jsonData))
    # it works but it is redundant
    tempJsonData = json.dumps(jsonData)
    pyObj = json.loads(str(tempJsonData))
    strHuman = "Human"
    strBot  = "Bot"
    board = [['-','-','-'],['-','-','-'],['-','-','-']]
    
    for i in range(9):
        boxIndex = i+1
        boxKey = "Box " + str(boxIndex)
        loc = gameInput(boxIndex)
        gameBoardState = pyObj["GameBoardState"]
        value = gameBoardState[boxKey]

        if (value == strHuman):
            board[loc[0]][loc[1]] = 1
        elif (value == strBot):
            board[loc[0]][loc[1]] = 0
        
    return board


def createJsonGameOver(jsonData, winner):
    pyObj = json.loads(json.dumps(jsonData))
    pyObj["Winner"] = winner
    pyObj["Status"] = "Game Over"
    newJson = json.dumps(pyObj)
    return newJson

def updateJsonForBotMove(jsonData, botChoice):
    pyObj = json.loads(json.dumps(jsonData))
    gameBoardState = pyObj["GameBoardState"]
    boxKey = "Box " + str(botChoice)
    gameBoardState[boxKey] = "Bot"
    newJson = json.loads(json.dumps(pyObj))
    return newJson

# This function takes board as an argument
# It scans and board and returns a list of
# available moves that bot can play
def choicesLeftToPlay(board):
    choices = []
    human = 1
    bot   = 0
    for i in range(9):
        boxIndex = i+1
        loc = gameInput(boxIndex)
        playedByHumanOrBot = board[loc[0]][loc[1]]
        if (playedByHumanOrBot != human and playedByHumanOrBot != bot):
            choices.append(boxIndex)

    return choices