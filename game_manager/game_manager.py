import pygame
from components.menu.menu import Menu
from components.game.game import Game
from components.cutscene.one import One

MENU = "menu"
GAME = "game"
CUTSCENE_ONE = "one"


class Settings:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game Manager Example")

        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)


class GameManager:
    def __init__(self):
        self.settings = Settings()
        self.components = {
            MENU : Menu(self, self.settings),
            GAME : Game(self, self.settings),
            CUTSCENE_ONE : One(self, self.settings),
        }
        self.current_component = MENU 

    def switch_to(self, component_name):
        if component_name in self.components:
            self.current_component = component_name

    def run(self):
        while True:
            current_component = self.components[self.current_component]
            current_component.mainloop()
