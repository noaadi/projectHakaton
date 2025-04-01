import pygame

# Constants
WIDTH, HEIGHT = 750, 550
GRID_SIZE = 3
BOARD_SIZE = 450
BOARD_X = (WIDTH - BOARD_SIZE) // 2
BOARD_Y = (HEIGHT - BOARD_SIZE) // 2
SQUARE_SIZE = BOARD_SIZE // GRID_SIZE
LINE_WIDTH = 10
FONT_SIZE = 80
BUTTON_FONT_SIZE = 30

# Colors
YELLOW = (255, 255, 197)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GRAY = (200, 200, 200)
RED_BUTTON = (180, 50, 50)
WHITE_TEXT = (255, 255, 255)


class TicTacToe:
    def __init__(self, screen):
        self.screen = screen
        self.board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = "X"
        self.game_over = False
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        self.small_font = pygame.font.Font(None, 40)
        self.return_to_menu = False
        self.x_wins = 0
        self.o_wins = 0
        self.winner_text = ""

    def draw_board(self):
        self.screen.fill(YELLOW)

        #  "Return to Menu"
        button_rect = pygame.Rect(10, 10, 170, 40)
        pygame.draw.rect(self.screen, RED_BUTTON, button_rect, border_radius=10)
        menu_text = self.button_font.render("Return to Menu", True, WHITE_TEXT)
        self.screen.blit(menu_text, (20, 20))

        # drawing the board
        for i in range(1, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK,
                             (BOARD_X, BOARD_Y + i * SQUARE_SIZE),
                             (BOARD_X + BOARD_SIZE, BOARD_Y + i * SQUARE_SIZE), LINE_WIDTH)
            pygame.draw.line(self.screen, BLACK,
                             (BOARD_X + i * SQUARE_SIZE, BOARD_Y),
                             (BOARD_X + i * SQUARE_SIZE, BOARD_Y + BOARD_SIZE), LINE_WIDTH)

        # putting the X and O on the board
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col]:
                    text = self.font.render(self.board[row][col], True, BLUE if self.board[row][col] == "X" else RED)
                    text_rect = text.get_rect(center=(BOARD_X + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                      BOARD_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    self.screen.blit(text, text_rect)

        # showing the score
        x_score_text = self.small_font.render(f"X WINS: {self.x_wins}", True, BLACK)
        o_score_text = self.small_font.render(f"O WINS: {self.o_wins}", True, BLACK)
        self.screen.blit(x_score_text, (WIDTH - 150, 10))
        self.screen.blit(o_score_text, (WIDTH - 150, 40))

        # winner text
        if self.game_over:
            winner_text1 = self.small_font.render(self.winner_text.split("!")[0] + "!", True, BLACK)
            winner_text2 = self.small_font.render("Press ENTER to play again", True, BLACK)

            self.screen.blit(winner_text1, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
            self.screen.blit(winner_text2, (WIDTH // 2 - 150, HEIGHT // 2 + 20))

        pygame.display.flip()

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]
        for col in range(GRID_SIZE):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        if all(self.board[row][col] is not None for row in range(GRID_SIZE) for col in range(GRID_SIZE)):
            return "Tie"
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not self.game_over:
                # checks if the player pressed a square and checks if he won
                if BOARD_X <= x < BOARD_X + BOARD_SIZE and BOARD_Y <= y < BOARD_Y + BOARD_SIZE:
                    row, col = (y - BOARD_Y) // SQUARE_SIZE, (x - BOARD_X) // SQUARE_SIZE
                    if self.board[row][col] is None:
                        self.board[row][col] = self.current_player
                        winner = self.check_winner()
                        if winner:
                            self.game_over = True
                            if winner == "X":
                                self.x_wins += 1
                                self.winner_text = "Player X won!"
                            elif winner == "O":
                                self.o_wins += 1
                                self.winner_text = "Player O won!"
                            else:
                                self.winner_text = "It's a tie!"
                        else:
                            self.current_player = "O" if self.current_player == "X" else "X"

            # press on "Return to Menu"
            if 10 <= x <= 180 and 10 <= y <= 50:
                self.x_wins = 0
                self.o_wins = 0
                self.return_to_menu = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.game_over:
                self.reset_game()

    def reset_game(self):
        self.board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = "X"
        self.game_over = False
        self.winner_text = ""

    def update(self):
        pass

    def render(self):
        self.draw_board()
