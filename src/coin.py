from pygame.sprite import Sprite
import pygame
from config import *


class Coin(Sprite):

    def __init__(self, x, y, screen):
        super().__init__()
        self.x = x
        self.y = y
        self.screen = screen

        self.image_index = 0

        self.speed = 4

        self.images = []

        for number in range(1, 4):
            img = pygame.image.load(f'assets/images/coin_{number}.png')
            self.images.append(img)

        image = self.images[0]
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())

        self.image_index = 0
        self.coin_flip_timer = COIN_FLIP_DELAY

    def get_next_image(self):
        self.coin_flip_timer -= 1
        if self.coin_flip_timer == 0:
            self.coin_flip_timer = COIN_FLIP_DELAY
            self.image_index += 1
        if self.image_index == len(self.images):
            self.image_index = 0
        return self.images[self.image_index]

    def update(self):
        self.x -= self.speed
        image = self.get_next_image()

        self.rect.x = self.x
        if DEBUG_MODE:
            pygame.draw.rect(self.screen, RED, self.rect)

        self.screen.blit(image, (self.x, self.y))
