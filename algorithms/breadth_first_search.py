import pygame
from collections import deque
from typing import List
from maze.maze import Node


def breadth_first_search(
    grid: List[List[Node]], start: Node, end: Node, draw, diagonal
):
    """Doesn't care about weighted maze and gives shortest path"""
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
    queue = deque([start])
    visited = {(start.row, start.col): None}
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        curr = queue.popleft()

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
                f"Breadth First Search\nPath Length: {len(path)}\nTotal Nodes Visited: {len(visited)}\n"
            )
            return
        if curr != start and not curr.is_weighted():
            curr.make_visited()

        curr.update_neighbours(grid, diagonal)
        for i in curr.neighbours:
            if (i.row, i.col) not in visited:
                if i != start and i != end and not i.is_weighted():
                    i.make_will_visit()
                queue.append(i)
                visited[(i.row, i.col)] = (x, y)
        draw()
