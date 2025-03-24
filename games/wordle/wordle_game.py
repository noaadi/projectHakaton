import pygame
import random
from games.game import Game


class WordleGame(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.word_list = ["ONE", "TWO", "THREE"]
        self.target_word = random.choice(self.word_list)
        self.already_attempts = []
        self.max_attempts = 6
        self.user_input = ""
        self.font = pygame.font.Font(None, 50)
        self.message = "Guess the word!"
        self.running = True

        # Return button
        self.return_button = pygame.Rect(10, 10, 180, 50)
        self.button_font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True
                self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(self.user_input) == len(self.target_word):
                    self.already_attempts.append(self.user_input.upper())
                    self.user_input = ""
                if self.already_attempts[-1] == self.target_word:
                    self.message = "You Win!"
                    self.running = False
                else:
                    self.message = "Try Again!"
                self.user_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif len(self.user_input) < 5 and event.unicode.isalpha():
                self.user_input += event.unicode.upper()

    def update(self):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))

        # Render guess input
        input_surface = self.font.render(self.user_input, True, (255, 255, 255))
        self.screen.blit(input_surface, (350, 250))

        # Render message
        message_surface = self.font.render(self.message, True, (255, 200, 0))
        self.screen.blit(message_surface, (300, 350))

        # Draw Return to Menu button
        pygame.draw.rect(self.screen, (180, 50, 50), self.return_button, border_radius=8)
        btn_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.return_button.center)
        self.screen.blit(btn_text, btn_rect)
