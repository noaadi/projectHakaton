import pygame
import os
from game_engine import GameEngine
from games.hanged_man.hanged_man_game import Hanged_man
from games.wordle.wordle_game import WordleGame
from games.snake.snake_game import SnakeGame
from games.trivia.trivia_game import TriviaGame
from games.flappy_bird.flappy_bird import FlappyBird
from games.tic_tac_toe.Tic_tac_toe import TicTacToe
from games.number_api.Number_api import Number_Facts
from games.Advisor.Advisor_game import Advisor


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(os.path.join("assets", "press_start.ttf"), 16)
        self.icon_font = pygame.font.Font(os.path.join("assets", "press_start.ttf"), 18)

        self.bg_color = (156, 189, 156)
        self.btn_border = (60, 80, 60)
        self.btn_fill = (110, 140, 110)
        self.text_color = (30, 30, 30)

        self.shutdown_button = pygame.Rect(750, 10, 40, 40)
        self.vol_down_button = pygame.Rect(560, 10, 30, 30)
        self.vol_up_button = pygame.Rect(680, 10, 30, 30)
        self.vol_bar_rect = pygame.Rect(595, 12, 75, 26)

        self.games = [
            ("WORDLE", WordleGame),
            ("SNAKE", SnakeGame),
            ("TRIVIA", TriviaGame),
            ("FLAPPY BIRD", FlappyBird),
            ("TIC TAC TOE", TicTacToe),
            ("HANGED MAN", Hanged_man),
            ("INTERESTING FACT", Number_Facts),
            ("TAKE 'N ADVICE", Advisor)
        ]

        self.buttons = []
        self.scroll_offset = 0
        self.button_width = 180
        self.button_height = 60
        self.margin_x = 40
        self.margin_y = 20
        self.columns = 3

        self.build_buttons()

    def build_buttons(self):
        self.buttons.clear()
        for i, (label, _) in enumerate(self.games):
            row = i // self.columns
            col = i % self.columns
            x = 100 + col * (self.button_width + self.margin_x)
            y = 160 + row * (self.button_height + self.margin_y)
            self.buttons.append((label, pygame.Rect(x, y, self.button_width, self.button_height)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            if self.shutdown_button.collidepoint(event.pos):
                pygame.quit()
                os._exit(0)

            if self.vol_up_button.collidepoint(event.pos):
                current_vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(current_vol + 0.025, 1.0))

            if self.vol_down_button.collidepoint(event.pos):
                current_vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(current_vol - 0.025, 0.0))

            for i, (_, rect) in enumerate(self.buttons):
                if rect.collidepoint(x, y):
                    return self.games[i][0]

    def render(self):
        self.screen.fill(self.bg_color)
        pygame.draw.rect(self.screen, (100, 120, 100), (50, 40, 700, 520), 8, border_radius=15)

        title_font = pygame.font.Font(os.path.join("assets", "press_start.ttf"), 24)
        title = title_font.render("GAMEBOY MENU", True, self.text_color)
        self.screen.blit(title, title.get_rect(center=(400, 100)))

        for label, rect in self.buttons:
            scrolled_rect = rect.move(0, self.scroll_offset)
            pygame.draw.rect(self.screen, self.btn_fill, scrolled_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.btn_border, scrolled_rect, 3, border_radius=5)

            # render text with wrapping if needed
            full_text = f"PLAY {label.upper()}"
            text_surface = self.font.render(full_text, True, self.text_color)

            if text_surface.get_width() <= self.button_width - 10:
                # single line
                text_rect = text_surface.get_rect(center=scrolled_rect.center)
                self.screen.blit(text_surface, text_rect)
            else:
                # wrap into max 2 lines
                words = full_text.split()
                lines = ['']
                for word in words:
                    test_line = lines[-1] + (' ' if lines[-1] else '') + word
                    test_surface = self.font.render(test_line, True, self.text_color)
                    if test_surface.get_width() <= self.button_width - 10:
                        lines[-1] = test_line
                    else:
                        lines.append(word)

                lines = lines[:2]  # limit to 2 lines
                line_height = self.font.get_height()
                total_height = len(lines) * line_height
                start_y = scrolled_rect.centery - total_height // 2

                for i, line in enumerate(lines):
                    line_surface = self.font.render(line, True, self.text_color)
                    line_rect = line_surface.get_rect(center=(scrolled_rect.centerx, start_y + i * line_height))
                    self.screen.blit(line_surface, line_rect)

        # volume controls
        pygame.draw.rect(self.screen, (80, 80, 80), self.vol_down_button, border_radius=4)
        pygame.draw.rect(self.screen, (80, 80, 80), self.vol_up_button, border_radius=4)

        vol_down_icon = self.font.render("<", True, (255, 255, 255))
        vol_up_icon = self.font.render(">", True, (255, 255, 255))
        self.screen.blit(vol_down_icon, vol_down_icon.get_rect(center=self.vol_down_button.center))
        self.screen.blit(vol_up_icon, vol_up_icon.get_rect(center=self.vol_up_button.center))

        volume_label = self.font.render("VOLUME:", True, self.text_color)
        self.screen.blit(volume_label, (435, 17))

        pygame.draw.rect(self.screen, (200, 200, 200), self.vol_bar_rect, border_radius=6)
        volume = pygame.mixer.music.get_volume()
        fill_width = int(self.vol_bar_rect.width * volume)
        fill_rect = pygame.Rect(self.vol_bar_rect.left, self.vol_bar_rect.top, fill_width, self.vol_bar_rect.height)
        pygame.draw.rect(self.screen, (0, 200, 0), fill_rect, border_radius=6)

        pygame.draw.rect(self.screen, (200, 50, 50), self.shutdown_button, border_radius=6)
        pygame.draw.circle(self.screen, (255, 255, 255), self.shutdown_button.center, 10, 2)
        pygame.draw.line(self.screen, (255, 255, 255),
                         (self.shutdown_button.centerx, self.shutdown_button.top + 6),
                         (self.shutdown_button.centerx, self.shutdown_button.centery - 3), 2)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    engine = GameEngine()
    menu = MainMenu(engine.screen)

    music_path = os.path.join("assets", "menu_music.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    while engine.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.running = False

            selected_game = menu.handle_event(event)
            if selected_game:
                for label, game_cls in menu.games:
                    if selected_game == label:
                        pygame.mixer.music.stop()
                        engine.load_game(game_cls)
                        engine.run()
                        pygame.mixer.music.play(-1)

        menu.render()
        pygame.display.flip()
