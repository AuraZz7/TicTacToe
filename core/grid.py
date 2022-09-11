from core.prepare import *


class Grid(object):
    def __init__(self):
        self.tiles = [(0, top), (TILE_SIZE, top), (2*TILE_SIZE, top),
                      (0, TILE_SIZE+top), (TILE_SIZE, TILE_SIZE+top), (2*TILE_SIZE, TILE_SIZE+top),
                      (0, 2*TILE_SIZE+top), (TILE_SIZE, 2*TILE_SIZE+top), (2*TILE_SIZE, 2*TILE_SIZE+top)]
        self.t = self.turn = self.winner = self.win_line = self.clicked = self.game_over = None
        self.x_score = self.o_score = 0
        self.reset()

    def reset(self):
        self.t = [None] * 9
        self.turn = "X"
        self.winner = self.win_line = None
        self.game_over = False
        self.clicked = False

    def update(self):
        self.check_winner()
        self.update_user_tile()
        if self.winner is not None:
            self.end_game()

    def place_tile(self, placement):
        self.t[placement[0]][placement[1]] = self.turn
        self.turn = "O" if self.turn == "X" else "X" if self.turn == "O" else None

    def update_user_tile(self):
        if pg.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True
            hover_tile = self.get_tile_from_pos(pg.mouse.get_pos())
            for i, tile in enumerate(self.tiles):
                if tile == hover_tile and self.t[i] is None:
                    self.t[i] = self.turn
                    self.turn = "O" if self.turn == "X" else "X" if self.turn == "O" else None

        if not pg.mouse.get_pressed()[0] and self.clicked:
            self.clicked = False

    def update_ai_tile(self):
        # 1 - Try to win
        for x in range(3):
            # Checking for horizontal possible wins
            if self.t[x][0] == self.t[x][1] and self.t[x][2] is None:
                self.place_tile((x, 2))
            elif self.t[x][1] == self.t[x][2] and self.t[x][0] is None:
                self.place_tile((x, 0))
            # Checking for vertical possible wins
            if self.t[0][x] == self.t[1][x] and self.t[2][x] is None:
                self.place_tile((2, x))
            elif self.t[1][x] == self.t[2][x] and self.t[0][x] is None:
                self.place_tile((0, x))

        # Checking for diagonal possible wins
        if self.t[0][0] == self.t[1][1] and self.t[2][2] is None:
            self.place_tile((2, 2))
        elif self.t[1][1] == self.t[2][2] and self.t[0][0] is None:
            self.place_tile((0, 0))

        if self.t[0][2] == self.t[1][1] and self.t[2][0] is None:
            self.place_tile((2, 0))

    def check_winner(self):
        for x in range(3):
            # Check horizontal wins
            if self.t[x*3] == self.t[x*3+1] == self.t[x*3+2] is not None:
                self.win_line = [x*3, x*3+2]
            # Check vertical wins
            if self.t[x] == self.t[x+3] == self.t[x+6] is not None:
                self.win_line = [x, x+6]
        # Check diagonal TL to BR win
        if self.t[0] == self.t[4] == self.t[8] is not None:
            self.win_line = [0, 8]
        # Check diagonal TR to BL win
        if self.t[2] == self.t[4] == self.t[6] is not None:
            self.win_line = [2, 6]

        if self.win_line is not None:
            self.winner = self.t[self.win_line[0]]

    def end_game(self):
        if self.winner == "X":
            self.x_score += 1
        elif self.winner == "O":
            self.o_score += 1
        self.turn = self.winner
        self.game_over = True

    def get_tile_from_pos(self, pos):
        pos_x = pos_y = None
        for i, tile in enumerate(self.tiles):
            if tile[0] <= pos[0] <= tile[0] + TILE_SIZE:
                pos_x = tile[0]
            if tile[1] <= pos[1] <= tile[1] + TILE_SIZE:
                pos_y = tile[1]
        if pos_x is not None and pos_y is not None:
            return pos_x, pos_y
        return None

    def draw(self):
        self.draw_grid()
        self.draw_moves()
        if not self.game_over:
            self.draw_hover()
        else:
            self.draw_win_line(self.win_line[0], self.win_line[1])

    def draw_hover(self):
        pos = self.get_tile_from_pos(pg.mouse.get_pos())
        for i, tile in enumerate(self.tiles):
            if tile == pos and self.t[i] is None:
                if self.turn == "X":
                    self.draw_x(pos, 128)
                elif self.turn == "O":
                    self.draw_o(pos, 128)

    def draw_moves(self):
        for i, t in enumerate(self.t):
            if t == "X":
                self.draw_x(self.tiles[i], 255)
            elif t == "O":
                self.draw_o(self.tiles[i], 255)

    @staticmethod
    def draw_x(pos, alpha):
        x, y = pos

        pg.draw.line(alpha_surf, (0, 0, 0, alpha), (x + 0.1*TILE_SIZE, y+0.1*TILE_SIZE), (x + 0.9*TILE_SIZE, y+0.9*TILE_SIZE), 5)
        pg.draw.line(alpha_surf, (0, 0, 0, alpha), (x + 0.1*TILE_SIZE, y+0.9*TILE_SIZE), (x + 0.9*TILE_SIZE, y+0.1*TILE_SIZE), 5)

    @staticmethod
    def draw_o(pos, alpha):
        pg.draw.circle(alpha_surf, (200, 200, 200, alpha), (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2), TILE_SIZE * 0.4, 5)

    def draw_win_line(self, starting, ending):
        diff = ending-starting
        col = black if self.t[starting] == "X" else grey
        size = 9

        start, end = self.tiles[starting], self.tiles[ending]

        pg.draw.line(screen, col,
                     (start[0] + (TILE_SIZE * (0.2 if diff in (2, 8) else 0.5 if diff == 6 else 0.8)),
                      start[1] + (TILE_SIZE * (0.2 if diff in (4, 6, 8) else 0.5))),
                     (end[0] + (TILE_SIZE * (0.2 if diff == 4 else 0.5 if diff == 6 else 0.8)),
                      end[1] + (TILE_SIZE * (0.5 if diff == 2 else 0.8))), size)

    @staticmethod
    def draw_grid():
        # Draw top line
        pg.draw.line(screen, bg_col, (0, top), (SCREEN_WIDTH, top), 20)
        # Draw vertical lines
        pg.draw.line(screen, bg_col, (TILE_SIZE, top), (TILE_SIZE, SCREEN_HEIGHT), 10)
        pg.draw.line(screen, bg_col, (2 * TILE_SIZE, top), (2 * TILE_SIZE, SCREEN_HEIGHT), 10)
        # Draw horizontal lines
        pg.draw.line(screen, bg_col, (0, TILE_SIZE + top), (SCREEN_WIDTH, TILE_SIZE + top), 10)
        pg.draw.line(screen, bg_col, (0, 2 * TILE_SIZE + top), (SCREEN_WIDTH, 2 * TILE_SIZE + top), 10)


grid = Grid()