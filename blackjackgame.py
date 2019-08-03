import random

class deck:
    decknum = 8
    
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
        random.shuffle(self.deck)
    
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
        # To do: Display possible actions
        if action == 'h':
            self.hit(deckobject)
        elif action == 's':
            self.stand()
        elif action == 'sp':
            self.handsplit(playerobject)
        elif action == 'dd':
            self.doubledown(deckobject)
        elif action == 'chips':
            self.showchips
    
    def startactions(self, action):
        if action == 'bet':
            newbet= 10
            self.changebet(newbet)
            
    @classmethod
    def changebet(cls, newbet=10):
        player.betamount = newbet
    
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
    playing = 1

    def __init__(self):
        self.deck = deck()
        self.play = dict()
        self.play[0] = player()
        self.deal = dealer()
        
    def newround(self):
        player.playturn = 1
        player.currenthands = 0
        self.play[0].bet()
        
        for i in range(2):
            self.play[0].carddraw(self.deck)
            self.deal.carddraw(self.deck)
        
        # To do: Check for blackjack

        print("Dealer : {}".format(self.deal.dealerhand))
        print("Player : {}".format(self.play[0].displayhand))

    def playerround(self):
        while player.playturn == 1:
            a = input("Action:")
            self.play[0].playactions(a,self.deck, self.play)
            print(self.play[0].displayhand)
            self.play[0].checkbust()

    def dealerround(self):
        while self.deal.handscore < 17:
            self.deal.carddraw(self.deck) 
            self.deal.checkace()
            print(self.deal.displayhand)


    def endround(self):
        print("{} vs {}".format(self.play[0].displayhand, self.deal.displayhand))
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
        
        self.play[0].pot = 0
        self.play[0].hand = []
        self.deal.hand = []
        
        print(player.chips)
        a = input("Continue? (y/n):")
        if a.lower() == 'n':
            table.playing = 0
        elif a.lower() == 'y':
            pass
            #To do: set new betting


def __main__():
    t = table()
    while table.playing == 1:
        t.newround()
        t.playerround()
        t.dealerround()
        t.endround()
    print("End with ${}".format(player.chips))
    input("Any key to quit")

__main__()

#Other 'to do'
#Cant bet more then owned
#Dealer/player win count
#Table count (simple speed count)
#Deck reset
#Insurance
#Pair betting
#Minimum bets / integer number
