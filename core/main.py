from core.helper import *


def main():

    clock = pg.time.Clock()
    fps = 60

    running = True
    while running:
        clock.tick(fps)

        alpha_surf.fill((255, 255, 255, 0))
        screen.fill(line_col)
        grid.draw()
        screen.blit(alpha_surf, (0, 0))

        draw_score()

        if not grid.game_over:
            grid.update()

        else:
            draw_game_over()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE and grid.game_over:
                    grid.reset()

        pg.display.update()
