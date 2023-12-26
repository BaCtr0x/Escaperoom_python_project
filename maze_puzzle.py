import string
import numpy as np
import time
import random
from collections import deque
from queue import Queue
import string

from utils import cinput, write, clear_console


def create_maze(dim: int) -> np.ndarray:
    # Create a grid filled with walls
    maze = np.full((dim * 2 + 1, dim * 2 + 1), '#')

    # Define the starting point
    x, y = (0, 0)
    maze[2 * x + 1, 2 * y + 1] = '.'

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < dim and ny < dim and maze[2 * nx + 1, 2 * ny + 1] == '#':
                maze[2 * nx + 1, 2 * ny + 1] = '.'
                maze[2 * x + 1 + dx, 2 * y + 1 + dy] = '.'
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    # Create an entrance and an exit
    maze[1, 0] = 'S'
    maze[-2, -1] = 'E'

    return maze


def find_path(maze: np.ndarray) -> np.ndarray:
    # BFS algorithm to find the shortest path
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start = (1, 1)
    end = (maze.shape[0]-2, maze.shape[1]-2)
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))
    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = (node[0]+dx, node[1]+dy)
            if next_node == end:
                return path + [next_node]
            if (0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and
                maze[next_node] == '.' and not visited[next_node]):
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))


# places the random letters, that create the solution of the puzzle randomly along the path through the maze
def place_puzzle_letters(maze: np.ndarray, path: np.ndarray, num_letters: int) -> str:
    letters = string.ascii_uppercase
    random_letters = random.sample(letters, num_letters)

    random_pos = random.sample(path, num_letters)

    for ind, pos in enumerate(random_pos):
        maze[pos] = random_letters[ind]

    return ''.join(random_letters)


# TODO start and end replace via coordinates and not replace
def write_maze(maze: np.ndarray, solution: str):
    # Print the resulting maze
    maze_str = []
    for row in maze:
        maze_str.append(' '.join(row))
    maze_str = "\n".join(maze_str)
    for letter in solution:
        maze_str = maze_str.replace(f"{letter}", f"[y]{letter}[/y]")
    maze_str = maze_str.replace("S", "[g]S[/g]").replace("E", "[r]E[/r]")
    write(maze_str, 0)


if __name__ == "__main__":
    maze = create_maze(32)

    path = find_path(maze)

    solution = place_puzzle_letters(maze, path, 12)

    write_maze(maze, solution)

