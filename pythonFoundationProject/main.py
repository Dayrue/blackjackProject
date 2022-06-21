import random
import pygame as pg
import os
import time
import foundationProject

#Allows me to not have to put full directory path for pictures or other files
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Sets size of window and initializes font for use
win = pg.display.set_mode((800, 800))
pg.font.init()
my_font = pg.font.SysFont('Times New Roman', 30)

#Loading all necessary images into pygame
sprites = pg.image.load("pictures/cardSprites.png").convert_alpha()
felt = pg.image.load("pictures/bjFelt.png")
blankImg = pg.image.load("pictures/blankCard.png")
bet1000 = pg.image.load("pictures/bet1000.png")
bet5000 = pg.image.load("pictures/bet5000.png")
bet10000 = pg.image.load("pictures/bet10000.png")
clearBet = pg.image.load("pictures/clearBet.png")
doubleBet = pg.image.load("pictures/doubleBet.png")

#sets the colors for input box when choosing to run simulations
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')

class dealerHand:
    #Inits dealer hand, the total value, the value showed to the player, the x and y cords for their card pics and whether or not their hand is soft
    def __init__(self):
        self.hand = []
        self.handValue = 0
        self.showValue = 0
        self.x = 650
        self.y = 110
        self.cardPics = []
        self.soft = False

    #deals a card and removes it from the deck
    def dealCard(self):
        card = random.randint(0, len(cards) - 1 )
        self.hand.append(cards[card])
        cards.remove(cards[card])

    #appends sprite to the dealers card pictures
    def showCards(self):
        if len(self.cardPics) == len(self.hand):
            return
        tempList = []
        for i in self.hand:
            indy = indexCards.index(i)
            tempList.append(get_image(sprites, indy))
        self.cardPics = tempList

    def dealAnimation(self):
        self.showCards()
        x, y = 50, 50
        while y < self.y:
            win.blit(felt, (0, 0))
            win.blit(self.cardPics[len(self.cardPics) - 1], (x, y))
            y += 5
            pg.display.update()
        while x < self.x:
            win.blit(felt, (0, 0))
            win.blit(self.cardPics[len(self.cardPics) - 1], (x, y))
            x += 5
            pg.display.update()

class playerHand:
    def __init__(self, balance):
        self.hand = []
        self.x = 650
        self.y = 600
        self.handValue = 0
        self.balance = balance
        self.cardPics = []
        self.soft = False

    def dealCard(self):
        card = random.randint(0, len(cards) - 1)
        self.hand.append(cards[card])
        cards.remove(cards[card])
    
    def showCards(self):
        if len(self.cardPics) == len(self.hand):
            return
        tempList = []
        for i in self.hand:
            indy = indexCards.index(i)
            tempList.append(get_image(sprites, indy))
        self.cardPics = tempList

    def dealAnimation(self):
        self.showCards()
        x, y = 50, 50
        while y < self.y:
            win.blit(felt, (0, 0))
            win.blit(self.cardPics[len(self.cardPics) - 1], (x, y))
            y += 5
            pg.display.update()
        while x < self.x:
            win.blit(felt, (0, 0))
            win.blit(self.cardPics[len(self.cardPics) - 1], (x, y))
            x += 5
            pg.display.update()

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = (COLOR_INACTIVE)
        self.text = text
        self.txt_surface = my_font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = my_font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

def getPlayerBalance():
    # Gets the saved player balance from playerBalance.txt
    with open("playerBalance.txt", "r") as f:
        for x in f.read().split('\n'):
    
            return float(f.read())

def initialDeal(d, p):
    #deals the initial four cards
    p.dealCard()
    d.dealCard()
    p.dealCard()
    d.dealCard()

def calcValue(x, dealer=False):
    #iterates through the cards in either the dealer or player's hand
    value = 0
    aces = 0
    if dealer:
        #used to get the initial dealer value showed to the player
        i = d.hand[1]
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
    #Checks whether or not ace should count as 11 or 1
    if aces > 0:
        if value + aces + 10 <= 21:
            value = value + aces + 10
            if value == 17:
                x.soft = True
        else:
            value += aces
    x.handValue = value

def dealerLogic(d):
    #Creates the logic for the dealer to hit when under 17 or soft 17
    exit = False
    if p.handValue > 21:
        return
    while not exit:
        calcValue(d)
        
        if d.handValue == 17 and d.soft:
            d.dealCard()
        elif d.handValue < 17:
            d.dealCard()
        else:
            exit = True

def winLogic(d, p, bet):
    #checks dealer hand and player value to determine who wins the hand
    calcValue(d)
    if len(p.hand) == 2 and p.handValue == 21:
        message = my_font.render('BlackJack', False, (255, 255, 255))
        win.blit(message, (400, 330))
        p.balance = p.balance + (bet * 1.5)

    elif p.handValue > d.handValue and p.handValue <= 21:
        message = my_font.render('Win', False, (255, 255, 255))
        win.blit(message, (400, 330))
        p.balance += bet

    elif d.handValue > 21 and p.handValue <= 21:
        message = my_font.render('Win', False, (255, 255, 255))
        win.blit(message, (400, 330))
        p.balance += bet

    elif d.handValue == p.handValue and p.handValue <= 21:
        message = my_font.render('Push', False, (255, 255, 255))
        win.blit(message, (400, 330))

    else:
        message = my_font.render('Loss', False, (255, 255, 255))
        win.blit(message, (400, 330))
        p.balance -= bet
    pg.display.update()

def startGame(d, p):
    #resets the game
    initialDeal(d, p)
    calcValue(d, True)    
    calcValue(p)

def draw_window(surface, showDeal):
    #Displays all messages for the main gameboard
    surface.blit(felt, (0, 0))
    
    dealValue = my_font.render('Dealer Value: ' + str(d.handValue), False, (255, 255, 255))
    surface.blit(dealValue, (400,0))
    
    playValue = my_font.render('Player Value: ' + str(p.handValue), False, (255, 255, 255))
    surface.blit(playValue, (400,750))

    balance = my_font.render(('Balance: ' + f'{p.balance:.2f}' + " Bet: " + str(bet)), False, (255, 255, 255))
    surface.blit(balance, (200,250))

    if p.handValue <= 11:
        reco = "Hit"
    else:
        reco = foundationProject.getRecommendation(str(d.handValue) + str(p.handValue))

    recommendation = my_font.render((f'Recommended: {reco}'), False, (255, 255, 255))
    surface.blit(recommendation, (100, 750))

    surface.blit(bet1000, (100, 400))
    surface.blit(bet5000, (350, 400))
    surface.blit(bet10000, (600, 400))
    surface.blit(clearBet, (225, 475))
    surface.blit(doubleBet, (475, 475))

    p.showCards()
    d.showCards()
    
    x, y = 650, 600
    for i in p.cardPics:
        win.blit(i, (x, y))
        x -= 80

    x, y = 650, 110
    if showDeal:
        for i in d.cardPics:
            win.blit(i, (x, y))
            x -= 80
    else:
        win.blit(blankImg, (650, y))
        win.blit(d.cardPics[1], (600, y))

    pg.display.update()

def betScreen():
    #Screen displayed for the player to determine which bet they want
    win.blit(felt, (0, 0))
    balance = my_font.render(('Balance: ' + f'{p.balance:.2f}' + " Bet: " + str(bet)), False, (255, 255, 255))
    win.blit(balance, (200,250))

    betMessage = my_font.render(("Place your bet"), False, (255, 255, 255))
    win.blit(betMessage, (300, 300))

    win.blit(bet1000, (100, 400))
    win.blit(bet5000, (350, 400))
    win.blit(bet10000, (600, 400))
    win.blit(clearBet, (225, 475))
    win.blit(doubleBet, (475, 475))

    pg.display.update()

def restartGame(d, p, cards):
    #Restarts the game
    d = dealerHand()
    p = playerHand(p.balance)
    startGame(d, p)
    if len(cards) < 15:
        draw_window(win, False)
        
        dealHand = my_font.render('Shuffling...', False, (255, 255, 255))
        win.blit(dealHand, (250, 400))
        pg.display.update()
        time.sleep(2)
        cards = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah",
                "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad",
                "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac",
                "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As"]
    return d, p, cards

def get_image(sheet, i):
    #Used to pull sprites of cards
    if i < 13:
        y = 0
    elif i >= 13 and i < 26:
        y = 117
        i -= 13
    elif i >= 26 and i < 39:
        y = 234
        i -= 26
    elif i >= 39 and i < 52:
        y = 352
        i -= 39

    image = pg.Surface((80, 116)).convert_alpha()
    image.blit(sheet, (0, 0), ((80 * i) + (1 * i), y, 80, 116))

    return image

def drawTableWin():
    #Displays window used to view SQL functions
    win.fill((0, 0, 0))
    dealValue = my_font.render('Dealer Value: ' + str(d.handValue), False, (255, 255, 255))
    win.blit(dealValue, (200,200))
    
    playValue = my_font.render('Player Value: ' + str(p.handValue), False, (255, 255, 255))
    win.blit(playValue, (550, 200))

    instruction1 = my_font.render('Press esc to exit', False, (255, 255, 255))
    win.blit(instruction1, (50, 500))

    instruction2 = my_font.render('Press 1 to view recommendation', False, (255, 255, 255))
    win.blit(instruction2, (50, 550))

    instruction3 = my_font.render('Press 2 to view full probabilities', False, (255, 255, 255))
    win.blit(instruction3, (50, 600))

    instruction4 = my_font.render('Press 3 to run more simulations', False, (255, 255, 255))
    win.blit(instruction4, (50, 650))

    instruction5 = my_font.render('Press 4 to declare custom recommendation', False, (255, 255, 255))
    win.blit(instruction5, (50, 700))

    instruction6 = my_font.render('Press 5 to view total simulated games', False, (255, 255, 255))
    win.blit(instruction6, (50, 750))

def tableShowReco():
    #Carries out press 1 action on SQL window
    drawTableWin()
    reco = my_font.render(f'Reccomendation: {foundationProject.getRecommendation(str(d.handValue) + str(p.handValue))}', False, (255, 255, 255))
    win.blit(reco, (50, 450))

def tableShowFullProbs():
    #Show complete win loss probs on SQL window
    try:
        drawTableWin()
        hitWin = foundationProject.getWinProbs(str(d.handValue) + str(p.handValue))[0]
        standWin = foundationProject.getWinProbs(str(d.handValue) + str(p.handValue))[1]
        totalWin = foundationProject.getWinProbs(str(d.handValue) + str(p.handValue))[2]
        hit = my_font.render(f'Hit Win Prob.: {hitWin}', False, (255, 255, 255))
        win.blit(hit, (50, 300))
        stand = my_font.render(f'Stand Win Prob.: {standWin}', False, (255, 255, 255))
        win.blit(stand, (50, 350))
        total = my_font.render(f'Total Win Prob.: {totalWin}', False, (255, 255, 255))
        win.blit(total, (50, 400))

        pg.display.update()
    except:
        errorMessage = my_font.render(f'Please run more Simulations before viewing probabilities.', False, (255, 255, 255))
        win.blit(errorMessage, (50, 300))
        pg.display.update()
        time.sleep(2)
        drawTableWin()
        pg.display.update()
        return

def tableMoreSims():
    #Runs more blackjack sims and then updates all the tables for it
    inputBox = InputBox(550, 350, 140, 32)
    total = my_font.render('Enter number of games you wish to run: ', False, (255, 255, 255))
    win.blit(total, (50, 350))
    run2 = True
    while run2:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    run2 = False
                    running = my_font.render('Loading Tables...', False, (255, 255, 255))
                    win.blit(running, (200, 420))
                    pg.display.update()
                    try:
                        return int(inputBox.text)
                    except:
                        return 1

            inputBox.handle_event(event)
            
        inputBox.update()
        inputBox.draw(win)
         
        pg.display.flip()

def totalSimGames():
    total = my_font.render('Total Games Simulated: ' + str(foundationProject.totalSims()), False, (255, 255, 255))
    win.blit(total, (50, 350))
    pg.display.update()

def customRecosWin():
    inputBox1 = InputBox(280, 280, 50, 32)
    inputBox2 = InputBox(280, 330, 50, 32)
    inputBox3 = InputBox(280, 380, 50, 32)
    in1 = my_font.render('Dealer Value: ', False, (255, 255, 255))
    in2 = my_font.render('Player Value: ', False, (255, 255, 255))
    in3 = my_font.render('Recommendation: ', False, (255, 255, 255))
    win.blit(in1, (50, 280))
    win.blit(in2, (50, 330))
    win.blit(in3, (50, 380))
    run2 = True
    while run2:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    run2 = False
                    running = my_font.render('Loading Tables...', False, (255, 255, 255))
                    win.blit(running, (200, 420))
                    pg.display.update()
                    # print(int(inputBox1.text), int(inputBox2.text), inputBox3.text)
                    try:
                        return int(inputBox1.text), int(inputBox2.text), inputBox3.text
                    except:
                        print("Not valid inputs")

            inputBox1.handle_event(event)
            inputBox2.handle_event(event)
            inputBox3.handle_event(event)
            
        inputBox1.update()
        inputBox2.update()
        inputBox3.update()
        inputBox1.draw(win)
        inputBox2.draw(win)
        inputBox3.draw(win)
         
        pg.display.flip()

def TableWin():
    #displays the main SQL window
    drawTableWin()
    pg.display.update()
    run1 = True
    while run1:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run1 = False
                if event.key == pg.K_1 or event.key == pg.K_KP_1:
                    drawTableWin()
                    tableShowReco()
                if event.key == pg.K_2 or event.key == pg.K_KP_2:
                    drawTableWin()
                    tableShowFullProbs()
                if event.key == pg.K_3 or event.key == pg.K_KP_3:
                    drawTableWin()
                    foundationProject.updateTables(int(tableMoreSims()))
                    drawTableWin()
                if event.key == pg.K_4 or event.key == pg.K_KP_4:
                    drawTableWin()
                    try:
                        holder = customRecosWin()
                        dealerVal = holder[0]
                        playerVal = holder[1]
                        recommend = holder[2]
                        hand = str(dealerVal) + str(playerVal)
                        foundationProject.customReco(hand, recommend)
                        drawTableWin()
                    except:
                        drawTableWin()
                if event.key == pg.K_5 or event.key == pg.K_KP_5:
                    totalSimGames()
                
        pg.display.update()

#Main playing deck
cards = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah",
        "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad",
        "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac",
        "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As"]

#deck used for indexing and gathering sprites
indexCards = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah",
            "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad",
            "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac",
            "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As"]

with open("playerBalance.txt", "r") as f:
    newList = []
    for i in f.read().split("\n"):
        newList.append(i)
    init_balance = float(newList[0])

p = playerHand(init_balance)
d = dealerHand()

bet = 1000

initialDeal(d, p)
calcValue(p)
calcValue(d, True)

gameOver = False
stand = False
double = True
doubleUsed = False
run = True
showDeal = False
changeBet = False

while run:
    p.showCards()
    pg.display.update()

    calcValue(p)
    calcValue(d)

    #if dealer or player gets blackjack the hand is ended
    if p.handValue == 21 and len(p.hand) == 2:
        stand = True
        showDeal = True
    
    calcValue(d)
    if d.handValue == 21 and len(d.hand) == 2:
        stand = True
        showDeal = True
    
    calcValue(d, True)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False
            gameRun = False
        if event.type == pg.MOUSEBUTTONUP and changeBet == True:
            pos = pg.mouse.get_pos()
            if pos[0] in range(100, 180) and pos[1] in range(400, 480) and bet + 1000 <= p.balance:
                bet += 1000
                betScreen()
            elif pos[0] in range(350, 430) and pos[1] in range(400, 480) and bet + 5000 <= p.balance:
                bet += 5000
                betScreen()
            elif pos[0] in range(600, 680) and pos[1] in range(400, 480) and bet + 10000 <= p.balance:
                bet += 10000
                betScreen()
            elif pos[0] in range(225, 305) and pos[1] in range(475, 555):
                bet = 0
                betScreen()
            elif pos[0] in range(475, 555) and pos[1] in range(475, 555) and bet * 2 <= p.balance:
                bet = bet * 2
                betScreen()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_h and not stand:
                p.dealCard()
                calcValue(p)
                double = False
                if p.handValue >= 21:
                    stand = True
                    showDeal = True
            
            if event.key == pg.K_d and not stand and double:
                bet = bet * 2
                doubleUsed = True
                p.dealCard()
                calcValue(p)
                stand = True 
                showDeal = True

            if event.key == pg.K_s and not gameOver:
                stand = True
                showDeal = True

            if event.key == pg.K_TAB:
                TableWin()
                
            if (event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER) and gameOver:
                d, p, cards = restartGame(d, p, cards)
                stand = False
                gameOver = False
                doubleUsed = False
                double = True
                showDeal = False
                changeBet = False

        if stand and not gameOver:
            calcValue(d)
            if d.handValue != 21 and (p.handValue != 21 or len(p.hand) > 2):
                dealerLogic(d)
            draw_window(win, showDeal)
            winLogic(d, p, bet)
            if doubleUsed:
                bet = bet / 2
            if bet > p.balance:
                bet = p.balance
            gameOver = True
            changeBet = True
            time.sleep(1.5)
            betScreen()

    if not gameOver:
        draw_window(win, showDeal)

#Saves the player balance
with open("playerBalance.txt", "w") as f:
    f.write(str(p.balance))
    f.close()
