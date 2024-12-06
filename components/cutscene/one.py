import sys
import pygame

from .common.utills import typewriter_effect

# TODO: export this logic to Cutscene class


class One:
    def __init__(self, manager, settings):
        self.settings = settings
        self.manager = manager
        self.font = pygame.font.Font(None, 32)
        self.witch_image = pygame.image.load(
            "components/cutscene/assets/cutscene_one_witch.png"
        )
        self.witch_image = pygame.transform.scale(self.witch_image, (650, 650))

        self.text = """
            (Narator): You have no clue about who you are... 
            That doesn't bother you for some reason. You are still as happy as one can be, 
            and with a wide and adorable smile you are looking around. You find yourself in a 
            quite, and yet unfamilier place. How strange, you don't have any memories about 
            your past, not a single one. But you know for sure just one thing, you are a MAGE.
            And so you take your first steps to face the unknown and learn more about the beautiful
            world that waits for you ahead.
        """
        self.is_content_animated = False
        self.is_text_animated = False
        self.rect = pygame.Rect(
            50,
            self.settings.height - 100,
            self.settings.width - 100,
            self.settings.height - 700,
        )

    def mainloop(self):
        from game_manager.game_manager import GAME

        self.settings.screen.fill(self.settings.BLACK)
        self.settings.screen.blit(self.witch_image, (90, 50))
        if not self.is_content_animated:
            typewriter_effect(
                self.settings.screen,
                self.rect,
                self.text,
                self.font,
                self.settings.WHITE,
                50,
                (35, 35, 35),
            )
            self.is_content_animated = True
        else:
            pygame.draw.rect(
                self.settings.screen, (35, 35, 35), self.rect, border_radius=20
            )
            self.settings.screen.blit(
                self.font.render("Press SPACE to continue", True, self.settings.WHITE),
                (self.rect.topleft[0] + 10, self.rect.topleft[1] + 10),
            )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.switch_to(GAME)
