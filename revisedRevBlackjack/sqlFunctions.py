import mysql.connector
import pwinput
import blackjackText

username = input("Username for mySQL: ")
useDatabase = input("Database you want to use: ")
password = pwinput.pwinput(prompt='Password for mySQL: ', mask='*')

db = mysql.connector.connect(
    host="localhost",
    user=username,
    passwd=password,
    database = useDatabase
    )

mycursor = db.cursor()

def createTables():
    try:
        mycursor.execute("""CREATE TABLE HandOutcomes (handNumber int PRIMARY KEY AUTO_INCREMENT, handIdentifier varchar(50), 
                    dealerValue int, playerValue int, action varchar(50), result varchar(50))""")
    except:
        print("HandOutcomes already exists")
    
    try:
        mycursor.execute("CREATE TABLE WinProbabilities (handIdentifier varchar(50) PRIMARY KEY, hitWinProb varchar(50), standWinProb varchar(50), totalWinProb varchar(50), totalLossProb varchar(50))")
        for i in range(2, 12):
            for x in range(12, 22):
                mycursor.execute(f"INSERT INTO WinProbabilities (handIdentifier) VALUES ({str(i)}{str(x)})")
        db.commit()
    except:
        print("WinProbabilities already exists")

    try:
        mycursor.execute("CREATE TABLE Recommendations (handIdentifier varchar(50) PRIMARY KEY, recommendation varchar(50))")
    except:
        print("Recommendations table already exists")

def dropTable(name):
    mycursor.execute("DROP TABLE " + name)

def insertHandoutcomes(dinit, pinit, action, outcome):
    mycursor.execute("INSERT INTO handOutcomes (handIdentifier, dealerValue, playerValue, action, result) VALUES (%s, %s, %s, %s, %s)", (str(dinit) + str(pinit), dinit, pinit, action, outcome))
    db.commit()

def getRecommendation(hand):
    mycursor.execute(f"SELECT recommendation FROM Recommendations WHERE handIdentifier = {hand}")
    for i in mycursor:
        return i[0]

def getFullWinProbs(hand):
    mycursor.execute(f"SELECT hitWinProb, standWinProb, totalWinProb FROM winProbabilities WHERE handIdentifier = {hand}")
    for i in mycursor:
        return i[0], i[1], i[2]

def totalSimmedGames():
    mycursor.execute("SELECT COUNT(*) FROM HANDOUTCOMES")
    for i in mycursor:
        return i[0]

def fillHandProbs():
    for i in range(2, 12):
        for x in range(12, 22):
            fillHandProbsCon(str(i) + str(x))
    db.commit()

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

    print(hitTotal, hitWinTotal, standTotal, standWinTotal)
    
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

def insertReco(hand, recommend):
    mycursor.execute(f"UPDATE Recommendations SET recommendation = '{recommend}' WHERE handIdentifier = {hand}")
    db.commit()

def updateTables(num):
    blackjackText.fillHandOutcomes(num)
    fillHandProbs()
    fillRecos()