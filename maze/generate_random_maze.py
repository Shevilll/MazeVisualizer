import random
from maze.maze import Node
from typing import List


def generate_random_maze(
    make_grid,
    draw,
    grid: List[List[Node]],
    start: Node,
    end: Node,
    reset_maze,
):
    def generate_maze(make_grid):
        grid: List[List[Node]] = make_grid()
        for i in grid:
            for node in i:
                node.make_barrier()

        def get_neighbors(node):
            row, col = node
            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            return [
                (r, c)
                for r, c in neighbors
                if 0 <= r < len(grid) and 0 <= c < len(grid[0])
            ]

        # Recursive Backtracking algorithm
        def recursive_backtracking(node: Node):
            grid[node[0]][node[1]].reset()  # Mark the current cell as a passageway

            # Randomly shuffle the neighbors
            neighbors = get_neighbors(node)
            if neighbors:
                random.shuffle(neighbors)

                for neighbor in neighbors:
                    r, c = neighbor
                    if grid[r][c].is_barrier():  # If the neighbor is a wall
                        count_walls = sum(
                            grid[rr][cc].is_barrier()
                            for rr, cc in get_neighbors(neighbor)
                        )
                        if (
                            count_walls >= 3
                        ):  # Check if there are at least 3 neighboring walls
                            grid[r][
                                c
                            ].reset()  # Remove the wall between current cell and neighbor
                            recursive_backtracking(neighbor)

        # Start the maze generation from a random cell
        node = (random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1))
        recursive_backtracking(node)
        start = grid[random.randint(0, len(grid) - 1)][
            random.randint(0, len(grid[0]) - 1)
        ]  # Set the starting point
        end = grid[random.randint(0, len(grid) - 1)][
            random.randint(0, len(grid[0]) - 1)
        ]  # Set the ending point

        start.make_start()
        end.make_end()

        return grid, start, end

    new_grid, start, end = generate_maze(
        make_grid,
    )
    reset_maze()
    for i in range(len(new_grid)):
        for j in range(len(new_grid[i])):
            grid[i][j] = new_grid[i][j]
        draw()

    return grid, start, end
