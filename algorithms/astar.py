import pygame
from maze.maze import Node
from queue import PriorityQueue
from typing import List


def heuristic(x1, y1, x2, y2):
    """returns Manhattan distance to the goal"""
    return abs(x1 - x2) + abs(y1 - y2)


def astar(grid: List[List[Node]], start: Node, end: Node, draw):
    for i in grid:
        for node in i:
            if node.is_visited() or node.is_path() or node.will_visit():
                node.reset()
        draw()
    p_queue = PriorityQueue()

    g_scores = {node: float("inf") for row in grid for node in row}
    g_scores[start] = heuristic(start.row, start.col, end.row, end.col)
    f_scores = {node: float("inf") for row in grid for node in row}
    f_scores[start] = heuristic(start.row, start.col, end.row, end.col)

    p_queue.put((heuristic(start.row, start.col, end.row, end.col), start))
    visited = {(start.row, start.col): None}
    while not p_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        curr: Node = p_queue.get()[1]

        x, y = curr.row, curr.col
        if grid[x][y] == end:
            path = [grid[x][y]]
            while (x, y) != (start.row, start.col):
                x, y = visited[(x, y)]
                path.append(grid[x][y])
            for i in path[1 : len(path) - 1]:
                i.make_path()
                draw()
            return
        if curr != start:
            curr.make_visited()

        curr.update_neighbours(grid)
        for i in curr.neighbours:
            tentative_g_score = g_scores[curr] + 1
            if tentative_g_score < g_scores[i]:
                g_scores[i] = tentative_g_score
                f_scores[i] = tentative_g_score + heuristic(
                    i.row, i.col, end.row, end.col
                )
                if (i.row, i.col) not in visited:
                    visited[(i.row, i.col)] = (x, y)
                    p_queue.put((f_scores[i], i))
                    if i != start and i != end:
                        i.make_will_visit()
        draw()
