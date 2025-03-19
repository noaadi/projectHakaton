import pygame
import random
from games.game import Game


class WordleGame(Game):
    """Implements the Wordle game logic."""

    def __init__(self, screen):
        super().__init__(screen)
        self.word_list = ["APPLE", "BANANA", "CHERRY"]
        self.target_word = random.choice(self.word_list)
        self.user_input = ""
        self.font = pygame.font.Font(None, 50)
        self.message = "Guess the word!"

    def handle_event(self, event):
        """Handles user input for word guessing."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.user_input.upper() == self.target_word:
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
        """Updates the game logic (if needed)."""
        pass

    def render(self):
        """Renders the game screen."""
        self.screen.fill((0, 0, 0))

        # Render user input
        text_surface = self.font.render(self.user_input, True, (255, 255, 255))
        self.screen.blit(text_surface, (350, 250))

        # Render message
        message_surface = self.font.render(self.message, True, (255, 200, 0))
        self.screen.blit(message_surface, (300, 350))
