import pygame
import os
from game_engine import GameEngine
from games.wordle.wordle_game import WordleGame
from games.snake.snake_game import SnakeGame  # Import Snake game
from games.trivia.trivia_game import TriviaGame  # Import Trivia game

class MainMenu:
    def __init__(self, screen):
        self.screen = screen


        # 🎮 Load pixelated retro font
        self.font = pygame.font.Font(os.path.join("assets", "press_start.ttf"), 20)

        # GameBoy greenish-gray theme
        self.bg_color = (156, 189, 156)
        self.btn_border = (60, 80, 60)
        self.btn_fill = (110, 140, 110)
        self.text_color = (30, 30, 30)

        self.wordle_button = pygame.Rect(240, 200, 320, 60)
        self.snake_button = pygame.Rect(240, 300, 320, 60)
        self.trivia_button = pygame.Rect(240, 400, 320, 60)
        self.shutdown_button = pygame.Rect(750, 10, 40, 40) 


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.wordle_button.collidepoint(event.pos):
                return "Wordle"
            elif self.snake_button.collidepoint(event.pos):
                return "Snake"
            elif self.trivia_button.collidepoint(event.pos):
                return "Trivia"
            elif self.shutdown_button.collidepoint(event.pos):
                pygame.quit()
                os._exit(0)  

    def render(self):
        self.screen.fill(self.bg_color)


        pygame.draw.rect(self.screen, self.btn_fill, self.wordle_button, border_radius=10)
        pygame.draw.rect(self.screen, self.btn_fill, self.snake_button, border_radius=10)
        pygame.draw.rect(self.screen, self.btn_fill, self.trivia_button, border_radius=10)
        pygame.draw.rect(self.screen, (100, 120, 100), (50, 40, 700, 520), 8, border_radius=15)

        # Buttons
        pygame.draw.rect(self.screen, self.btn_fill, self.wordle_button, border_radius=5)
        pygame.draw.rect(self.screen, self.btn_border, self.wordle_button, 3, border_radius=5)

        pygame.draw.rect(self.screen, self.btn_fill, self.snake_button, border_radius=5)
        pygame.draw.rect(self.screen, self.btn_border, self.snake_button, 3, border_radius=5)

        pygame.draw.rect(self.screen, self.btn_fill, self.trivia_button, border_radius=5)
        pygame.draw.rect(self.screen, self.btn_border, self.trivia_button, 3, border_radius=5)

        # 🔴 Shutdown Button
        pygame.draw.rect(self.screen, (200, 50, 50), self.shutdown_button, border_radius=6)
        pygame.draw.circle(self.screen, (255, 255, 255), self.shutdown_button.center, 10, 2)
        pygame.draw.line(self.screen, (255, 255, 255), (self.shutdown_button.centerx, self.shutdown_button.top + 6), (self.shutdown_button.centerx, self.shutdown_button.centery - 3), 2)

        # Title
        title_font = pygame.font.Font(os.path.join("assets", "press_start.ttf"), 24)
        title = title_font.render("GAMEBOY MENU", True, self.text_color)
        self.screen.blit(title, title.get_rect(center=(400, 100)))

        # Button Text
        wordle_text = self.font.render("PLAY WORDLE", True, self.text_color)
        snake_text = self.font.render("PLAY SNAKE", True, self.text_color)
        trivia_text = self.font.render("PLAY TRIVIA", True, self.text_color)

        trivia_text_rect = trivia_text.get_rect(center=self.trivia_button.center)
        self.screen.blit(trivia_text, trivia_text_rect)
        self.screen.blit(wordle_text, wordle_text.get_rect(center=self.wordle_button.center))
        self.screen.blit(snake_text, snake_text.get_rect(center=self.snake_button.center))

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    engine = GameEngine()
    menu = MainMenu(engine.screen)

    # 🎵 Load & play retro background music
    music_path = os.path.join("assets", "menu_music.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    while engine.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.running = False

            selected_game = menu.handle_event(event)
            if selected_game == "Wordle":
                pygame.mixer.music.stop()
                engine.load_game(WordleGame)
                engine.run()
                pygame.mixer.music.play(-1)
            elif selected_game == "Snake":
                pygame.mixer.music.stop()
                engine.load_game(SnakeGame)
                engine.run()

            elif selected_game == "Trivia":
                pygame.mixer.music.stop()
                engine.load_game(TriviaGame)
                engine.run()
                pygame.mixer.music.play(-1)


        menu.render()
        pygame.display.flip()
