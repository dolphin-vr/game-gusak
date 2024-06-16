import random
import os
import pygame
from pygame.constants import QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

WIDTH = 1200
HEIGTH = 800

FONT= pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

PLAYER_SIZE = (20, 20)
ENEMY_SIZE = (30, 30)
BONUS_SIZE = (30, 30)

main_display = pygame.display.set_mode((WIDTH, HEIGTH))

bg = pygame.transform.scale(pygame.image.load('./resourses/images/background.png'), (WIDTH, HEIGTH - 30))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

player = pygame.image.load('./resourses/images/goose/1-1.png').convert_alpha()
player_rect = pygame.Rect(0, 400, *PLAYER_SIZE)
player_move_up = [0, -4]
player_move_down = [0, 4]
player_move_left = [-4, 0]
player_move_right = [4, 0]


def create_enemy():
    enemy = pygame.image.load('./resourses/images/enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(50, HEIGTH - 50), *ENEMY_SIZE)
    enemy_move = [random.randint(-5, -1), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus = pygame.image.load('./resourses/images/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(100, WIDTH - 100), 30, *BONUS_SIZE)
    bonus_move = [0, random.randint(1, 5)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

enemies = []
bonuses = []

score = 0
health = 100

playing = True

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()
    
    main_display.blit(bg, (bg_X1, 30))
    main_display.blit(bg, (bg_X2, 30))

    keys = pygame.key.get_pressed()

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_DOWN] and player_rect.bottom < HEIGTH:
        player_rect = player_rect.move(player_move_down)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            health -= 25
            enemies.pop(enemies.index(enemy))
            if health <= 0:
                playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 100
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_WHITE), (WIDTH - 100, 2))
    main_display.blit(FONT.render(str(health), True, COLOR_RED), (100, 2))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGTH:
            bonuses.pop(bonuses.index(bonus))
