import random
import pygame


class Candy:
    def __init__(self, row_num, col_num, settings):
        self.settings = settings
        self.screen = self.settings.screen

        # list of candy colors
        # self.candy_colors = [
        #     "blue",
        #     "green",
        #     "orange",
        #     "pink",
        #     "purple",
        #     "red",
        #     "teal",
        #     "yellow",
        # ]

        # candy size
        self.candy_size = (self.settings.candy_width, self.settings.candy_height)

        # set the candy"s position on the board
        self.row_num = row_num
        self.col_num = col_num

        # for future self: 
        # the 12 is the number of tiles in a row in the match3.png image
        # while the 9 is the number of tile in a col in the match3.png image
        self.image = pygame.image.load("media/match3.png").subsurface((
            random.choice(range(1, 12)) * self.settings.candy_width,
            random.choice(range(1, 9)) * self.settings.candy_height,
            self.settings.candy_width,
            self.settings.candy_height
        ))
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
