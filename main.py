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
    hasRendered = False
    hasGoneOffscreen = True
    shouldAllowNewCards = True
    pygame.init()
    clock.tick(config.FPS)
    
    while True:

        screen.blit(canvas,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
        
        print(config.IS_ANYTHING_MOVING)

        # Get the card
        # Allow getting card only if no card is moving 

        if len(cardsInPlay) > 0:
            isEverythingStill = all([card.isStationary() for card in cardsInPlay])

        if not hasGoneOffscreen and isEverythingStill:
            cardsInPlay = []
            hasGoneOffscreen = True

        if len(cardsInPlay) == 0:
            isEverythingStill = True 

        if isEverythingStill and hasRendered and shouldAllowNewCards and hasGoneOffscreen:
            
            players[index].isTurn = True
            cardsInPlay.append(
                players[index].getCard(ongoingSuit,isFirstTurnInGame)
            )
            isFirstTurnInGame = False
            assert not players[index].isTurn, "Player {} has not completed their turn yet.".format(index) 
            playersInPlay.append(index)
            players[index].cardThrownThisTurn.target = config.TARGET_RECT[index]
            prevIndex = index
            shouldAllowNewCards = False
            # index = index + 1 if index != 3 else 0

        # Draw it on the screen and do not do anything else until it has reached the target
        renderCards(screen=screen,decks=[player0.cards, player1.cards, player2.cards, player3.cards],ongoingSuit = ongoingSuit,isFirstTurnInGame=isFirstTurnInGame,showEligible = player0.id not in playersInPlay)
        hasRendered = True

        if len(cardsInPlay) > 1: # if this is not the first card that thrown
            isEverythingStill = all([card.isStationary() for card in cardsInPlay])
            if isEverythingStill:
                thula = isThula([
                    players[index].cardThrownThisTurn,
                    players[prevIndex].cardThrownThisTurn
                ])
                if thula: # if there is a thula
                    for player in playersInPlay:
                        players[player].cards.remove(players[player].cardThrownThisTurn)
                    for card in cardsInPlay:
                        card.target = config.DECK_RECT[highestCard]
                    players[highestCard].insert(cardsInPlay)
                    
                    cardsInPlay = []
                    playersInPlay = []
                    # prevIndex = None
                    index = highestCard
                    highestCard = None
                    shouldAllowNewCards = True

                else: # if there's not a thula
                    # prevIndex = index
                    highestCard = highestCard if players[highestCard].cardThrownThisTurn.rank > players[index].cardThrownThisTurn.rank else index
                    index = index + 1 if index != 3 else 0
                    shouldAllowNewCards = True

        if len(cardsInPlay) == 1 and isEverythingStill: # if this is the first card that's thrown just do the following things
                # prevIndex = 
                ongoingSuit = cardsInPlay[0].suit
                totalRounds += 1
                index = index + 1 if index != 3 else 0
                highestCard = index
                shouldAllowNewCards = True

        if len(cardsInPlay) == 4 and isEverythingStill: # if not thula and round complete
            for player in playersInPlay:
                players[player].cardThrownThisTurn.target = config.OFFSCREEN_RECT
                # cardsInPlay = []
                playersInPlay = []
            hasGoneOffscreen = False
            shouldAllowNewCards = True

        pygame.display.flip()

        print(config.IS_ANYTHING_MOVING)


if __name__ == '__main__':
    main()