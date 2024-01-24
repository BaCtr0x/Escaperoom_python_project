import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from tabulate import tabulate

from utils import write, cinput, clear_console, menu_delay


ordered_level = []


# Helper function that extracts the games with completed levels
def get_games_with_completed_levels(games: dict) -> dict:
    filtered_entries = {key: value for key, value in games.items() if value["levels_completed"]}
    return filtered_entries


# helper function that extracts the games with used hints
def get_games_with_used_hints(games: dict) -> dict:
    filtered_entries = {key: value for key, value in games.items() if value["hints_used"]}
    return filtered_entries


# This function creates a dictionary of all the games that have at least one completed level for all players
def create_dict_completed_levels(games: dict) -> dict:
    res = {}

    # go over the games with their key and value
    for key, value in games.items():
        player_name = value["player_name"]

        # if the player name is not yet in the results dictionary add it
        if player_name not in res:
            res[player_name] = {}

        # set the res of the current player to the level and store the time he took in the last session
        # instead we could loop over all level check if the player completed it and otherwise enter -1 as time to
        # indicate a not finished level
        for level, time_taken in value["levels_completed"].items():
            if level not in res[player_name] or time_taken < res[player_name][level]:
                res[player_name][level] = time_taken
    return res


# similar to the create_dict_completed_levels function but with hints instead of completed levels
def create_dict_completed_levels_hints(games: dict) -> dict:
    res = {}

    for key, value in games.items():
        player_name = value["player_name"].lower()

        # add the player to the res dictionary if it is not in it yet
        if key not in res:
            res[player_name] = {}

        # go over every level of the possible levels
        for level in ordered_level:
            #
            try:
                _ = res[player_name][level]
            except KeyError:
                res[player_name][level] = 0
            try:
                _ = len(value["hints_used"][level])
            except KeyError:
                value["hints_used"][level] = []

            if res[player_name][level] < len(value["hints_used"][level]):
                res[player_name][level] = len(value["hints_used"][level])
    return res


# As before but with a given name and not all players
def create_dict_completed_levels_same_name(games: dict) -> dict:

    res = {}

    # go over the games dictionary and create the dictionary of completed games
    for key, value in games.items():
        # get the name
        name = key.split("_")[0]

        # check whether the unique identifier (key) is already in res
        if key not in res:
            res[name] = value["levels_completed"]

        # go over the levels and times and add them to the res if it is a better time then the one seen before
        # we do this so we can plot the best times for the player
        for level, time_taken in value["levels_completed"].items():
            if time_taken < res[name][level]:
                res[name][level] = time_taken
    return res


# This function extracts all the information from the time dictionary and hints dictionary needed for the scatter plot
def create_dict_for_scatter_plot(times: dict, hints: dict, games_keys=None) -> dict:
    # Extracting data for plotting
    player_names = []
    hints_dict = {}
    times_dict = {}

    # Using lambda expression with map and keys
    # list(map(lambda x: list(x.keys()), times.values())) gets a list with different number of levels
    # [
    # ['logic_puzzle', 'image_puzzle', 'maze_puzzle', 'number_puzzle'],
    # ['logic_puzzle', 'image_puzzle'],
    # ['logic_puzzle']
    # ]
    # max() selects the one with the most played levels
    puzzle_names = max(list(map(lambda x: list(x.keys()), times.values())))

    # go over the dictionary of times, containing players and their corresponding time for each level
    for key, value in times.items():
        player_names.append(key)

        # make the key lower case
        key = key.lower()

        # now go over the levels and add times and hints accordingly, pn == puzzle name
        for pn in puzzle_names:
            # check if we have seen the puzzle before, if so we can append otherwise we need to create a new instance
            if pn in times_dict.keys():
                # check whether the puzzle is in the times dictionary or not
                # if not add None for times and -1 for hints
                if pn not in value.keys():
                    times_dict[pn].append(None)
                    hints_dict[pn].append(0)
                else:
                    times_dict[pn].append(value[pn])
                    # check whether the player used any hints for the current puzzle if not then just place a 0
                    # otherwise enter the corresponding number
                    if pn not in hints[key].keys():
                        hints_dict[pn].append(0)
                    else:
                        hints_dict[pn].append(hints[key][pn])
            else:
                # if there is no time for the puzzle
                if pn not in value.keys():
                    times_dict[pn] = [None]
                    hints_dict[pn] = [0]
                else:
                    times_dict[pn] = [value[pn]]
                    # same as above, but without appending but instead adding the first entry to it
                    if pn not in hints[key].keys():
                        hints_dict[pn] = [0]
                    else:
                        hints_dict[pn] = [hints[key][pn]]

    # now hints_dict looks like this:
    # {'cesar_puzzle': [0, 0, 0, 0, 0], 'image_puzzle': [0, 0, 0, 0, 0], 'logic_puzzle': [0, 3, 0, 2, 1],
    # 'maze_puzzle': [2, 0, 0, 2, 0], 'number_puzzle': [0, 0, 0, 0, 0]}

    # Transpose the dictionary by sorting keys in reverse order
    #times_dict = {key: times_dict[key] for key in sorted(times_dict.keys(), reverse=True)}
    #hints_dict = {key: hints_dict[key] for key in sorted(hints_dict.keys(), reverse=True)}

    # Create dict of DataFrames
    res = {}
    for puzzle in puzzle_names:
        res[puzzle] = {"Player Name": player_names, "Time": times_dict[puzzle], "Hints used": hints_dict[puzzle]}
    return res


# This function filters the loaded games from the json file by a given player name
def filter_dict_by_name(games: dict, name: str) -> dict:
    # reduce list of games to the ones with the given name
    games_list = [elem for elem in games.keys() if name.lower() in elem]
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
                    if inp > len(names)-1:
                        inp = cinput("Please select a valid number.\n")
                    else:
                        name = names[inp]
                        break
                except ValueError:
                    inp = cinput("Please select a enter a valid number.\n")
        # filter the filtered games list again by the entered name
        games_list = [elem for elem in games.keys() if name in elem]
        filtered_games = {}
        for game in games_list:
            filtered_games[game] = games[game]
    return filtered_games


# Function to plot the games dictionary, which is filtered before hand for times or hints and names or all
def line_plot(games: dict, y_lable: str):

    # create a dataframe from the data
    df = pd.DataFrame(games)

    # Reorder the DataFrame based on the ordered_level list
    df = df.reindex(ordered_level)

    # Use seaborn for plotting
    sns.set(style="darkgrid")

    # define the colors for the plot
    palette = sns.color_palette("mako_r", len(games.keys()))

    # do the line plot based on the data, marker true for node and color via palette
    sns.lineplot(data=df, markers=True, palette=palette)

    # Set labels and title
    plt.xlabel('Levels')
    plt.ylabel(y_lable)
    if "hint" in y_lable.lower():
        plt.title('Fewest hints per Level')
    else:
        plt.title('Best Times per Level')

    # make the plot interactive such that the user can press enter inside the console to continue
    plt.ion()

    # Show the plot
    plt.show()

    # press enter to close all plots
    cinput("Press enter to continue.\n")
    plt.close("all")


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

    # make the plot interactive such that the user can press enter inside the console to continue
    plt.ion()

    # Show the plot
    plt.show()

    # press enter to close all plots
    cinput("Press enter to continue.\n")
    plt.close('all')


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

    data = create_dict_completed_levels_hints(games)

    # data comes in reversed, so we need to fix this like this
    data = dict(reversed(data.items()))

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
    hints = create_dict_completed_levels_hints(games)

    games_keys = list(games.keys())

    # create the needed ditcs we use for dataframes
    dicts = create_dict_for_scatter_plot(times, hints, games_keys)

    # create the scatter plot based on the dictionary
    scatter_plots(dicts)


# this plots the times and hints of all players in one graph
def plot_times_hints_all(games: dict):
    games = get_games_with_completed_levels(games)
    times = create_dict_completed_levels(games)
    hints = create_dict_completed_levels_hints(games)
    dfs = create_dict_for_scatter_plot(times, hints)

    scatter_plots(dfs)


# calculates the score based of the time taken and the number of hints used
def calculate_score(time_taken: float, hints_used: int):
    base_score = 10000
    # for every 30 seconds above 10 minutes get a penalty of 50 points
    time_penalty = max(0.0, (time_taken - 600.0) // 30.0) * 50.0

    # add a penalty of 100 points for each hint used
    hints_penalty = hints_used * 100

    total_penalty = time_penalty + hints_penalty

    # just make sure that we do not have a negative score at the end
    score = max(0.0, base_score - total_penalty)
    return score


# Takes the puzzle string, removes the '_' and turns first letters of words into capital letters
def capitalize_words(s):
    words = s.split('_')

    # turns the first letter into an upper case letter
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)


# reverse function of the capitalize_words function
def decapitalize_words(s):
    words = s.lower().split()
    decapitalized_words = '_'.join(words)
    return decapitalized_words


# This function display the score board in a tabular manner
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
        # the first entry in the row is the player name
        row = [player["player_name"], " ".join(player_key.split("_")[1:])]
        player_score = 0

        # go over the puzzles and obtain the time and hints used per level
        for puzzle in puzzle_headers:
            # at this point puzzle is capitalized for the header, so we need to recapitalize them for the search
            puzzle = decapitalize_words(puzzle)

            # get the time and hints used, here we get the entry of the current puzzle from the json and set
            # the time_taken to None if there is no entry in the dictionary
            # We do the same for hints
            time_taken = player["levels_completed"].get(puzzle.replace("_time/hints", ""), None)
            hints_used = player["hints_used"].get(puzzle.replace("_time/hints", ""), None)

            # as we want to display the number of hints, we get the len of the list if the player used any kind of hint
            if hints_used is not None:
                hints_used = len(hints_used)

            # write the time of time_taken without the s if there is no time for the current puzzle
            if time_taken is None:
                row.append(f"{time_taken} / {hints_used}")
            else:
                if hints_used is None:
                    row.append(f"{time_taken}s / {0}")
                else:
                    row.append(f"{time_taken}s / {hints_used}")

        # Calculate and append score
        # the total_time_taken is calculated similarly to the time_taken, but with a for loop to loop over all times
        # and create a list with all times, after that summ them up using sum()
        total_time_taken = sum(
            [player["levels_completed"].get(decapitalize_words(puzzle).replace("_time/hints", ""), 0)
             for puzzle in puzzle_headers])
        total_hints_used = sum(
            [len(player["hints_used"].get(decapitalize_words(puzzle).replace("_time/hints", ""), []))
             for puzzle in puzzle_headers])

        # call calculate_score to obtain the score of the player
        player_score = calculate_score(total_time_taken, total_hints_used)

        # Check if the player died if so set the score to Dead instead of a number
        if player["level_state"]["image_puzzle"]["death"] or player["level_state"]["number_puzzle"]["death"]:
            # we append a placeholder to add Died in red later and have the correct stile in the table
            row.append(-1.0)
        else:
            row.append(player_score)

        rows.append(row)

    # Sort by score in descending order ([-1])
    rows = sorted(rows, key=lambda x: x[-1], reverse=True)

    # Print the scoreboard using the tabulate library
    clear_console()
    write("[b]Score Board[/b]\n\n")

    # write the tabulate to the console based on the information in rows, the header as defined at the top and using
    # the pretty stile
    write(f"{tabulate(rows, headers=headers, tablefmt='pretty')}\n \n \n".replace("-1.0", "[r]Dead[/r]"), 0.0050)

    # allow the player to continue by pressing enter
    inp = cinput("If you want to close the score board, press enter\n")
    clear_console()


# This function displays the statistics menu and clears the console if wanted
def show_menu(clear=False):
    # if we want to clear the console before we do this here
    if clear:
        clear_console()

    # write the menu to the console using the write function to allow centering and formatting tags
    write("[b] Statistics [/b]\n\n"
          "1. Times plot of all players\n"
          "2. Times plot of specific player\n"
          "3. Hints plot of all players\n"
          "4. Hints plot of specific player\n"
          "5. Plot times and hints all players\n"
          "6. Plot times and hints of specific player\n"
          "7. Score board\n"
          "8. exit", menu_delay)


# This is just to make sure later that the dataframe for the player specific plots is ordered correctly
def set_ordered_level(stored_games: dict):
    # load the global variable ordered_level
    global ordered_level

    # take the first entry in the stored_games and go over the levels in the level_state section to store the correct
    # order of levels
    for level in stored_games[list(stored_games.keys())[0]]["level_state"]:
        ordered_level.append(level)


# This function handles the general functionality of the show stats section, allowing to call different functions
# via a dictionary as an interface, which makes the function calling more dynamic
def show_stats() -> bool:
    # define the path to the file of stored games
    filename = 'game_data.json'
    stored_games = {}

    # fill the stored_games dictionary with the information from the file
    with open(filename, 'r') as json_file:
        stored_games = json.load(json_file)

    # create the list of the levels in played order
    set_ordered_level(stored_games)

    # dictionary as an interface as done for the main menu
    stat_options = {
        1: plot_times_all,
        2: plot_times_sp,
        3: plot_hints_all,
        4: plot_hints_sp,
        5: plot_times_hints_all,
        6: plot_times_hints_sp,
        7: score_board
    }

    # display the main menu of the statistics section
    show_menu()

    # ask the player what he wants to do
    inp = cinput("What do you want to do, please enter a number.\n")

    # handle the player input
    while True:
        # allow the player to always exit the menu
        if "ex" in inp:
            return False

        # try to convert the input into an integer, if this doesn't work the player did not enter a valid number
        # we presume that the player will not enter the entire name but rather opt for a number as mentioned in
        # the prompt
        try:
            inp = int(inp)
            if inp == 8:
                return False

            # check whether the inserted number is within the range of options or below/above
            elif 0 < inp < 8:
                stat_options[inp](stored_games)
                show_menu(clear=True)
                inp = cinput("What do you want to do now? Please enter a number.\n")
                continue
            else:
                inp = cinput("Please enter a valid number.\n")
        # we get a ValueError if we want to convert something that is not a number into an integer
        except ValueError:
            inp = cinput("Please enter a valid number.\n")
