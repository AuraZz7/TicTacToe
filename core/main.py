from core.prepare import *


class Grid(object):
    def __init__(self):
        self.tiles = [[(0, top), (TILE_SIZE, top), (2*TILE_SIZE, top)],
                      [(0, TILE_SIZE+top), (TILE_SIZE, TILE_SIZE+top), (2*TILE_SIZE, TILE_SIZE+top)],
                      [(0, 2*TILE_SIZE+top), (TILE_SIZE, 2*TILE_SIZE+top), (2*TILE_SIZE, 2*TILE_SIZE+top)]]
        self.chosen_tiles = self.turn = self.winner = self.clicked = None
        self.x_score = self.o_score = 0
        self.reset()

    def reset(self):
        self.chosen_tiles = [[None, None, None], [None, None, None], [None, None, None]]
        self.turn = "X"
        self.winner = None
        self.clicked = False

    def update(self):
        self.update_chosen_tiles()
        self.check_winner()

    def update_chosen_tiles(self):
        click = pg.mouse.get_pressed()[0]

        if pg.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True
            tile = self.get_tile_from_pos(pg.mouse.get_pos())
            if tile is not None:
                for x in range(len(self.tiles)):
                    for y in range(len(self.tiles)):
                        if self.tiles[x][y] == tile and self.chosen_tiles[x][y] is None:
                            self.chosen_tiles[x][y] = self.turn
                            self.turn = "O" if self.turn == "X" else "X" if self.turn == "O" else None

        if not click and self.clicked:
            self.clicked = False

    def check_winner(self):
        global game_over
        for x in range(3):
            print(x)
            if self.chosen_tiles[x][0] == self.chosen_tiles[x][1] == self.chosen_tiles[x][2]:
                self.winner = self.chosen_tiles[x][0]
            if self.chosen_tiles[0][x] == self.chosen_tiles[1][x] == self.chosen_tiles[2][x]:
                self.winner = self.chosen_tiles[0][x]

        if self.chosen_tiles[0][0] == self.chosen_tiles[1][1] == self.chosen_tiles[2][2]:
            self.winner = self.chosen_tiles[0][0]

        if self.chosen_tiles[0][2] == self.chosen_tiles[1][1] == self.chosen_tiles[2][0]:
            self.winner = self.chosen_tiles[0][2]

        if self.winner is not None:
            if self.winner == "X":
                self.x_score += 1
            elif self.winner == "O":
                self.o_score += 1
            self.turn = self.winner
            game_over = True

    def get_tile_from_pos(self, pos):
        pos_x = pos_y = None
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles)):
                if self.tiles[x][y][0] <= pos[0] <= self.tiles[x][y][0] + TILE_SIZE:
                    pos_x = self.tiles[x][y][0]
                if self.tiles[x][y][1] <= pos[1] <= self.tiles[x][y][1] + TILE_SIZE:
                    pos_y = self.tiles[x][y][1]
        if pos_x is not None and pos_y is not None:
            return pos_x, pos_y
        return None

    def draw(self):
        self.draw_grid()
        self.draw_moves()
        if not game_over:
            self.draw_hover()

    def draw_hover(self):
        pos = self.get_tile_from_pos(pg.mouse.get_pos())
        if pos is not None:
            for x in range(len(self.tiles)):
                for y in range(len(self.tiles)):
                    if pos == self.tiles[x][y]:
                        if self.chosen_tiles[x][y] is None:
                            if self.turn == "X":
                                self.draw_x(pos, 128)
                            elif self.turn == "O":
                                self.draw_o(pos, 128)

    def draw_moves(self):
        for x in range(len(self.chosen_tiles)):
            for y in range(len(self.chosen_tiles)):
                if self.chosen_tiles[x][y] == "X":
                    self.draw_x(self.tiles[x][y], 255)
                elif self.chosen_tiles[x][y] == "O":
                    self.draw_o(self.tiles[x][y], 255)

    @staticmethod
    def draw_x(pos, alpha):
        x, y = pos

        pg.draw.line(alpha_surf, (0, 0, 0, alpha), (x + 0.1*TILE_SIZE, y+0.1*TILE_SIZE), (x + 0.9*TILE_SIZE, y+0.9*TILE_SIZE), 5)
        pg.draw.line(alpha_surf, (0, 0, 0, alpha), (x + 0.1*TILE_SIZE, y+0.9*TILE_SIZE), (x + 0.9*TILE_SIZE, y+0.1*TILE_SIZE), 5)

    @staticmethod
    def draw_o(pos, alpha):
        pg.draw.circle(alpha_surf, (0, 0, 0, alpha), (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2), TILE_SIZE * 0.4, 5)

    @staticmethod
    def draw_grid():
        # Draw top line
        pg.draw.line(screen, black, (0, top), (SCREEN_WIDTH, top), 5)
        # Draw vertical lines
        pg.draw.line(screen, black, (TILE_SIZE, top), (TILE_SIZE, SCREEN_HEIGHT), 2)
        pg.draw.line(screen, black, (2 * TILE_SIZE, top), (2 * TILE_SIZE, SCREEN_HEIGHT), 2)
        # Draw horizontal lines
        pg.draw.line(screen, black, (0, TILE_SIZE + top), (SCREEN_WIDTH, TILE_SIZE + top), 2)
        pg.draw.line(screen, black, (0, 2 * TILE_SIZE + top), (SCREEN_WIDTH, 2 * TILE_SIZE + top), 2)


def main():

    clock = pg.time.Clock()
    fps = 60

    grid = Grid()

    restart_txt = get_font(48).render("Press space to play again", True, black)

    running = True
    while running:
        global game_over
        clock.tick(fps)

        alpha_surf.fill((255, 255, 255, 0))
        screen.fill(white)
        grid.draw()
        screen.blit(alpha_surf, (0, 0))

        X_score_txt = get_font(36).render(f"X's score: {grid.x_score}", True, black)
        O_score_txt = get_font(36).render(f"O's score: {grid.o_score}", True, black)
        turn_txt = get_font(40).render(f"{grid.turn}'s turn", True, black)

        screen.blit(X_score_txt, (0, top - X_score_txt.get_height()))
        screen.blit(O_score_txt, (SCREEN_WIDTH - O_score_txt.get_width(), top - O_score_txt.get_height()))
        screen.blit(turn_txt, (SCREEN_WIDTH // 2 - turn_txt.get_width() // 2, top - turn_txt.get_height()))

        if not game_over:
            grid.update()

        else:
            game_over_txt = get_font(60).render(f"{grid.winner} won!", True, black)
            screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, SCREEN_HEIGHT * 0.5))
            screen.blit(restart_txt, (SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, SCREEN_HEIGHT * 0.6))

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE and game_over:
                    game_over = False
                    grid.reset()

        pg.display.update()
