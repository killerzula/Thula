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


def getInformation(player:Player):
    return "Cards in Hand: {}\nThulas Received: {}\nThulas Bestowed: {}".format(
            len(player.cards),
            player.thulaReceived,
            player.thulaGiven
        )

getInformation = lambda x: "Cards in Hand: {}\nThulas Received: {}\nThulas Bestowed: {}".format(
                        len(x.cards),
                        x.thulaReceived,
                        x.thulaGiven
                    )

# getIndexBeforeProteus = lambda x: len(x)-1 if players[x].cardThrownThisTurn.suit != 'PROTEAN' else getIndexBeforeProteus(x[:-1])


def main():
    
    index = firstPlayer
    highestCard = firstPlayer

    hasProteusVisited = False
    cardsInPlay = []
    playersInPlay = []
    ongoingSuit = None
    isFirstTurnInGame = True
    totalRounds = 0
    hasRendered = False
    hasGoneOffscreen = True
    shouldAllowNewCards = True
    cardThisTurn = None
    text = []

    def getIndexBeforeProteus(playersInPlay:list):
        if not hasProteusVisited:
            return playersInPlay[-2]
        else:
            if playersInPlay[-1].suit == 'PROTEAN':
                return playersInPlay[-1] 
            else:
                getIndexBeforeProteus(playersInPlay[0:-1])

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

        if len(player0.cards) == 0:
            quit()

        # Get the card
        # Allow getting card only if no card is moving 

        if hasProteusVisited:
            cardThisTurn.update()

        if len(cardsInPlay) > 0:
            isEverythingStill = all([card.isStationary() for card in cardsInPlay])

        if not hasGoneOffscreen and isEverythingStill: # after round completion without thula
            # this condition and loop is inserted for removing cards only after they have moved to their destination
            for player in playersInPlay:
                players[player].cardThrownThisTurn.target = None
                if players[player].cardThrownThisTurn: # if player has not run out of cards
                    players[player].cards.remove(players[player].cardThrownThisTurn)
            cardsInPlay = []
            playersInPlay = []
            hasRendered = False # allow for rendering after cards have been moved (causes issue without this after thula)
            hasGoneOffscreen = True

        for idx, player in enumerate(players): # get all the information that is to be displayed
            text = getInformation(player)
            blit_text(screen, text, config.TEXT_RECT[idx], font)

        if len(cardsInPlay) == 0:
            isEverythingStill = True 

        # glowEdge(screen=screen, playerID=index)
        if isEverythingStill and hasRendered and shouldAllowNewCards and hasGoneOffscreen:
            
            players[index].isTurn = True
            cardThisTurn = players[index].getCard(ongoingSuit,isFirstTurnInGame)
            cardsInPlay.append(cardThisTurn)
            isFirstTurnInGame = False
            assert not players[index].isTurn, "Player {} has not completed their turn yet.".format(index) 
            playersInPlay.append(index)
            players[index].cardThrownThisTurn.target = config.TARGET_RECT[index]
            shouldAllowNewCards = False
            if cardsInPlay[-1].suit == 'PROTEAN':
                hasProteusVisited = True
                shouldAllowNewCards = True
                if len(cardsInPlay) == 1:
                    ongoingSuit = None

        # Draw it on the screen and do not do anything else until it has reached the target
        renderCards(screen=screen,decks=[player0.cards, player1.cards, player2.cards, player3.cards],ongoingSuit = ongoingSuit,isFirstTurnInGame=isFirstTurnInGame,showEligible = player0.id not in playersInPlay)
        hasRendered = True

        if (len(cardsInPlay) > 1 and not hasProteusVisited) or (len(cardsInPlay)> 2 and hasProteusVisited): # if this is not the first card that thrown
            isEverythingStill = all([card.isStationary() for card in cardsInPlay])
            if isEverythingStill and hasGoneOffscreen:
                assert not players[index].cardThrownThisTurn.suit == 'PROTEAN', "Proteus is not happy..." 
                thula = isThula([
                    players[index].cardThrownThisTurn,
                    players[getIndexBeforeProteus(playersInPlay)].cardThrownThisTurn
                ])
                if thula: # if there is a thula
                    pygame.time.wait(config.DELAY_AFTER_THULA)
                    for card in cardsInPlay:
                        card.target = config.DECK_RECT[highestCard]
                    players[highestCard].insertCards(cardsInPlay)
                    ongoingSuit = None
                    isEverythingStill = False
                    hasGoneOffscreen = False
                    hasProteusVisited = False
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

        if len(cardsInPlay) == 4 and isEverythingStill and not thula: # if not thula and round complete
            for player in playersInPlay:
                players[player].cardThrownThisTurn.target = config.OFFSCREEN_RECT
            highestCard = highestCard if players[highestCard].cardThrownThisTurn.rank > players[index].cardThrownThisTurn.rank else index
            index = highestCard
            ongoingSuit = None
            hasGoneOffscreen = False
            hasProteusVisited = False
            shouldAllowNewCards = True
            pygame.time.wait(config.DELAY_AFTER_ROUND_NO_THULA)

        pygame.display.flip()

if __name__ == '__main__':
    main()
