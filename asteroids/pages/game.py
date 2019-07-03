import json
import random
import time

import pygame
from pygame.locals import *

from ..sprites import Asteroid, Powerup, Spaceship

with open("config.json") as configfile:
    config = json.load(configfile)

FRAMERATE = config["framerate"]
SCREEN_SIZE = config["screenSize"]
SHIP_EXPLOSION_SOUND_FILENAME = config["game"]["shipExplodeSound"]
SHOOT_SOUND_FILENAME = config["game"]["shootSound"]
BACKGROUND = pygame.Color(*config["game"]["background"])

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (227, 88, 7)


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


def generate_asteroid(size, score):
    if random.uniform(0, sum(SCREEN_SIZE)) < SCREEN_SIZE[0]:
        t = random.randint(0, 2 * SCREEN_SIZE[0])
        pos = (t % SCREEN_SIZE[0], SCREEN_SIZE[1] if t > SCREEN_SIZE[0] else 0)
    else:
        t = random.randint(0, 2 * SCREEN_SIZE[1])
        pos = (SCREEN_SIZE[0] if t > SCREEN_SIZE[1] else 0, t % SCREEN_SIZE[1])

    if(score < 15):
        speed = (random.uniform(1, 2), random.uniform(1, 2))
    elif(score >= 15 and score <= 30):
        speed = (random.uniform(1, 2) + 1, random.uniform(1, 2) + 1)
    elif(score > 30 and score <= 45):
        speed = (random.uniform(1, 2) + 2, random.uniform(1, 2) + 2)
    elif(score > 45 and score <= 60):
        speed = (random.uniform(1, 2) + 3, random.uniform(1, 2) + 3)
    elif(score > 60 and score <= 75):
        speed = (random.uniform(1, 2) + 5, random.uniform(1, 2) + 5)
    else:
        speed = (random.uniform(1, 2) + 5, random.uniform(1, 2) + 5)

    asteroid = Asteroid(size, speed, pos)

    return asteroid


def game(screen):
    clock = pygame.time.Clock()
    # delayClock = pygame.time.delay(5000)

    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    score_text = pygame.font.SysFont("Monotype Corsiva", 20)
    score = 0
    time_played = 0

    bullet_count = 0

    # Level text
    level_text = pygame.font.SysFont("Monotype Corsiva", 20) 

    last_asteroid = 0
    asteroid = generate_asteroid(
        random.randint(config["asteroid"]["minRadius"],
                       config["asteroid"]["maxRadius"]), score)
    asteroids.add(asteroid)
    all_sprites.add(asteroid)

    player = Spaceship((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
    all_sprites.add(player)
    extra = False
    starPower = False

    # score_text = pygame.font.SysFont("Monotype Corsiva", 20)
    # score = 0
    # time_played = 0

    paused = False
    dead = False
    exit = False
    font = pygame.font.Font(None, 25)
    frame_count = 0
    start_time = 90
    
    star_start_time = 0

    while not dead:
        actions = get_actions()

        if actions["quit"]:
            exit = True
            break
        if actions["die"]:
            dead = True

        paused ^= actions["pause"]

        if not paused:
            total_seconds = frame_count // FRAMERATE
 
            minutes = total_seconds // 60

            seconds = total_seconds % 60
 
            output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

            frame_count += 1

            if actions["fire"]:
                pygame.mixer.Sound(SHOOT_SOUND_FILENAME).play()
                bullet = player.shoot()
                bullets.add(bullet)
                all_sprites.add(bullet)
                bullet_count += 1

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

            if last_asteroid > 5000:
                last_asteroid = 0
                asteroid = generate_asteroid(
                    random.randint(config["asteroid"]["minRadius"],
                                   config["asteroid"]["maxRadius"]), score)
                asteroids.add(asteroid)
                all_sprites.add(asteroid)

            for sprite in all_sprites:
                sprite.pos[0] %= SCREEN_SIZE[0]
                sprite.pos[1] %= SCREEN_SIZE[1]

            collide_list = pygame.sprite.groupcollide(asteroids, bullets, True, True, pygame.sprite.collide_mask)
            for asteroid in collide_list:
                score += 10
                for i in asteroid.split():
                    if isinstance(i, Powerup):
                        powerups.add(i)
                    else:
                        asteroids.add(i)
                    all_sprites.add(i)

            collide_list = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_mask)
            for powerup in collide_list:
                if powerup.name == "star":
                    starPower = True
                if powerup.name == "bomb":
                    sprites = asteroids.sprites()
                    score += 10 * len(sprites)
                    all_sprites.remove(*sprites)
                    asteroids.empty()
                if powerup.name == "shield":
                    extra = True
                    powerups.remove(powerup)
                if powerup.name == "diamond":
                    score += 50

            collide_list = pygame.sprite.spritecollide(player, asteroids, True, pygame.sprite.collide_mask)
            for asteroid in collide_list:
                if starPower == True:
                    star_start_time = 0
                    break
                    
            for asteroid in collide_list:
                if extra == False:
                    pygame.mixer.Sound(SHIP_EXPLOSION_SOUND_FILENAME).play()
                    player.die()

                    all_sprites.add(player)
                    screen.fill(BACKGROUND)
                    all_sprites.draw(screen)
                    pygame.display.update()

                    clock.tick(2)
                    player.kill()
                    dead = True
                else:
                    extra = False
                    asteroids.remove(asteroid)

            all_sprites.update()
            screen.fill(BACKGROUND)
            all_sprites.draw(screen)

            score_display = score_text.render("Score: %i" % score, True, GREEN)
            screen.blit(
                score_display,
                (SCREEN_SIZE[0] // 2 - score_display.get_width() // 2, 15),
            )
            text = font.render(output_string, True, WHITE)
            screen.blit(text,(800, 15))

            # Level Display
            if(score < 15):
                level_display = level_text.render("Level 0", True, YELLOW)
            elif(score >= 15 and score <= 30):
                level_display = level_text.render("Level 1", True, YELLOW)
            elif(score > 30 and score <= 45):
                level_display = level_text.render("Level 2", True, YELLOW)
            elif(score > 45 and score <= 60):
                level_display = level_text.render("Level 3", True, YELLOW)
            elif(score > 60 and score <= 75):
                level_display = level_text.render("Level 4", True, YELLOW)
            else:
                level_display = level_text.render("Level 5", True, YELLOW)
            screen.blit(level_display, (600, 15))

            # Bullets Display
            bullet_display = score_text.render("Bullets: %i" %bullet_count, True, ORANGE)
            screen.blit(bullet_display,(700, 15))

            # Powerups
            if extra == True:
                shield_display = score_text.render("Shield On!!!", True, GREEN)
                screen.blit(shield_display, (0, 15))
            
            if starPower == True:
                multiply_point_display = score_text.render("Multiplied points!!!", True, RED)
                screen.blit(multiply_point_display, (100, 15))
                collide_list = pygame.sprite.groupcollide(asteroids, bullets, True, True, pygame.sprite.collide_mask)
                for asteroid in collide_list:
                    score += 15
                star_start_time += clock.get_time()
                if(star_start_time > 5000):
                    star_start_time = 0
                    starPower = False

            pygame.display.update()

            last_asteroid += clock.get_time()
            time_played += clock.get_time()

            for powerup in powerups:
                powerup.time += clock.get_time()

        clock.tick(FRAMERATE)
        pygame.display.flip()

    return score, time_played, exit
