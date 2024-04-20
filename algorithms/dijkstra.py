import pygame
from maze.maze import Node
from queue import PriorityQueue
from typing import List


def dijkstra(
    grid: List[List[Node]], start: Node, end: Node, draw, diagonal, animations
):
    """Care about weighted maze and gives shortest path"""
    for i in grid:
        for node in i:
            if (
                node.is_visited() or node.is_path() or node.will_visit()
            ) and not node.is_weighted():
                node.reset()
        if animations:
            draw()
    p_queue = PriorityQueue()
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0

    p_queue.put((0, start))
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
                if animations:
                    draw()
            print(
                f"Dijsktra\nPath Length: {len(path)}\nTotal Nodes Visited: {len(visited)}\n"
            )
            return
        if curr != start and not curr.is_weighted():
            curr.make_visited()

        curr.update_neighbours(grid, diagonal)
        for i in curr.neighbours:
            newdist = dist[curr] + i.weight
            if newdist < dist[i]:
                dist[i] = newdist
                if (i.row, i.col) not in visited:
                    visited[(i.row, i.col)] = (x, y)
                    p_queue.put((newdist, i))
                    if i != start and i != end and not i.is_weighted():
                        i.make_will_visit()
        if animations:
            draw()
