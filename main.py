import pygame
from pygame.constants import QUIT

pygame.init()

FPS = pygame.time.Clock()

WIDTH = 1200
HEIGTH = 800

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

PLAYER_SIZE = (20, 20)

main_display = pygame.display.set_mode((WIDTH, HEIGTH))

player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_move = [1, 1]

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

    main_display.fill(COLOR_BLACK)

    if player_rect.bottom >= HEIGTH or player_rect.top <= 0:
        player_move[1] = -player_move[1]

    if player_rect.right >= WIDTH or player_rect.left <= 0:
        player_move[0] = -player_move[0]

    main_display.blit(player, player_rect)

    player_rect = player_rect.move(player_move)

    pygame.display.flip()
