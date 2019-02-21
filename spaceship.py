import math
import pygame
from pygame.locals import *


ACCELERATION = 0.15


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

    def accelerate(self):
        self.speed[0] += ACCELERATION * math.sin(math.radians(self.angle))
        self.speed[1] += ACCELERATION * -math.cos(math.radians(self.angle))

    def rotate(self, angle):
        self.angle += angle

        self.image = pygame.transform.rotate(spaceship_surface, -self.angle)

        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

        self.mask = pygame.mask.from_surface(self.image)

