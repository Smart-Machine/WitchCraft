import sys
import pygame

from game_manager.game_manager import MENU, CUTSCENE_ONE 

class Game:
    def __init__(self, manager, settings):
        self.settings = settings
        self.manager = manager
        self.font = pygame.font.Font(None, 36)
        self.game_text = self.font.render(
            "Game - Press Esc to Go Back to Menu", True, self.settings.WHITE
        )

    def mainloop(self):
        self.settings.screen.fill(self.settings.BLACK)
        self.settings.screen.blit(
            self.game_text,
            (self.settings.screen_width // 4, self.settings.screen_height // 2),
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.switch_to(MENU)
                if event.key == pygame.K_1:
                    self.manager.switch_to(CUTSCENE_ONE)
