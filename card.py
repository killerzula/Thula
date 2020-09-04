###################################################################################
###################################################################################
# Sprite Movement Towards Target Example
# programed/documented by Mad Cloud Games
# contact Mad Cloud Games @ madcloudgames@gmail.com with any comments, questions, or changes
#
# This project is released under the GNU General Public License V3
# This code is open source
# We would love to know what it gets used for
###################################################################################
###################################################################################

import pygame, math
import config

from pygame.locals import *


pygame.init()

class Vector():
    '''
        Class:
            creates operations to handle vectors such
            as direction, position, and speed
        '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self): # used for printing vectors
        return "(%s, %s)"%(self.x, self.y)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("This "+str(key)+" key is not a vector key!")

    def __sub__(self, o): # subtraction
        return Vector(self.x - o.x, self.y - o.y)

    def length(self): # get length (used for normalize)
        return math.sqrt((self.x**2 + self.y**2)) 

    def normalize(self): # divides a vector by its length
        l = self.length()
        if l != 0:
            return (self.x / l, self.y / l)
        return None


class Card(pygame.sprite.Sprite):
    
    def __init__(self,image,rank,suit):
        '''
        Class:
            creates a Card sprite
        Parameters:
            - self, image, rank, suite
        '''
        super(Card,self).__init__()
        self.surf = pygame.transform.smoothscale(
                        pygame.image.load(image).convert_alpha(), 
                        (config.CARD_WIDTH, config.CARD_HEIGHT)
                    ) # load image
        self.rect = self.surf.get_rect()

        self.trueX = -100 # created because self.rect.center does not hold
        self.trueY = -100 # decimal values but these do
        self.rect.center = (self.trueX, self.trueY) # set starting position
        self.speed = 20 # movement speed of the sprite
        self.speedX = 0 # speed in x direction
        self.speedY = 0 # speed in y direction
        self.hasReachedTarget = False
        self.target = None # starts off with no target

        self.rank = rank
        self.suit = suit

    def get_direction(self, target):
        '''
        Function:
            takes total distance from sprite.center
            to the sprites target
            (gets direction to move)
        Returns:
            a normalized vector
        Parameters:
            - self
            - target
                x,y coordinates of the sprites target
                can be any x,y coorinate pair in
                brackets [x,y]
                or parentheses (x,y)
        '''
        if self.target: # if the square has a target
            position = Vector(self.rect.centerx, self.rect.centery) # create a vector from center x,y value
            target = Vector(target[0], target[1]) # and one from the target x,y
            self.dist = target - position # get total distance between target and position

            direction = self.dist.normalize() # normalize so its constant in all directions
            return direction
        
    def distance_check(self, dist):
        '''
        Function:
            tests if the total distance from the
            sprite to the target is smaller than the
            ammount of distance that would be normal
            for the sprite to travel
            (this lets the sprite know if it needs
            to slow down. we want it to slow
            down before it gets to it's target)
        Returns:
            bool
        Parameters:
            - self
            - dist
                this is the total distance from the
                sprite to the target
                can be any x,y value pair in
                brackets [x,y]
                or parentheses (x,y)
        '''
        dist_x = dist[0] ** 2 # gets absolute value of the x distance
        dist_y = dist[1] ** 2 # gets absolute value of the y distance
        t_dist = dist_x + dist_y # gets total absolute value distance
        speed = self.speed ** 2 # gets aboslute value of the speed

        if t_dist < (speed): # read function description above
            return True
        

    def update(self):
        '''
        Function:
            gets direction to move then applies
            the distance to the sprite.center
            ()
        Parameters:
            - self
        '''
        
        self.dir = self.get_direction(self.target) # get direction
        if self.dir: # if there is a direction to move
            if self.distance_check(self.dist): # if we need to stop
                self.rect.center = self.target # center the sprite on the target
            else: # if we need to move normal
                self.trueX += (self.dir[0] * self.speed) # calculate speed from direction to move and speed constant
                self.trueY += (self.dir[1] * self.speed)
                self.rect.center = (round(self.trueX),round(self.trueY)) # apply values to sprite.center
        else:
            self.hasReachedTarget = True

    def isStationary(self):
        return self.get_direction(self.target) == None

def main():

    screen = pygame.display.set_mode((1100,600))
    pygame.display.set_caption("Sprite Movement Towards Target Example - Mad Cloud Games")
    background_color = pygame.Surface(screen.get_size()).convert()
    background_color.fill((240,50,0))
    
    sprite = Card(image='assets/cards/2_of_hearts.png',rank=2, suit='HEARTS') # create the sprite

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == MOUSEBUTTONDOWN:
                sprite.target = event.pos # set the sprite.target to the mouse click position

        screen.blit(background_color, (0,0))
        
        sprite.update() # update the sprite
        screen.blit(sprite.surf, sprite.rect.topleft) # blit the sprite to the screen

        pygame.display.flip()
    
    pygame.quit() # for a smooth quit
if __name__ == "__main__":
    main()