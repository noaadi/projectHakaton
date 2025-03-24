import pygame
from game_engine import GameEngine
from games.wordle.wordle_game import WordleGame
from games.snake.snake_game import SnakeGame  # Import Snake game
from games.trivia.trivia_game import TriviaGame  # Import Trivia game



class MainMenu:
    """Main menu screen with buttons for Wordle and Snake."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)

        # Define buttons for Wordle and Snake
        self.wordle_button = pygame.Rect(300, 200, 200, 60)
        self.snake_button = pygame.Rect(300, 300, 200, 60)
        self.trivia_button = pygame.Rect(300, 400, 200, 60)


    def handle_event(self, event):
        """Handles user interactions with the buttons."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.wordle_button.collidepoint(event.pos):
                return "Wordle"
            elif self.snake_button.collidepoint(event.pos):
                return "Snake"
            elif self.trivia_button.collidepoint(event.pos):
                return "Trivia"
            

    def render(self):
        """Renders the menu with buttons."""
        self.screen.fill((30, 30, 30))  # Background color

        # Draw buttons
        pygame.draw.rect(self.screen, (50, 150, 250), self.wordle_button, border_radius=10)
        pygame.draw.rect(self.screen, (50, 250, 100), self.snake_button, border_radius=10)
        pygame.draw.rect(self.screen, (136, 150, 69), self.trivia_button, border_radius=10)


        # Render button text
        wordle_text = self.font.render("Play Wordle", True, (255, 255, 255))
        wordle_text_rect = wordle_text.get_rect(center=self.wordle_button.center)
        self.screen.blit(wordle_text, wordle_text_rect)

        snake_text = self.font.render("Play Snake", True, (255, 255, 255))
        snake_text_rect = snake_text.get_rect(center=self.snake_button.center)
        self.screen.blit(snake_text, snake_text_rect)

        trivia_text = self.font.render("Play Trivia", True, (255, 255, 255))
        trivia_text_rect = trivia_text.get_rect(center=self.trivia_button.center)
        self.screen.blit(trivia_text, trivia_text_rect)


if __name__ == "__main__":
    engine = GameEngine()
    menu = MainMenu(engine.screen)

    while engine.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.running = False

            selected_game = menu.handle_event(event)
            if selected_game == "Wordle":
                engine.load_game(WordleGame)
                engine.run()
            elif selected_game == "Snake":
                engine.load_game(SnakeGame)
                engine.run()
            elif selected_game == "Trivia":
                engine.load_game(TriviaGame)
                engine.run()

        menu.render()
        pygame.display.flip()
