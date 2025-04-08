### 🧠 Trivia Game 🧩
A fun and interactive trivia game built with Python and Pygame. Test your knowledge across a variety of topics and compete for the highest score. This game is designed as part of a modular game engine with return-to-menu and play-again functionality.

### 📦 Features

- Multiple trivia questions with multiple-choice answers

Correct and incorrect answer feedback with score updates

End-of-game summary showing final score

Return-to-menu button available at all times

Option to restart the game once finished

Customizable font and colors for a smooth user experience

Class-based structure, making it easy to integrate or extend

### 🎮 How to Play

Click on one of the four choices to select your answer

The game will display whether your answer is correct or incorrect

Answer all the questions to finish the game

After completing the trivia, you can click "Play Again" to restart or "Return to Menu" to exit

## 🧠 How the Code Works This is a subclass of Game that handles:

### 🔁 __init__
Initializes the screen, sets up questions with multiple-choice answers, and stores the correct answer index.

Sets up a font for displaying text and buttons for interaction.

Initializes UI elements like the "Return to Menu" and "Play Again" buttons.

### 🧩 handle_event(event)
Handles mouse clicks for selecting answers, interacting with the "Return to Menu" button, and clicking "Play Again" after a game over.

Allows users to press the ESC key to exit the game and return to the menu at any time.

### 🔄 update()
This function doesn’t update anything each frame, as trivia is not a dynamic, constantly updating game.

### 🎨 render()

* Draws the current question and answer choices on the screen.
* Implements a soft green hover effect for the answer buttons.
* Shows the final score and a "Play Again" button after all questions are answered.
* Draws the current question and answer choices on the screen.
* Implements a soft green hover effect for the answer buttons.
* Shows the final score and a "Play Again" button after all questions are answered.
