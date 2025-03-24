import pygame
from abc import ABC, abstractmethod

class Game(ABC):
    """Abstract base class for all games."""

    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.return_to_menu = False  

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
