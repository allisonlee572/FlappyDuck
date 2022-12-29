import pygame
from pygame.sprite import Sprite
from config import *


class Tube(Sprite):

    def __init__(self, x, tube_height, mode, screen):
        super().__init__()
        self.x = x
        self.tube_height = tube_height
        self.screen = screen

        self.image = pygame.image.load(f'assets/images/Downward_Tube_2.png')

        self.y = tube_height - self.image.get_height()

        if mode == TUBE_UP:
            self.image = pygame.transform.flip(self.image, False, True)
            self.y = HEIGHT - tube_height

        self.speed = 4

        self.rect = pygame.Rect(x, self.y, self.image.get_width(), self.image.get_height())

    def update(self):
        self.x -= self.speed

        self.rect.x = self.x
        self.rect.y = self.y
        if DEBUG_MODE:
            pygame.draw.rect(self.screen, RED, self.rect)

        self.screen.blit(self.image, (self.x, self.y))

