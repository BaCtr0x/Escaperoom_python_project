import time
import re
import sys
import time
import os
import json
from datetime import datetime
import shutil
import matplotlib.pyplot as plt
import seaborn as sb

# ------------------------------------------- Global Values -----------------------------------------------------------

# value changed through options function in main.py 0.015, for debugging set this to 0.00
default_delay = 0.00

# ---------------------------------------- Classes and Structs ---------------------------------------------------------


# defines all the colors and bold and italic for the tags
TAG_COLORS = {
    'b': '1',  # Bold
    'it': '3',  # Italic
    'r': '91',  # Red
    'g': '92',  # Green
    'y': '93',  # Yellow
    'p': '95',  # Purple
    'c': '96',  # Cyan
    'lp': '94'  # Light purple
}


# ----------------------------------------- Utility Functions ----------------------------------------------------------


# A simple function to change the typing speed of the write function
def change_typing_speed(speed: str):
    # we need to get the global default_delay to change it here
    global default_delay

    # this might need to be updated if the different speeds are not good
    speed_dic = {
        0: 0.5,
        1: 0.4,
        2: 0.3,
        3: 0.2,
        4: 0.1,
        5: 0.05,
        6: 0.04,
        7: 0.03,
        8: 0.02,
        9: 0.015,
        10: 0.0
    }
    try:
        speed = int(speed)
        default_delay = speed_dic[speed]
    except ValueError:
        print("Please enter a number between 0 and 10.")


def get_terminal_width() -> int:
    try:
        terminal_width, _ = shutil.get_terminal_size()
        return terminal_width
    except Exception as e:
        print(f"Error getting terminal width: {e}")
        return 0


def remove_tags(text):
    # Define the regular expression pattern for the tags
    pattern = r'\[/?[a-zA-Z]{1,2}\]'

    # Use re.sub to replace all occurrences of the pattern with an empty string
    result = re.sub(pattern, '', text)

    return result


def get_text_len_without_tag(text: str) -> int:
    text = remove_tags(text)
    return len(text)


def clear_console():
    try:
        # Check if the operating system is Windows
        if os.name == 'nt':
            os.system('cls')  # For Windows
        else:
            os.system('clear')  # For Unix-based systems (Linux, macOS)
    except Exception as e:
        print(f"Failed to clear the console: {e}")


def is_closing_tag(tag):
    # Define the regular expression pattern for a closing tag
    pattern = r'^/([a-zA-Z]{1,2})$'

    # Use re.match to check if the tag matches the pattern
    match = re.match(pattern, tag)

    # Return True if it's a closing tag, False otherwise
    return bool(match)


# prints the given text in a writing like style. This is not yet gorgeous, but a start delay=0.015
# for debugging I would set delay to 0.0 to have a print like behavior
# Given different tags in [] you can add italic, bold, red, green, cyan, purple and yellow text.
# The different tags are defined at the top of this file under TAG_COLORS
def write(text: str, delay=None):
    delay = default_delay if delay is None else delay

    def print_centered_line(line):
        padding_len = (get_terminal_width() - get_text_len_without_tag(line)) // 2
        sys.stdout.write(' ' * padding_len)
        in_tag = False
        for char in line:
            if char == '[':
                in_tag = True
                tag = ''
            elif char == ']' and in_tag:
                in_tag = False
                if tag in ['b', 'it', 'r', 'g', 'y', 'p', 'c', 'lp']:
                    sys.stdout.write(f'\033[{TAG_COLORS[tag]}m')
                elif is_closing_tag(tag):
                    sys.stdout.write('\033[0m')  # End special case
                else:
                    sys.stdout.write('[' + tag + ']')  # Print unrecognized tag
            elif in_tag:
                tag += char
            else:
                sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)

    lines = text.split('\n')
    for line in lines:
        print_centered_line(line)
        sys.stdout.write('\n')  # Move to the next line after printing a centered line


# helper function to store times in a dictionary
def save_times(times: dict, filename: str):
    with open(filename, 'w') as json_file:
        json.dump(times, json_file, indent=4)


def get_date() -> str:
    date = datetime.now()
    date = date.strftime("%d-%m-%Y_%H:%M")
    return date


def print_red(skk):
    print(f"\033[91m {skk}\033[00m")


def print_green(skk):
    print(f"\033[92m {skk}\033[00m")


def print_yellow(skk):
    print(f"\033[93m {skk}\033[00m")


def print_lg_purple(skk):
    print(f"\033[94m {skk}\033[00m")


def print_purple(skk):
    print(f"\033[95m {skk}\033[00m")


def print_cyan(skk):
    print(f"\033[96m {skk}\033[00m")


def print_lg_cyan(skk):
    print(f"\033[97m {skk}\033[00m")


def print_black(skk):
    print(f"\033[98m {skk}\033[00m")


# This function centers the input prompt to fit the centering of the write function
def cinput(prompt=""):
    padding = (get_terminal_width() - len(prompt)) // 2
    input_text = input(' ' * padding + prompt)
    return input_text


# This function filters the loaded games from the json file by a given player name
def filter_dict_by_name(games: dict, name: str) -> dict:
    games_list = [elem for elem in games.keys() if name in elem]
    filtered_games = {}
    for game in games_list:
        filtered_games[game] = games[game]
    return filtered_games


def line_plot_times_name(games: dict, name: str):
    print("moin")



if __name__ == "__main__":
    # Example usage:
    write("[b]Bold[/b] and [it]italic[/it] text. With [r]red[/r], [g]green[/g], [y]yellow[/y], [c]cyan[/c], "
          "[p]purple[/p] and [lp] light purple[/lp] options. \n")
