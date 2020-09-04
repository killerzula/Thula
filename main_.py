import pygame
import random
import time

import config
from utils import *
from player import Player
from computer import Computer

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption(config.WINDOW_CAPTION)
canvas = pygame.image.load('assets/canvas.png')

deckSprites = pygame.sprite.Group()

cards = createDeck()
random.shuffle(cards)

playerCards = sortCards(cards[0:13])

for card in playerCards:
    deckSprites.add(card)

player0 = Player(cards=playerCards, id = 0, sprites=deckSprites)
player1 = Computer(cards=sortCards(cards[13:26]), id = 1)
player2 = Computer(cards=sortCards(cards[26:39]), id = 2)
player3 = Computer(cards=sortCards(cards[39:52]), id = 3)

players = [player0, player1, player2, player3]

for player in players:
    if player.hasAceOfSpades:
        firstPlayer = player.id
        break

def main():
    
    index = firstPlayer
    prevIndex = firstPlayer
    highestCard = firstPlayer

    cardsInPlay = []
    playersInPlay = []
    ongoingSuit = None
    isFirstTurnInGame = True
    totalRounds = 0
    
    pygame.init()
    clock.tick(config.FPS)
    flag = False
    while True:

        screen.blit(canvas,(0,0))

        ### TAKE INPUTS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
        
        ### PERFROM COMPUTATIONS
        print(config.IS_ANYTHING_MOVING)
        if flag:
            if not config.IS_ANYTHING_MOVING: # only do this stuff when nothing is moving
                if len(players[index].cards) != 0: # if the player still has cards        
                    players[index].isTurn = True
                    players[index].getCard(ongoingSuit=ongoingSuit, isFirstTurnInGame=isFirstTurnInGame)
                    players[index].cardThrownThisTurn.target = config.TARGET_RECT[index]
                    if len(cardsInPlay) == 0:   # if this is the first turn in current round
                        totalRounds += 1
                        ongoingSuit = players[index].cardThrownThisTurn.suit
                        highestCard = index

                    cardsInPlay.append(players[index].cardThrownThisTurn)
                    playersInPlay.append(index)
                    
                assert not players[index].isTurn # make sure current player has completed turn

                if len(cardsInPlay) > 1:
                    if players[highestCard].cardThrownThisTurn.rank > players[index].cardThrownThisTurn.rank:
                        highestCard = highestCard
                    else: 
                        highestCard = index

                    thula = isThula([
                        players[index].cardThrownThisTurn,
                        players[prevIndex].cardThrownThisTurn
                    ])
                    
                    prevIndex = index
                    index = index + 1 if index != 3 else 0 # update index for next player             

                    if thula:
                        for idx, card in enumerate(cardsInPlay):
                            if card.isStationary:
                                card.target = config.DECK_RECT[highestCard]
                                players[playersInPlay[idx]].cards.remove(card)
                        players[highestCard].insert(cardsInPlay)
                        cardsInPlay = []
                        playersInPlay = []
                        index = highestCard

                    if not thula and len(cardsInPlay) == 4:
                        for idx, card in enumerate(cardsInPlay):
                            if card.isStationary:
                                card.target = config.DECK_RECT[highestCard]
                                players[playersInPlay[idx]].cards.remove(card)
                        cardsInPlay = []
                        playersInPlay = []
                        index = highestCard
                        

        ### RENDER STUFF

        renderCards(
            screen=screen,
            decks=[player0.cards, player1.cards, player2.cards, player3.cards], # deck order is important
            ongoingSuit = ongoingSuit,
            isFirstTurnInGame=isFirstTurnInGame,
            showEligible=False
            )
        flag = True
        isFirstTurnInGame = False
        pygame.display.flip()
        print(config.IS_ANYTHING_MOVING)

if __name__ == '__main__':
    main()