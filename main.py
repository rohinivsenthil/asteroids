import pygame


def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")

    screen_size = (960, 720)
    screen = pygame.display.set_mode(screen_size)

    exit = False

    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

    pygame.quit()


if __name__ == '__main__':
    main()
