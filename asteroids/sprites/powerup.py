import json
import math
import random

import pygame
from pygame.locals import *

with open('config.json') as configfile:
    config = json.load(configfile)['powerup']

SPEED = config['speed']
TIME = config['time']
POWERUPS = config['powerups']


class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        r = random.random()
        s = 0

        self.time = 0

        self.name = ''
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(0, 0))

        name=random.choice(list(POWERUPS.keys()))
        value=POWERUPS[name]
        s = value['generation']
        if r < s:
            self.name = name
            self.image = pygame.image.load(value['image'])
            self.rect = self.image.get_rect(center=pos)
            self.mask = pygame.mask.from_surface(self.image)
        if r > s:
            self.kill()

        self.pos = list(pos)

        angle = random.uniform(0, math.pi * 2)
        self.speed = [math.sin(angle) * SPEED, -math.cos(angle) * SPEED]

        self.elapsed = 0

    def update(self):
        if self.time > TIME:
            self.kill()

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

        self.rect.center = self.pos
