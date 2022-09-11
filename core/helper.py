from core.prepare import *
from core.grid import grid


def get_font(size):
    return pg.font.Font(None, size)


restart_txt = get_font(48).render("Press space to play again", True, black)


def draw_score():
    X_score_txt = get_font(36).render(f"X's score: {grid.x_score}", True, black)
    O_score_txt = get_font(36).render(f"O's score: {grid.o_score}", True, black)
    turn_txt = get_font(40).render(f"{grid.turn}'s turn", True, black)

    screen.blit(X_score_txt, (0, top - X_score_txt.get_height()))
    screen.blit(O_score_txt, (SCREEN_WIDTH - O_score_txt.get_width(), top - O_score_txt.get_height()))
    screen.blit(turn_txt, (SCREEN_WIDTH // 2 - turn_txt.get_width() // 2, top - turn_txt.get_height()))


def draw_game_over():
    game_over_txt = get_font(60).render(f"{grid.winner} won!", True, black)
    screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, SCREEN_HEIGHT * 0.5))
    screen.blit(restart_txt, (SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, SCREEN_HEIGHT * 0.6))

