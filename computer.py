import pygame, random
import utils


class Computer():

    def __init__(self, cards:list, id:int):
        assert len(cards) == 13, "Cards not equally distributed"
        self.thulaReceived = 0
        self.thulaGiven = 0
        self.cards = cards
        self.id = id
        self.isTurn = False
        self.cardThrownThisTurn = None
        self.hasAceOfSpades = False
        for card in self.cards:
            if card.suit == 'SPADES' and card.rank == 14:
                self.hasAceOfSpades = True

    def getAceOfSpades(self):
        for card in self.cards:
            if card.suit == 'SPADES' and card.rank == 14:
                return card
    
    def getCard(self, ongoingSuit: str, isFirstTurnInGame:bool):
        assert self.isTurn, "Wait for your turn, please"
        if ongoingSuit: # if round is ongoing
            cards = filter(lambda c: c.suit == ongoingSuit, self.cards)
            matchingCards = []
            for card in cards:
                matchingCards.append(card)

            if len(matchingCards) == 0:
                self.thulaGiven += 1
                self.isTurn = False
                self.cardThrownThisTurn = random.sample(self.cards, 1)[0]
            else:
                self.isTurn = False
                self.cardThrownThisTurn = random.sample(matchingCards, 1)[0]

        else: # if round is to be started
            if isFirstTurnInGame:
                self.cardThrownThisTurn = self.getAceOfSpades()
                self.isTurn = False
            else:
                self.cardThrownThisTurn = random.sample(self.cards, 1)[0]
                self.isTurn = False
        
        return self.cardThrownThisTurn


    def insertCards(self, cards: list):
        self.thulaReceived += 1 # cards are only inserted in case of thula
        for card in cards:
            self.cards.append(card)
        self.cards = utils.sortCards(self.cards)       

