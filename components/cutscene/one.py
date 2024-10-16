import sys
import pygame

from game_manager.game_manager import GAME 

class One:
    def __init__(self, manager, settings):
        self.settings = settings
        self.manager = manager
        self.font = pygame.font.Font(None, 36)
        self.one_text = self.font.render(
            "Some text", True, self.settings.WHITE
        )

    def mainloop(self):
        self.settings.screen.fill(self.settings.BLACK)
        self.settings.screen.blit(
            self.one_text,
            (self.settings.screen_width // 4, self.settings.screen_height // 2),
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.switch_to(GAME)
