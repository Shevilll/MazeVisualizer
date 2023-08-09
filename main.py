import pygame

# Help
# Press Escape to break animation
# Press d for Depth First Search
# Press b for Breadth First Search
# Press c to clear the display
# Left Click to place Nodes
# Right Click to remove Nodes
# Press r to generate random maze
# Press g for greedy best first search
# Press a for astar

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

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, total_rows, total_cols, WIDTH, HEIGHT)
                node: Node = grid[row][col]

                if not start:
                    node.make_start()
                    start = node

                elif start and not end and start != node:
                    node.make_end()
                    end = node

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
                    )
                if event.key == pygame.K_b and start and end:
                    from algorithms.breadth_first_search import breadth_first_search

                    breadth_first_search(
                        grid,
                        start,
                        end,
                        lambda: draw(total_rows, total_cols, grid),
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
                    )
                if event.key == pygame.K_a and start and end:
                    from algorithms.astar import astar

                    astar(
                        grid,
                        start,
                        end,
                        lambda: draw(total_rows, total_cols, grid),
                    )
        draw(total_rows, total_cols, grid)
    pygame.quit()


if __name__ == "__main__":
    main()
