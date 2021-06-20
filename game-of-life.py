import random
from sys import setrecursionlimit
import time

DEAD = 0
LIVE = 1
display_as = {
    DEAD: " ",
    # This is "unicode" for a filled-in square. You can also just use a thick
    # "ASCII" character like a '$' or '#'.
    LIVE: u"\u2588",
}


class GameOfLife:
    def __init__(self, width=100, height=100):
        self.width = width  # number of columns
        self.height = height  # number of rows
        self.habitat = self.sterile()  # initialise a sterile habitat

    def sterile(self):
        # construct empty state of dimensions width * height with all DEAD cells
        return [[DEAD for _ in range(self.width)] for _ in range(self.height)]

    def __str__(self):
        # dunder method to represent object
        lines = []
        for row in self.habitat:
            line = ""
            for col in row:
                line += display_as[col] * 2
            lines.append(line)
        return "\n".join(lines)

    def populate(self, probability=0.9):
        # populate a sterile habitat
        # a cell becomes alive depending on the user specified probability
        for r in range(self.height):
            for c in range(self.width):
                random_number = random.random()
                if random_number > probability:
                    self.habitat[r][c] = LIVE

    def next_cell_value(self, row_col):
        # Get the next value of a single cell in a state.
        # cell_coords: a tuple of the co-ordinates of a cell
        # state: the current state of the Game board
        # returns the new state of the given cell - either DEAD or LIVE

        r, c = row_col
        live_neighbors = 0

        # Iterate around this cell's neighbors
        # max and min makes sure we dont fall off the board
        # for rows for cols
        for row in range(max(0, r - 1), min(self.height - 1, r + 1) + 1):
            for col in range(max(0, c - 1), min(self.width - 1, c + 1) + 1):
                if row == r and col == c:
                    # our original location, don't check
                    continue
                if self.habitat[row][col] == LIVE:
                    live_neighbors += 1

        # Any live cell with two or three live neighbours survives.
        if self.habitat[r][c] == LIVE and 2 <= live_neighbors <= 3:
            return LIVE
        # Any dead cell with three live neighbours becomes a live cell.
        elif self.habitat[r][c] == DEAD and live_neighbors == 3:
            return LIVE
        # else all other live cells die in the next generation. Similarly, all other dead cells stay dead.
        else:
            return DEAD

    def next_habitat_state(self):
        # input current habitat state and update it
        # make a temporary habitat so that we don't interfere with next cell value calculations by changing the cells directly
        temp_habitat = self.sterile()
        for r in range(self.height):
            for c in range(self.width):
                temp_habitat[r][c] = self.next_cell_value((r, c))
        self.habitat = temp_habitat

    def observe(self, timesleep=0.3):
        # runs indefinetely
        while True:
            print(self)
            self.next_habitat_state()
            time.sleep(timesleep)

    def load_board_state(self, filepath):
        # Loads a board state from the given filepath
        # the filepath to load the state from. Dead cells should be represented by 0s, live cells by 1s
        with open(filepath, "r") as f:
            lines = [l.rstrip() for l in f.readlines()]
        self.height = len(lines)
        self.width = len(lines[0])
        self.habitat = self.sterile()

        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                self.habitat[r][c] = int(char)


if __name__ == "__main__":
    # initiate with (width, height):
    game = GameOfLife(50, 50)
    # populate with 0.5 prob:
    # game.populate(0.5)
    # load board state
    game.load_board_state("glider.txt")
    # observe game of life in terminal
    # you must press control c to exit
    game.observe()
