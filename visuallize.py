import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import json
from utils import write, cinput


def get_games_with_completed_levels(games: dict) -> dict:
    filtered_entries = {key: value for key, value in games.items() if value["levels_completed"]}
    return filtered_entries


def get_games_with_used_hints(games: dict) -> dict:
    filtered_entries = {key: value for key, value in games.items() if value["hints_used"]}
    return filtered_entries


def create_dict_completed_levels(games: dict) -> dict:
    print("moin")


# This function filters the loaded games from the json file by a given player name
def filter_dict_by_name(games: dict, name: str) -> dict:
    games_list = [elem for elem in games.keys() if name in elem]
    filtered_games = {}
    for game in games_list:
        filtered_games[game] = games[game]
    return filtered_games


# This function creates a simple line plot for all games by a given player name over the time they needed for the
# entire game
def plot_times_sp(games: dict, name: str):
    print("moin")


def plot_times_all(games: dict):
    games = get_games_with_completed_levels(games)
    df = pd.DataFrame(games)
    sb.lineplot()
    print("moin")


def plot_hints_sp(games: dict):
    print("moin")


def plot_hints_all(games: dict):
    print("moin")


def plot_times_hints_sp(games: dict):
    print("moin")


def plot_times_hints_all(games: dict):
    print("moin")


def score_board(games: dict):
    print("moin")


# TODO: this needs to be filled.
#  Maybe write functions for time by name showing the different times for each level by a given name and others
#  and access them through a dictionary, like the main menu management. The functions could then reside in the utils.py

def show_stats() -> bool:
    write("[b] Statistics [/b]")
    filename = 'game_data.json'
    stored_games = {}
    with open(filename, 'r') as json_file:
        stored_games = json.load(json_file)

    stat_options = {
        1: plot_times_all,
        2: plot_times_sp,
        3: plot_hints_all,
        4: plot_hints_sp,
        5: plot_times_hints_all,
        6: plot_times_hints_sp,
        7: score_board
    }

    write("1. Times plot of all players\n"
          "2. Times plot of specific player\n"
          "3. Hints plot of all players\n"
          "4. Hints plot of specific player\n"
          "5. Plot times and hints all players\n"
          "6. Plot times and hints of specific player\n"
          "7. Score board\n"
          "8. exit")
    inp = cinput("What do you want to do, please enter a number.\n")
    while True:
        try:
            inp = int(inp)
            if inp == 8:
                return True
            elif inp < 9:
                return stat_options[inp](stored_games)
            else:
                inp = cinput("Please enter a valid number.")
        except KeyError:
            inp = cinput("Please enter a valid number.")
