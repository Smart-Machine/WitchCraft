from .candy import Candy

class Board:
    
    def __init__(self, settings):
        self.settings = settings
        self.width = self.settings.width
        self.height = self.settings.height
        self.candy_width = self.settings.candy_width
        self.candy_height = self.settings.candy_height
        self.board = []
        self.create_board()
    
    def create_board(self):
        for row_num in range(self.height // self.candy_height):
            # add a new row to the board
            self.board.append([])
            for col_num in range(self.width // self.candy_width):
                # create the candy and add it to the board
                candy = Candy(row_num, col_num, self.settings)
                self.board[row_num].append(candy)
