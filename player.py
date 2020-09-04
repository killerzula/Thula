import pygame, random
import utils

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Player():
    def __init__(self, cards:list, id:int, sprites:pygame.sprite.Group):
        assert len(cards) == 13, "Cards not equally distributed"
        self.thulaReceived = 0
        self.thulaGiven = 0
        self.cards = cards
        self.id = id
        self.isTurn = False
        self.cardThrownThisTurn = None
        self.hasAceOfSpades = False
        self.spriteGroup = sprites

        for card in self.cards:
            if card.suit == 'SPADES' and card.rank == 14:
                self.hasAceOfSpades = True
                break
    
    def getCard(self, ongoingSuit: str, isFirstTurnInGame:bool):
        assert self.isTurn, "Wait for your turn, please"
        if ongoingSuit: # if round is ongoing
            cards = filter(lambda c: c.suit == ongoingSuit, self.cards)
            matchingCards = []
            for card in cards:
                matchingCards.append(card)

            if len(matchingCards) == 0:
                self.thulaGiven += 1
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            for card in self.spriteGroup:
                                if card.rect.collidepoint(event.pos):
                                    self.cardThrownThisTurn = card
                                    self.isTurn = False
                                    return self.cardThrownThisTurn
                        if event.type == pygame.QUIT:
                            utils.quit()
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                utils.quit()
            else:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            for card in self.spriteGroup:
                                if card.rect.collidepoint(event.pos) and card.suit == ongoingSuit:
                                    self.cardThrownThisTurn = card
                                    self.isTurn = False
                                    return self.cardThrownThisTurn
                        if event.type == pygame.QUIT:
                            utils.quit()
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                utils.quit()
        else: # if round is to be started
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        for card in self.spriteGroup:
                            if isFirstTurnInGame: # if this is the first round in the game
                                # if card.rect.collidepoint(event.pos) and card.suit == 'SPADES' and card.rank == 14:
                                if card.rect.collidepoint(event.pos):
                                    # in case of first round in game player should only throw the ace of spades
                                    self.cardThrownThisTurn = card
                                    self.isTurn = False
                                    return self.cardThrownThisTurn
                            else:
                                if card.rect.collidepoint(event.pos):
                                    # after a thula player may throw any card
                                    self.cardThrownThisTurn = card
                                    self.isTurn = False
                                    return self.cardThrownThisTurn
                    if event.type == pygame.QUIT:
                        utils.quit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            utils.quit()
                            

    def insertCards(self, cards: list):
        self.thulaReceived += 1 # cards are only inserted in case of thula
        for card in cards:
            self.cards.insert(card)
        self.cards = utils.sortCards(self.cards)       