import string
import numpy as np
import time
import random
from collections import deque
from queue import Queue
import string
import math

from utils import cinput, write, clear_console


# Helper function for the random_star_end function to calculate the distance between two points
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    x_dist = abs(x1 - x2)
    y_dist = abs(y1 - y2)
    return x_dist + y_dist


# generates start and end coordinates with a given distance
def random_start_end(dim: int, min_distance=0) -> list:
    if min_distance == 0:
        min_distance = (dim + 1) * 2

    max_num_gen = 100000
    current_gen_num = 0

    best_distance = 0
    best_pair = []

    # not pretty but works
    while True:
        s_direct = random.randint(0, 1)
        e_direct = random.randint(0, 1)

        if s_direct == 0:
            start = [random.randint(1, 2 * dim - 1), 0]
        else:
            start = [0, random.randint(1, 2 * dim - 1)]

        if e_direct == 0:
            end = [0, random.randint(1, 2 * dim - 1)]
        else:
            end = [random.randint(1, 2 * dim - 1), 0]

        test_distance = calculate_distance(start, end)

        # return if a good start, end pair was found
        if test_distance >= min_distance:
            return [start, end]
        elif test_distance > best_distance:
            best_distance = test_distance
            best_pair = [start, end]

        # abort if the maximum number of generations is reached and return the best found pair
        if current_gen_num == max_num_gen:
            return best_pair
        else:
            current_gen_num += 1


def create_maze(dim: int, s_e_pos: list) -> np.ndarray:
    # Create a grid filled with walls
    maze = np.full((dim * 2 + 1, dim * 2 + 1), '#')

    # Define the starting point
    x, y = (0, 0)
    maze[2 * x + 1, 2 * y + 1] = '.'

    # Define possible directions
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

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
    start = s_e_pos[0]
    end = s_e_pos[1]
    maze[start[0], start[1]] = 'S'
    maze[end[0], end[1]] = 'E'

    return maze


def create_maze_rand_se(dim: int, s_e_pos: list) -> np.ndarray:

    # Choose a random start and end position from the given list
    start, end = s_e_pos

    # Increment the second element if it is 0
    end_check = [end[0] + 1, end[1]] if end[0] == 0 else [end[0], end[1] + 1]

    # Create a grid filled with walls
    maze = np.full((dim * 2 + 1, dim * 2 + 1), '#')

    # Initialize the stack with the starting point and mark it as visited
    stack = [start]
    visited = {tuple(start)}

    # Define possible directions
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    maze[start[0], start[1]] = '.'

    connection_to_end = False
    while len(stack) > 0:
        x, y = stack[-1]

        # With this, we ensure that the paths differ from run to run
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < 2 * dim and 0 < ny < 2 * dim and (nx, ny) not in visited:
                if dx == 0:
                    # check if the front diagonals are part of a path and not a corner block
                    go = maze[x + -1, y + dy] != "." and maze[x + 1, y + dy] != "." and \
                         maze[nx + -1, ny + dy] != "." and maze[nx + 1, ny + dy] != "."
                else:
                    # check if the front diagonals are part of a path and not a corner block
                    go = maze[x + dx, y + -1] != "." and maze[x + dx, y + 1] != "." and \
                         maze[nx + dx, ny + -1] != "." and maze[nx + dx, ny + 1] != "."
                if maze[x + 2 * dx, y + 2 * dy] != "." and go:
                    maze[nx, ny] = '.'
                    maze[x + dx, y + dy] = '.'
                    stack.append([nx, ny])
                    visited.add((nx, ny))
                    # to ensure that the returned maze has a connection from start to end
                    if [nx, ny] == end_check:
                        connection_to_end = True
                    break
        else:
            stack.pop()

    if not connection_to_end:
        maze = create_maze_rand_se(m_dim, s_e_pos)

    # Mark the start and end positions
    maze[start[0], start[1]] = chr(9654)
    maze[end[0], end[1]] = '■'

    return maze


def find_shortest_path(maze: np.ndarray, s_e_pos: list) -> np.ndarray:
    # BFS algorithm to find the shortest path
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # add one to start in the maze if the position is 0 for start or end
    # s_e_pos[0] = [num + 1 if num == 0 else num for num in s_e_pos[0]]
    # s_e_pos[1] = [num - 2 if num == 0 else num for num in s_e_pos[1]]

    start = tuple(s_e_pos[0])
    end = tuple(s_e_pos[1])

    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))
    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = (node[0] + dx, node[1] + dy)
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

    #TODO: check einbauen, dass ende nicht als letter versehen werden kann

    for ind, pos in enumerate(random_pos):
        maze[pos] = random_letters[ind]

    return ''.join(random_letters)


def write_maze(maze: np.ndarray, solution: str, s_e_pos: list, dim: int):
    # Print the resulting maze
    maze_str = []
    for row in maze:
        maze_str.append(' '.join(row))
    maze_str = "\n".join(maze_str)

    start = s_e_pos[0]
    end = s_e_pos[1]

    # start_ind_replace = (start[1] + start[0] * (dim * 2 + 1)) * 2
    # end_ind_replace = (end[1] + end[0] * (dim * 2 + 1)) * 2

    for letter in solution:
        maze_str = maze_str.replace(f"{letter}", f"[y]{letter}[/y]")
    maze_str = maze_str.replace(f"{chr(9654)}", f"[g]{chr(9654)}[/g]")
    maze_str = maze_str.replace(f"{'■'}", f"[r]{'■'}[/r]")

    # change the start string S to "[g]S[/g]" at its index in the string
    # maze_str = maze_str[:start_ind_replace] + "[g]S[/g]" + maze_str[start_ind_replace + 1:]
    #
    # if start_ind_replace > end_ind_replace:
    #     maze_str = maze_str[:end_ind_replace] + "[r]E[/r]" + maze_str[end_ind_replace + 1:]
    # else:
    #     # account for the added symbols by replacing 'S' with "[g]S[/g]"
    #     end_ind_replace += 7
    #     maze_str = maze_str[:end_ind_replace] + "[r]E[/r]" + maze_str[end_ind_replace + 1:]

    write(maze_str, 0)


if __name__ == "__main__":
    m_dim = 16

    s_e_pos = random_start_end(m_dim)

    maze = create_maze_rand_se(m_dim, s_e_pos)

    # print(maze)

    path = find_shortest_path(maze, s_e_pos)

    solution = place_puzzle_letters(maze, path, 12)

    write_maze(maze, solution, s_e_pos, m_dim)
