# day two of GO IT Course
# import antigravity


import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

# game fps
FPS = pygame.time.Clock()

# game screen size
WIDTH = 1200
HEIGHT = 800
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My GAME for Go IT Course')

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)

# player
player_size = (20, 20)  # player size
player_color = WHITE  # player color
player = pygame.Surface(player_size)  # player init
player.fill(player_color)  # player paint
player_rect = player.get_rect()  # player start position (0, 0)

# player move speed in 4 direction
player_move_down = [0, 1]
player_move_up = [0, -1]
player_move_left = [-1, 0]
player_move_right = [1, 0]


# enemy
def create_enemy():

    enemy_size = (30, 30)
    enemy = pygame.Surface(enemy_size)
    enemy_color = RED
    enemy.fill(enemy_color)

    # 40 so that the object always appears on the screen
    # without moving beyond the play area
    enemy_rect = pygame.Rect(
        WIDTH, random.randint(40, HEIGHT - 40), *enemy_size
        )
    enemy_move = [random.randint(-6, -1), 0]

    return [enemy, enemy_rect, enemy_move]


# bonus
def create_bonus():

    # list of random bonus shapes [size, color, speed]
    bonus_shape_list = [
        [10, BLUE, 1],
        [20, YELLOW, 2],
        [30, ORANGE, 4],
        [40, GREEN, random.randint(3, 6)]]

    # pick random bonus shape from list
    bonus_shape = random.choice(bonus_shape_list)

    bonus_size = (bonus_shape[0], bonus_shape[0])
    bonus = pygame.Surface(bonus_size)
    bonus_color = bonus_shape[1]
    bonus.fill(bonus_color)

    # 40 so that the object always appears on the screen
    # without moving beyond the play area
    bonus_rect = pygame.Rect(random.randint(40, WIDTH - 40), 0, *bonus_size)
    bonus_move = [0, bonus_shape[2]]

    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

# list of enemy and bonus objects
list_of_objects = []

# game condition
playing = True

while playing:

    FPS.tick(240)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
            break
        if event.type == CREATE_ENEMY:
            list_of_objects.append(create_enemy())
        if event.type == CREATE_BONUS:
            list_of_objects.append(create_bonus())

    # fill whole game screen with solid color
    main_display.fill(BLACK)

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    for myobject in list_of_objects:
        myobject[1] = myobject[1].move(myobject[2])
        main_display.blit(myobject[0], myobject[1])

    # render player at coordinates
    main_display.blit(player, player_rect)

    # render new frame
    pygame.display.flip()

    # delete object when it off the game screen
    for myobject in list_of_objects:
        if myobject[1].right < 0 or myobject[1].top > HEIGHT:
            list_of_objects.pop(list_of_objects.index(myobject))
