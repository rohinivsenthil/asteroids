import math
import json

import pygame
from pygame.locals import *

from . import Bullet

with open('config.json') as configfile:
    config = json.load(configfile)['spaceship']


IMAGE_FILENAME = config['image']
SHOOT_SOUND_FILENAME = config['shootSound']
ACCELERATION = config['acceleration']
MAX_SPEED = config['maxSpeed']

spaceship_surface = pygame.image.load(IMAGE_FILENAME)


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

    def shoot(self):
        pygame.mixer.Sound(SHOOT_SOUND_FILENAME).play()
        return Bullet(self.angle, self.pos)

    def update(self):
        self.speed[0] *= 1 - (ACCELERATION / MAX_SPEED)
        self.speed[1] *= 1 - (ACCELERATION / MAX_SPEED)

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

        self.rect.center = self.pos