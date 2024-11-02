import pygame

from components.menu.menu import Menu
from components.game.game import Game
from components.cutscene.one import One
from components.game.models.board import Board

MENU = "menu"
GAME = "game"
CUTSCENE_ONE = "one"


class Settings:
    def __init__(
        self,
        width=840,
        height=840,
        candy_width=32,
        candy_height=32,
        scoreboard_height=50,
    ):
        self.width = width 
        self.height = height 
        self.candy_width = candy_width 
        self.candy_height = candy_height
        self.scoreboard_height = scoreboard_height 
        self.window_size = (self.width, self.height + self.scoreboard_height)
    
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Game Manager Example")

        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)


class GameManager:
    def __init__(self):
        self.settings = Settings()
        self.board = Board(self.settings)
        self.components = {
            MENU: Menu(self, self.settings),
            GAME: Game(self, self.settings, self.board),
            CUTSCENE_ONE: One(self, self.settings),
        }
        self.current_component = MENU

    def switch_to(self, component_name):
        if component_name in self.components:
            self.current_component = component_name

    def run(self):
        while True:
            current_component = self.components[self.current_component]
            current_component.mainloop()
