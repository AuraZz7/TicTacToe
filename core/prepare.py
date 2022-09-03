import pygame as pg

pg.init()

# Setting up screen
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
alpha_surf = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)


# Font
def get_font(size):
    return pg.font.Font(None, size)


# Colours
white = (255, 255, 255)
black = (0, 0, 0)

# Game variables
TILE_SIZE = SCREEN_WIDTH // 3
top = 100
game_over = False
