import pygame as pg

pg.init()

# Setting up screen
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
alpha_surf = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)


# Font


# Colours
white = (255, 255, 255)
grey = (200, 200, 200)
black = (0, 0, 0)
bg_col = (42, 153, 209)
line_col = (41, 119, 158)

# Game variables
TILE_SIZE = SCREEN_WIDTH // 3
top = 100
game_over = False
