import sqlFunctions
import blackjackText2

def truncateAllTables():
    
    sqlFunctions.truncateTable("Recommendations")
    sqlFunctions.truncateTable("WinProbabilities")
    sqlFunctions.truncateTable("HandOutcomes")

def updateTables(num):
    print(num)
    blackjackText2.fillHandOutcomes(num)
    sqlFunctions.fillHandProbs()
    sqlFunctions.fillRecos()

def getRecommendation(hand):
    return sqlFunctions.getRecommendation(hand)

def getWinProbs(hand):
    return sqlFunctions.getFullWinProbs(hand)

def customReco(hand, recommend):
    sqlFunctions.insertReco(hand, recommend)

def countTotal():
    return sqlFunctions.countTotalHands()

def createDatabase():
    sqlFunctions.createDatabase()

def createTables(num):
    if num == 1:
        sqlFunctions.createHandOutcomes()
    elif num == 2:
        sqlFunctions.createRecos()
    elif num == 3:
        sqlFunctions.createWinProbabilities()

def totalSims():
    return sqlFunctions.totalSimmedGames()
