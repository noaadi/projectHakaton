import pygame
import random
from games.game import Game


class WordleGame(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.word_list = [
            "CHAIR", "TABLE", "HOUSE", "WATER", "LIGHT",
            "MUSIC", "PLANT", "DREAM", "SMILE", "CLOUD",
            "STONE", "BRAVE", "SHINE", "GLASS", "BRUSH",
            "SWEET", "TRAIN", "SOUND", "HEART", "HAPPY"
        ]

        self.target_word = random.choice(self.word_list)
        self.already_attempts = []
        self.max_attempts = 6
        self.user_input = ""
        self.font = pygame.font.Font(pygame.font.match_font('arial'), 40)
        self.message = "Guess the word!"
        self.running = True
        self.message_y = 50
        self.game_over = False
        self.return_to_menu = False

        # Return button
        self.return_button = pygame.Rect(10, 10, 180, 50)
        self.button_font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not self.game_over and len(self.user_input) == 5:
                    self.already_attempts.append(self.user_input.upper())
                    self.user_input = ""

                    if self.already_attempts[-1] == self.target_word:
                        self.message = "You Won!"
                        self.game_over = True
                    elif len(self.already_attempts) == self.max_attempts:
                        self.message = "You didn't succeed, try again."
                        self.game_over = True
                    else:
                        self.message = "Try Again!"

                elif self.game_over:
                    self.reset_game()

            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif len(self.user_input) < 5 and event.unicode.isalpha():
                self.user_input += event.unicode.upper()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True

    def update(self):
        self.screen.fill((255, 228, 236))  # Light pink background

        square_size = 50
        spacing = 10
        start_x = (self.screen.get_width() - (5 * (square_size + spacing))) // 2
        start_y = 100

        for i, word in enumerate(self.already_attempts):
            for j, letter in enumerate(word):
                color = (128, 128, 128)
                if letter == self.target_word[j]:
                    color = (0, 255, 0)
                elif letter in self.target_word:
                    color = (255, 255, 0)

                x_pos = start_x + j * (square_size + spacing)
                y_pos = start_y + i * (square_size + spacing)
                pygame.draw.rect(self.screen, color, pygame.Rect(x_pos, y_pos, square_size, square_size),
                                 border_radius=8)

                text_surface = self.font.render(letter, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x_pos + square_size // 2, y_pos + square_size // 2))
                self.screen.blit(text_surface, text_rect)

        if not self.game_over:
            input_y = start_y + len(self.already_attempts) * (square_size + spacing)
            for j in range(5):
                x_pos = start_x + j * (square_size + spacing)
                pygame.draw.rect(self.screen, (211, 211, 211), pygame.Rect(x_pos, input_y, square_size, square_size),
                                 border_radius=8)  # Light gray
                if j < len(self.user_input):
                    text_surface = self.font.render(self.user_input[j], True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(x_pos + square_size // 2, input_y + square_size // 2))
                    self.screen.blit(text_surface, text_rect)

    def render(self):
        self.update()

        # Display message
        message_surface = self.font.render(self.message, True, (0, 0, 0))
        message_rect = message_surface.get_rect(center=(self.screen.get_width() // 2, self.message_y))
        self.screen.blit(message_surface, message_rect)

        # Draw "Return to Menu" button
        pygame.draw.rect(self.screen, (180, 50, 50), self.return_button, border_radius=8)
        btn_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.return_button.center)
        self.screen.blit(btn_text, btn_rect)

        # Show restart message if game is over
        if self.game_over:
            restart_message = self.font.render("Press ENTER for a new game", True, (0, 0, 0))
            restart_rect = restart_message.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
            self.screen.blit(restart_message, restart_rect)

    def reset_game(self):
        self.already_attempts = []
        self.user_input = ""
        self.target_word = random.choice(self.word_list)
        self.message = "Guess the word!"
        self.game_over = False
        self.return_to_menu = False
