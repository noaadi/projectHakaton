import pygame
import os
import requests
from games.game import Game

class Number_Facts(Game):

    def __init__(self, screen):
        super().__init__(screen)
        self.text = ""
        self.day_input = ""
        self.month_input = ""
        self.num_input = ""
        self.font = pygame.font.Font(os.path.join("assets", "press_start.ttf"), 20)
        self.game_over = False
        self.num_fact = False
        self.date_fact = False
        self.return_button = pygame.Rect(40, 10, 300, 50)
        self.play_again_button = pygame.Rect(300, 500, 200, 50)
        self.date_button = pygame.Rect(200, 200, 200, 50)
        self.num_button = pygame.Rect(450, 200, 250, 50)

    def get_fact_num(self, num):
        url = f"http://numbersapi.com/{num}?json"
        try:
            response = requests.get(url)
            if response.ok:
                data = response.json()
                return data["text"]
            else:
                return "Failed to fetch trivia."
        except Exception as e:
            return f"Error: {str(e)}"

    def get_fact_date(self, day, month):
        url = f"http://numbersapi.com/{month}/{day}/date?json"
        try:
            response = requests.get(url)
            if response.ok:
                data = response.json()
                return data["text"]
            else:
                return "Failed to fetch trivia."
        except Exception as e:
            return f"Error: {str(e)}"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True
                self.running = False
            elif self.game_over and self.play_again_button.collidepoint(event.pos):
                self.__init__(self.screen)
            elif self.num_button.collidepoint(event.pos):
                self.num_fact = True
                self.date_fact = False
                self.num_input = ""
            elif self.date_button.collidepoint(event.pos):
                self.date_fact = True
                self.num_fact = False
                self.day_input = ""
                self.month_input = ""

        if event.type == pygame.KEYDOWN and not self.game_over:
            if event.unicode.isdigit():
                if self.num_fact:
                    self.num_input += event.unicode
                    if len(self.num_input) >= 1:
                        self.text = self.get_fact_num(self.num_input)
                        self.num_input = ""

                elif self.date_fact:
                    if len(self.day_input) < 2:
                        self.day_input += event.unicode
                    elif len(self.month_input) < 2:
                        self.month_input += event.unicode
                    if len(self.day_input) == 2 and len(self.month_input) == 2:
                        day = int(self.day_input)
                        month = int(self.month_input)
                        self.text = self.get_fact_date(day, month)
                        self.day_input = ""
                        self.month_input = ""

    def update(self):
        if not self.running:
            self.game_over = True

        if self.text:
            self.num_fact = False
            self.date_fact = False
            self.running = False

    def wrap_text(self, text, x, y, max_width, color=(0, 0, 0), line_height=30):
        """
        Wraps the text to fit within the given width.
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)  # Add the last line

        for i, line in enumerate(lines):
            line_surface = self.font.render(line, True, color)
            self.screen.blit(line_surface, (x, y + i * line_height))

    def render(self):
        self.screen.fill((255, 255, 255))

        # Welcome Text
        welcome_text = "This game gives you fun facts about numbers and dates!"
        self.wrap_text(welcome_text, 60, 100, 600)  # Wrap text to fit screen width

        if self.num_fact:
            input_surface = self.font.render(f"Number: {self.num_input}", True, (0, 0, 0))
            self.screen.blit(input_surface, (60, 150))
        elif self.date_fact:
            input_surface = self.font.render(f"Day: {self.day_input}  Month: {self.month_input}", True, (0, 0, 0))
            self.screen.blit(input_surface, (60, 150))

        # Fact Text
        if self.text:
            self.wrap_text(self.text, 60, 300, 600)  # Wrap fact text to fit screen width

        # Buttons
        pygame.draw.rect(self.screen, (200, 200, 200), self.return_button, border_radius=8)
        pygame.draw.rect(self.screen, (0, 0, 0), self.return_button, 2)
        self.screen.blit(self.font.render("RETURN TO MENU", True, (0, 0, 0)),
                         self.font.render("RETURN TO MENU", True, (0, 0, 0)).get_rect(center=self.return_button.center))

        pygame.draw.rect(self.screen, (180, 255, 180), self.num_button, border_radius=8)
        pygame.draw.rect(self.screen, (0, 0, 0), self.num_button, 2)
        self.screen.blit(self.font.render("NUMBER FACT", True, (0, 0, 0)),
                         self.font.render("NUMBER FACT", True, (0, 0, 0)).get_rect(center=self.num_button.center))

        pygame.draw.rect(self.screen, (180, 180, 255), self.date_button, border_radius=8)
        pygame.draw.rect(self.screen, (0, 0, 0), self.date_button, 2)
        self.screen.blit(self.font.render("DATE FACT", True, (0, 0, 0)),
                         self.font.render("DATE FACT", True, (0, 0, 0)).get_rect(center=self.date_button.center))

        if self.game_over:
            pygame.draw.rect(self.screen, (200, 200, 200), self.play_again_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.play_again_button, 2)
            self.screen.blit(self.font.render("PLAY AGAIN", True, (0, 0, 0)),
                             self.font.render("PLAY AGAIN", True, (0, 0, 0)).get_rect(center=self.play_again_button.center))
