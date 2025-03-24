import pygame
import random
from games.game import Game

class TriviaGame(Game):
    def __init__(self, screen):
        super().__init__(screen)
        
        # Questions and choices data
        self.questions = [
            {
                'question': "What is the capital of France?",
                'choices': ["Berlin", "Madrid", "Paris", "Rome"],
                'answer': 2  # The index of the correct answer (0-based)
            },
            {
                'question': "Who wrote '1984'?",
                'choices': ["George Orwell", "Aldous Huxley", "Mark Twain", "J.K. Rowling"],
                'answer': 0
            },
            {
                'question': "What is the largest planet in our solar system?",
                'choices': ["Earth", "Mars", "Jupiter", "Saturn"],
                'answer': 2
            },
            {
                'question': "What is 5 + 7?",
                'choices': ["11", "12", "13", "14"],
                'answer': 1
            }
        ]
        
        self.current_question = 0
        self.score = 0
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 36)
        self.message = "Answer the question!"
        
        # Return button always in the top left corner
        self.return_button = pygame.Rect(10, 10, 180, 50)

        # Play Again button
        self.playagain_button = pygame.Rect(300, 340, 250, 50)

        # Button rectangles for choices
        self.choice_buttons = [
            pygame.Rect(100, 200, 600, 50),  # Option 1
            pygame.Rect(100, 270, 600, 50),  # Option 2
            pygame.Rect(100, 340, 600, 50),  # Option 3
            pygame.Rect(100, 410, 600, 50),  # Option 4
        ]
        
        self.return_to_menu = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True
                self.running = False
            
            # Check if user clicked any answer button
            for i, button in enumerate(self.choice_buttons):
                if button.collidepoint(event.pos) and self.current_question < len(self.questions):
                    if i == self.questions[self.current_question]['answer']:
                        self.score += 1
                        self.message = "Correct!"
                    else:
                        self.message = "Incorrect!"
                    
                    self.current_question += 1
                    if self.current_question >= len(self.questions):
                        self.message = f"Game Over! Final score: {self.score}/{len(self.questions)}"
                        # Don't quit, just stay on the Game Over screen
                        self.running = False
                        
        if self.current_question >= len(self.questions):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.playagain_button.collidepoint(event.pos):
                    # Reset the game state to start over
                    self.current_question = 0
                    self.score = 0
                    self.message = "Answer the question!"
                    self.running = True
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.return_to_menu = True
                self.running = False

    def update(self):
        pass

    def render(self):
        # Start of design changes
        self.screen.fill((255, 245, 230))  # Creamy white background for a warm, soft appearance
        # End of design changes
        
        # Display the current question
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]['question']

            # Start of text wrapping logic
            def wrap_text(text, font, max_width):
                words = text.split(' ')
                lines = []
                current_line = ""

                for word in words:
                    # Check if adding the word exceeds the max width
                    test_line = current_line + " " + word if current_line else word
                    test_width, _ = font.size(test_line)
                    if test_width <= max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)

                return lines

            # Get wrapped question text
            wrapped_question = wrap_text(question, self.font, 600)  # 600 is the max width for the question
            # End of text wrapping logic

            # Start of question text color and rendering
            question_color = (30, 100, 40)  # Darker green for the question text
            y_offset = 100  # Starting y position for the question text
            for line in wrapped_question:
                question_surface = self.font.render(line, True, question_color)
                self.screen.blit(question_surface, (100, y_offset))
                y_offset += question_surface.get_height() + 10  # Space between lines
            # End of question text color and rendering

            # Display choices as buttons
            choices = self.questions[self.current_question]['choices']
            for i, button in enumerate(self.choice_buttons):
                # Start of button hover effect and color changes
                if button.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (180, 220, 150), button, border_radius=8)  # Soft green on hover
                else:
                    pygame.draw.rect(self.screen, (100, 150, 100), button, border_radius=8)  # Muted green button
                # End of button hover effect and color changes

                choice_text = self.button_font.render(f"{i + 1}. {choices[i]}", True, (255, 255, 255))  # White text for clarity
                btn_rect = choice_text.get_rect(center=button.center)
                self.screen.blit(choice_text, btn_rect)
        else:
            # Start of Game Over screen design
            game_over_surface = self.font.render(self.message, True, (255, 165, 0))  # Bright orange for message
            pygame.draw.rect(self.screen, (60, 179, 113), self.playagain_button, border_radius=8)  # Soft green Play Again button
            playagain_text = self.button_font.render("Play Again!", True, (255, 255, 255))  # White text for button
            playagain_rect = playagain_text.get_rect(center=self.playagain_button.center)
            self.screen.blit(game_over_surface, (200, 250))  # Centered game over message
            self.screen.blit(playagain_text, playagain_rect)  # Centered Play Again button text

            # Start of moving Return to Menu button below the Play Again button
            return_button_position = pygame.Rect(300, 420, 250, 50)  # Below the Play Again button
            pygame.draw.rect(self.screen, (240, 100, 60), return_button_position, border_radius=8)  # Warm red for "Return to Menu"
            return_button_text = self.button_font.render("Return to Menu", True, (255, 255, 255))  # White text for the button
            return_button_rect = return_button_text.get_rect(center=return_button_position.center)
            self.screen.blit(return_button_text, return_button_rect)
            # End of moving Return to Menu button below the Play Again button

        # Always show Return to Menu button at the top left of the screen during the game
        pygame.draw.rect(self.screen, (180, 50, 50), self.return_button, border_radius=8)
        btn_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.return_button.center)
        self.screen.blit(btn_text, btn_rect)
