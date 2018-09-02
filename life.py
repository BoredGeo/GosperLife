"""
 ##############################################
 #                                            #
 #          CONWAY'S GAME OF LIFE             #
 #                                            #
 ##############################################

 Class board will include its size, an init method with and without num
 of seeds, an update board function which will have an 8-neighbor algorithm,
 and a get_state method which will return the board as an array.

 Rules:
 1. Any live cell with fewer than two live neighbors dies
 2. Any live cell with two or three live neighbors lives on to the next gen
 3. Any live cell with more than three live neighbors dies
 4. Any dead cell with exactly three live neighbors becomes a live cell

 special cases: Canada goose if board is larger than 25x25 and seeds = 66
                Gosper gun if board is larger than 40x40 and seeds = 99
"""

import time
import random
import os
from itertools import product
import numpy as np


COUNTER = 0
random.seed(time.time())


class Board:
    """ The Board class represents a state in the game of life.
    It can calculate the next step, seed the board and represent
    it as a string for the screen """

    COLOR = [random.randint(0, 256)] * 3
    dC = [5, 6, 7]

    def __init__(self, dim, seeds):
        self.board = np.zeros((dim, dim))
        self.dim = dim
        # seed board
        if seeds == 66 and dim > 25:
            self.seed_goose()
        elif seeds == 99 and dim > 38:
            self.seed_gosper()
        else:
            self.seed_random(seeds)

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def seed_random(self, seeds):
        """random seeding"""
        while np.sum(self.board) < seeds:
            i = random.randint(0, self.dim - 1)
            j = random.randint(0, self.dim - 1)
            self.board[i, j] = 1

    @classmethod
    def update_rgb(cls):
        """ changing the color of the board in the shell """
        for i in range(3):
            if ((cls.COLOR[i] + cls.dC[i]) > 255
                    or (cls.COLOR[i] + cls.dC[i]) < 0):
                cls.dC[i] *= -1
            cls.COLOR[i] += cls.dC[i]

    def update_board(self, old):
        """ actual life calculation """
        self.update_rgb()
        for i in range(self.dim):
            for j in range(self.dim):
                indj = range(j-1, j+2)
                cell_sum = old[i-1].take(indj, mode="wrap").sum()
                cell_sum += old[i].take(indj, mode="wrap").sum()
                cell_sum += old[(i+1) % self.dim].take(indj, mode="wrap").sum()
                cell_sum -= old[i, j]
                if cell_sum > 3 or cell_sum < 2:  # always death
                    self.board[i, j] = 0
                elif cell_sum == 3:        # always life
                    self.board[i, j] = 1
                else:               # stasis
                    self.board[i, j] = old[i][j]

    def __str__(self):
        str_rep = u"\033[38;2;{0};{1};{2}m\u2017".format(self.COLOR[0],
                                                         self.COLOR[1],
                                                         self.COLOR[2])\
                    * (2 * (self.dim + 1)) + "\n"
        for row in self.board:
            str_rep += u"\u2551"
            str_rep += ''.join(u"\u2588\u2588" if cell > 0
                               else u"\u0020\u0020" for cell in row)
            str_rep += u"\u2551"+"\n"
        str_rep += u"\u203E"*2*(self.dim + 1)+"\n"
        str_rep += "Game of life, iteration " + str(COUNTER+1) + "\n"
        return str_rep

    def seed_goose(self):
        """ special case, if user specifies 66 seeds,
        a canada goose is seeded """
        try:
            glider = np.loadtxt('goose.txt', delimiter=',')
            for coord in product(list(range(5, self.dim-14, 20)), repeat=2):
                i = coord[0]
                j = coord[1]
                self.board[i:i+12, j:j+14] = glider
        except IOError:
            print("goose.txt file not found, defaulting to random seeding")
            self.seed_random(random.randint(1, (self.dim**2)/2))

    def seed_gosper(self):
        """ special case, if user specifies 99 seeds,
        a gosper gun is seeded """
        try:
            gosper = np.loadtxt('gosper.txt', delimiter=',')
            i = int((self.dim - 9) / 2)
            j = int((self.dim - 36) / 2)
            self.board[i:i+9, j:j+36] = gosper
        except IOError:
            print("gosper.txt file not found, defaulting to random seeding")
            self.seed_random(random.randint(1, (self.dim**2)/2))


def print_board(board):
    """ gets array, delete previous display,
    prints it and flushes the display """
    global COUNTER
    os.system('clear')
    print(board)
    COUNTER += 1
    time.sleep(0.3)


def game_on(board1, board2, num_of_iter):
    """ run the game """
    global COUNTER
    exit_status = 0
    print("Game starting.\n")
    print_board(board1)

    # main loop
    exit_game = False
    while not exit_game:
        board2.update_board(board1.board)
        print_board(board2)
        if board1 == board2:
            exit_status = 1
            exit_game = True
        board1, board2 = board2, board1
        if COUNTER >= num_of_iter:
            if input(f"Reached {num_of_iter} iterations, would you like \
                      to continue {num_of_iter} more? (y/n) ").lower() == 'y':
                num_of_iter += num_of_iter
            else:
                exit_game = True
    return exit_status


def main():
    """ main game user input """
    dim = int(input("Enter board size DxD cells: "))
    if dim > 80 or dim < 2:
        print("Illegal board size, using default\n")
        dim = 32
    # TODO: resize terminal to fit dimension sepcified by user
    seeds = int(input("Enter number of seeds (0 for random initialization): "))
    if seeds < 1 or seeds > dim**2:
        print(f"You can't have {seeds} seeds! Defaulting to random")
        seeds = random.randint(1, (dim**2)/2)
    num_of_iterations = int(input("How many iterations \
                                  would you like to run: "))
    if not 0 < num_of_iterations < 1000:
        print("Either too many or too few. Defaulting to 100.")
        num_of_iterations = 100

    # ------------------------------------------------------------------------
    # initiate boards
    # run game
    # ------------------------------------------------------------------------
    board1 = Board(dim, seeds)
    board2 = Board(dim, 0)
    out = game_on(board1, board2, num_of_iterations)
    out_stat = "Life reached status quo" if out else ""
    out_stat += "\nGame Over after"
    print(out_stat, COUNTER, "iterations\n")


if __name__ == "__main__":
    main()
