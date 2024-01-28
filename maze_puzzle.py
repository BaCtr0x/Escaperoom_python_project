import string
import numpy as np
import time
import random
from collections import deque
from queue import Queue
import string
import math

from utils import cinput, write, clear_console, default_commands

# list of hints for the user
hints = [
    f"The start point is '[/y][g]{chr(9654)}[/g][y]' and the end is '[/y][r]■[/r][y]'.",
    "Follow the path and see what you can find.",
    "The letters don't seem to have a meaning, but does it matter?",
    "Entering the letters in the encountered order might do the trick."
]

# dimension of the maze (will be doubled later)
m_dim = 22

# number of letters of the solution word
sol_len = 12


# Helper function for the random_star_end function to calculate the distance between two points
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    # abs to have positive distances
    x_dist = abs(x1 - x2)
    y_dist = abs(y1 - y2)
    return x_dist + y_dist


# generates start and end coordinates with a given distance
def random_start_end(dim: int, min_distance=0) -> list:
    # calculates the minimum distance between start and end if none is provided, this ensures that they are not too
    # close together
    if min_distance == 0:
        min_distance = (dim + 1) * 2

    # maximum number of generations as the generation is random based and thus no perfect run at first execution is
    # ensured
    max_num_gen = 100000
    current_gen_num = 0

    best_distance = 0
    best_pair = []

    # not pretty but works
    while True:
        # get a random direction of start and end
        s_direct = random.randint(0, 1)
        e_direct = random.randint(0, 1)

        # get random numbers on the edge of the maze along the randomly selected axis
        if s_direct == 0:
            # 1 and (2 * dim) - 1 to avoid corner points, as we cannot go diagonally and thus would not be able to start
            # or stop there. We use -1 as the maze is generated with dimensions (2 * dim) + 1
            start = [random.randint(1, 2 * dim - 1), 0]
        else:
            start = [0, random.randint(1, 2 * dim - 1)]

        # do the same for the end position
        if e_direct == 0:
            end = [0, random.randint(1, 2 * dim - 1)]  # dim * 2 instead of 0, to have the end be on the bottom
        else:
            end = [random.randint(1, 2 * dim - 1), 0]

        # calculate the distance between start and end to check if they are a good fit
        test_distance = calculate_distance(start, end)

        # return if a good start, end pair was found
        if test_distance >= min_distance:
            return [start, end]
        # if the current positions are better than the ones before, store the current one as the best encountered option
        elif test_distance > best_distance:
            best_distance = test_distance
            best_pair = [start, end]

        # abort if the maximum number of generations is reached and return the best found pair
        if current_gen_num == max_num_gen:
            return best_pair
        else:
            current_gen_num += 1


# creates the maze as a ndarray given a start and end position as well as a dimension that is later doubled
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

    # Define possible directions (y,x)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # set the start to '.'
    maze[start[0], start[1]] = '.'

    connection_to_end = False

    # create the path through of the maze
    while len(stack) > 0:
        # get the last element of the stack
        x, y = stack[-1]

        # With this, we ensure that the paths differ from run to run
        random.shuffle(directions)

        # check the directions and continue on if possible
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # check if the next step is within the maze and a position that has not been visited yet
            if 0 < nx < 2 * dim and 0 < ny < 2 * dim and (nx, ny) not in visited:
                if dx == 0:
                    # check if the front diagonals are part of a path and not a corner block
                    go = maze[x + -1, y + dy] != "." and maze[x + 1, y + dy] != "." and \
                         maze[nx + -1, ny + dy] != "." and maze[nx + 1, ny + dy] != "."
                else:
                    # check if the front diagonals are part of a path and not a corner block
                    go = maze[x + dx, y + -1] != "." and maze[x + dx, y + 1] != "." and \
                         maze[nx + dx, ny + -1] != "." and maze[nx + dx, ny + 1] != "."
                # change the position to a path symbol if allowed
                if maze[x + 2 * dx, y + 2 * dy] != "." and go:
                    maze[nx, ny] = '.'
                    stack.append([nx, ny])
                    visited.add((nx, ny))
                    # to ensure that the returned maze has a connection from start to end
                    if [nx, ny] == end_check:
                        connection_to_end = True
                    break
        else:
            # pop from stack for backtracking
            stack.pop()

    # run the entire process again if the connection to end operation did not work, just an edge case, can be removed
    # with some tweeking
    if not connection_to_end:
        maze = create_maze_rand_se(m_dim, s_e_pos)

    # Mark the start and end positions
    maze[start[0], start[1]] = chr(9654)
    maze[end[0], end[1]] = '■'

    return maze


# BFS algorithm to find the shortest path, different appraoches are explained nicely here:
# https://lvngd.com/blog/generating-and-solving-mazes-with-python/
# the best option would have been A* but its more complicated and would have taken too much time to implement,
# additionally this is fine for these small mazes, if we scale the maze much further this would be too inefficient
def find_shortest_path(maze: np.ndarray, s_e_pos: list) -> np.ndarray:

    # could also be placed as a global variable, but I like this more, as it is easier to remember while coding
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # get the start and end position
    start = tuple(s_e_pos[0])
    end = tuple(s_e_pos[1])

    # create a ndarray of zeroes to store the visited notes in
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True

    # create the queue for the BFS algorithm and add the start position to it
    queue = Queue()
    queue.put((start, []))

    # perform the BFS algorithm until the queue is empty, which is the case when no path could be found from start to end
    while not queue.empty():
        # get the current node (position) and the path to this node
        (node, path) = queue.get()

        # check the possible directions to go along
        for dx, dy in directions:

            # calculate the next node
            next_node = (node[0] + dx, node[1] + dy)

            # return the found path if the end node is reached
            if next_node == end:
                return path + [next_node]

            # add next node to the list of visited nodes and add the next node to the queue to start from there in the
            # next step, extend the current path by this node as well.
            if (0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and
                    maze[next_node] == '.' and not visited[next_node]):
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))


# places the random letters, that create the solution of the puzzle randomly along the path through the maze
def place_puzzle_letters(maze: np.ndarray, path: np.ndarray, num_letters: int) -> str:
    letters = string.ascii_uppercase
    # sample num_letters many letters from the upper case letters of the english alphabet
    random_letters = random.sample(letters, num_letters)

    # sample random positions from the shortest path
    r_pos = 0
    random_pos = []
    max_distance = int(len(path) / num_letters)
    for i in range(num_letters):
        r_pos += random.randint(num_letters, max_distance)
        random_pos.append(path[r_pos])
    # random_pos = random.sample(path, num_letters)

    # place the randomly sampled letters at the random positions along the shortest path
    for ind, pos in enumerate(random_pos):
        maze[pos] = random_letters[ind]

    # return the string of random letters, which is the solution to this puzzle
    return ''.join(random_letters)


# This function converts the maze as the ndarray to the string that is being printed
def maze_to_string(maze: np.ndarray, solution: str, s_e_pos: list) -> str:
    # Print the resulting maze
    maze_str = []

    # appends all rows to the maze string, and add a space in between the symbols, as this makes the maze look better
    # when printed
    for row in maze:
        maze_str.append(' '.join(row))

    # add line breaks after every row
    maze_str = "\n".join(maze_str)

    start = s_e_pos[0]
    end = s_e_pos[1]

    # make the letters of the solution appear yellow
    for letter in solution:
        maze_str = maze_str.replace(f"{letter}", f"[y]{letter}[/y]")

    # turn the start symbol, which is an arrow to a green arrow
    maze_str = maze_str.replace(f"{chr(9654)}", f"[g]{chr(9654)}[/g]")

    # turn the end box into a red end box
    maze_str = maze_str.replace(f"{'■'}", f"[r]{'■'}[/r]")

    # return the finished maze string
    return maze_str


# This function uses the write function to print the maze string
def write_maze(maze: np.ndarray, solution: str, s_e_pos: list):
    # first convert the ndarray of the maze into a string
    maze_str = maze_to_string(maze, solution, s_e_pos)

    # print the maze
    write(maze_str)


# This function is the heart of this puzzle, as it manages the everything
def maze_puzzle(game) -> time:
    # get the number of hints from the stored game, this is zero as len([]) is 0 which is the case of a new game
    hint_count = len(game.get_hints_used(game.get_current_level()))

    # get the state of the game for this level, which contains the maze and the solution, such that the maze is the
    # same when the game is loaded
    level_state = game.get_level_state()

    # print the introduction text of the room
    write("\nYou enter the well lit room. The warm light of the four torches that are placed on top of a fence about\n"
          "5 meters in front of you, covers everything in its orange flickering colour and lets the shadows of the \n"
          "room dance with every breeze. The air is fresh and cold. And as you make a few steps towards the fence you\n"
          "realise that you are standing on some kind of balcony hanging over a huge hall that was carved into the\n"
          "mountain. The hall is split into uncountably many path by walls at least 3 meters in height. Cold air \n"
          "rushes up from down under and you start to shiver. You concentrate and take in the hole view, just to\n"
          "realize that you are looking at a giant maze.\n"
         )

    # checks whether the game has been loaded or not and correspondingly creates a maze or takes the old one
    if level_state == {"death": False}:

        s_e_pos = random_start_end(m_dim)

        maze = create_maze_rand_se(m_dim, s_e_pos)

        path = find_shortest_path(maze, s_e_pos)

        solution = place_puzzle_letters(maze, path, sol_len)

        state = {
            "maze": maze_to_string(maze, solution, s_e_pos),
            "solution": solution
        }

        game.set_level_state(state)

        write_maze(maze, solution, s_e_pos)

    # get the maze and solution from the stored game and print it
    else:
        maze = level_state["maze"]
        solution = level_state["solution"]
        write(maze)

    write(
        f"\nYou take a look around, you see {sol_len} stone wheels set into the left wall, all set to random letters.\n"
        "A few questions immediately rush through your head: 'What is the connection?', 'Who would build something\n"
        "like this' and what am I supposed to do?\n\n"
    )

    start = time.time()

    # set solution to lowercase
    solution = solution.lower()

    # use input loop to handle user interaction
    while True:
        ans = cinput("What do you set the stone tires to?\n").replace(" ", "").replace(",", "").lower()
        if ans == solution:
            stop = time.time()
            write("\nAs you enter the random letters you hear a dark rumble coming from above, like the grinding of \n"
                  "stone on stone, mixed with the mechanical clicking of ginormous gear wheels.\n"
                  "Your eyes jump back to the cavern in which you examined the maze and see part of the ceiling\n"
                  "descending to the ground. With a loud thump it stops exactly at the height of you platform.\n"
                  "And just now you see the small hinges of in the fence in front of you creating a small gate within\n"
                  "it. You walk over and as you come closer small lanterns light up one after the other to clear the\n"
                  "view of the now resting bridge across the hall. You have no idea what is going on and don's know\n"
                  "who would build such a structure, but it doesn't matter. You need to find the old lady and hopefully\n"
                  "her daughter as fast a possible. With this you rush across the bridge and enter the almost familiar\n"
                  "darkness of the corridor at the end to see what ever is next.\n")

            # return the time taken to solve the puzzle and 0 to indicate that the next level can be loaded
            return round(stop - start, 2), 0
        elif "ex" in ans or "hi" in ans or "he" in ans or "_" in ans:
            stop = default_commands(ans, hints, hint_count, game)
            # check if the hint command was used
            if type(stop) == int:
                hint_count = stop
            # case of entering 'exit'
            elif type(stop) == float:
                return round(stop - start, 2), 1
        elif "olaf" in ans:
            write(solution, 0)
        else:
            write("\nNothing seems to happen, maybe the order is not correct yet.\n")


# just for debugging
if __name__ == "__main__":
    m_dim = 16

    s_e_pos = random_start_end(m_dim)

    maze = create_maze_rand_se(m_dim, s_e_pos)

    # print(maze)

    path = find_shortest_path(maze, s_e_pos)

    solution = place_puzzle_letters(maze, path, 12)

    write_maze(maze, solution, s_e_pos, m_dim)
