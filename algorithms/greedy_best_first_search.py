import pygame
from maze.maze import Node
from queue import PriorityQueue
from typing import List


def heuristic(x1, y1, x2, y2):
    """returns Manhattan distance to the goal"""
    return abs(x1 - x2) + abs(y1 - y2)


def greedy_best_first_search(
    grid: List[List[Node]], start: Node, end: Node, draw, diagonal
):
    """Care about weighted maze and doesn't gives shortest path"""
    for i in grid:
        for node in i:
            if (
                node.is_visited()
                or node.is_path()
                or node.will_visit()
                and not node.is_weighted()
            ):
                node.reset()
        draw()
    p_queue = PriorityQueue()
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
                if not i.is_weighted():
                    i.make_path()
                draw()
            print(
                f"Greedy Best First Search\nPath Length: {len(path)}\nTotal Nodes Visited: {len(visited)}\n"
            )
            return
        if curr != start and not curr.is_weighted():
            curr.make_visited()

        curr.update_neighbours(grid, diagonal)
        for i in curr.neighbours:
            if (i.row, i.col) not in visited:
                if i != start and i != end and not i.is_weighted():
                    i.make_will_visit()
                p_queue.put((heuristic(i.row, i.col, end.row, end.col) + i.weight, i))
                visited[(i.row, i.col)] = (x, y)
        draw()
