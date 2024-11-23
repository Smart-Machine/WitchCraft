import sys
import pygame

from .models.candy import Candy


class Game:
    def __init__(self, manager, settings, board):
        self.settings = settings
        self.manager = manager
        self.board = board

        self.score = 0
        self.moves = 0

        # self.font = pygame.font.Font(None, 36)
        # self.game_text = self.font.render(
        #     "Game - Press Esc to Go Back to Menu", True, self.settings.WHITE
        # )

        # candy that the user clicked on
        self.clicked_candy = None

        # the adjacent candy that will be swapped with the clicked candy
        self.swapped_candy = None

        # coordinates of the point where the user clicked on
        self.click_x = None
        self.click_y = None

        self.clock = pygame.time.Clock()

    def draw(self):
        # draw the background
        pygame.draw.rect(
            self.settings.screen,
            (0, 0, 0),
            (
                0,
                0,
                self.settings.width,
                self.settings.height + self.settings.scoreboard_height,
            ),
        )

        # draw the candies
        for row in self.board.board:
            for candy in row:
                candy.draw()

        # display the score and moves
        font = pygame.font.SysFont("Roboto Mono", 32)
        score_text = font.render(f"Mana: {self.score}", 1, (255, 255, 255))
        score_text_rect = score_text.get_rect(
            center=(
                self.settings.width / 2,
                self.settings.height + self.settings.scoreboard_height / 2,
            )
        )
        self.settings.screen.blit(score_text, score_text_rect)

        # moves_text = font.render(f"Moves: {self.moves}", 1, (255, 255, 255))
        # moves_text_rect = moves_text.get_rect(center=(self.settings.width * 3 / 4, self.settings.height + self.settings.scoreboard_height / 2))
        # self.settings.screen.blit(moves_text, moves_text_rect)

    # swap the positions of two candies
    def swap(self, candy1, candy2):
        temp_row = candy1.row_num
        temp_col = candy1.col_num

        candy1.row_num = candy2.row_num
        candy1.col_num = candy2.col_num

        candy2.row_num = temp_row
        candy2.col_num = temp_col

        # update the candies on the board list
        self.board.board[candy1.row_num][candy1.col_num] = candy1
        self.board.board[candy2.row_num][candy2.col_num] = candy2

        # snap them into their board positions
        candy1.snap()
        candy2.snap()

    # find neighboring candies that match the candy"s color
    def find_matches(self, candy, matches):
        # add the candy to the set
        matches.add(candy)

        # check the candy above if it"s the same color
        if candy.row_num > 0:
            neighbor = self.board.board[candy.row_num - 1][candy.col_num]
            if candy.color == neighbor.color and neighbor not in matches:
                matches.update(self.find_matches(neighbor, matches))

        # check the candy below if it"s the same color
        if candy.row_num < self.settings.height / self.settings.candy_height - 1:
            neighbor = self.board.board[candy.row_num + 1][candy.col_num]
            if candy.color == neighbor.color and neighbor not in matches:
                matches.update(self.find_matches(neighbor, matches))

        # check the candy to the left if it"s the same color
        if candy.col_num > 0:
            neighbor = self.board.board[candy.row_num][candy.col_num - 1]
            if candy.color == neighbor.color and neighbor not in matches:
                matches.update(self.find_matches(neighbor, matches))

        # check the candy to the right if it"s the same color
        if candy.col_num < self.settings.width / self.settings.candy_width - 1:
            neighbor = self.board.board[candy.row_num][candy.col_num + 1]
            if candy.color == neighbor.color and neighbor not in matches:
                matches.update(self.find_matches(neighbor, matches))

        return matches

    # return a set of at least 3 matching candies or an empty set
    def match_three(self, candy):
        matches = self.find_matches(candy, set())
        if len(matches) >= 3:
            return matches
        else:
            return set()

    def mainloop(self):
        from game_manager.game_manager import MENU, CUTSCENE_ONE

        # set of matching candies
        matches = set()
        for event in pygame.event.get():
            # detect kill game 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # detect key press 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.switch_to(MENU)
                if event.key == pygame.K_1:
                    self.manager.switch_to(CUTSCENE_ONE)
            # detect mouse click
            if self.clicked_candy is None and event.type == pygame.MOUSEBUTTONDOWN:
                # get the candy that was clicked on
                for row in self.board.board:
                    for candy in row:
                        if candy.rect.collidepoint(event.pos):
                            self.clicked_candy = candy
                            # save the coordinates of the point where the user clicked
                            self.click_x = event.pos[0]
                            self.click_y = event.pos[1]
            # detect mouse motion
            if self.clicked_candy is not None and event.type == pygame.MOUSEMOTION:
                # calculate the distance between the point the user clicked on
                # and the current location of the mouse cursor
                distance_x = abs(self.click_x - event.pos[0])
                distance_y = abs(self.click_y - event.pos[1])
                # reset the position of the swapped candy if direction of mouse motion changed
                if self.swapped_candy is not None:
                    self.swapped_candy.snap()
                # determine the direction of the neighboring candy to swap with
                if distance_x > distance_y and self.click_x > event.pos[0]:
                    direction = "left"
                elif distance_x > distance_y and self.click_x < event.pos[0]:
                    direction = "right"
                elif distance_y > distance_x and self.click_y > event.pos[1]:
                    direction = "up"
                else:
                    direction = "down"

                # if moving left/right, snap the clicked candy to its row position
                # otherwise, snap it to its col position
                if direction in ["left", "right"]:
                    self.clicked_candy.snap_row()
                else:
                    self.clicked_candy.snap_col()

                # if moving the clicked candy to the left,
                # make sureit"s not on the first col
                if direction == "left" and self.clicked_candy.col_num > 0:
                    # get the candy to the left
                    self.swapped_candy = self.board.board[self.clicked_candy.row_num][
                        self.clicked_candy.col_num - 1
                    ]
                    # move the two candies
                    self.clicked_candy.rect.left = (
                        self.clicked_candy.col_num * self.settings.candy_width - distance_x
                    )
                    self.swapped_candy.rect.left = (
                        self.swapped_candy.col_num * self.settings.candy_width + distance_x
                    )
                    # snap them into their new positions on the board
                    if (
                        self.clicked_candy.rect.left
                        <= self.swapped_candy.col_num * self.settings.candy_width
                        + self.settings.candy_width / 4
                    ):
                        self.swap(self.clicked_candy, self.swapped_candy)
                        matches.update(self.match_three(self.clicked_candy))
                        matches.update(self.match_three(self.swapped_candy))
                        self.moves += 1
                        self.clicked_candy = None
                        self.swapped_candy = None

                # if moving the clicked candy to the right,
                # make sure it"s not on the last col
                if (
                    direction == "right"
                    and self.clicked_candy.col_num
                    < self.settings.width / self.settings.candy_width - 1
                ):
                    # get the candy to the right
                    self.swapped_candy = self.board.board[self.clicked_candy.row_num][
                        self.clicked_candy.col_num + 1
                    ]

                    # move the two candies
                    self.clicked_candy.rect.left = (
                        self.clicked_candy.col_num * self.settings.candy_width + distance_x
                    )
                    self.swapped_candy.rect.left = (
                        self.swapped_candy.col_num * self.settings.candy_width - distance_x
                    )

                    # snap them into their new positions on the board
                    if (
                        self.clicked_candy.rect.left
                        >= self.swapped_candy.col_num * self.settings.candy_width
                        - self.settings.candy_width / 4
                    ):
                        self.swap(self.clicked_candy, self.swapped_candy)
                        matches.update(self.match_three(self.clicked_candy))
                        matches.update(self.match_three(self.swapped_candy))
                        self.moves += 1
                        self.clicked_candy = None
                        self.swapped_candy = None

                # if moving the clicked candy up,
                # make sure it"s not on the first row
                if direction == "up" and self.clicked_candy.row_num > 0:
                    # get the candy above
                    self.swapped_candy = self.board.board[self.clicked_candy.row_num - 1][
                        self.clicked_candy.col_num
                    ]
                    # move the two candies
                    self.clicked_candy.rect.top = (
                        self.clicked_candy.row_num * self.settings.candy_height - distance_y
                    )
                    self.swapped_candy.rect.top = (
                        self.swapped_candy.row_num * self.settings.candy_height + distance_y
                    )

                    # snap them into their new positions on the board
                    if (
                        self.clicked_candy.rect.top
                        <= self.swapped_candy.row_num * self.settings.candy_height
                        + self.settings.candy_height / 4
                    ):
                        self.swap(self.clicked_candy, self.swapped_candy)
                        matches.update(self.match_three(self.clicked_candy))
                        matches.update(self.match_three(self.swapped_candy))
                        self.moves += 1
                        self.clicked_candy = None
                        self.swapped_candy = None

                # if moving the clicked candy down,
                # make sure it"s not on the last row
                if (
                    direction == "down"
                    and self.clicked_candy.row_num
                    < self.settings.height / self.settings.candy_height - 1
                ):
                    # get the candy below
                    self.swapped_candy = self.board.board[self.clicked_candy.row_num + 1][
                        self.clicked_candy.col_num
                    ]

                    # move the two candies
                    self.clicked_candy.rect.top = (
                        self.clicked_candy.row_num * self.settings.candy_height + distance_y
                    )
                    self.swapped_candy.rect.top = (
                        self.swapped_candy.row_num * self.settings.candy_height - distance_y
                    )

                    # snap them into their new positions on the board
                    if (
                        self.clicked_candy.rect.top
                        >= self.swapped_candy.row_num * self.settings.candy_height
                        - self.settings.candy_height / 4
                    ):
                        self.swap(self.clicked_candy, self.swapped_candy)
                        matches.update(self.match_three(self.clicked_candy))
                        matches.update(self.match_three(self.swapped_candy))
                        self.moves += 1
                        self.clicked_candy = None
                        self.swapped_candy = None

            # detect mouse release
            if self.clicked_candy is not None and event.type == pygame.MOUSEBUTTONUP:
                # snap the candies back to their original positions on the grid
                self.clicked_candy.snap()
                self.clicked_candy = None
                if self.swapped_candy is not None:
                    self.swapped_candy.snap()
                    self.swapped_candy = None

        self.draw()
        pygame.display.update()

        # check if there"s at least 3 matching candies
        if len(matches) >= 3:
            # add to score
            self.score += len(matches)
            # animate the matching candies shrinking
            while len(matches) > 0:
                self.clock.tick(1000)
                # decrease width and height by 1
                for candy in matches:
                    new_width = max(0, candy.image.get_width() - 5)
                    new_height = max(0, candy.image.get_height() - 5)
                    new_size = (new_width, new_height)
                    candy.image = pygame.transform.scale(candy.image, new_size)
                    candy.rect.left = (
                        candy.col_num * self.settings.candy_width
                        + (self.settings.candy_width - new_width) / 2
                    )
                    candy.rect.top = (
                        candy.row_num * self.settings.candy_height
                        + (self.settings.candy_height - new_height) / 2
                    )

                # check if the candies have shrunk to zero size
                for row_num in range(len(self.board.board)):
                    for col_num in range(len(self.board.board[row_num])):
                        candy = self.board.board[row_num][col_num]
                        if (
                            candy.image.get_width() <= 0
                            or candy.image.get_height() <= 0
                        ):
                            matches.remove(candy)

                            # generate a new candy
                            self.board.board[row_num][col_num] = Candy(
                                row_num, col_num, self.settings
                            )

                self.draw()
                pygame.display.update()
