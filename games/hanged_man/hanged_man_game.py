import pygame
import random
import os
import random
from games.game import Game


"""# Hangman Game 🎮

This is a simple hangman game I made using Python and Pygame. It's kind of like the classic hangman game, but with some graphics and buttons. You have to guess the word before the stickman gets fully drawn.

## What's in the game?

- You get a random word to guess
- You can see which letters you already guessed
- You only have 6 chances to guess wrong
- If you win, you see a win screen. If you lose, you get a game over screen.
- There's a button to try again or go back to the menu

## How to run it

1. First, make sure you have Python installed (preferably Python 3.8 or higher).
2. Also install Pygame if you don’t have it yet:

```bash
pip install pygame"""




class Hanged_man(Game):

    "hanged man game for the gamboy"



    def __init__(self,screen):
        super().__init__(screen)
        self.words=["word","work","tel aviv","cop","nitzanim"]
        self.word=random.choice(self.words)
        self.guessed=set()
        self.in_word=set()
        self.attempts=6
        self.sub_word="_"*len(self.word)
        letter1=random.choice(range(0, len(self.word)))
        letter2=random.choice(range(0, len(self.word)))
        while letter2==letter1:
            letter2 = random.choice(range(0, len(self.word)))

        self.guess_in_word(random.choice(self.word[letter1]))
        self.guess_in_word(random.choice(self.word[letter2]))
        self.font = pygame.font.Font(os.path.join("assets", "press_start.ttf"), 20)
        self.game_over=False
        self.return_button = pygame.Rect(40, 10, 300, 50)
        self.try_again_button = pygame.Rect(300, 400, 200, 50)

    #drawin the hanged man and the hanging place
    def draw_hangman(self):
        """Draws an enhanced hangman with more detail, colors, and smooth shading."""
        screen_width = self.screen.get_width()
        base_x = screen_width - 200
        base_y = 300
        color_dark = (50, 50, 50)  # Dark gray for gallows
        color_black = (0, 0, 0)  # Black for hangman
        color_red = (200, 0, 0)  # Red for losing effect

        # Gallows structure
        if self.attempts <= 5:
            pygame.draw.rect(self.screen, color_dark, (base_x, base_y - 10, 110, 10))  # Base
        if self.attempts <= 4:
            pygame.draw.rect(self.screen, color_dark, (base_x + 45, base_y - 200, 10, 200))  # Vertical Pole
        if self.attempts <= 3:
            pygame.draw.rect(self.screen, color_dark, (base_x + 45, base_y - 200, 120, 10))  # Top Bar
        if self.attempts <= 2:
            pygame.draw.rect(self.screen, color_dark, (base_x + 145, base_y - 200, 5, 30))  # Rope

        # Hangman parts
        if self.attempts <= 1:
            pygame.draw.circle(self.screen, color_black, (base_x + 148, base_y - 150), 20, 5)  # Head

        if self.attempts <= 0:
            pygame.draw.line(self.screen, color_black, (base_x + 148, base_y - 130), (base_x + 148, base_y - 80),
                             6)  # Body
            pygame.draw.line(self.screen, color_black, (base_x + 148, base_y - 120), (base_x + 128, base_y - 100),
                             5)  # Left Arm
            pygame.draw.line(self.screen, color_black, (base_x + 148, base_y - 120), (base_x + 168, base_y - 100),
                             5)  # Right Arm
            pygame.draw.line(self.screen, color_black, (base_x + 148, base_y - 80), (base_x + 128, base_y - 50),
                             5)  # Left Leg
            pygame.draw.line(self.screen, color_black, (base_x + 148, base_y - 80), (base_x + 168, base_y - 50),
                             5)  # Right Leg

            # **Face details when losing**
            pygame.draw.line(self.screen, color_red, (base_x + 140, base_y - 160), (base_x + 145, base_y - 155),
                             3)  # Left eye
            pygame.draw.line(self.screen, color_red, (base_x + 145, base_y - 160), (base_x + 140, base_y - 155), 3)
            pygame.draw.line(self.screen, color_red, (base_x + 152, base_y - 160), (base_x + 157, base_y - 155),
                             3)  # Right eye
            pygame.draw.line(self.screen, color_red, (base_x + 157, base_y - 160), (base_x + 152, base_y - 155), 3)
            pygame.draw.arc(self.screen, color_black, (base_x + 138, base_y - 145, 20, 10), 3.14, 0, 3)  # Sad mouth

    # cheking if the guess is in the word if it isnt than we update the attempts and the guesses and update the subword
    def guess_in_word(self,guess):
        if guess in self.word:
            self.in_word.add(guess)
            self.change_sub_word(guess)

        else:
            self.guessed.add(guess)
            self.attempts-=1


#making the subword into a list type object so we can make changes on her than we make it string again
    def change_sub_word(self, guess):
        sub_word_list = list(self.sub_word)
        for i in range(len(self.word)):
            if guess == self.word[i]:
                sub_word_list[i] = guess
        self.sub_word = "".join(sub_word_list)

    def handle_event(self, event):
        if event.type==pygame.KEYDOWN and self.game_over==False:#cheking if somone pressed on the keyboard
            if event.unicode.isalpha():#if its a to z
                guess = event.unicode.lower()#getting it to lower case
                self.guess_in_word(guess)#cheking if the guess is in the word if it isnt than we update the attempts and the guesses and update the subword

    #cheking if somone want to retrun to the menu or to play again
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.collidepoint(event.pos):
                self.return_to_menu = True
                self.running = False
            if self.game_over and self.try_again_button.collidepoint(event.pos):
                self.__init__(self.screen)

#checking if all the ltters are guessed using 2 sets
    def all_letters_guessed(self):
        letters_in_word = set(self.word.replace(" ", ""))  #removing spaces and making the word a set
        return letters_in_word.issubset(self.in_word)#cheking if all the words that guessed correcly is whole the word

    #finish condtions
    def update(self):
        if self.attempts == 0:
            self.game_over = True
        elif self.all_letters_guessed():
            self.game_over = True

#screen clearing and blit to the screen
    def render(self):
        self.screen.fill((255, 255, 255))
        self.draw_hangman()
        word_display=self.sub_word
        word_surface = self.font.render(word_display, True, (0, 0, 0))
        self.screen.blit(word_surface, (200, 150))
        guessed_display=f"Guesses: {",".join(self.guessed)}"
        guessed_surface=self.font.render(guessed_display,True,(0,0,0))
        self.screen.blit(guessed_surface,(200,350))
        attempts_surface = self.font.render(f"Attempts left: {self.attempts}", True, (255, 0, 0))
        self.screen.blit(attempts_surface, (200, 200))
        pygame.draw.rect(self.screen, (0, 0, 0), self.return_button, 2, border_radius=6)
        btn_text = self.font.render("RETURN TO MENU", True, (0, 0, 0))
        self.screen.blit(btn_text, btn_text.get_rect(center=self.return_button.center))

        if self.game_over==True:#if the game is over
            result_text = "YOU WIN!" if self.attempts > 0 else f"GAME OVER!:You lost"
            result_surface = self.font.render(result_text, True, (255, 0, 0))
            self.screen.blit(result_surface, (200, 250))#the results
            word_text=f"Word: {self.word}"
            word_surface=self.font.render(word_text,True,(255,0,0))
            self.screen.blit(word_surface,(200,300))
            pygame.draw.rect(self.screen, (200, 200, 200), self.try_again_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), self.try_again_button, 2, border_radius=8)
            try_again_text = self.font.render("TRY AGAIN", True, (0, 0, 0))
            self.screen.blit(try_again_text, try_again_text.get_rect(center=self.try_again_button.center))

        