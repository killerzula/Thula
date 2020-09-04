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
    
    index = 0
    prevIndex = firstPlayer
    highestCard = firstPlayer

    cardsInPlay = []
    playersInPlay = []
    ongoingSuit = None
    isFirstTurnInGame = True
    totalRounds = 0
    hasRendered = False
    skipForLastPlayer = False
    pygame.init()
    clock.tick(config.FPS)
    
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

        if not config.IS_ANYTHING_MOVING and hasRendered:
            
            players[index].isTurn = True
            isFirstTurnInGame = False
            cardsInPlay.append(
                players[index].getCard(ongoingSuit,isFirstTurnInGame)
            )
            players[index].isTurn = False
            players[index].cardThrownThisTurn.target = config.TARGET_RECT[index]

            index = index + 1 if index != 3 else 0

            if index == 0:
                for card in cardsInPlay:
                    card.target = config.OFFSCREEN_RECT

        renderCards(
            screen=screen,
            decks=[player0.cards, player1.cards, player2.cards, player3.cards], # deck order is important
            ongoingSuit = ongoingSuit,
            isFirstTurnInGame=isFirstTurnInGame,
            showEligible = player0.id not in playersInPlay 
            )

        hasRendered = True
        
        pygame.display.flip()

        print(config.IS_ANYTHING_MOVING)


if __name__ == '__main__':
    main()