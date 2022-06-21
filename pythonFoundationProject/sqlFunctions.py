import mysql.connector
import blackjackText2

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mySQLPassword",
    database = "PythonFoundationProject"
    )

mycursor = db.cursor(buffered=True)



def dropTable(table):
    mycursor.execute("DROP TABLE " + str(table))




def createHandOutcomes():
    mycursor.execute("""CREATE TABLE HandOutcomes (handNumber int PRIMARY KEY AUTO_INCREMENT, handIdentifier varchar(50), 
                    dealerValue int, playerValue int, action varchar(50), result varchar(50));""")

def createWinProbabilities():
    mycursor.execute("CREATE TABLE WinProbabilities (handIdentifier varchar(50) PRIMARY KEY, hitWinProb varchar(50), standWinProb varchar(50), totalWinProb varchar(50), totalLossProb varchar(50))")
    

def createRecos():
    mycursor.execute("CREATE TABLE Recommendations (handIdentifier varchar(50) PRIMARY KEY, recommendation varchar(50))")



def fillRecos():
    mycursor.execute("TRUNCATE TABLE Recommendations")
    for i in range(2, 12):
        for x in range(12, 22):
            mycursor.execute(f"INSERT INTO Recommendations (handIdentifier) VALUES ({str(i)}{str(x)})")
    db.commit()

    mycursor.execute("SELECT handIdentifier, hitWinProb, standWinProb FROM WinProbabilities")
    myList = []
    for i in mycursor:
        myList.append(i)
    for i in myList:
        if i[1] == "N/A" and i[2] == "N/A":
            mycursor.execute("UPDATE Recommendations SET recommendation = 'N/A' WHERE handIdentifier = " + str(i[0]))
            db.commit()
        elif i[1] == "N/A":
            mycursor.execute(f"UPDATE Recommendations SET recommendation = 'Stand' WHERE handIdentifier = '{i[0]}'")
            db.commit()
        elif i[2] == "N/A":
            mycursor.execute(f"UPDATE Recommendations SET recommendation = 'Hit' WHERE handIdentifier = '{i[0]}'")
            db.commit()
        elif float(i[1][:len(i[1]) - 2]) > float(i[2][:len(i[2]) - 2]):
            mycursor.execute("UPDATE Recommendations SET recommendation = 'Hit' WHERE handIdentifier = " + str(i[0]))
            db.commit()
        else:
            mycursor.execute("UPDATE Recommendations SET recommendation = 'Stand' WHERE handIdentifier = " + str(i[0]))
            db.commit()

def truncateTable(table):
    mycursor.execute("TRUNCATE TABLE " + str(table))

def showTable(table):
    mycursor.execute("SELECT * FROM " + str(table))
    for i in mycursor:
        print(i)

def fillHandProbs():
    for i in range(2, 12):
        for x in range(12, 22):
            fillHandProbsCon(str(i) + str(x))


def fillHandProbsCon(hand):
    mycursor.execute(f"SELECT COUNT(*) FROM HandOutcomes WHERE handIdentifier = {hand} AND action = 'Hit'")
    for i in mycursor:
        hitTotal = int(i[0])
    mycursor.execute(f"SELECT COUNT(*) FROM HandOutcomes WHERE handIdentifier = {hand} AND action = 'Hit' AND result = 'Win'")
    for i in mycursor:
        hitWinTotal = int(i[0])
    mycursor.execute(f"SELECT COUNT(*) FROM HandOutcomes WHERE handIdentifier = {hand} AND action = 'Stand'")
    for i in mycursor:
        standTotal = int(i[0])
    mycursor.execute(f"SELECT COUNT(*) FROM HandOutcomes WHERE handIdentifier = {hand} AND action = 'Stand' AND result = 'Win'")
    for i in mycursor:
        standWinTotal = int(i[0])
    mycursor.execute(f"SELECT COUNT(*) FROM HandOutcomes WHERE handIdentifier = {hand}")
    for i in mycursor:
        total = int(i[0])
    mycursor.execute(f"SELECT COUNT(*) FROM HandOutcomes WHERE handIdentifier = {hand} AND result = 'Win'")
    for i in mycursor:
        winTotal = int(i[0])
    
    

    if hitTotal != 0:
        mycursor.execute(f"""UPDATE WinProbabilities 
                            SET hitWinProb = '{str((hitWinTotal/hitTotal) * 100)}%'   
                            WHERE handIdentifier = {hand};""")
    else:
        mycursor.execute(f"""UPDATE WinProbabilities 
                            SET hitWinProb = 'N/A'
                            WHERE handIdentifier = {hand};""")
    if standTotal != 0:
        mycursor.execute(f"""UPDATE WinProbabilities 
                            SET standWinProb = '{str((standWinTotal/standTotal)*100)}%'
                            WHERE handIdentifier = {hand};""")
    else:
        mycursor.execute(f"""UPDATE WinProbabilities 
                            SET standWinProb = 'N/A'
                            WHERE handIdentifier = {hand};""")
    if total != 0:
        mycursor.execute(f"""UPDATE WinProbabilities 
                            SET totalWinProb = '{str((winTotal/total)*100)}%' 
                            WHERE handIdentifier = {hand};""")
    else:
        mycursor.execute(f"""UPDATE WinProbabilities 
                            SET totalWinProb = 'N/A' 
                            WHERE handIdentifier = {hand};""")
    db.commit()

def getFullWinProbs(hand):
    mycursor.execute(f"SELECT hitWinProb, standWinProb, totalWinProb FROM winProbabilities WHERE handIdentifier = {hand}")
    for i in mycursor:
        return i[0], i[1], i[2]

def getRecommendation(hand):
    mycursor.execute(f"SELECT recommendation FROM Recommendations WHERE handIdentifier = {hand}")
    for i in mycursor:
        return i[0]

def insertReco(hand, recommend):
    mycursor.execute(f"UPDATE Recommendations SET recommendation = '{recommend}' WHERE handIdentifier = {hand}")
    db.commit()

def countTotalHands():
    mycursor.execute("SELECT COUNT(*) FROM HandOutcomes")
    for i in mycursor:
        return i[0]

def createDatabase():
    mycursor.execute("CREATE DATABASE PythonFoundationProject")

def createForeignKey():
    mycursor.execute("ALTER TABLE HandOutcomes ADD FOREIGN KEY (HandIdentifier) REFERENCES WinProbabilities(handIdentifier);")