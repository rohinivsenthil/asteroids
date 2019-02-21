import pygame
from pygame.locals import *


def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")

    screen_size = (960, 720)
    screen = pygame.display.set_mode(screen_size)

    background = pygame.Color(0, 0, 0)

    exit = False

    while not exit:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit = True

        screen.fill(background)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
