import pygame
import sys

class GameEngine:
    """Manages the game loop and execution."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("GameBoy Collection")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_game = None

    def load_game(self, game_class):
        """Load and start a new game."""
        self.current_game = game_class(self.screen)

    def run(self):
        """Main game loop."""
        while self.running:
            self.screen.fill((30, 30, 30))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.current_game:
                    self.current_game.handle_event(event)

            if self.current_game:
                self.current_game.update()
                self.current_game.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
