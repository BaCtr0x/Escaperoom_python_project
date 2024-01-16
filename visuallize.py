import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from tabulate import tabulate

from utils import write, cinput, clear_console, menu_delay


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
    return res


def create_dict_completed_levels_hints(games: dict) -> dict:
    res = {}

    for key, value in games.items():
        player_name = value["player_name"]

        if player_name not in res:
            res[player_name] = {}

        for level, hints_used in value["hints_used"].items():
            if level not in res[player_name] or len(hints_used) < res[player_name][level]:
                res[player_name][level] = len(hints_used)
    return res


def create_dict_completed_levels_same_name(games: dict) -> dict:
    res = {}

    for key, value in games.items():

        if key not in res:
            res[key] = {}

        for level, time_taken in value["levels_completed"].items():
            if level not in res[key] or time_taken < res[key][level]:
                res[key][level] = time_taken
    return res


def create_dict_completed_levels_hints_same_name(games: dict) -> dict:
    res = {}

    for key, value in games.items():

        if key not in res:
            res[key] = {}

        for level, hints_used in value["hints_used"].items():
            if level not in res[key] or len(hints_used) < res[key][level]:
                res[key][level] = len(hints_used)
    return res


def create_dict_for_scatter_plot(times: dict, hints: dict) -> dict:
    # Extracting data for plotting
    player_names = []
    hints_dict = {}
    times_dict = {}

    # Using lambda expression with map and keys
    puzzle_names = max(list(map(lambda x: list(x.keys()), times.values())))

    for key, value in times.items():
        player_names.append(key)
        for pn in puzzle_names:
            if pn in times_dict.keys():
                if pn not in value.keys():
                    times_dict[pn].append(None)
                    hints_dict[pn].append(None)
                else:
                    times_dict[pn].append(value[pn])
                    hints_dict[pn].append(hints[key][pn])
            else:
                if pn not in value.keys():
                    times_dict[pn] = [None]
                    hints_dict[pn] = [None]
                else:
                    times_dict[pn] = [value[pn]]
                    hints_dict[pn] = [hints[key][pn]]

    # Transpose the dictionary by sorting keys in reverse order
    times_dict = {key: times_dict[key] for key in sorted(times_dict.keys(), reverse=True)}
    hints_dict = {key: hints_dict[key] for key in sorted(hints_dict.keys(), reverse=True)}

    # Create dict of DataFrames
    res = {}
    for puzzle in puzzle_names:
        res[puzzle] = {"Player Name": player_names, "Time": times_dict[puzzle], "Hints used": hints_dict[puzzle]}
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
              "These are the players that have done so:\n", menu_delay)
        [write(f"{ind}. {name}", menu_delay) for ind, name in enumerate(names)]
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
def line_plot(games: dict, y_lable: str):
    # create a dataframe from the data
    df = pd.DataFrame(games)

    # Use seaborn for plotting
    sns.set(style="darkgrid")

    palette = sns.color_palette("mako_r", len(games.keys()))
    sns.lineplot(data=df, markers=True, palette=palette)

    # Set labels and title
    plt.xlabel('Levels')
    plt.ylabel(y_lable)
    if "hint" in y_lable.lower():
        plt.title('Fewest hints per Level')
    else:
        plt.title('Best Times per Level')

    # Show the plot
    plt.show()


def scatter_plots(dfs: dict):
    num_plots = len(dfs)
    num_cols = 2  # Number of columns in the subplot grid
    num_rows = -(-num_plots // num_cols)  # Calculate the number of rows needed

    # set seaborn plotting aesthetics as default
    sns.set()

    # Create a subplot grid
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 6 * num_rows))
    axes = axes.flatten()  # Flatten the axes array for easier indexing

    # Set the style outside the loop to apply it to the entire figure
    sns.set(style="darkgrid")

    for i, (puzzle_name, df) in enumerate(dfs.items()):
        df = pd.DataFrame(df)

        # Scatter plot using Seaborn
        palette = sns.color_palette("mako_r", df.count().values[0])

        # Use the current subplot
        ax = axes[i]

        sns.set(style="darkgrid")

        sns.scatterplot(x='Hints used', y='Time', hue='Player Name', data=df, s=100, markers=True,
                        palette=palette, ax=ax)

        # Adding labels and title
        ax.set_xlabel('Number of Hints')
        ax.set_ylabel('Time Taken (seconds)')
        ax.set_title(f'Time vs. Number of Hints for {puzzle_name.replace("_", " ")}')

    # Adjust layout to prevent overlapping titles
    plt.tight_layout()

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

    data = create_dict_completed_levels_same_name(games)
    # TODO: aus irgend nem Grund sind hier die keys falschrum, aber nur im plot/df later
    line_plot(data, "Time")


# This function creates a line plot of the times for each puzzle of all players, where these times are the personal
# bests of each player for each puzzle
def plot_times_all(games: dict):
    games = get_games_with_completed_levels(games)
    data = create_dict_completed_levels(games)

    line_plot(data, "Time")


def plot_hints_sp(games: dict):
    games = get_games_with_completed_levels(games)
    name = cinput("What is your name?\n")
    games = filter_dict_by_name(games, name)

    # check if the user wanted to go back
    if games == {1: -1}:
        return

    data = create_dict_completed_levels_hints_same_name(games)
    # TODO: aus irgend nem Grund sind hier die keys falschrum, aber nur im plot/df later
    line_plot(data, "Hints used")


def plot_hints_all(games: dict):
    games = get_games_with_completed_levels(games)
    data = create_dict_completed_levels_hints(games)

    line_plot(data, "Hints used")


def plot_times_hints_sp(games: dict):
    # filter for at least on finished level
    games = get_games_with_completed_levels(games)

    # filter by an input name
    name = cinput("What is your name?\n")
    games = filter_dict_by_name(games, name)

    # check if the user wanted to go back
    if games == {1: -1}:
        return

    # get dicts for time and hints
    times = create_dict_completed_levels_same_name(games)
    hints = create_dict_completed_levels_hints_same_name(games)

    # create the needed ditcs we use for dataframes
    dicts = create_dict_for_scatter_plot(times, hints)

    scatter_plots(dicts)


def plot_times_hints_all(games: dict):
    games = get_games_with_completed_levels(games)
    times = create_dict_completed_levels(games)
    hints = create_dict_completed_levels_hints(games)
    dfs = create_dict_for_scatter_plot(times, hints)

    scatter_plots(dfs)


# calculates the score based of the time taken and the number of hints used
def calculate_score(time_taken: float, hints_used: int):
    base_score = 10000
    time_penalty = max(0.0, (time_taken - 600.0) // 30.0) * 50.0
    hints_penalty = hints_used * 100
    total_penalty = time_penalty + hints_penalty
    score = max(0.0, base_score - total_penalty)
    return score


# Takes the puzzle string, removes the '_' and turns first letters of words into capital letters
def capitalize_words(s):
    words = s.split('_')
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)


# reverse function of the capitalize_words function
def decapitalize_words(s):
    words = s.lower().split()
    decapitalized_words = '_'.join(words)
    return decapitalized_words


def score_board(games: dict):
    headers = ["Player Name", "Date"]
    puzzle_headers = []
    puzzle_scores = []

    # Extract puzzle names and add headers
    for player in games.values():
        for puzzle, time_hints_dict in player["levels_completed"].items():
            puzzle = capitalize_words(puzzle)
            if f"{puzzle} Time/Hints" not in puzzle_headers:
                puzzle_headers.extend([f"{puzzle} Time/Hints"])

    headers.extend(puzzle_headers)
    headers.append("Score")

    # Populate puzzle times, hints, and calculate scores
    rows = []
    for player_key, player in games.items():
        row = [player["player_name"], " ".join(player_key.split("_")[1:])]
        player_score = 0

        for puzzle in puzzle_headers:
            puzzle = decapitalize_words(puzzle)
            time_taken = player["levels_completed"].get(puzzle.replace("_time/hints", ""), None)
            hints_used = len(player["hints_used"].get(puzzle.replace("_time/hints", ""), []))
            if time_taken is None:
                row.append(f"{time_taken}  / {hints_used}")
            else:
                row.append(f"{time_taken}s / {hints_used}")

        # Calculate and append score
        total_time_taken = sum(
            [player["levels_completed"].get(decapitalize_words(puzzle).replace("_time/hints", ""), 0)
             for puzzle in puzzle_headers])
        total_hints_used = sum(
            [len(player["hints_used"].get(decapitalize_words(puzzle).replace("_time/hints", ""), []))
             for puzzle in puzzle_headers])
        player_score = calculate_score(total_time_taken, total_hints_used)
        row.append(player_score)

        rows.append(row)

    # Sort by score in descending order
    rows = sorted(rows, key=lambda x: x[-1], reverse=True)

    # Print the scoreboard using the tabulate library
    clear_console()
    write("[b]Score Board[/b]\n\n")
    write(f"{tabulate(rows, headers=headers, tablefmt='pretty')}\n \n \n", 0.0050)
    inp = cinput("If you want to close the score board, press enter\n")
    clear_console()


def show_menu(clear=False):
    if clear:
        clear_console()
    write("[b] Statistics [/b]\n\n"
          "1. Times plot of all players\n"
          "2. Times plot of specific player\n"
          "3. Hints plot of all players\n"
          "4. Hints plot of specific player\n"
          "5. Plot times and hints all players\n"
          "6. Plot times and hints of specific player\n"
          "7. Score board\n"
          "8. exit", menu_delay)


# This function handles the general functionality of the show stats section, allowing to call different functions
# via a dictionary as an interface, which makes the function calling more dynamic
def show_stats() -> bool:
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
                inp = cinput("Please enter a valid number.\n")
        except ValueError:
            inp = cinput("Please enter a valid number.\n")
