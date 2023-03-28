###############################################################################
# Filename: a_star.py
#
# Author: Shubh Mall
#
# Purpose:
#   This file implements the A star path finding algorithm between two nodes.
#
# Requirements:
#   pip install pygame
###############################################################################


###############################################################################
#                               Includes                                      #
###############################################################################
import pygame
import math
from queue import PriorityQueue

###############################################################################
#                               CONSTANTS                                     #
###############################################################################
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Color Values
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

###############################################################################
#                               CLASSES                                       #
###############################################################################
class Node:
    '''
    This class represents a single node in the window grid. It will contain
    information about its color, neighbours and its location

    Attributes:
        - row (int): row number on the grid
        - col (int): column number on the grid
        - width (int): width of each node. Node is represented as a square
        - total_rows (int): total number of rows & columns of the grid.
                            Grid is a square
        - x (int): pixel position in x-axis of node
        - y (int): pixel position in y-axis of node
        - color (tuple): rgb value of node
        - neighbours (list): a list of neighbouring nodes
    '''

    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
         return self.color == GREEN

    def is_barrier (self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
        return

    def make_closed(self):
        self.color = RED
        return

    def make_open(self):
        self.color = GREEN
        return

    def make_barrier(self):
        self.color = BLACK
        return

    def make_start(self):
        self.color = ORANGE
        return

    def make_end(self):
        self.color = TURQUOISE
        return

    def make_path(self):
        self.color = PURPLE
        return

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        return

    def update_neighbours(self.grid):
        pass

    def __lt__(self, other):
        # For now
        return False