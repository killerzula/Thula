import pygame
import os
import random
import math
import sys

# from card import Card, FOLDER_PATH, CARD_HEIGHT, CARD_WIDTH
from card import Card
import config


def sortCards(cards: list):
    order = ['SPADES', 'HEARTS', 'CLUBS', 'DIAMONDS']
    order = {key: i for i, key in enumerate(order)}
    cards = sorted(cards, key=lambda k: k.rank, reverse=True)  # sort by rank
    # sort by suit by order specified by list 'order'
    cards = sorted(cards, key=lambda d: order[d.suit])
    # see: https://stackoverflow.com/a/34308981
    return cards


def createDeck():
    merged = []
    images = [file_ for file_ in os.listdir(
        config.FOLDER_PATH) if os.path.isfile(os.path.join(config.FOLDER_PATH, file_))]
    for image in images:
        rank, _, suit = os.path.splitext(image)[0].split('_')
        image = os.path.join(config.FOLDER_PATH, image)

        if rank == 'jack':
            rank = 11
        elif rank == 'queen':
            rank = 12
        elif rank == 'king':
            rank = 13
        elif rank == 'ace':
            rank = 14

        merged.append(
            Card(image=image,
                 rank=int(rank), suit=suit.upper())
        )
    return merged


def renderCards(screen:pygame.Surface, decks:list, ongoingSuit:str, isFirstTurnInGame:bool):

    # left, top, width, height
    # The above order is used for rect, see http://www.pygame.org/docs/ref/rect.html
    # for deck in decks:
        # if not all([card.hasReachedTarget for card in deck])

    checkIfStationary = []
    for deck in decks:
        checkIfStationary += [card.isStationary for card in deck]
    
    global config
    config.IS_ANYTHING_MOVING = not all(checkIfStationary)
    del checkIfStationary

    margin = lambda cardCount: (config.SCREEN_WIDTH - ((cardCount - 1) * config.CARD_DRAW_OFFSET + config.CARD_WIDTH)) // 2
    for playerID, deck in enumerate(decks):
        inDeck = []
        mobile = []
        for card in deck:
            if not card.target:
                inDeck.append(card)
            else:
                mobile.append(card)

        if len(inDeck) == 0:
            # TODO: Do something about this
            pass
        for index, card in enumerate(inDeck):
            if isFirstTurnInGame:
                eligible = card.suit == 'SPADES' and card.rank == 14
            else:
                if not ongoingSuit:
                    eligible = True
                else:
                    eligible = card.suit == ongoingSuit
            if eligible:
                top = config.SCREEN_HEIGHT - config.CARD_HEIGHT - config.CARD_DRAW_PADDING_BOTTOM - config.ELIGIBLE_CARD_HEIGHT_OFFSET
            else:
                top = config.SCREEN_HEIGHT - config.CARD_HEIGHT - config.CARD_DRAW_PADDING_BOTTOM
            height = config.CARD_HEIGHT
            width = config.CARD_DRAW_OFFSET
            if index == 0:
                left = margin(len(inDeck))
            elif index == len(inDeck) - 1:
                left = left + config.CARD_DRAW_OFFSET
                width = config.CARD_WIDTH
            else:
                left = left + config.CARD_DRAW_OFFSET
            card.trueX = left + (width // 2)
            card.trueY = top + (height // 2)
            # card.trueX = DECK_RECT[playerID][0]
            # card.trueY = DECK_RECT[playerID][1]
            if playerID != 0:
                continue
            else:
                card.rect = pygame.Rect((left, top, width, height))
                screen.blit(card.surf, card.rect.topleft)

        for card in mobile:
            card.hasBeenMobile = True
            card.update()
            screen.blit(card.surf,card.rect.topleft) 

def quit():
    pygame.quit()
    sys.exit()


def glowEdge(screen,player):
    
    # Rect(left, top, width, height) -> Rect

    if player == 0:
        rect = (
            0,
            config.SCREEN_HEIGHT - config.GLOW_THICKNESS,
            config.SCREEN_WIDTH,
            config.GLOW_THICKNESS
            )
    elif player == 1:
        rect = (
            0,
            0,
            config.GLOW_THICKNESS,
            config.SCREEN_HEIGHT
        )
    elif player == 2:
        rect = (
            0,
            0,
            config.SCREEN_WIDTH,
            config.GLOW_THICKNESS
        )
    else:
        rect = (
            config.SCREEN_WIDTH - config.GLOW_THICKNESS,
            0,
            config.GLOW_THICKNESS,
            config.SCREEN_HEIGHT
        )
    pygame.draw.rect(screen,config.GLOW_COLOR,rect)


def isThula(cards:list):
    assert len(cards) == 2, "Cards provided for thula check must be only 2"
    return cards[0].suit != cards[1].suit
