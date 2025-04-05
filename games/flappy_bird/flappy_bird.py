import pygame
import random
from games.game import Game


class FlappyBird(Game):
    def __init__(self, screen):
        """Initialize the Flappy Bird game."""
        super().__init__(screen)
        self.width, self.height = 800, 600
        self.bird_x, self.bird_y = 100, self.height // 2
        self.bird_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.pipe_width = 70
        self.pipe_speed = 5
        self.speed_multiplier = 1.0
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.reset_game()
        self.return_to_menu = False
        # Initialize sound effects
        self.ScoreSfx = pygame.mixer.Sound("assets/sfx/FlappyBirdScore.mp3")
        self.DeathSfx = pygame.mixer.Sound("assets/sfx/FlappyBirdDeath.mp3")
        self.JumpSfx = pygame.mixer.Sound("assets/sfx/FlappyBirdJump.mp3")

        # Particle effects (Explosion effect when the bird dies)
        self.particles = []

        # return button
        self.return_button = pygame.Rect(10, 10, 180, 50)
        self.button_font = pygame.font.Font(None, 36)

    def reset_game(self):
        """Reset the game after the player loses."""
        self.bird_y = self.height // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_speed = 5
        self.speed_multiplier = 1.0
        self.spawn_pipe()
        self.return_to_menu = False
        # Reset particles
        self.particles = []

    def spawn_pipe(self):
        """Create a new pipe with a random gap size."""
        pipe_height = random.randint(50, 400)
        pipe_gap = random.randint(140, 200)  # Randomized gap between top and bottom pipe
        self.pipes.append([self.width, pipe_height, pipe_gap])

    def handle_event(self, event):
        """Handle player input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                if self.game_over:
                    self.reset_game()
                else:
                    self.bird_velocity = self.jump_strength
                    self.JumpSfx.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True
        if event.type == pygame.QUIT:
            self.running = False

    def update(self):
        """Update the game state."""
        if self.game_over:
            self.update_particles()  # Update the particles when the game is over
            return

        # Apply gravity
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        # Increase speed over time
        self.speed_multiplier = 1.0 + (self.score / 10)
        self.speed_multiplier = min(self.speed_multiplier, 3.0)

        # Move pipes to the left
        for pipe in self.pipes:
            pipe[0] -= self.pipe_speed * self.speed_multiplier

        # Remove pipes that have moved off-screen
        if self.pipes[0][0] + self.pipe_width < 0:
            self.pipes.pop(0)
            self.spawn_pipe()
            self.score += 1
            self.ScoreSfx.play()

        # Create bird hitbox
        bird_rect = pygame.Rect(self.bird_x, self.bird_y, 30, 30)

        # Check for collisions with pipes
        for pipe_x, pipe_height, pipe_gap in self.pipes:
            top_pipe = pygame.Rect(pipe_x, 0, self.pipe_width, pipe_height)
            bottom_pipe = pygame.Rect(pipe_x, pipe_height + pipe_gap, self.pipe_width,
                                      self.height - pipe_height - pipe_gap)
            if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                self.DeathSfx.play()
                self.game_over = True
                self.create_explosion(self.bird_x + 15, self.bird_y + 15)  # Trigger explosion effect

        # Check if bird hits the ground or flies too high
        if self.bird_y >= self.height or self.bird_y <= 0:
            self.DeathSfx.play()
            self.game_over = True
            self.create_explosion(self.bird_x + 15, self.bird_y + 15)  # Trigger explosion effect

    def create_explosion(self, x, y):
        """Create an explosion effect (particles) at the bird's position."""
        for _ in range(50):  # Generate 50 particles
            velocity_x = random.uniform(-3, 3)
            velocity_y = random.uniform(-3, 3)
            lifetime = random.randint(20, 40)  # Particle lifetime
            self.particles.append([x, y, velocity_x, velocity_y, lifetime])

    def update_particles(self):
        """Update particles during the game over state."""
        for particle in self.particles[:]:
            particle[0] += particle[2]  # Move the particle in the x direction
            particle[1] += particle[3]  # Move the particle in the y direction
            particle[4] -= 1  # Decrease the lifetime of the particle
            if particle[4] <= 0:
                self.particles.remove(particle)  # Remove particle if its lifetime is over

    def render(self):
        """Render everything on the screen."""
        self.clock.tick(60)
        self.screen.fill((135, 206, 250))  # Sky blue background

        # Draw pipes
        for pipe_x, pipe_height, pipe_gap in self.pipes:
            # Main pipes
            pygame.draw.rect(self.screen, (0, 200, 0), (pipe_x, 0, self.pipe_width, pipe_height))  # Top pipe
            pygame.draw.rect(self.screen, (0, 200, 0), (
                pipe_x, pipe_height + pipe_gap, self.pipe_width, self.height - pipe_height - pipe_gap))  # Bottom pipe

            # Pipe caps (for Mario-style pipes)
            cap_width = self.pipe_width + 20
            cap_height = 20
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe_x - 10, pipe_height - cap_height, cap_width, cap_height))
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe_x - 10, pipe_height + pipe_gap, cap_width, cap_height))

        # Draw the bird
        self.draw_bird(self.bird_x, self.bird_y)

        # Draw particles (explosion effect)
        self.draw_particles()

        # Score display
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 75))

        # Game over text
        if self.game_over:
            game_over_text = self.font.render("Game Over! Press Space To Restart", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.width // 4, self.height // 2))

        # Draw "Return to Menu" button
        pygame.draw.rect(self.screen, (180, 50, 50), self.return_button, border_radius=8)
        btn_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.return_button.center)
        self.screen.blit(btn_text, btn_rect)

        pygame.display.flip()

    def draw_bird(self, x, y):
        """Draws a simple bird with a body, eyes, and a beak."""
        bird_color = (255, 215, 0)  # Golden yellow
        eye_color = (0, 0, 0)  # Black eyes
        beak_color = (255, 100, 0)  # Orange beak

        # Adds bird body (circle)
        pygame.draw.circle(self.screen, bird_color, (x + 15, y + 15), 15)

        # Adds bird eye
        pygame.draw.circle(self.screen, (255, 255, 255), (x + 22, y + 10), 5)  # White eye
        pygame.draw.circle(self.screen, eye_color, (x + 24, y + 10), 3)  # Black pupil

        # Adds beak
        pygame.draw.polygon(self.screen, beak_color, [(x + 30, y + 15), (x + 40, y + 12), (x + 30, y + 10)])

    def draw_particles(self):
        """Draw the particles (explosion effect)."""
        for particle in self.particles:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(particle[0]), int(particle[1])), 5)
