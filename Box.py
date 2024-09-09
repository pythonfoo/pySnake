try:
    import pygame_sdl2 as pygame
except ImportError:
    import pygame

import conf


class Box(object):
    def __init__(self, screen, blockSize, x, y, bType='body'):
        self.screen = screen
        self.blockSize = blockSize
        self.direction = 2
        self.bType = bType
        self.x = x
        self.y = y
        self.color = conf.SNAKE_COLOR
        self.back = None
        self.directionChanged = 0

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        # self.directionChanged = 1
        self.direction = direction

    def update(self):
        if self.direction == 1:
            self.y -= 1
        elif self.direction == 2:
            self.x += 1
        elif self.direction == 3:
            self.y += 1
        elif self.direction == 4:
            self.x -= 1

    def blit(self):
        relX = self.x * self.blockSize
        relY = self.y * self.blockSize
        pygame.draw.rect(self.screen, self.color, (relX, relY, self.blockSize, self.blockSize))
        if self.back is not None:
            self.back.setDirection(self.direction)
