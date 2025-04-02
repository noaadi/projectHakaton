# 🐍 Snake GameBoy Edition 🎮

A retro-style Snake game coded with Python and Pygame, themed like a GameBoy cartridge, including nostalgic fonts, colors, and sound effects. Built as part of a modular game engine with return-to-menu support.

---

## 📦 Features

- classic snake gameplay in a GameBoy skin
- sound effects for eating, dying, and selecting
- score display, pause/game over screen, try again + menu button
- fully integrated into a larger game engine menu system
- pixel-font visuals and GameBoy color palette
- self-contained class-based structure (perfect for integration or mods)

---

## 🎮 How to Play

- arrow keys `← ↑ → ↓` control the snake
- eat red blocks (food) to grow and score points
- avoid walls and don’t bite yourself
- click `RETURN TO MENU` to quit
- click `TRY AGAIN` if you crash

---

## 🧠 How the Code Works

This is a subclass of `Game` that handles:

### 🔁 `__init__`
- sets up the screen, snake data, food position, fonts and UI buttons
- loads sound effects (`eat.wav`, `death.wav`, `select.wav`)
- sets up GameBoy colors and the snake's starting body and direction

### 🧱 `generate_food()`
- picks a random (x, y) spot in a grid that matches the snake block size

### ⌨️ `handle_event(event)`
- handles arrow key presses to change snake direction (no reverse allowed)
- handles mouse clicks on menu or try again buttons
- plays a "select" sound on key press or button press

### 🔄 `update()`
- moves the snake’s head in current direction
- checks for collisions (wall or self)
- eats food (plays sound + grows) or continues moving

### 🎨 `render()`
- draws snake body
- draws eyes on the snake head (directional!)
- draws the food square
- draws the score using retro font
- draws `RETURN TO MENU` button always
- if dead:
  - shows overlay
  - shows “GAME OVER”
  - shows score + try again button

---
