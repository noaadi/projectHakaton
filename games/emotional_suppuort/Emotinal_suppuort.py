import pygame
from openai import AzureOpenAI, BadRequestError
import os
from games.game import Game
from dotenv import load_dotenv
load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# --- Azure OpenAI Setup ---

endpoint = os.getenv("ENDPOINT_URL", "https://nitz-hackathon-2025.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", AZURE_OPENAI_API_KEY)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)


def ask(prompt, chat_history):
    chat_history.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

    completion = client.chat.completions.create(
        model=deployment,
        messages=chat_history,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    response = completion.choices[0].message.content.strip()
    if len(response) > 200:
        response = response[:200] + "..."
    chat_history.append({"role": "assistant", "content": [{"type": "text", "text": response}]})
    return response, chat_history


def is_safe_input(text):
    unsafe_keywords = ["kill myself", "end it all", "die", "suicide"]
    return not any(phrase in text.lower() for phrase in unsafe_keywords)


# --- Pygame Emotional Support Game ---
class EmotionalSupportGame(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.SysFont(None, 32)
        self.message = "Click the button for support ❤"
        self.return_button = pygame.Rect(40, 10, 300, 50)
        self.button_rect = pygame.Rect(250, 300, 300, 50)
        self.chat_history = [
            {"role": "system", "content": [{"type": "text",
                                            "text": "You are a comforting and empathetic assistant. Respond to emotional input with concise, gentle, and kind messages. Use no more than 2 sentences."}]}
        ]
        self.collecting_input = False
        self.user_input = ""

        # New loading-related variables
        self.loading = False
        self.loading_start_time = 0
        self.loading_message = "Loading"

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.message = "How are you feeling today?"
                self.collecting_input = True
                self.user_input = ""

        elif event.type == pygame.KEYDOWN and self.collecting_input:
            if event.key == pygame.K_RETURN:
                if is_safe_input(self.user_input):
                    self.loading = True
                    self.loading_start_time = pygame.time.get_ticks()
                    self.collecting_input = False
                else:
                    self.message = "That sounds serious. Please talk to someone you trust or a mental health professional. You matter."
                    self.collecting_input = False
                    self.user_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                self.user_input += event.unicode

    def update(self):
        if self.loading:
            now = pygame.time.get_ticks()
            dots = ((now - self.loading_start_time) // 500) % 4
            self.loading_message = "Loading" + "." * dots

            if now - self.loading_start_time > 1500:
                try:
                    self.message, self.chat_history = ask(self.user_input, self.chat_history)
                except BadRequestError:
                    self.message = "I'm really sorry you're feeling this way. Please talk to someone you trust or a professional."
                self.user_input = ""
                self.loading = False

    def render(self):
        self.screen.fill((30, 30, 60))

        # Show input field
        if self.collecting_input:
            input_surface = self.font.render(self.user_input, True, (255, 255, 255))
            self.screen.blit(input_surface, (100, 250))

        # Draw button
        pygame.draw.rect(self.screen, (70, 130, 180), self.button_rect, border_radius=10)
        button_text = self.font.render("Get Support", True, (0, 0, 0))
        self.screen.blit(button_text, (self.button_rect.x + 90, self.button_rect.y + 12))
        pygame.draw.rect(self.screen, (255, 255, 255), self.return_button, 2, border_radius=6)
        btn_text = self.font.render("RETURN TO MENU", True, (255, 255, 255))
        self.screen.blit(btn_text, btn_text.get_rect(center=self.return_button.center))

        # Show animated loading or regular message
        if self.loading:
            loading_surface = self.font.render(self.loading_message, True, (255, 255, 255))
            self.screen.blit(loading_surface, (100, 100))
        else:
            self.render_multiline_text(self.message, 100, 100, 600)

    def render_multiline_text(self, text, x, y, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        for i, line in enumerate(lines):
            line_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(line_surface, (x, y + i * 30))
