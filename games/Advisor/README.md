# 💬 Advisor GameBoy Edition 🎮

A nostalgic GameBoy-style advice generator built with Python and Pygame. Choose your mood and get wise, funny, or thoughtful tips with a click — all wrapped in a retro UI inspired by classic handheld consoles. Fully integrated with your modular game engine and return-to-menu functionality.

---

## 📦 Features

- pixel-perfect GameBoy-style UI and font
- creamy background, soft greens, retro text shadows
- mood selection screen with 4 different categories
- randomized advice for each mood
- "Lapidos" label for signature charm
- return-to-menu support on both screens
- fully class-based for easy integration or expansion

---

## 🧠 Mood Categories

*Choose your vibe and get a matching piece of advice:*

- Chill 🧘 – for calming or mindful thoughts
- Motivated ⚡ – for power-up moments
- Social 🗣️ – for wisdom in conversations
- Random 🎲 – for chaotic neutral tips

---

## 🎮 How to Use

* Choose a mood from the 4-button menu

* Click "Give me advice" to get a random tip in that category

* Click "RETURN TO MENU" to go back to the main game screen

* Hit ESC at any time to return via keyboard

### 🔁 __init__
- loads fonts and sets up buttons
- picks a random advice from the matching category
- prepares button and text sizes with scaling for UI

### 🎯 handle_event(event)
- handles mouse clicks and escape key
- updates advice when clicking the “Give me advice” button
- navigates back to menu on button or key press

### 🖼️ render_mood_screen()
- displays the 4 moods with custom buttons
- renders mood names and a “RETURN TO MENU” button

### 🧠 render_advice_screen()
- shows the Inspirational “Lapidos” label 😍
- wraps advice text neatly
- displays the “Give me advice” and “RETURN TO MENU” buttons
---

### ✨ Built With

* Python 🐍
* Pygame 🎮
* Retro passion ❤️

By Tom Girshovsky