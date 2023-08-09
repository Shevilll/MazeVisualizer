import pygame
from typing import List, Type, Tuple
from main import win, WIDTH, HEIGHT

# colors
RED = (255, 0, 0)  # End
GREEN = (0, 255, 0)  # Start
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Visited
WHITE = (255, 255, 255)  # Background
BLACK = (0, 0, 0)  # Barrier
PURPLE = (128, 0, 128)  # Path
ORANGE = (255, 165, 0)  # Plan to visit
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(
        self,
        win: pygame.display,
        row: int,
        col: int,
        x_gap: int,
        y_gap: int,
        total_rows: int,
        total_cols: int,
    ) -> None:
        self.win = win
        self.row = row
        self.col = col
        self.x_coord = row * x_gap
        self.y_coord = col * y_gap
        self.x_gap = x_gap
        self.y_gap = y_gap
        self.color = WHITE
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.neighbours: List[Node] = []

    def is_barrier(self):
        return self.color == BLACK

    def make_barrier(self):
        self.color = BLACK

    def is_start(self):
        return self.color == GREEN

    def make_start(self):
        self.color = GREEN

    def is_end(self):
        return self.color == RED

    def make_end(self):
        self.color = RED

    def reset(self):
        self.color = WHITE

    def make_path(self):
        self.color = PURPLE

    def is_path(self):
        return self.color == PURPLE

    def is_visited(self):
        return self.color == YELLOW

    def make_visited(self):
        self.color = YELLOW

    def will_visit(self):
        return self.color == ORANGE

    def make_will_visit(self):
        self.color = ORANGE

    def draw(self):
        pygame.draw.rect(
            self.win, self.color, (self.x_coord, self.y_coord, self.x_gap, self.y_gap)
        )

    def update_neighbours(self, grid: List[List[Type["Node"]]]):
        self.neighbours = []

        # up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])

        # left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

        # right
        if (
            self.col < self.total_cols - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):
            self.neighbours.append(grid[self.row][self.col + 1])

        # down
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):
            self.neighbours.append(grid[self.row + 1][self.col])

    def __lt__(self, other):
        return False


def get_clicked_pos(pos: Tuple, rows: int, cols: int, width: int, height: int):
    x_gap = width // cols
    y_gap = height // rows
    y, x = pos

    row = y // x_gap
    col = x // y_gap

    return row, col


def make_grid(
    rows: int, cols: int, width: int, height: int, total_rows: int, total_cols: int
):
    grid: List[List] = []
    x_gap = width // cols
    y_gap = height // rows
    for i in range(cols):
        grid.append([])
        for j in range(rows):
            node = Node(win, i, j, x_gap, y_gap, total_rows, total_cols)
            grid[i].append(node)
    return grid


def draw_grid(win: pygame.display, width: int, height: int, rows: int, cols: int):
    x_gap = height // rows
    y_gap = width // cols
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * x_gap), (width, i * x_gap))
        for j in range(cols):
            pygame.draw.line(win, BLACK, (j * y_gap, 0), (j * y_gap, height))


def draw(total_rows: int, total_cols: int, grid: List[List[Node]]):
    win.fill(WHITE)
    for i in grid:
        for node in i:
            node.draw()
    draw_grid(win, WIDTH, HEIGHT, total_rows, total_cols)
    pygame.display.update()


def reset_maze(total_rows: int, total_cols: int, grid: List[List[Node]]):
    for i in grid:
        for node in i:
            node.reset()
        draw(total_rows, total_cols, grid)
