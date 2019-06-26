import json
import random

import pygame
from pygame.locals import *

from .pages import game

with open("config.json") as configfile:
    config = json.load(configfile)

SCREEN_SIZE = config["screenSize"]
FRAMERATE = config["framerate"]


def main():
    pygame.mixer.pre_init(buffer=1024)
    pygame.init()
    pygame.display.set_caption("Asteroids")

    screen = pygame.display.set_mode(SCREEN_SIZE)

    exit = False

    while not exit:
        score, time_played, exit = game(screen)

    pygame.quit()


if __name__ == "__main__":
    main()
