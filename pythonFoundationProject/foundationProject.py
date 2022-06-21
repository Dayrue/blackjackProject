import sqlFunctions
import blackjackText2


# sqlFunctions.createHandOutcomes()
# blackjackText2.fillHandOutcomes(10)

# sqlFunctions.truncateTable("HandOutcomes")
# sqlFunctions.truncateTable("Recommendations")
# sqlFunctions.truncateTable("WinProbabilities")


# sqlFunctions.showTable("HandOutcomes")
# sqlFunctions.fillHandProbs()
# sqlFunctions.showTable("WinProbabilities")
# sqlFunctions.fillRecos()

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
# sqlFunctions.createRecos()
# fillTables(1000)
# truncateAllTables()
