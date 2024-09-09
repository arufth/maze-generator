import backtracking as bt

# Define maze parameters: width, height, and file path
width = 100
height = 50
path = './maze.png'

# Create a Backtracking object and generate the maze
bt = bt.Backtracking( height, width, path, False, 300)
bt.createMaze()