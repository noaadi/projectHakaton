import pygame
import random
from games.game import Game


class DinoRun(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # צבעים
        self.bg_color = (200, 200, 180)
        self.dino_color = (50, 50, 50)  # Color for the dino
        self.obs_color = (0, 150, 0)

        # קרקע
        self.ground_y = 320

        # דינוזואר (using basic shapes instead of an image)
        self.dino_width = 40
        self.dino_height = 40
        self.dino = pygame.Rect(100, self.ground_y - self.dino_height, self.dino_width, self.dino_height)
        self.dino_vel_y = 0
        self.gravity = 1
        self.jump_strength = -15
        self.is_jumping = False

        # מכשולים
        self.obstacles = []
        self.obstacle_timer = 0
        self.obstacle_interval = 1500  # אלפיות שנייה
        self.speed = 6

        # פונט
        self.font = pygame.font.Font(pygame.font.match_font('arial'), 28)
        self.score = 0
        self.game_over = False

        # כפתור חזרה
        self.return_button = pygame.Rect(10, 10, 180, 50)
        self.button_font = pygame.font.Font(None, 32)
        self.return_to_menu = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.is_jumping and not self.game_over:
                self.dino_vel_y = self.jump_strength
                self.is_jumping = True
            elif self.game_over and event.key == pygame.K_RETURN:
                self.reset_game()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True

    def update(self):
        if not self.game_over:
            self.dino_vel_y += self.gravity
            self.dino.y += self.dino_vel_y

            if self.dino.y >= self.ground_y - self.dino.height:
                self.dino.y = self.ground_y - self.dino.height
                self.is_jumping = False

            # יצירת מכשולים
            self.obstacle_timer += self.clock.get_time()
            if self.obstacle_timer >= self.obstacle_interval:
                self.obstacle_timer = 0
                obstacle_height = random.randint(30, 60)
                obstacle = pygame.Rect(800, self.ground_y - obstacle_height, 20, obstacle_height)
                self.obstacles.append(obstacle)

            # תזוזת מכשולים
            for obstacle in self.obstacles:
                obstacle.x -= self.speed

            # בדיקת התנגשויות
            for obstacle in self.obstacles:
                if self.dino.colliderect(obstacle):
                    self.game_over = True

            # ניקוי מכשולים שיצאו מהמסך
            self.obstacles = [obs for obs in self.obstacles if obs.x > -30]

            # ניקוד
            self.score += 1

        self.clock.tick(60)

    def render(self):
        self.update()
        self.screen.fill(self.bg_color)

        # קרקע
        pygame.draw.rect(self.screen, (100, 80, 60), (0, self.ground_y, 800, 5))

        # דינוזואר - Draw the dino using basic shapes
        self.draw_dino(self.dino.x, self.dino.y)

        # מכשולים
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, self.obs_color, obs)

        # טקסט ניקוד
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (600, 20))

        # כפתור חזרה
        pygame.draw.rect(self.screen, (180, 50, 50), self.return_button, border_radius=8)
        btn_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
        self.screen.blit(btn_text, btn_text.get_rect(center=self.return_button.center))

        # הודעת סיום
        if self.game_over:
            msg = self.font.render("Game Over! Press ENTER to restart", True, (0, 0, 0))
            self.screen.blit(msg, msg.get_rect(center=(400, 160)))

    def reset_game(self):
        self.dino.y = self.ground_y - self.dino.height
        self.dino_vel_y = 0
        self.is_jumping = False
        self.obstacles = []
        self.obstacle_timer = 0
        self.score = 0
        self.game_over = False
        self.return_to_menu = False

    def draw_dino(self, x, y):
        # Body: Use an ellipse-like shape (just a rectangle with rounded corners)
        pygame.draw.rect(self.screen, self.dino_color, pygame.Rect(x, y, self.dino_width, self.dino_height),
                         border_radius=5)

        # Head: Smaller oval shape (circle)
        pygame.draw.circle(self.screen, self.dino_color, (x + self.dino_width // 2, y - self.dino_height // 2),
                           self.dino_width // 3)

        # Eyes (simple circles)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (x + self.dino_width // 2 - 10, y - self.dino_height // 2 - 10), 5)  # Left eye
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (x + self.dino_width // 2 + 10, y - self.dino_height // 2 - 10), 5)  # Right eye
        pygame.draw.circle(self.screen, (0, 0, 0), (x + self.dino_width // 2 - 10, y - self.dino_height // 2 - 10),
                           3)  # Left pupil
        pygame.draw.circle(self.screen, (0, 0, 0), (x + self.dino_width // 2 + 10, y - self.dino_height // 2 - 10),
                           3)  # Right pupil

        # Tail: A simple triangular shape
        pygame.draw.polygon(self.screen, self.dino_color, [(x + self.dino_width, y + self.dino_height // 2),
                                                           (x + self.dino_width + 30, y + self.dino_height // 2 + 20),
                                                           (x + self.dino_width + 30, y + self.dino_height // 2 - 20)])

        # Legs: Draw simple rectangles (as legs)
        pygame.draw.rect(self.screen, self.dino_color,
                         pygame.Rect(x + 5, y + self.dino_height - 10, 12, 18))  # Left leg
        pygame.draw.rect(self.screen, self.dino_color,
                         pygame.Rect(x + self.dino_width - 17, y + self.dino_height - 10, 12, 18))  # Right leg

        # Arms: Use small rectangles for arms
        pygame.draw.rect(self.screen, self.dino_color, pygame.Rect(x - 8, y + self.dino_height / 4, 12, 8))  # Left arm
        pygame.draw.rect(self.screen, self.dino_color,
                         pygame.Rect(x + self.dino_width - 4, y + self.dino_height / 4, 12, 8))  # Right arm

        # Adding a simple mouth (as a curved line or a small rectangle)
        pygame.draw.arc(self.screen, (0, 0, 0),
                        pygame.Rect(x + self.dino_width // 3, y - self.dino_height // 2 + 5, self.dino_width // 3, 10),
                        3.14, 2 * 3.14, 2)

