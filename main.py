import json

import pygame
from pygame.locals import *
from spaceship import Spaceship


with open('config.json') as configfile:
    config = json.load(configfile)

SCREEN_SIZE = config['screenSize']


def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")

    screen = pygame.display.set_mode(SCREEN_SIZE)

    background = pygame.Color(0, 0, 0)

    all_sprites = pygame.sprite.Group()

    player = Spaceship((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
    all_sprites.add(player)

    clock = pygame.time.Clock()

    exit = False

    while not exit:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit = True

            if (event.type == KEYDOWN) and (event.key == K_SPACE):
                all_sprites.add(player.shoot())

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            player.rotate(-2)
        if keys[K_RIGHT]:
            player.rotate(2)

        if keys[K_UP]:
            player.accelerate()

        player.pos[0] %= SCREEN_SIZE[0]
        player.pos[1] %= SCREEN_SIZE[1]

        all_sprites.update()

        screen.fill(background)
        all_sprites.draw(screen)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
