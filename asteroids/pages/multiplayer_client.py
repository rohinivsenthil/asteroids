import json
import random
import socket

import pygame
from pygame.locals import *

from ..sprites import AlternativeSpaceship, Asteroid, Spaceship
from .common import collide_asteroids_bullets, do_actions, get_actions, draw

with open("config.json") as configfile:
    config = json.load(configfile)

FRAMERATE = config["framerate"]
SCREEN_SIZE = config["screenSize"]
SHIP_EXPLOSION_SOUND_FILENAME = config["game"]["shipExplodeSound"]
SHOOT_SOUND_FILENAME = config["game"]["shootSound"]
ASTEROID_GENERATION = config["asteroid"]["generation"]
SHIELD_EFFECT = pygame.image.load(config["powerup"]["powerups"]["shield"]["effect"])

GREEN = (0, 255, 0)


def generate_asteroid(size):
    if random.uniform(0, sum(SCREEN_SIZE)) < SCREEN_SIZE[0]:
        t = random.randint(0, 2 * SCREEN_SIZE[0])
        pos = (t % SCREEN_SIZE[0], SCREEN_SIZE[1] if t > SCREEN_SIZE[0] else 0)
    else:
        t = random.randint(0, 2 * SCREEN_SIZE[1])
        pos = (SCREEN_SIZE[0] if t > SCREEN_SIZE[1] else 0, t % SCREEN_SIZE[1])

    speed = (random.uniform(1, 2), random.uniform(1, 2))
    asteroid = Asteroid(size, speed, pos)

    return asteroid


def multiplayer_client(screen):
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    last_asteroid = 0

    player1 = Spaceship((SCREEN_SIZE[0] // 4, SCREEN_SIZE[1] // 2))
    bullets1 = pygame.sprite.Group()
    extra1 = False
    score1 = 0
    dead1 = False

    player2 = AlternativeSpaceship(
        ((SCREEN_SIZE[0] * 3) // 4, SCREEN_SIZE[1] // 2))
    bullets2 = pygame.sprite.Group()
    extra2 = False
    score2 = 0
    dead2 = False

    all_sprites.add(player1)
    all_sprites.add(player2)

    score_text = pygame.font.SysFont("Monotype Corsiva", 20)
    time_played = 0

    paused = False
    exit = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 3000))
        while not (dead1 and dead2):
            actions2 = get_actions()
            s.sendall(json.dumps(actions2).encode('ascii'))
            actions1 = json.loads(s.recv(1024))

            if actions2["quit"]:
                exit = True
                break

            if actions1["die"]:
                dead1 = True
                player1.kill()
            if actions2["die"]:
                dead2 = True
                player2.kill()

            paused ^= actions2["pause"]

            if not paused:
                do_actions(actions1, all_sprites, bullets1, player1)
                do_actions(actions2, all_sprites, bullets2, player2)

                #if last_asteroid == ASTEROID_GENERATION:
                #    last_asteroid = 0
                #    asteroid = generate_asteroid(
                #        random.randint(
                #            config["asteroid"]["minRadius"],
                #            config["asteroid"]["maxRadius"],
                #        ))
                #    asteroids.add(asteroid)
                #    all_sprites.add(asteroid)

                for sprite in all_sprites:
                    sprite.pos[0] %= SCREEN_SIZE[0]
                    sprite.pos[1] %= SCREEN_SIZE[1]

                score1 += collide_asteroids_bullets(
                    asteroids, bullets1, powerups, all_sprites)
                score2 += collide_asteroids_bullets(
                    asteroids, bullets2, powerups, all_sprites)

                collide_list = pygame.sprite.spritecollide(
                    player1, powerups, True, pygame.sprite.collide_mask)
                for powerup in collide_list:
                    if powerup.name == "bomb":
                        sprites = asteroids.sprites()
                        score1 += 10 * len(sprites)
                        all_sprites.remove(*sprites)
                        asteroids.empty()
                    if powerup.name == "shield":
                        extra1 = True
                        powerups.remove(powerup)

                if pygame.sprite.spritecollide(player1, asteroids, True,
                                               pygame.sprite.collide_mask):
                    if not extra1:
                        pygame.mixer.Sound(
                            SHIP_EXPLOSION_SOUND_FILENAME).play()
                        player1.kill()
                        dead1 = True
                    else:
                        extra1 = False

                if pygame.sprite.spritecollide(player1, bullets2, True,
                                               pygame.sprite.collide_mask):
                    if not extra1:
                        pygame.mixer.Sound(
                            SHIP_EXPLOSION_SOUND_FILENAME).play()
                        player1.kill()
                        dead1 = True
                    else:
                        extra1 = False

                if pygame.sprite.spritecollide(player2, asteroids, True,
                                               pygame.sprite.collide_mask):
                    if not extra2:
                        pygame.mixer.Sound(
                            SHIP_EXPLOSION_SOUND_FILENAME).play()
                        player2.kill()
                        dead2 = True
                    else:
                        extra2 = False

                if pygame.sprite.spritecollide(player2, bullets1, True,
                                               pygame.sprite.collide_mask):
                    if not extra2:
                        pygame.mixer.Sound(
                            SHIP_EXPLOSION_SOUND_FILENAME).play()
                        player2.kill()
                        dead2 = True
                    else:
                        extra2 = False

                all_sprites.update()
                draw(all_sprites, screen)

                score_display = score_text.render("Score: %i" % score1,
                                                  True, GREEN)
                screen.blit(
                    score_display,
                    (SCREEN_SIZE[0] // 2 - score_display.get_width() // 2,
                     15),
                )

                if extra1:
                    screen.blit(SHIELD_EFFECT, (player1.pos[0] - 65, player1.pos[1] - 50))
                if extra2:
                    screen.blit(SHIELD_EFFECT, (player2.pos[0] - 65, player2.pos[1] - 50))

                pygame.display.update()

                #last_asteroid += 1
                time_played += clock.get_time()

                for powerup in powerups:
                    powerup.time += clock.get_time()

            clock.tick(FRAMERATE)

    return score1, time_played, exit
