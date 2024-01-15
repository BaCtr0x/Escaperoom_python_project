import time
import re
import sys
import time
import os
import json
from datetime import datetime
import shutil
from tabulate import tabulate

# ------------------------------------------- Global Values -----------------------------------------------------------

# value changed through options function in main.py 0.015, for debugging set this to 0.00
default_delay = 0.000

# ---------------------------------------- Classes and Structs ---------------------------------------------------------


# defines all the colors and bold and italic for the tags based on ANSI escape sequences
TAG_COLORS = {
    'b': '1',  # Bold
    'it': '3',  # Italic
    'r': '91',  # Red
    'g': '92',  # Green
    'y': '93',  # Yellow
    'p': '95',  # Purple
    'c': '96',  # Cyan
    'lp': '94',  # Light purple
    'o': '33',  # Orange
    'bl': '34'  #blue
}


# ----------------------------------------- Utility Functions ----------------------------------------------------------

# a function to display stored games in a tabular manner
def display_games(stored_games: dict, displayable_games: list):
    headers = ["Index", "Name", "Date", "Time", "Current level", "Used hints"]

    info_mat = []
    for ind, game in enumerate(displayable_games):
        game_dic = stored_games[game]
        current_level = game_dic["current_level"]

        try:
            hints_used = len(game_dic["hints_used"].keys()[current_level])
        except TypeError:
            hints_used = 0

        game_list = game.split("_")
        name = game_dic["player_name"]
        date = game_list[1]
        time = game_list[2]

        row = [f"{ind}.", name, date, time, current_level, hints_used]

        info_mat.append(row)

    sorted_info = sorted(info_mat, key=lambda x: (x[2], x[3]))
    for s_ind in range(len(sorted_info)):
        sorted_info[s_ind][0] = f"{s_ind}."
    # index noch überschreiben mit neuem
    write(f"{tabulate(sorted_info, headers=headers, tablefmt='pretty')}\n \n \n", 0)


# delete all the save states
def delete_all_safe_states():
    clear_console()
    write("So you want to delete all safe states?\n", 0)
    ans = cinput("Please confirm your answer with 'yes' or 'no'\n")
    while True:
        if "y" in ans:
            ans = cinput("Are you sure? (y,n)\n")
            if "y" in ans:
                filename = 'game_data.json'
                existing_data = {}

                # Step 3: Write the modified data back to the file
                with open(filename, 'w') as file:
                    json.dump(existing_data, file, indent=4)
                write("[b][r]All safe states have been deleted![/r][/b]")
                inp = cinput("Press enter to go back to the options menu.\n")
                return False
            else:
                return False
        else:
            return False


def delete_specific_safe_state():
    filename = 'game_data.json'
    write("[b]Options[/b]\n"
          "So you want to [b]delete[/b] a specific safe state.\n")
    name = cinput("Please enter a player name of which you want to delete a safe state.\n").lower()

    if not os.path.exists(filename):
        write("[b]No[/b] game has been played yet.", 0)
    else:
        with open(filename, 'r') as json_file:
            stored_games = json.load(json_file)
        games = [elem for elem in stored_games.keys() if name in elem.lower()]
        if len(games) == 0:
            write("It seems that there are no save games with the entered player name :(\n", 0)
            ans = cinput("Did you misspell or want to delete a different save state? (y,n)\n")
            if "y" in ans:
                delete_specific_safe_state()
            else:
                return False
        else:
            display_games(stored_games, games)
            ans = cinput("Which save state do you want to delete? Please enter the index number.\n").replace(".", "")
            while True:
                if "ex" in ans:
                    return False
                try:
                    ans = int(ans)
                    # Sorting based on date and time
                    sorted_info = sorted(games, key=lambda x: (x.split('_')[1], x.split('_')[2]))
                    del_key = sorted_info[ans]
                    write(f"You are about to delete {del_key}.\n")
                    ans = cinput("Are you sure you want to delete it? (y,n)\n")
                    if "y" in ans:
                        del stored_games[del_key]

                        # Write the modified data back to the file
                        with open(filename, 'w') as json_file:
                            json.dump(stored_games, json_file, indent=4)
                        cinput(f"{del_key} has been successfully deleted. Press enter to continue.\n")
                    return False
                except ValueError:
                    ans = cinput(f"Please select a number between 0 and {len(games) - 1}.\n")
    # TODO finish this

# A simple function to change the typing speed of the write function
def change_typing_speed():
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
    clear_console()
    write("[b]Change writing speed[/b]\n\n"
          "So you want to change the speed of which the text is displayed.\n", 0)

    speed = cinput("Please enter a number between 0 and 10, where 0 is very slow and instantaneous.\n")

    while True:
        try:
            speed = int(speed)
            default_delay = speed_dic[speed]
            write("This is an example to show you the typing speed you entered.\n")
            speed = cinput("Is this good? (y,n)\n").lower()
        except ValueError:
            if "ex" in speed:
                return False
            else:
                speed = cinput("Please enter a number between 0 and 10.")

        if speed == "y" or speed == "yes":
            return False
        elif "ex" in speed:
            return False
        else:
            write("Please enter a new value: \n", 0)
            speed = cinput().lower()


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
                if tag in ['b', 'it', 'r', 'g', 'y', 'p', 'c', 'lp', 'o', 'bl']:
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


def print_hint(hint: str):
    write(f"[y]{hint}[/y]\n")


# This function centers the input prompt to fit the centering of the write function
def cinput(prompt=""):
    padding = (get_terminal_width() - len(prompt)) // 2
    cursor_padding = get_terminal_width() // 2
    input_text = input(' ' * padding + prompt + ' ' * cursor_padding)
    return input_text


# this function handles the basic commands for help, hint and exit
def default_commands(inp: str, hints: list, hint_count: int, game) -> time:
    if "ex" in inp:
        stop = time.time()
        game.save_game()
        return stop
    elif "he" in inp:
        help_text()
    elif "o_h" in inp:
        old_hints = '\n'.join(game.get_hints_used())
        write(f"[y]{old_hints}[/y]\n")
    elif "hin" in inp:
        print_hint(hints[hint_count])
        game.set_hint_used(hints[hint_count])
        hint_count += 1 + len(game.get_hints_used(game.get_current_level()))
    return 0


# a help function that allows the user to always write help to get help
def help_text():
    write("[c]You can either do type the answer. Be aware, that it will require you to enter the answer\n"
          "as stated by the prompt. The other options are: \n"
          "- 'hint', to get a hint for the current puzzle\n"
          "- 'exit', to get back to the main menu.[/c]\n"
          "- 'old_hints' if you loaded a game you can get your hints back\n")


if __name__ == "__main__":
    # Example usage:
    write("[b]Bold[/b] and [it]italic[/it] text. With [r]red[/r], [g]green[/g], [y]yellow[/y], [c]cyan[/c], "
          "[p]purple[/p] and [lp] light purple[/lp] options. \n")
