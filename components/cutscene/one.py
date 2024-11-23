import sys
import pygame

from .common.utills import typewriter_effect

#TODO: export this logic to Cutscene class

class One:
    def __init__(self, manager, settings):
        self.settings = settings
        self.manager = manager
        self.font = pygame.font.Font(None, 36)
        # self.one_text = self.font.render("Some text", True, self.settings.WHITE)

        self.text = "Hello, Stranger! It seems that we have something important to discuss here... The matter is that you are in dangeor and should be catious about the upfollowing things that are dangerous"
        self.rect = pygame.Rect(100, self.settings.height - 100, self.settings.width - 200, self.settings.height - 700)

    def mainloop(self):
        from game_manager.game_manager import GAME

        self.settings.screen.fill(self.settings.BLACK)
        typewriter_effect(self.settings.screen, self.rect, self.text, self.font, self.settings.WHITE, 80, (35, 35, 35)) 
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.switch_to(GAME)
