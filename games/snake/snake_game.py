import pygame
import random
import os
from games.game import Game


class SnakeGame(Game):
    """Retro-styled Snake GameBoy Edition."""

    def __init__(self, screen):
        super().__init__(screen)
        self.block_size = 20
        self.width, self.height = 800, 600
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = (self.block_size, 0)
        self.next_direction = self.direction
        self.clock = pygame.time.Clock()
        self.speed = 10

        # 🎮 Fonts & buttons
        self.font = pygame.font.Font(
            os.path.join("assets", "press_start.ttf"), 16)
        self.button_font = pygame.font.Font(
            os.path.join("assets", "press_start.ttf"), 14)
        self.sfx_eat = pygame.mixer.Sound("assets/sfx/eat.wav")
        self.sfx_death = pygame.mixer.Sound("assets/sfx/death.wav")
        self.sfx_select = pygame.mixer.Sound("assets/sfx/select.wav")

        self.return_button = pygame.Rect(10, 10, 220, 40)
        self.try_again_button = pygame.Rect(300, 250, 200, 50)

        self.food = self.generate_food()
        self.game_over = False

        # GameBoy color palette
        self.bg_color = (156, 189, 156)
        self.snake_color = (33, 45, 33)
        self.food_color = (204, 40, 40)
        self.ui_color = (60, 80, 60)
        self.text_color = (20, 30, 20)

    def generate_food(self):
        max_x = self.width // self.block_size
        max_y = self.height // self.block_size
        x = random.randint(0, max_x - 1) * self.block_size
        y = random.randint(0, max_y - 1) * self.block_size
        return (x, y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True
                self.running = False
            if self.game_over and self.try_again_button.collidepoint(event.pos):
                self.sfx_select.play()
                self.__init__(self.screen)

        if not self.game_over and event.type == pygame.KEYDOWN:
            self.sfx_select.play()
            if event.key == pygame.K_UP and self.direction != (0, self.block_size):
                self.next_direction = (0, -self.block_size)
            elif event.key == pygame.K_DOWN and self.direction != (0, -self.block_size):
                self.next_direction = (0, self.block_size)
            elif event.key == pygame.K_LEFT and self.direction != (self.block_size, 0):
                self.next_direction = (-self.block_size, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-self.block_size, 0):
                self.next_direction = (self.block_size, 0)

    def update(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head = (self.snake[0][0] + self.direction[0],
                self.snake[0][1] + self.direction[1])

        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            self.sfx_death.play()
            self.game_over = True
            return

        if head in self.snake:
            self.sfx_death.play()
            self.game_over = True
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.sfx_eat.play()
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def render(self):
        self.clock.tick(self.speed)
        self.screen.fill(self.bg_color)


        # Draw snake
        for i, segment in enumerate(self.snake):
            x, y = segment
            pygame.draw.rect(self.screen, self.snake_color,
                            pygame.Rect(x, y, self.block_size, self.block_size))

            if i == 0:
                # Draw face on the head
                eye_size = 4
                eye_offset_x = 4
                eye_offset_y = 4

                # Adjust eyes based on direction
                dx, dy = self.direction
                if dx != 0:  # Left or Right
                    eye1 = (x + 4, y + 5)
                    eye2 = (x + 12, y + 5)
                else:  # Up or Down
                    eye1 = (x + 5, y + 4)
                    eye2 = (x + 5, y + 12)

                pygame.draw.rect(self.screen, (255, 255, 255),
                                (*eye1, eye_size, eye_size))
                pygame.draw.rect(self.screen, (255, 255, 255),
                                (*eye2, eye_size, eye_size))

                # Draw food
                pygame.draw.rect(self.screen, self.food_color,
                                pygame.Rect(self.food[0], self.food[1], self.block_size, self.block_size))

                # Score (GameBoy LCD text)
                score_text = self.font.render(
                    f"SCORE: {len(self.snake) - 3}", True, self.text_color)
                self.screen.blit(score_text, (10, 60))

                # Return to Menu button
                pygame.draw.rect(self.screen, self.ui_color,
                                self.return_button, border_radius=6)
                pygame.draw.rect(self.screen, self.text_color,
                                self.return_button, 2, border_radius=6)
        btn_text = self.button_font.render(
            "RETURN TO MENU", True, self.bg_color)
        self.screen.blit(btn_text, btn_text.get_rect(
            center=self.return_button.center))

        # Game Over overlay
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(220)
            overlay.fill(self.bg_color)
            self.screen.blit(overlay, (0, 0))

            over_text = self.font.render("GAME OVER", True, self.text_color)
            score_text = self.font.render(
                f"SCORE: {len(self.snake) - 3}", True, self.text_color)

            self.screen.blit(over_text, over_text.get_rect(
                center=(self.width // 2, 150)))
            self.screen.blit(score_text, score_text.get_rect(
                center=(self.width // 2, 200)))

            pygame.draw.rect(self.screen, self.ui_color,
                             self.try_again_button, border_radius=8)
            pygame.draw.rect(self.screen, self.text_color,
                             self.try_again_button, 2, border_radius=8)

            try_again_text = self.button_font.render(
                "TRY AGAIN", True, self.bg_color)
            self.screen.blit(try_again_text, try_again_text.get_rect(
                center=self.try_again_button.center))
