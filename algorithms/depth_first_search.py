import pygame
from typing import List
from maze.maze import Node


def depth_first_search(grid: List[List[Node]], start: Node, end: Node, draw):
    """Doesn't care about weighted maze and doesn't gives shortest path"""
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
    stack = [start]
    visited = {(start.row, start.col): None}
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        curr = stack.pop()

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
                f"Depth First Search\nPath Length: {len(path)}\nTotal Nodes Visited: {len(visited)}\n"
            )
            return
        if curr != start and not curr.is_weighted():
            curr.make_visited()

        curr.update_neighbours(grid)
        for i in curr.neighbours:
            if (i.row, i.col) not in visited:
                if i != start and i != end and not i.is_weighted():
                    i.make_will_visit()
                stack.append(i)
                visited[(i.row, i.col)] = (x, y)
        draw()
