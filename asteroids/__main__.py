import json
import random

import pygame
from pygame.locals import *

from .sprites import Asteroid, Spaceship

with open('config.json') as configfile:
    config = json.load(configfile)

SCREEN_SIZE = config['screenSize']
FRAMERATE = config['framerate']
SHIP_EXPLOSION = config['ship_explode']

def get_actions():
    actions = {
        'accelerate': False,
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

    keys = pygame.key.get_pressed()

    if keys[K_q]:
        actions['die'] = True
    if keys[K_UP]:
        actions['accelerate'] = True
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


def main():
    pygame.mixer.pre_init(buffer=1024)
    pygame.init()
    pygame.display.set_caption("Asteroids")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = pygame.Color(0, 0, 0)
    clock = pygame.time.Clock()

    exit = False

    while not exit:
        all_sprites = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        last_asteroid = 0
        asteroid = generate_asteroid(random.randint(config['asteroid']['minRadius'], config['asteroid']['maxRadius']))
        asteroids.add(asteroid)
        all_sprites.add(asteroid)

        player = Spaceship((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        all_sprites.add(player)

        score = 0

        paused = False
        dead = False

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
                    bullet = player.shoot()
                    bullets.add(bullet)
                    all_sprites.add(bullet)

                if actions['left']:
                    player.rotate(-2)
                if actions['right']:
                    player.rotate(2)

                if actions['accelerate']:
                    player.accelerate()

                if last_asteroid > 5000:
                    last_asteroid = 0
                    asteroid = generate_asteroid(random.randint(config['asteroid']['minRadius'], config['asteroid']['maxRadius']))
                    asteroids.add(asteroid)
                    all_sprites.add(asteroid)


                for sprite in all_sprites:
                    sprite.pos[0] %= SCREEN_SIZE[0]
                    sprite.pos[1] %= SCREEN_SIZE[1]

                collide_list = pygame.sprite.groupcollide(asteroids, bullets, True, True, pygame.sprite.collide_mask)
                for asteroid in collide_list:
                    score += 10
                    for i in asteroid.split():
                        asteroids.add(i)
                        all_sprites.add(i)

                if pygame.sprite.spritecollide(player, asteroids, True, pygame.sprite.collide_mask):
                    pygame.mixer.Sound(SHIP_EXPLOSION).play()
                    player.kill()
                    dead = True

                all_sprites.update()
                screen.fill(background)
                all_sprites.draw(screen)
                pygame.display.update()

                last_asteroid += clock.get_time()

            clock.tick(FRAMERATE)

    pygame.quit()


if __name__ == '__main__':
    main()
