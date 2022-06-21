import random
import keyboard
import mysql.connector

class Hand:
    def __init__(self):
        self.hand = []
        self.handValue = 0
        self.initialValue = 0
        self.soft = False

    def dealCard(self, cards):
        card = random.randint(0, len(cards) - 1)
        self.hand.append(cards[card])
        cards.remove(cards[card])

def startGame(d, p):
    initialDeal(d, p)
    calcValue(d, True)    
    calcValue(p)

def dealerLogic(d, p, cards):
    exit = False
    if p.handValue > 21:
        return
    while not exit:
        calcValue(d)
        
        if d.handValue == 17 and d.soft:
            d.dealCard(cards)
        elif d.handValue < 17:
            d.dealCard(cards)
        else:
            exit = True

def calcValue(x, dealer=False):
    value = 0
    aces = 0
    if dealer:
        i = x.hand[1]
        if i[0] in ["J", "Q", "K"]:
            value += 10
        elif i[:2] == "10":
            value += 10
        elif i[0] == "A":
            value += 11
        else:
            value += int(i[0])
        x.handValue = value
        return
    for i in x.hand:
        if i[0] in ["J", "Q", "K"]:
            value += 10
        elif i[:2] == "10":
            value += 10
        elif i[0] == "A":
            aces += 1
        else:
            value += int(i[0])
    if aces > 0:
        if value + aces + 10 <= 21:
            value = value + aces + 10
            if value == 17:
                x.soft = True
        else:
            value += aces
    x.handValue = value

def initialDeal(d, p, cards):
    p.dealCard(cards)
    d.dealCard(cards)
    p.dealCard(cards)
    d.dealCard(cards)
    calcValue(p)
    calcValue(d, True)

def playerLogic(p, cards):
    calcValue(p)
    if p.handValue <= 11:
        while p.handValue <= 11:
            p.dealCard(cards)
            calcValue(p)
    if p.handValue >= 17:
        p.initialValue = p.handValue
        return "Stand"
    
    
    p.initialValue = p.handValue

    action = random.randint(1, 2)
    if action == 1:
        return "Stand"
    elif action == 2:
        while p.handValue < 17:
            p.dealCard(cards)
            calcValue(p)
        return "Hit"

def winLogic(d, p):
    calcValue(d)
    if len(p.hand) == 2 and p.handValue == 21:
        return "Blackjack"

    elif p.handValue > d.handValue and p.handValue <= 21:
        return "Win"

    elif d.handValue > 21 and p.handValue <= 21:
        return "Win"

    elif d.handValue == p.handValue and p.handValue <= 21:
        return "Push"

    else:
        return "Loss"

def fillHandOutcomes(num):
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mySQLpassword",
    database = "PythonFoundationProject"
    )

    mycursor = db.cursor()

    cards = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah",
        "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad",
        "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac",
        "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As"]

    i=0
    while i < num:
        p = Hand()
        d = Hand()
        if keyboard.is_pressed("esc"):
            break

        initialDeal(d, p, cards)
        p.initialValue = p.handValue
        d.initialValue = d.handValue
        
        action = playerLogic(p, cards)


        dealerLogic(d, p, cards)
        outcome = winLogic(d, p)

        if outcome != "Blackjack" and not (len(d.hand) == 2 and d.handValue == 21):
            mycursor.execute("INSERT INTO handOutcomes (handIdentifier, dealerValue, playerValue, action, result) VALUES (%s, %s, %s, %s, %s)", (str(d.initialValue) + str(p.initialValue), d.initialValue, p.initialValue, action, outcome))
            db.commit()
            i += 1

        if len(cards) <= 10:
            cards = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah",
                    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad",
                    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac",
                    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As"]