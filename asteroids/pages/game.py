import json
import random

import pygame
from pygame.locals import *

from ..sprites import Asteroid, Spaceship, Powerup

with open('config.json') as configfile:
    config = json.load(configfile)

FRAMERATE = config['framerate']
SCREEN_SIZE = config['screenSize']
SHIP_EXPLOSION_SOUND_FILENAME = config['game']['shipExplodeSound']
SHOOT_SOUND_FILENAME = config['game']['shootSound']
BACKGROUND = pygame.Color(*config['game']['background'])

GREEN = (0, 255, 0)


def get_actions():
    actions = {
        'accelerate': False,
        'recelerate': False,
        'stop': False,
        'die': False,
        'left': False,
        'pause': False,
        'quit': False,
        'right': False,
        'fire': False
    }

    for event in pygame.event.get():
        if event.type == QUIT:
            actions['quit'] = True

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                actions['fire'] = True
            if event.key == K_p:
                actions['pause'] = True
            if event.key == K_UP:
                actions['accelerate'] = True
            if event.key == K_DOWN:
                actions['recelerate'] = True
        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_DOWN:
                actions['accelerate'] = False
                actions['recelerate'] = True
                actions['stop'] = True

    keys = pygame.key.get_pressed()

    if keys[K_q]:
        actions['die'] = True
    # if keys[K_UP]:
    #     actions['accelerate'] = True
    if keys[K_LEFT]:
        actions['left'] = True
    if keys[K_RIGHT]:
        actions['right'] = True

    return actions


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


def game(screen):
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    last_asteroid = 0
    asteroid = generate_asteroid(
        random.randint(config['asteroid']['minRadius'],
                       config['asteroid']['maxRadius']))
    asteroids.add(asteroid)
    all_sprites.add(asteroid)

    player = Spaceship((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
    all_sprites.add(player)

    score_text = pygame.font.SysFont("Monotype Corsiva", 20)
    score = 0
    time_played = 0

    paused = False
    dead = False
    exit = False

    while not dead:
        actions = get_actions()

        if actions['quit']:
            exit = True
            break
        if actions['die']:
            dead = True

        paused ^= actions['pause']

        if not paused:
            if actions['fire']:
                pygame.mixer.Sound(SHOOT_SOUND_FILENAME).play()
                bullet = player.shoot()
                bullets.add(bullet)
                all_sprites.add(bullet)

            if actions['left']:
                player.rotate(-2)
            if actions['right']:
                player.rotate(2)

            if actions['accelerate']:
                player.accelerate()

            if actions['recelerate']:
                player.recelerate()

            if actions['stop']:
                player.stop()

            if last_asteroid > 5000:
                last_asteroid = 0
                asteroid = generate_asteroid(
                    random.randint(config['asteroid']['minRadius'],
                                   config['asteroid']['maxRadius']))
                asteroids.add(asteroid)
                all_sprites.add(asteroid)

            for sprite in all_sprites:
                sprite.pos[0] %= SCREEN_SIZE[0]
                sprite.pos[1] %= SCREEN_SIZE[1]

            collide_list = pygame.sprite.groupcollide(
                asteroids, bullets, True, True, pygame.sprite.collide_mask)
            for asteroid in collide_list:
                score += 10
                for i in asteroid.split():
                    if isinstance(i, Powerup):
                        powerups.add(i)
                    else:
                        asteroids.add(i)
                    all_sprites.add(i)

            collide_list = pygame.sprite.spritecollide(
                player, powerups, True, pygame.sprite.collide_mask)
            for powerup in collide_list:
                if powerup.name == 'bomb':
                    sprites = asteroids.sprites()
                    score += 10 * len(sprites)
                    all_sprites.remove(*sprites)
                    asteroids.empty()

            if pygame.sprite.spritecollide(player, asteroids, True,
                                           pygame.sprite.collide_mask):
                pygame.mixer.Sound(SHIP_EXPLOSION_SOUND_FILENAME).play()
                player.die()

                all_sprites.add(player)
                screen.fill(BACKGROUND)
                all_sprites.draw(screen)
                pygame.display.update()

                clock.tick(2)
                player.kill()
                dead = True

            all_sprites.update()
            screen.fill(BACKGROUND)
            all_sprites.draw(screen)

            score_display = score_text.render("Score: %i" % score, True, GREEN)
            screen.blit(
                score_display,
                (SCREEN_SIZE[0] // 2 - score_display.get_width() // 2, 15))

            pygame.display.update()

            last_asteroid += clock.get_time()
            time_played += clock.get_time()

            for powerup in powerups:
                powerup.time += clock.get_time()

        clock.tick(FRAMERATE)

    return score, time_played, exit
