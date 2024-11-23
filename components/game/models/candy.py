import random
import pygame


class Candy:
    def __init__(self, row_num, col_num, settings):
        self.settings = settings
        self.screen = self.settings.screen

        self.candy_color_width = 32 
        self.candy_color_height = 32

        # list of candy colors
        self.candy_colors = [
            (i * self.candy_color_width, j * self.candy_color_height)
            for i in range(1, 12)
            for j in range(4, 9) # starting from the 4th one to avoid repetition
        ]

        # candy size
        self.candy_size = (self.settings.candy_width, self.settings.candy_height)

        # set the candy"s position on the board
        self.row_num = row_num
        self.col_num = col_num

        # for future self:
        # the 12 is the number of tiles in a row in the match3.png image
        # while the 9 is the number of tile in a col in the match3.png image
        self.color = random.choice(self.candy_colors)
        self.image = pygame.image.load("media/match3.png").subsurface(
            (
                *self.color,
                self.candy_color_width,
                self.candy_color_height
            )
        )
        self.image = pygame.transform.scale(self.image, self.candy_size)
        self.rect = self.image.get_rect()
        self.rect.left = col_num * self.settings.candy_width
        self.rect.top = row_num * self.settings.candy_height

        # assign a random image
        # self.color = random.choice(self.candy_colors)
        # image_name = f"media/swirl_{self.color}.png"
        # self.image = pygame.image.load(image_name)
        # self.image = pygame.transform.smoothscale(self.image, self.candy_size)
        # self.rect = self.image.get_rect()
        # self.rect.left = col_num * self.settings.candy_width
        # self.rect.top = row_num * self.settings.candy_height
    
    def __repr__(self):
        return f"Candy({self.color})"

    # draw the image on the screen
    def draw(self):
        self.screen.blit(self.image, self.rect)

    # snap the candy to its position on the board
    def snap(self):
        self.snap_row()
        self.snap_col()

    def snap_row(self):
        self.rect.top = self.row_num * self.settings.candy_height

    def snap_col(self):
        self.rect.left = self.col_num * self.settings.candy_width
