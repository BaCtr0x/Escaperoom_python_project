import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from utils import write, cinput, clear_console


def get_games_with_completed_levels(games: dict) -> dict:
    filtered_entries = {key: value for key, value in games.items() if value["levels_completed"]}
    return filtered_entries


def get_games_with_used_hints(games: dict) -> dict:
    filtered_entries = {key: value for key, value in games.items() if value["hints_used"]}
    return filtered_entries


def create_dict_completed_levels(games: dict) -> dict:
    res = {}

    for key, value in games.items():
        player_name = value["player_name"]

        if player_name not in res:
            res[player_name] = {}

        for level, time_taken in value["levels_completed"].items():
            if level not in res[player_name] or time_taken < res[player_name][level]:
                res[player_name][level] = time_taken
    print(res)
    return res


# This function filters the loaded games from the json file by a given player name
def filter_dict_by_name(games: dict, name: str) -> dict:
    # reduce list of games to the ones with the given name
    games_list = [elem for elem in games.keys() if name in elem]
    filtered_games = {}
    for game in games_list:
        filtered_games[game] = games[game]

    if len(filtered_games) < 1:
        # get all the names of players with at least one completed puzzle
        names = list({value["player_name"] for key, value in games.items()})

        write("The player you entered has not played a game yet, with at least one completed level.\n"
              "These are the players that have done so:\n", 0)
        [write(f"{ind}. {name}") for ind, name in enumerate(names)]
        inp = cinput("Did you mean one of them? Please select a number or type no.\n").replace(".", "").replace(" ", "")

        # Handle user input
        while True:
            if inp == "no":
                # return an exit dictionary
                return {1: -1}
            elif inp in names:
                name = inp
                break
            else:
                try:
                    inp = int(inp)
                    if inp > len(names):
                        inp = cinput("Please select a valid number.\n")
                    else:
                        name = names[inp]
                        break
                except ValueError:
                    inp = cinput("Please select a enter a valid number.\n")
        games_list = [elem for elem in games.keys() if name in elem]
        filtered_games = {}
        for game in games_list:
            filtered_games[game] = games[game]
    return filtered_games


# Function to plot the games dictionary, which is filtered before hand for times or hints and names or all
def line_plot(games: dict):
    # create a dataframe from the data
    df = pd.DataFrame(games)

    # Use seaborn for plotting
    sns.set(style="darkgrid")

    palette = sns.color_palette("mako_r", len(games.keys()))
    sns.lineplot(data=df, markers=True, palette=palette)

    # Set labels and title
    plt.xlabel('Levels')
    plt.ylabel('Time')
    plt.title('Best Times per Level')

    # Show the plot
    plt.show()


# This function creates a simple line plot for all games by a given player name over the time they needed for the
# entire game
def plot_times_sp(games: dict):
    games = get_games_with_completed_levels(games)
    name = cinput("What is your name?\n")
    games = filter_dict_by_name(games, name)

    # check if the user wanted to go back
    if games == {1: -1}:
        return

    data = create_dict_completed_levels(games)
    # TODO: aus irgend nem Grund sind hier die keys falschrum, aber nur im plot/df later
    line_plot(data)


# This function creates a line plot of the times for each puzzle of all players, where these times are the personal
# bests of each player for each puzzle
def plot_times_all(games: dict):
    games = get_games_with_completed_levels(games)
    data = create_dict_completed_levels(games)

    line_plot(data)


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


def show_menu(clear=False):
    if clear:
        clear_console()
    write("1. Times plot of all players\n"
          "2. Times plot of specific player\n"
          "3. Hints plot of all players\n"
          "4. Hints plot of specific player\n"
          "5. Plot times and hints all players\n"
          "6. Plot times and hints of specific player\n"
          "7. Score board\n"
          "8. exit")


# TODO: this needs to be filled.
#  Maybe write functions for time by name showing the different times for each level by a given name and others
#  and access them through a dictionary, like the main menu management. The functions could then reside in the utils.py
def show_stats() -> bool:
    write("[b] Statistics [/b]")
    filename = 'game_data.json'
    stored_games = {}
    with open(filename, 'r') as json_file:
        stored_games = json.load(json_file)

    # dictionary as an interface
    stat_options = {
        1: plot_times_all,
        2: plot_times_sp,
        3: plot_hints_all,
        4: plot_hints_sp,
        5: plot_times_hints_all,
        6: plot_times_hints_sp,
        7: score_board
    }

    show_menu()
    inp = cinput("What do you want to do, please enter a number.\n")
    while True:
        if "ex" in inp:
            return False
        try:
            inp = int(inp)
            if inp == 8:
                return False
            elif inp < 8:
                stat_options[inp](stored_games)
                show_menu(clear=True)
                inp = cinput("What do you want to do now?\n")
                continue
            else:
                inp = cinput("Please enter a valid number.")
        except ValueError:
            inp = cinput("Please enter a valid number.")
