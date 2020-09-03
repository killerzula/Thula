import pygame
import os 

from constraints import CARD_HEIGHT, CARD_WIDTH

folderPath = 'assets/cards'

class Card(pygame.sprite.Sprite):
    def __init__(self, image, position, rank, suit):
        super(Card, self).__init__()
        self.surf = pygame.transform.smoothscale(
                        pygame.image.load(image), 
                        (CARD_WIDTH, CARD_HEIGHT)
                    )
        self.rect = self.surf.get_rect(topleft = position)
        self.rank = rank
        self.suit = suit

    # def updatePosition(self, position: tuple):
    #     offset = (
    #         self.rect[0] - position[0],
    #         self.rect[1] - position[1]
    #     )
    #     self.rect.move_ip(offset)
    def updatePosition(self, position: tuple):
        self.rect.move_ip(position)

    def getCenter(self):
        return (
            int(self.rect[0] + (CARD_WIDTH  / 2)),
            int(self.rect[1] + (CARD_HEIGHT / 2))
        )