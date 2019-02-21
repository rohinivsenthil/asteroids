import math
import json

import pygame
from pygame.locals import *


with open('config.json') as configfile:
    config = json.load(configfile)['spaceship']

ACCELERATION = config['acceleration']
MAX_SPEED = config['maxSpeed']


spaceship_surface = pygame.Surface((30, 30), SRCALPHA, 32)
pygame.draw.polygon(
    spaceship_surface,
    pygame.Color(0, 0, 255),
    [(0, 30), (15, 0), (30, 30), (15, 20)],
    2
)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = spaceship_surface
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.angle = 0

        self.pos = list(pos)
        self.speed = [0, 0]

    def accelerate(self):
        self.speed[0] += ACCELERATION * math.sin(math.radians(self.angle))
        self.speed[1] += ACCELERATION * -math.cos(math.radians(self.angle))

    def rotate(self, angle):
        self.angle += angle

        self.image = pygame.transform.rotate(spaceship_surface, -self.angle)

        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.speed[0] *= 1 - (ACCELERATION / MAX_SPEED)
        self.speed[1] *= 1 - (ACCELERATION / MAX_SPEED)

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

        self.rect.center = self.pos

