# day one of GO IT Course
# import antigravity


import pygame
from pygame.constants import QUIT

pygame.init()

# game fps
FPS = pygame.time.Clock()

# game screen size
WIDTH = 1200
HEIGHT = 800
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My GAME')

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# player
player_size = (20, 20)  # size of the player
player_color = WHITE  # color for player
player = pygame.Surface(player_size)  # player init
player.fill(player_color)  # player painting
player_rect = player.get_rect()  # player start position (0, 0)
player_speed = [1, 1]  # player start speed [x ,y]

playing = True  # game condition

while playing:

    FPS.tick(240)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
            break

    main_display.fill(BLACK)  # fill whole game screen with solid color

    main_display.blit(player, player_rect)  # render player at coordinates

    # move player with speed [x, y]
    player_rect = player_rect.move(player_speed)

    if player_rect.bottom >= HEIGHT or player_rect.top <= 0:
        player_speed[1] = - player_speed[1]  # invert vertical speed
    if player_rect.right >= WIDTH or player_rect.left <= 0:
        player_speed[0] = - player_speed[0]  # invert horizontal speed

    pygame.display.flip()  # render new frame
