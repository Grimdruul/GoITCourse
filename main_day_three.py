# day two of GO IT Course
# import antigravity


import os
import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

# Font
FONT = pygame.font.SysFont('Verdana', 20)

# Score counter
score = 0

# game fps
FPS = pygame.time.Clock()

# game screen size
WIDTH = 1200
HEIGHT = 800
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My GAME for Go IT Course')

# background
bg_img = pygame.image.load('img\\background.png')
bg = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 2.5  # backgroung speed

# colors
BLACK = (0, 0, 0)

# list of enemy and bonus objects
list_of_objects = []

# game condition
playing = True

# player
IMG_PATH = 'img\\goose\\'
PLAYER_IMAGES = os.listdir(IMG_PATH)
img_index = 0
player = pygame.image.load('img\\player.png').convert_alpha()  # player init
player_rect = player.get_rect()
# player start position
player_rect.x = int(WIDTH / 2)
player_rect.y = int(HEIGHT / 2)

# player move speed in 4 direction
player_max_speed = 4
player_move_down = [0, player_max_speed]
player_move_up = [0, - player_max_speed]
player_move_left = [- player_max_speed, 0]
player_move_right = [player_max_speed, 0]


# enemy
def create_enemy():

    enemy_size = (100, 40)
    enemy_img = pygame.image.load('img\\enemy.png').convert_alpha()
    enemy = pygame.transform.scale(enemy_img, enemy_size)

    # 50 so that the object always appears inside game screen
    enemy_rect = pygame.Rect(
        WIDTH, random.randint(50, HEIGHT - 50), *enemy_size
        )
    enemy_move = [random.randint(-6, -4), 0]

    return [enemy, enemy_rect, enemy_move]


# bonus
def create_bonus():

    # list of random bonus shapes [size, speed]
    bonus_shape_list = [
        [30, 1],
        [40, 2],
        [50, 4],
        [60, random.randint(3, 6)]]

    # pick random bonus shape from list
    bonus_shape = random.choice(bonus_shape_list)
    bonus_size = (bonus_shape[0], bonus_shape[0])

    bonus_img = pygame.image.load('img\\bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus_img, bonus_size)

    # 50 so that the object always appears inside game screen
    bonus_rect = pygame.Rect(random.randint(50, WIDTH - 50), 0, *bonus_size)
    bonus_move = [0, bonus_shape[1]]

    return [bonus, bonus_rect, bonus_move]


# events
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

PLAYER_ANIMATION = pygame.USEREVENT + 3
pygame.time.set_timer(PLAYER_ANIMATION, 200)

# main cycle
while playing:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
            break
        if event.type == CREATE_ENEMY:
            list_of_objects.append(create_enemy())
        if event.type == CREATE_BONUS:
            list_of_objects.append(create_bonus())
        if event.type == PLAYER_ANIMATION:
            # cycle player animation
            player = pygame.image.load(
                os.path.join(IMG_PATH, PLAYER_IMAGES[img_index])
                )
            img_index += 1
            if img_index >= len(PLAYER_IMAGES):
                img_index = 0

    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < - bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < - bg.get_width():
        bg_x2 = bg.get_width()

    # move background
    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    # player controls
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

    # render score count
    main_display.blit(FONT.render(str(score), True, BLACK), (WIDTH - 50, 20))

    # render player at coordinates
    main_display.blit(player, player_rect)

    # render new frame
    pygame.display.flip()

    # delete object when it off the game screen
    for myobject in list_of_objects:
        if myobject[1].right < 0 or myobject[1].top > HEIGHT:
            list_of_objects.pop(list_of_objects.index(myobject))

        # objects collision
        if player_rect.colliderect(myobject[1]):
            # check object horizontal speed
            if myobject[2][0] == 0:
                # collide with bonus object
                list_of_objects.pop(list_of_objects.index(myobject))
                # bigger bonus object size - biger score
                score += myobject[1].size[0]
            else:
                # collide with enemy object
                playing = False
