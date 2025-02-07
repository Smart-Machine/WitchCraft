import sys
import pygame


class Menu:
    def __init__(self, manager, settings):
        self.settings = settings
        self.manager = manager
        self.font = pygame.font.Font(None, 36)
        self.title_text = self.font.render(
            "Press Space to Start Game", True, self.settings.WHITE
        )

    def mainloop(self):
        from game_manager.game_manager import CUTSCENE_ONE

        self.settings.screen.fill(self.settings.BLACK)
        self.settings.screen.blit(
            self.title_text,
            (self.settings.width // 3, self.settings.height // 2),
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.switch_to(CUTSCENE_ONE)
