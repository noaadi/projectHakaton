import pygame
import random
from games.game import Game  # Import the base Game class

class SnakeGame(Game):
    """Classic Snake game using Pygame."""

    def __init__(self, screen):
        super().__init__(screen)
        self.block_size = 20
        self.width, self.height = 800, 600
        self.snake = [(100, 100), (90, 100), (80, 100)]  # Snake body (list of positions)
        self.direction = (self.block_size, 0)  # Moving right
        self.food = self.generate_food()
        self.font = pygame.font.Font(None, 50)

    def generate_food(self):
        """Generates a new food position randomly on the grid."""
        return (random.randint(0, (self.width // self.block_size) - 1) * self.block_size,
                random.randint(0, (self.height // self.block_size) - 1) * self.block_size)

    def handle_event(self, event):
        """Handles keyboard input for controlling the snake."""
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
        """Updates the snake's position and checks for collisions."""
        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # Check for wall collision
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            self.running = False  # End game if hitting a wall

        # Check for self-collision
        if head in self.snake:
            self.running = False  # End game if colliding with itself

        self.snake.insert(0, head)  # Move snake forward

        # Check if food is eaten
        if head == self.food:
            self.food = self.generate_food()  # Generate new food
        else:
            self.snake.pop()  # Remove last segment if no food eaten

    def render(self):
        """Draws the game objects on the screen."""
        self.screen.fill((0, 0, 0))  # Background color

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], self.block_size, self.block_size))

        # Draw food
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food[0], self.food[1], self.block_size, self.block_size))

        # Display score
        score_text = self.font.render(f"Score: {len(self.snake) - 3}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
