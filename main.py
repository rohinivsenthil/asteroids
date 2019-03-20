import json
import random

import pygame
from pygame.locals import *

from asteroid import Asteroid
from spaceship import Spaceship

with open('config.json') as configfile:
    config = json.load(configfile)

SCREEN_SIZE = config['screenSize']
FRAMERATE = config['framerate']


def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")

    screen = pygame.display.set_mode(SCREEN_SIZE)

    background = pygame.Color(0, 0, 0)

    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Spaceship((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
    all_sprites.add(player)

    if random.uniform(0, sum(SCREEN_SIZE)) < SCREEN_SIZE[0]:
        t = random.randint(0, 2 * SCREEN_SIZE[0])
        pos = (t % SCREEN_SIZE[0], SCREEN_SIZE[1] if t > SCREEN_SIZE[0] else 0)
    else:
        t = random.randint(0, 2 * SCREEN_SIZE[1])
        pos = (t % SCREEN_SIZE[1], SCREEN_SIZE[0] if t > SCREEN_SIZE[1] else 0)

    speed = (random.uniform(1, 2), random.uniform(1, 2))
    asteroid = Asteroid(50, speed, pos)
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

    clock = pygame.time.Clock()

    exit = False

    while not exit:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit = True

            if (event.type == KEYDOWN) and (event.key == K_SPACE):
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullets.add(bullet)

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            player.rotate(-2)
        if keys[K_RIGHT]:
            player.rotate(2)

        if keys[K_UP]:
            player.accelerate()

        for sprite in all_sprites:
            sprite.pos[0] %= SCREEN_SIZE[0]
            sprite.pos[1] %= SCREEN_SIZE[1]

        collide_list = pygame.sprite.groupcollide(asteroids, bullets, True, True, pygame.sprite.collide_mask)
        for collision in collide_list.items():
                print(collision)

        all_sprites.update()

        screen.fill(background)
        all_sprites.draw(screen)

        pygame.display.update()

        clock.tick(FRAMERATE)

    pygame.quit()


if __name__ == '__main__':
    main()
