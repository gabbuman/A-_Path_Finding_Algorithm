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
import time
from queue import PriorityQueue

###############################################################################
#                               CONSTANTS                                     #
###############################################################################
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

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

# Set the caption of the display window
pygame.display.set_caption("A* Path Finding Algorithm")
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

    def update_neighbours(self, grid):
        self.neighbours = []
        # Node down
        if (self.row < self.total_rows - 1) and (not grid[self.row + 1][self.col].is_barrier()):
            self.neighbours.append(grid[self.row + 1][self.col])
        # Node up
        if (self.row > 0) and (not grid[self.row - 1][self.col].is_barrier()):
            self.neighbours.append(grid[self.row - 1][self.col])
        # Node right
        if (self.col < self.total_rows - 1) and (not grid[self.row][self.col + 1].is_barrier()):
            self.neighbours.append(grid[self.row][self.col + 1])
        # Node left
        if (self.col > 0) and (not grid[self.row][self.col - 1].is_barrier()):
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        # For now
        return False


###############################################################################
#                               FUNTIONS                                      #
###############################################################################
# The heuristic function used to calculate the f values between two nodes.
# Here, we calculate the manhatten distance (absolute distance between x and y axis).
def h(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # To keep track of nodes in the priority queue
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        # We found the shortest path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        # Sleep to slow down visualization
        #time.sleep(0.05)
        draw()

        if current != start:
            current.make_closed()

    return False

# Make a square grid with given rows and total width
def make_grid(rows, width):
    grid = []
    # gap of each grid cube
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Main drawing function
def draw(win, grid, rows, width):
    # Fill in the whole screen to erase previous frame
    win.fill(WHITE)

    # Fill in each node with its color
    for row in grid:
        for node in row:
            node.draw(win)

    # Draw the grid lines
    draw_grid(win, rows, width)
    pygame.display.update()

# Function to take in input from cursor position
def get_clicked_position(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap

    return row, col


# Main function
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Left click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            # Right click
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)