import pygame
from pygame.locals import *
from spaceship import Spaceship


def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")

    screen_size = (960, 720)
    screen = pygame.display.set_mode(screen_size)

    background = pygame.Color(0, 0, 0)

    all_sprites = pygame.sprite.Group()

    player = Spaceship((screen_size[0] // 2, screen_size[1] // 2))
    all_sprites.add(player)

    clock = pygame.time.Clock()

    exit = False

    while not exit:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit = True

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            player.rotate(-2)
        if keys[K_RIGHT]:
            player.rotate(2)

        if keys[K_UP]:
            player.accelerate()

        all_sprites.update()

        screen.fill(background)
        all_sprites.draw(screen)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
