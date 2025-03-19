import pygame
from abc import ABC, abstractmethod

class Game(ABC):
    """Abstract base class for all games."""

    def __init__(self, screen):
        self.screen = screen
        self.running = True

    @abstractmethod
    def handle_event(self, event):
        """Handle user input (must be implemented in child classes)."""
        pass

    @abstractmethod
    def update(self):
        """Update game logic (must be implemented in child classes)."""
        pass

    @abstractmethod
    def render(self):
        """Render game visuals (must be implemented in child classes)."""
        pass
