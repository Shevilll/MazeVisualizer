import pygame

# Todo
# Implement Travelling Salesman Problem

# Help

# Press d for Depth First Search
# Press b for Breadth First Search
# Press g for greedy best first search
# Press a for astar
# Press j for dijkstra

# Left Click to place Nodes
# Right Click to remove Nodes

# Press Escape to break animation
# Press c to clear the display
# Press r to generate random maze of barriers
# Press 1 to off/on walls
# Press 2 to off/on water
# Press 3 to off/on deepwater
# Press spacebar to off/on diagonal_neighbours
# Press x to turn off/on animations

# window settings
WIDTH = 800
HEIGHT = 750
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Visualizer")


def main():
    from maze.maze import make_grid, get_clicked_pos, Node, draw

    total_rows = 50
    total_cols = 50

    grid = make_grid(total_rows, total_cols, WIDTH, HEIGHT, total_rows, total_cols)

    start = None
    end = None
    wall = False
    water = False
    deepwater = False
    diagonal = False
    animations = True

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, total_rows, total_cols, WIDTH, HEIGHT)
                node: Node = grid[row][col]

                if not start and node != end:
                    node.make_start()
                    start = node

                elif start and not end and start != node:
                    node.make_end()
                    end = node
                elif start and end and start != end and end != node and wall:
                    node.make_wall()
                elif start and end and start != end and end != node and water:
                    node.make_water()
                elif start and end and start != end and end != node and deepwater:
                    node.make_deepwater()
                elif start and end and start != node and end != node:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, total_rows, total_cols, WIDTH, HEIGHT)
                node: Node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    animations = not animations
                if event.key == pygame.K_SPACE:
                    diagonal = not diagonal

                if event.key == pygame.K_1:
                    wall = not wall
                    water = False
                    deepwater = False

                if event.key == pygame.K_2:
                    wall = False
                    water = not water
                    deepwater = False

                if event.key == pygame.K_3:
                    wall = False
                    water = False
                    deepwater = not deepwater

                if event.key == pygame.K_c:
                    from maze.maze import reset_maze

                    start = None
                    end = None
                    reset_maze(total_rows, total_cols, grid)

                if event.key == pygame.K_r:
                    from maze.generate_random_maze import generate_random_maze
                    from maze.maze import reset_maze

                    (
                        grid,
                        start,
                        end,
                    ) = generate_random_maze(
                        lambda: make_grid(
                            total_rows,
                            total_cols,
                            WIDTH,
                            HEIGHT,
                            total_rows,
                            total_cols,
                        ),
                        lambda: draw(total_rows, total_cols, grid),
                        grid,
                        start,
                        end,
                        lambda: reset_maze(total_rows, total_cols, grid),
                    )
                if event.key == pygame.K_d and start and end:
                    from algorithms.depth_first_search import depth_first_search

                    depth_first_search(
                        grid,
                        start,
                        end,
                        lambda: draw(total_rows, total_cols, grid),
                        diagonal,
                        animations,
                    )
                if event.key == pygame.K_b and start and end:
                    from algorithms.breadth_first_search import breadth_first_search

                    breadth_first_search(
                        grid,
                        start,
                        end,
                        lambda: draw(total_rows, total_cols, grid),
                        diagonal,
                        animations,
                    )

                if event.key == pygame.K_g and start and end:
                    from algorithms.greedy_best_first_search import (
                        greedy_best_first_search,
                    )

                    greedy_best_first_search(
                        grid,
                        start,
                        end,
                        lambda: draw(total_rows, total_cols, grid),
                        diagonal,
                        animations,
                    )
                if event.key == pygame.K_a and start and end:
                    from algorithms.astar import astar

                    astar(
                        grid,
                        start,
                        end,
                        lambda: draw(total_rows, total_cols, grid),
                        diagonal,
                        animations,
                    )
                if event.key == pygame.K_j and start and end:
                    from algorithms.dijkstra import dijkstra

                    dijkstra(
                        grid,
                        start,
                        end,
                        lambda: draw(total_rows, total_cols, grid),
                        diagonal,
                        animations,
                    )
        draw(total_rows, total_cols, grid)
    pygame.quit()


if __name__ == "__main__":
    main()
