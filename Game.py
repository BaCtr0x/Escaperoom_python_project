from cesar_puzzle import cesar_puzzle
from logic_puzzle import logic_puzzle
from maze_puzzle import maze_puzzle

from utils import *

# This acts like an interface, here are all the levels that are playable
levels = {
    0: logic_puzzle,
    1: maze_puzzle,
    2: cesar_puzzle
}

default_filename = 'game_data.json'


# This is the Game class, which will store the current game instance and is used for saving the game
# It also is the heart of the game containing all functions needed, such as play, save_game and load_game
def write_main_story():
    write(
        "You wake up slowly. The comfort of your dreams vanishes into mist and you feel the cold air of the room\n"
        "brush against your skin. You pull up your blanket and wrap yourself back up to avoid the cold harsh outside\n"
        "world. The old room made of dark wood shines gloomily in the white light of the sun pushing through the\n"
        "thick clouds in the morning sky. The big candle on the desk at the far side of the room still flikers in the\n"
        "soft breeze that pushes through the cracks in the walls. Your notebook open on the last page rests heavy on\n"
        "the table. Its been three days since you started to uncover the strange story the old lady at the bar around\n"
        "the corner told you. A woman came to this secluded village about eight days ago, talking about her lost\n"
        "daughter and that shes knows about her whereabouts. That someone brought her here. But for what, she does not\n"
        "know. The old lady told you that the woman went of to a small hut in the mountains, but has not been seen since.\n"
        "Noone knows where this hut is or what it looks like, but after reading multiple articles and scanning the \n"
        "local newspaper for the past three days, you have an idea where it could be. \n \n"
        "The snow falls silently against the window, as you push yourself our under the warm blanket and into your cold\n"
        "pants that rest on the back of the wooden chair. You put on your shirt and the slightly ragged jacked your \n"
        "father gave you years ago. This is not what he wanted, but its a case you where looking for for soo long.\n"
        "Grabbing your notebook and a small flashlight you open the door and make your way to the small hut, hoping \n"
        "to find the woman and maybe even here daughter.\n")


class Game:
    def __init__(self, player_name, current_level=0):
        self._player_name = player_name
        self._current_level = current_level
        self._levels_completed = {}
        self._hints_used = {}
        self._unique_identifier = self.generate_unique_identifier()
        self._level_state = {}
        for level in levels.values():
            name = str(level).split(" ")[1].split(" ")[0]
            self._level_state[name] = {}

    def __get_level_name(self, level_ind=-1) -> str:
        if level_ind == -1:
            return str(levels[self._current_level]).split("at")[0].split(" ")[1]
        else:
            return str(levels[level_ind]).split("at")[0].split(" ")[1]

    def get_player_name(self) -> str:
        return self._player_name

    def get_current_level(self) -> int:
        return self._current_level

    def get_levels_completed(self) -> dict:
        return self._levels_completed

    def get_hints_used(self, level_ind=-1) -> list:
        if level_ind == -1:
            return self._hints_used[self.__get_level_name(self._current_level)]
        try:
            return self._hints_used[self.__get_level_name(level_ind)]
        except KeyError:
            return []

    def set_level_state(self, state: {}):
        name = str(levels[self._current_level]).split(" ")[1].split(" ")[0]
        self._level_state[name] = state

    def get_level_state(self):
        name = str(levels[self._current_level]).split(" ")[1].split(" ")[0]
        return self._level_state[name]

    def set_hint_used(self, hint: str):
        level = self.__get_level_name()
        if self.__get_level_name() not in self._hints_used.keys():
            self._hints_used[level] = [hint]
        else:
            self._hints_used[level].append(hint)

    def generate_unique_identifier(self) -> str:
        return f"{self._player_name.lower()}_{get_date()}"

    def complete_level(self, level: str, time_taken: time, hints_used: list):
        if level in self._levels_completed.keys():
            self._levels_completed[level] += time_taken
        else:
            self._levels_completed[level] = time_taken
        self._hints_used[level] = hints_used
        self._current_level += 1
        self.save_game()

    def save_game(self, filename=default_filename):
        game_data = {
            'player_name': self._player_name,
            'current_level': self._current_level,
            'levels_completed': self._levels_completed,
            'hints_used': self._hints_used,
            'level_state': self._level_state
        }

        if os.path.exists(filename):
            # If the file exists, load existing data
            with open(filename, 'r') as json_file:
                existing_data = json.load(json_file)
        else:
            # If the file doesn't exist, create an empty list
            existing_data = {}

        # Add the current game data to the existing data
        existing_data[self._unique_identifier] = game_data

        # Save the updated data to the file
        with open(filename, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

    def play(self) -> int:
        while self._current_level < len(levels.keys()):
            level_time, hints, ex = levels[self._current_level](self)
            if ex == 1:
                return 1
            level_name = str(levels[self._current_level]).split("at")[0].split(" ")[1]
            self.complete_level(level_name, level_time, hints)
        write("[b]Thanks for playing our game, we hope you enjoyed it :)[/b]\n")
        inp = cinput("Do you want to go back to the main menu (1) or exit the game (2)?\n")
        try:
            inp = int(inp)
            return inp
        except KeyError:
            write("You entered something else, we will move you to the main menu :)\n")
            return 1

    def load_game(self, filename=default_filename):
        if not os.path.exists(filename):
            write("[b]No[/b] game has been played yet.", 0)
        else:
            with open(filename, 'r') as json_file:
                stored_games = json.load(json_file)
                games = [elem for elem in stored_games.keys() if self._player_name.lower() in elem]

                if len(games) > 0:
                    loadable_games = list(filter(lambda key: stored_games[key]['current_level'] != len(levels.keys()),
                                                 games))
                    if len(loadable_games) == 0:
                        write("It seems that all the games with your name are already completed.\n", 0)
                        ans = cinput("Do you want to load a different player? (y,n)\n")
                        if "y" in ans:
                            ans = cinput("Which player do you want to load?\n")
                            self._player_name = ans
                            self.load_game()
                        else:
                            return

                    # remove all the games that are completed
                    # writes all the possible games to load with the given name
                    for ind, game in enumerate(loadable_games):
                        write(f"{ind}. {game}", 0)

                    inp = cinput("Which game do you want to load (number)?\n")
                    # Error handling if the user input is not a number
                    while True:
                        if inp == "exit":
                            return
                        try:
                            inp = int(inp)
                            break
                        except ValueError:
                            inp = cinput("Please enter just the number corresponding to the save you want to load.\n")
                    game_data = stored_games[loadable_games[inp]]
                    self._player_name = game_data["player_name"]
                    self._current_level = game_data["current_level"]
                    self._levels_completed = game_data["levels_completed"]
                    self._hints_used = game_data["hints_used"]
                    self._unique_identifier = games[inp]
                    self._level_state = game_data["level_state"]
                    clear_console()
                    # start the game after loading the values
                    self.play()

                else:
                    write("There is [b] no [/b] game save with your player name.")
                    ans = cinput("Did you misspell your name? (y,n)?\n")
                    if "y" in ans:
                        ans = cinput("What is your name?\n")
                        self._player_name = ans
                        self.load_game()
