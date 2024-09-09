import random
from enum import Enum
import numpy as np
import cv2
import sys

sys.setrecursionlimit(8000)


class Directions(Enum):
    """
    Enum to represent the four possible movement directions in the maze.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Backtracking:
    """
    This class generates a random maze using the backtracking algorithm.

    Attributes:
        height (int): Height of the maze.
        width (int): Width of the maze.
        path (str): File path to save the generated maze image.
        display_maze (bool): Flag to display the maze using OpenCV.
    """

    def __init__(self, height, width, path, display_maze, scale=10):
        """
        Initializes the Backtracking maze generator.

        Ensures the maze dimensions are odd and stores relevant settings.

        Args:
            height (int): The height of the maze.
            width (int): The width of the maze.
            path (str): The file path to save the maze image.
            display_maze (bool): Whether or not to display the maze during generation.
        """
        # Ensure dimensions are odd for proper maze structure
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.path = path
        self.display_maze = display_maze
        self.scale = scale

    def createMaze(self):
        """
        Generates the maze grid, displays it, and saves it to a file.

        The maze is created using a backtracking algorithm, starting from a random point.
        The outer boundary is initialized, and paths are created based on backtracking.
        """
        # Create a grid filled with unvisited cells (represented by 1s)
        maze = np.ones((self.height, self.width), dtype=np.float32)

        # Iterate over the grid to initialize paths and walls
        for i in range(self.height):
            for j in range(self.width):

                # Mark odd columns and rows as walls (represented by 0s)
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 0

                # Mark the outer boundary (edges) as visited (0.5)
                if i == 0 or j == 0 or i == self.height - 1 or j == self.width - 1:
                    maze[i, j] = 0.5

        # Select a random starting point within the grid, ensuring it falls on an even index
        start_x = random.choice(range(2, self.width - 2, 2))
        start_y = random.choice(range(2, self.height - 2, 2))

        # Begin maze generation from the random starting point
        self.generator(start_x, start_y, maze)

        # After generation, convert the boundary visited (0.5) cells to unvisited (1s)
        for i in range(self.height):
            for j in range(self.width):
                if maze[i, j] == 0.5:
                    maze[i, j] = 1

        # Create an entrance at the top and an exit at the bottom
        maze[1, 2] = 1  # Entrance
        maze[self.height - 2, self.width - 3] = 1  # Exit

        # Optionally display the maze using OpenCV
        if self.display_maze:
            cv2.namedWindow('Maze', cv2.WINDOW_NORMAL)
            cv2.imshow('Maze', maze)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Save the maze to a file, scaling the values to 255 for white color
        maze = maze * 255.0
        scaled_maze = cv2.resize(maze, (self.width * self.scale, self.height * self.scale), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(self.path, scaled_maze)

        return 0

    def generator(self, cx, cy, grid):
        """
        Recursively generates paths in the maze using the backtracking algorithm.

        Marks the current cell as part of the path and then randomly chooses
        an adjacent cell to move into. If all adjacent cells are visited, it backtracks.

        Args:
            cx (int): Current x-coordinate in the grid.
            cy (int): Current y-coordinate in the grid.
            grid (np.ndarray): The maze grid being generated.
        """
        # Mark the current cell as visited by setting it to 0.5
        grid[cy, cx] = 0.5

        # Check if all neighboring cells are already visited
        if not (grid[cy - 2, cx] == 0.5 and grid[cy + 2, cx] == 0.5 and grid[cy, cx - 2] == 0.5 and grid[cy, cx + 2] == 0.5):
            # List of directions to explore (UP, DOWN, LEFT, RIGHT)
            li = [1, 2, 3, 4]

            # Shuffle directions and explore in random order
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)

                # Move upwards
                if dir == Directions.UP.value:
                    ny = cy - 2
                    my = cy - 1
                # Move downwards
                elif dir == Directions.DOWN.value:
                    ny = cy + 2
                    my = cy + 1
                # No vertical movement
                else:
                    ny = cy
                    my = cy

                # Move left
                if dir == Directions.LEFT.value:
                    nx = cx - 2
                    mx = cx - 1
                # Move right
                elif dir == Directions.RIGHT.value:
                    nx = cx + 2
                    mx = cx + 1
                # No horizontal movement
                else:
                    nx = cx
                    mx = cx

                # If the next cell is unvisited, mark the mid-point and the next cell
                if grid[ny, nx] != 0.5:
                    grid[my, mx] = 0.5  # Midpoint between current and next
                    # Recursively visit the next cell
                    self.generator(nx, ny, grid)
