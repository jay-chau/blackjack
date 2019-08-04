from random import shuffle
from time import sleep

class deck:
    decknum = 8
    shuffleproportion = 0.6
    
    def __init__(self):
        self.decknew()
    
    def deckdraw(self):
        card = self.deck[0]
        del self.deck[0]
        return card
    
    def decknew(self):
        suits = [u"\u2666", u"\u2663",u"\u2665", u"\u2660"]
        cards = list(range(2,11))
        cards.extend(['J', 'Q', 'K', 'A'])
        deck = ["{}{}".format(str(c), s) for c in cards for s in suits]
        self.deck = deck*self.decknum
        shuffle(self.deck)
    
    @property
    def decklen(self):
        return len(self.deck)

class person:
    def __init__(self):
        self.hand=[]
        self.acecount=0
    
    def carddraw(self, deckobject):
        self.hand.append(deckobject.deckdraw())
    
    def checkace(self):
        if self.handscore > 21 and self.acecount > 0:
            loc = self.simplehand.index(11)
            self.hand[loc] = "{}{}".format(str(1),self.hand[loc][-1])


    @property
    def simplehand(self):
        h = [c[:-1] for c in self.hand]
        highcard = ['J', 'Q', 'K']
        h = [x if x not in highcard else 10 for x in h]

        self.acecount = h.count('A')
        h = [int(x) if x != 'A' else 11 for x in h]
        return h
    
    @property
    def displayhand(self):
        return [x.replace('1', 'A') if '10' not in x else x for x in self.hand]

    @property
    def handscore(self):
        return sum(self.simplehand)
        
class player(person):
    currenthands = 0
    chips = 1000
    betamount = 10
    playturn = 1
    
    def __init__(self):
        super().__init__()
        player.currenthands += 1
        self.pot = 0
    
    def bet(self, handsplit=False):
        player.chips -= player.betamount
        if handsplit == False:
            self.pot += player.betamount
        
    def hit(self, deckobject):
        self.carddraw(deckobject)

    def stand(self):
        print("Stand with {}".format(self.handscore))
        player.playturn = 0
    
    def handsplit(self, playerobject):
        print("Function not available")
        #To do: Not working
        c = self.simplehand
        if (c[0] == c[1]) and (len(c) == 2):
            self.bet(handsplit=True)
            i = player.currenthands
            playerobject[i] = player()
            playerobject[i-1].hand = self.hand[-1]
            playerobject[i-1].pot = player.betamount
            self.hand = self.hand[0]
            
    def doubledown(self, deckobject):
        if len(self.hand) == 2:
            self.bet()
            self.carddraw(deckobject)
            player.playturn = 0
        else:
            print("You cannot double down with more than 2 cards")
    
    def checkbust(self):
        self.checkace()
        if self.handscore > 21:
            print("Bust")
            player.playturn = 0      

    def playactions(self, action, deckobject, playerobject):
        a = action.lower()
        if a == 'h':
            self.hit(deckobject)
        elif a == 's':
            self.stand()
        elif a == 'sp':
            self.handsplit(playerobject)
        elif a == 'dd':
            self.doubledown(deckobject)
        else:
            print("No action selected")

            
    @classmethod
    def changebet(cls):
        changingbet = 1
        while changingbet == 1:
            a = input("Set new bet amount: ")
            try:
                cls.betamount = int(a)
                changingbet = 0
            except:
                print("Bet amount must be a number")
                pass
    
    @property
    def showchips(self):
        return player.chips
            
class dealer(person):
    def __init__(self):
        super().__init__()
      
    @property
    def dealerhand(self):
        return self.hand[1:]
    
    @property
    def dealerhandscore(self):
        return sum(self.simplehand[1:])

class table:
    speedcount = 0
    playing = 1
    roundnumber = 0
    sleeptime = 1

    def __init__(self):
        self.deck = deck()
        self.play = dict()
        self.play[0] = player()
        self.deal = dealer()
        
    def newround(self):
        table.roundnumber += 1
        player.playturn = 1
        player.currenthands = 0
        self.play[0].bet()
        
        for i in range(2):
            self.play[0].carddraw(self.deck)
            self.deal.carddraw(self.deck)

        self.showhands(1,0)
        sleep(table.sleeptime)
        print("Dealer : {}".format(self.deal.dealerhand))
        sleep(table.sleeptime)

        if self.play[0].handscore == 21:
            player.playturn = 0
            player.chips += int(self.play[0].pot * 5/2)     
        elif self.deal.dealerhand == 10:
            self.checkinsurance()
   
    def checkinsurance(self):
        a = input("Buy Insurance? (y/n)").lower()
        if a == 'y':
            #To Do: Set insurance pay"
            print("Feature not implemented")

        if self.deal.handscore == 21:
            print("Dealer has Blackjack")
            player.playturn = 0
        else:
            print("Dealer does not have Blackjack")
    
    def playerround(self):
        print('====PLAYER')
        print('=={HIT: h};{STAND: s};{SPLIT: sp};{DOUBLE DOWN: dd}')
        while player.playturn == 1:
            a = input("Action:")
            self.play[0].playactions(a,self.deck, self.play)
            self.showhands(1,0)
            self.play[0].checkbust()

    def dealerround(self):
        print("====DEALER")
        self.showhands(0,1)
        while self.deal.handscore < 17:
            self.deal.carddraw(self.deck) 
            self.deal.checkace()
            self.showhands(0,1)                
            sleep(table.sleeptime)
        if self.deal.handscore <= 21:
            print("Stand with {}".format(self.deal.handscore))
        else:
            print("Dealer Bust")

    def endround(self):
        print("======ROUND {} END".format(table.roundnumber))
        sleep(table.sleeptime)
        self.showhands(1,1)
        sleep(table.sleeptime)
        if self.play[0].handscore <= 21:
            if (self.play[0].handscore > self.deal.handscore) or (self.deal.handscore > 21):
                print("Player Wins")
                player.chips += self.play[0].pot * 2
            elif self.play[0].handscore < self.deal.handscore:
                print("Dealer Wins")
            else:
                print("Push")
                player.chips += self.play[0].pot
        else:
            print("Dealer Wins")
        
    def resetround(self):
        self.play[0].pot = 0
        self.play[0].hand = []
        self.deal.hand = []
        
        if self.deck.decklen < deck.decknum * 52 * deck.shuffleproportion:
            self.deck = deck()
            print("Deck has been shuffled")

        print("Current chips: {}".format(player.chips))
        print("Current bet: {}".format(player.betamount))
        setcontinue = 1
        print('=={YES: y};{NO: n};{CHANGE BET: b}')
        while setcontinue == 1:
            a = input("Continue?:").lower()
            if a == 'n':
                table.playing = 0
                setcontinue = 0
            elif a == 'b':
                self.play[0].changebet()
                setcontinue = 0
            elif a =='y':
                setcontinue = 0
            else:
                print("No action selected")
                pass
    
    def showhands(self, p, d):
        if p == 1:
            print("Player Hand: {}".format(self.play[0].displayhand))
        if d == 1:
            print("Dealer Hand: {}".format(self.deal.displayhand))


def __main__():
    t = table()
    while table.playing == 1:
        print("======ROUND {}".format(table.roundnumber + 1))
        sleep(table.sleeptime)
        
        t.newround()
        t.playerround()
        t.dealerround()
        t.endround()
        
        sleep(table.sleeptime)
        t.resetround()
    
    print("End with ${}".format(player.chips))
    input("Any key to quit")

__main__()

#Other 'to do'
#Cant bet more then owned
#Dealer/player win count
#Table count (simple speed count)
#Pair betting
# Dealer shouldnt play if player bust
