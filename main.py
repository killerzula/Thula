import pygame
import random
import time

import config
from utils import *
from player import Player
from computer import Computer

from pygame.locals import (
    K_ESCAPE,
    K_k,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption(config.WINDOW_CAPTION)
canvas = pygame.image.load('assets/canvas.png')

# font = pygame.font.Font(config.FONTFACE, config.FONT_SIZE) 
font = pygame.font.SysFont(config.FONTFACE, config.FONT_SIZE)

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


# def getInformation(player:Player):
#     return "Cards in Hand: {}\nThulas Received: {}\nThulas Bestowed: {}".format(
#             len(player.cards),
#             player.thulaReceived,
#             player.thulaGiven
#         )

getInformation = lambda x: "Cards in Hand: {}\nThulas Received: {}\nThulas Bestowed: {}".format(
                        len(x.cards),
                        x.thulaReceived,
                        x.thulaGiven
                    ) if x.id % 2 else "Cards in Hand: {}       Thulas Received: {}       Thulas Bestowed: {}".format(
                        len(x.cards),
                        x.thulaReceived,
                        x.thulaGiven
                    )

def main():
    
    index = firstPlayer
    highestCard = firstPlayer
    toggleInformation = True
    cardsInPlay = []
    playersInPlay = []
    ongoingSuit = None
    isFirstTurnInGame = True
    totalRounds = 0
    hasRendered = False
    hasGoneOffscreen = True
    shouldAllowNewCards = True
    thula = False
    pygame.init()
    clock.tick(config.FPS)
    text = []
    while True:

        screen.blit(canvas,(0,0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                if event.key == K_k:
                    toggleInformation = not toggleInformation

        if len(player0.cards) == 0:
            quit()

        if len(cardsInPlay) > 0:
            isEverythingStill = all([card.isStationary() for card in cardsInPlay])

        if not hasGoneOffscreen and isEverythingStill: # after round completion without thula
            # this condition and loop is inserted for removing cards only after they have moved to their destination
            for player in playersInPlay:
                players[player].cardThrownThisTurn.target = None
                if players[player].cardThrownThisTurn in players[player].cards: # if player has not run out of cards
                    players[player].cards.remove(players[player].cardThrownThisTurn)
            cardsInPlay = []
            playersInPlay = []
            hasRendered = False # allow for rendering after cards have been moved (causes issue without this after thula)
            hasGoneOffscreen = True

        if toggleInformation:
            for idx, player in enumerate(players): # get all the information that is to be displayed
                text = getInformation(player)
                blit_text(screen, text, config.TEXT_RECT[idx], font)

        if len(cardsInPlay) == 0:
            isEverythingStill = True 

        # glowEdge(screen=screen, playerID=index)
        if len(players[index].cards) != 0:
            if isEverythingStill and hasRendered and shouldAllowNewCards and hasGoneOffscreen:
                assert not index in playersInPlay, "Player {} has already played his turn".format(index)
                players[index].isTurn = True
                cardsInPlay.append(
                    players[index].getCard(ongoingSuit,isFirstTurnInGame)
                )
                isFirstTurnInGame = False
                assert not players[index].isTurn, "Player {} has not completed their turn yet.".format(index) 
                playersInPlay.append(index)
                players[index].cardThrownThisTurn.target = config.TARGET_RECT[index]
                shouldAllowNewCards = False

            # Draw it on the screen and do not do anything else until it has reached the target
            renderCards(screen=screen,decks=[player0.cards, player1.cards, player2.cards, player3.cards],ongoingSuit = ongoingSuit,isFirstTurnInGame=isFirstTurnInGame,showEligible = player0.id not in playersInPlay)
            hasRendered = True

            if len(cardsInPlay) > 1: # if this is not the first card that thrown
                isEverythingStill = all([card.isStationary() for card in cardsInPlay])
                if isEverythingStill and hasGoneOffscreen:
                    thula = isThula([
                        players[index].cardThrownThisTurn,
                        players[playersInPlay[-2]].cardThrownThisTurn
                    ])
                    if thula: # if there is a thula
                        pygame.time.wait(config.DELAY_AFTER_THULA)
                        for card in cardsInPlay:
                            card.target = config.DECK_RECT[highestCard]
                        players[highestCard].insertCards(cardsInPlay)
                        ongoingSuit = None
                        isEverythingStill = False
                        hasGoneOffscreen = False
                        index = highestCard
                        highestCard = None
                        shouldAllowNewCards = True

                    else: # if there's not a thula
                        highestCard = highestCard if players[highestCard].cardThrownThisTurn.rank > players[index].cardThrownThisTurn.rank else index
                        index = index + 1 if index != 3 else 0
                        shouldAllowNewCards = True

            if len(cardsInPlay) == 1 and isEverythingStill: # if this is the first card that's thrown just do the following things
                    ongoingSuit = cardsInPlay[0].suit
                    totalRounds += 1
                    highestCard = index
                    index = index + 1 if index != 3 else 0
                    shouldAllowNewCards = True

            if index in playersInPlay and isEverythingStill and not thula: # if not thula and round complete
                for player in playersInPlay:
                    players[player].cardThrownThisTurn.target = config.OFFSCREEN_RECT
                highestCard = highestCard if players[highestCard].cardThrownThisTurn.rank > players[index].cardThrownThisTurn.rank else index
                index = highestCard
                ongoingSuit = None
                hasGoneOffscreen = False
                shouldAllowNewCards = True
                pygame.time.wait(config.DELAY_AFTER_ROUND_NO_THULA)

        else:
            # if current player has no cards just pass the turn
            index = index + 1 if index != 3 else 0

        pygame.display.flip()

if __name__ == '__main__':
    main()
