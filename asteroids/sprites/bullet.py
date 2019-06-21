import json
import math

import pygame
from pygame.locals import *

with open('config.json') as configfile:
    config = json.load(configfile)['bullet']

IMAGE_FILENAME = config['image']
SPEED = config['speed']
MAX_DIST = config['maxDist']

bullet_surface = pygame.image.load(IMAGE_FILENAME)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, pos):
        super().__init__()

        self.image = pygame.transform.rotate(bullet_surface, -angle)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = list(pos)
        self.dist = 0

        self.speed = [
            math.sin(math.radians(angle)) * SPEED,
            -math.cos(math.radians(angle)) * SPEED
        ]

    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.dist += SPEED

        if self.dist > MAX_DIST:
            self.kill()

        self.rect.center = self.pos
