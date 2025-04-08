import pygame
import random
from games.game import Game


class TriviaGame(Game):
    def __init__(self, screen):
        super().__init__(screen)
        
        # here we write all the questions + answers. the "answer" is the correct option's index (0,1,2,3)
        self.questions = [
            {
                'question': "What is the capital of France?",
                'choices': ["Berlin", "Madrid", "Paris", "Rome"],
                'answer': 2  
            },
            {
                'question': "Who wrote '1984'?",
                'choices': ["George Orwell", "Aldous Huxley", "Mark Twain", "J.K. Rowling"],
                'answer': 0
            },
            {
                'question': "Who won the Eurovision in 2018?",
                'choices': ["Italy", "England", "Israel", "Russia"],
                'answer': 2
            },
            {
                'question': "How many bones do sharks have?",
                'choices': ["17", "150", "206", "0"],
                'answer': 3
            },
            {
                'question': "What is the largest planet in our solar system?",
                'choices': ["Earth", "Mars", "Jupiter", "Saturn"],
                'answer': 2
            },
            {
                'question': "What is the largest island?",
                'choices': ["Greenland", "Madagascar","Honshu",  "New Guinea"],
                'answer': 0
            },
            {
                'question': "What is the highest mountain in the world?",
                'choices': ["Everest", "Mount Hermon", "Godwin Austen", "Nuptse"],
                'answer': 0
            },
            {
                'question': "What is 5 + 7?",
                'choices': ["11", "12", "13", "14"],
                'answer': 1
            }
        ]
        
        self.current_question = 0  # this tells us what question we are showing right now
        self.score = 0             # how many points the player got
        self.running = True        # when game is running, this is true
        self.font = pygame.font.Font(None, 50)  # big font for questions
        self.button_font = pygame.font.Font(None, 36)  # smaller font for buttons
        self.message = ""  # defines a message variable
        
        self.return_button = pygame.Rect(10, 10, 180, 50)  # red button to go back to main menu
        self.playagain_button = pygame.Rect(300, 340, 250, 50)  # button that shows after game over
        self.end_return_button = pygame.Rect(300, 420, 250, 50) # the button that show in the end

        self.game_over_active = False

        # these 4 are the answer buttons
        self.choice_buttons = [
            pygame.Rect(100, 200, 600, 50),
            pygame.Rect(100, 270, 600, 50),
            pygame.Rect(100, 340, 600, 50),
            pygame.Rect(100, 410, 600, 50),
        ]
        
        self.return_to_menu = False  # used by the game engine to know we wanna go back

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check if we clicked the red return to menu button
            if self.game_over_active:
                if self.return_button.collidepoint(event.pos) or self.end_return_button.collidepoint(event.pos):
                    self.return_to_menu = True
                    self.running = False
            else:
                if self.return_button.collidepoint(event.pos):
                    self.return_to_menu = True
                    self.running = False
            
            # check if we clicked one of the 4 answer buttons
            for i, button in enumerate(self.choice_buttons):
                if button.collidepoint(event.pos) and self.current_question < len(self.questions):
                    # check if answer is correct
                    if i == self.questions[self.current_question]['answer']:
                        self.score += 1
                        self.message = "Correct!"
                    else:
                        self.message = "Incorrect!"
                    
                    # go to next question
                    self.current_question += 1
                    
                    # if there are no more questions
                    if self.current_question >= len(self.questions):
                        self.game_over_active = True
                        self.message = f"Game Over! Final score: {self.score}/{len(self.questions)}"
                        self.running = False
                        return  # super important!! this stops the click from pressing play again instantly

        # this part checks if user clicks the "Play Again" button after game ended
        if self.current_question >= len(self.questions):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.playagain_button.collidepoint(event.pos):
                    # restart everything
                    self.current_question = 0
                    self.score = 0
                    self.running = True
                    
        # ESC button = go back to menu anytime
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.return_to_menu = True
                self.running = False

    def update(self):
        pass  # we don’t really need to update anything every frame in trivia


    def render(self):
        # Start of design changes
        self.screen.fill((255, 245, 230))  # Creamy white background for a warm, soft appearance
        # End of design changes
        
        # Display the current question
        if self.current_question < len(self.questions):
            pygame.draw.rect(self.screen, (180, 50, 50), self.return_button, border_radius=8)
            btn_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
            btn_rect = btn_text.get_rect(center=self.return_button.center)
            self.screen.blit(btn_text, btn_rect)
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

            # Display the message (Correct! or Incorrect!)
            if self.message == "Correct!":
                message_surface = self.font.render(self.message, True, (60, 179, 113))  # Black text for the message
                self.screen.blit(message_surface, (335, 480))   
            if self.message == "Incorrect!":
                message_surface = self.font.render(self.message, True, (180, 50, 50))  # Black text for the message
                self.screen.blit(message_surface, (335, 480))  

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
            pygame.draw.rect(self.screen, (180, 50, 50), self.end_return_button, border_radius=8)
            return_text = self.button_font.render("Return to Menu", True, (255, 255, 255))
            return_rect = return_text.get_rect(center=self.end_return_button.center)
            self.screen.blit(game_over_surface, (200, 250))  # Centered game over message
            self.screen.blit(return_text, return_rect)
            self.screen.blit(playagain_text, playagain_rect)  # Centered Play Again button text

        
