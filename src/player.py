from pygame.sprite import Sprite
import pygame
from config import *


class Player(Sprite):

    def __init__(self, x, y, size, screen, flappy_duck_game):
        super().__init__()
        self.x = x
        self.y = y
        self.screen = screen
        self.flappy_duck_game = flappy_duck_game

        self.images = []

        for idx in range(1, 3):
            img = pygame.image.load(f'assets/images/Green duck #{idx}-01.png')
            img = pygame.transform.scale(img, (size, size))
            self.images.append(img)

        self.dizzy_image = pygame.image.load('assets/images/Green duck #5-01.png')
        self.dizzy_image = pygame.transform.scale(self.dizzy_image,(size, size))

        self.image_index = 0
        self.player_flap_timer = PLAYER_FLAP_DELAY

        self.fall_speed = 0

        self.mode = FLYING_MODE

        image = self.images[0]
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())

    def player_hit_tube(self):
        self.mode = DIZZY_MODE

    def get_next_image(self):
        self.player_flap_timer -= 1
        if self.player_flap_timer == 0:
            self.player_flap_timer = PLAYER_FLAP_DELAY
            self.image_index += 1
            if self.image_index == len(self.images):
                self.image_index = 0
        return self.images[self.image_index]

    def update(self):
        self.fall_speed += GRAVITY

        if self.mode == FLYING_MODE:
            image = self.get_next_image()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                self.fall_speed = -5
        else:
            image = self.dizzy_image

        if self.y > HEIGHT:
            self.kill()
            self.flappy_duck_game.mode = GAME_OVER

        self.y += self.fall_speed

        self.rect.x = self.x
        self.rect.y = self.y
        if DEBUG_MODE:
            pygame.draw.rect(self.screen, RED, self.rect)

        self.screen.blit(image, (self.x, self.y))
