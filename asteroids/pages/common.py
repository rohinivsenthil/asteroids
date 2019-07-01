import json

import pygame
from pygame.locals import *

from ..sprites import Powerup

with open("config.json") as configfile:
    config = json.load(configfile)

SHOOT_SOUND_FILENAME = config["game"]["shootSound"]
BACKGROUND = pygame.image.load(config["game"]["background"])


def get_actions():
    actions = {
        "accelerate": False,
        "recelerate": False,
        "stop": False,
        "die": False,
        "left": False,
        "pause": False,
        "quit": False,
        "right": False,
        "fire": False,
    }

    for event in pygame.event.get():
        if event.type == QUIT:
            actions["quit"] = True

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                actions["fire"] = True
            if event.key == K_p:
                actions["pause"] = True
            if event.key == K_UP:
                actions["accelerate"] = True
            if event.key == K_DOWN:
                actions["recelerate"] = True
        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_DOWN:
                actions["accelerate"] = False
                actions["recelerate"] = False
                actions["stop"] = True

    keys = pygame.key.get_pressed()

    if keys[K_q]:
        actions["die"] = True
    # if keys[K_UP]:
    #     actions['accelerate'] = True
    if keys[K_LEFT]:
        actions["left"] = True
    if keys[K_RIGHT]:
        actions["right"] = True

    return actions


def collide_asteroids_bullets(asteroids, bullets, powerups, all_sprites):
    score = 0
    collide_list = pygame.sprite.groupcollide(asteroids, bullets, True, True,
                                              pygame.sprite.collide_mask)

    for asteroid in collide_list:
        score += 10
        for i in asteroid.split():
            if isinstance(i, Powerup):
                powerups.add(i)
            else:
                asteroids.add(i)

            all_sprites.add(i)

    return score


def do_actions(actions, all_sprites, bullets, player):
    if actions["fire"]:
        pygame.mixer.Sound(SHOOT_SOUND_FILENAME).play()
        bullet = player.shoot()
        bullets.add(bullet)
        all_sprites.add(bullet)

    if actions["left"]:
        player.rotate(-2)
    if actions["right"]:
        player.rotate(2)

    if actions["accelerate"]:
        player.accelerate()
    if actions["recelerate"]:
        player.recelerate()

    if actions["stop"]:
        player.stop()


def draw(sprites, screen):
    screen.blit(BACKGROUND, (0, 0))
    sprites.draw(screen)
