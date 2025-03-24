import pygame
import random
from games.game import Game

class SnakeGame(Game):
    """Classic Snake game using Pygame."""

    def __init__(self, screen):
        super().__init__(screen)
        self.block_size = 20
        self.width, self.height = 800, 600
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = (self.block_size, 0)
        self.food = self.generate_food()
        self.font = pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()
        self.speed = 10

        # 🔁 Return to Menu Button
        self.return_button = pygame.Rect(10, 10, 180, 50)
        self.button_font = pygame.font.Font(None, 36)

    def generate_food(self):
        return (
            random.randint(0, (self.width // self.block_size) - 1) * self.block_size,
            random.randint(0, (self.height // self.block_size) - 1) * self.block_size
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True
                self.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, self.block_size):
                self.direction = (0, -self.block_size)
            elif event.key == pygame.K_DOWN and self.direction != (0, -self.block_size):
                self.direction = (0, self.block_size)
            elif event.key == pygame.K_LEFT and self.direction != (self.block_size, 0):
                self.direction = (-self.block_size, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-self.block_size, 0):
                self.direction = (self.block_size, 0)

    def update(self):
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            self.running = False
        if head in self.snake:
            self.running = False

        self.snake.insert(0, head)

        if head == self.food:
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def render(self):
        self.clock.tick(self.speed)
        self.screen.fill((0, 0, 0))

        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], self.block_size, self.block_size))

        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food[0], self.food[1], self.block_size, self.block_size))

        score_text = self.font.render(f"Score: {len(self.snake) - 3}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 70))

        # 🔘 Draw Return Button
        pygame.draw.rect(self.screen, (180, 50, 50), self.return_button, border_radius=8)
        btn_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.return_button.center)
        self.screen.blit(btn_text, btn_rect)
