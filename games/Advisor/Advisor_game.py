import pygame
import random
from games.game import Game

MOODS = ["Happy", "Sad", "Stressed", "Motivated"]
from advices import ADVICES


class Advisor(Game):
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)

        self.current_screen = "mood_select"
        self.selected_mood = None
        self.current_advice = None

        self.mood_buttons = []
        self.new_advice_button = pygame.Rect(250, 300, 300, 60)
        self.return_button = pygame.Rect(10, 10, 220, 40)

        self.return_to_menu = False
        self.running = True

        # Colors
        self.bg_color = (156, 189, 156)  # Same as Snake Game's background color
        self.text_color = (20, 30, 20)  # Same as Snake Game's text color
        self.btn_color = (100, 160, 120)
        self.ui_color = (60, 80, 60)

    def get_random_advice(self, mood_index):
        filtered = [a['advice'] for a in ADVICES if a['category'] == mood_index]
        return random.choice(filtered) if filtered else "No advice found."

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_screen == "mood_select":
                for btn_rect, mood_index in self.mood_buttons:
                    if btn_rect.collidepoint(event.pos):
                        self.selected_mood = mood_index
                        self.current_advice = self.get_random_advice(mood_index)
                        self.current_screen = "advice"
                        break
                if self.return_button.collidepoint(event.pos):
                    self.return_to_menu = True
                    self.running = False

            elif self.current_screen == "advice":
                if self.new_advice_button.collidepoint(event.pos):
                    self.current_advice = self.get_random_advice(self.selected_mood)

                if self.return_button.collidepoint(event.pos):
                    self.current_screen = "mood_select"
                    self.selected_mood = None
                    self.current_advice = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.return_to_menu = True
                self.running = False

    def update(self):
        pass

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def render(self):
        self.screen.fill(self.bg_color)
        if self.current_screen == "mood_select":
            self.render_mood_screen()
        elif self.current_screen == "advice":
            self.render_advice_screen()

    def render_mood_screen(self):
        title = self.font.render("How are you feeling?", True, self.text_color)
        self.screen.blit(title, (180, 80))

        self.mood_buttons = []
        for i, mood in enumerate(MOODS):
            btn_rect = pygame.Rect(150, 120 + i * 80, 400, 60)
            pygame.draw.rect(self.screen, self.ui_color, btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.text_color, btn_rect, 2, border_radius=8)
            mood_text = self.button_font.render(mood, True, (255, 255, 255))
            self.screen.blit(mood_text, mood_text.get_rect(center=btn_rect.center))
            self.mood_buttons.append((btn_rect, i))

        # Return to Menu button (bottom-left corner)
        pygame.draw.rect(self.screen, self.ui_color, self.return_button, border_radius=6)
        pygame.draw.rect(self.screen, self.text_color, self.return_button, 2, border_radius=6)
        return_text = self.button_font.render("RETURN TO MENU", True, self.bg_color)
        self.screen.blit(return_text, return_text.get_rect(center=self.return_button.center))

    def render_advice_screen(self):
        wrapped = self.wrap_text(self.current_advice, self.font, 600)
        y_offset = 80  # Shift everything down by 80 pixels
        y = y_offset + 100
        for line in wrapped:
            text_surf = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surf, (100, y))
            y += text_surf.get_height() + 10

        # Lapidos label
        lapidos_label = self.font.render(" - 'Lapidos'", True, self.text_color)
        self.screen.blit(lapidos_label, (100, y_offset))

        pygame.draw.rect(self.screen, self.btn_color, self.new_advice_button, border_radius=8)
        button_text = self.button_font.render("Give me advice", True, (255, 255, 255))
        self.screen.blit(button_text, button_text.get_rect(center=self.new_advice_button.center))

        pygame.draw.rect(self.screen, self.ui_color, self.return_button, border_radius=6)
        pygame.draw.rect(self.screen, self.text_color, self.return_button, 2, border_radius=6)
        return_text = self.button_font.render("RETURN TO MENU", True, self.bg_color)
        self.screen.blit(return_text, return_text.get_rect(center=self.return_button.center))
