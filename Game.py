from cesar_puzzle import cesar_puzzle
from logic_puzzle import logic_puzzle
from maze_puzzle import maze_puzzle
from image_puzzle import image_puzzle
from number_puzzle import number_puzzle

import matplotlib.pyplot as plt

from utils import *

# This acts like an interface, here are all the levels that are playable
levels = {
    0: logic_puzzle,
    1: image_puzzle,
    2: number_puzzle,
    3: maze_puzzle,
    4: cesar_puzzle
}

default_filename = 'game_data.json'


# This is the Game class, which will store the current game instance and is used for saving the game
# It also is the heart of the game containing all functions needed, such as play, save_game and load_game
def write_main_story():
    write(
        "[b]The beginning[/b]\n\n"
        "You wake up slowly. The comfort of your dreams vanishes into mist and you feel the cold air of the room\n"
        "brush against your skin. You pull up your blanket and wrap yourself back up to avoid the cold harsh outside\n"
        "world. The old room made of dark wood shines gloomily in the white light of the sun pushing through the\n"
        "thick clouds in the morning sky. The big candle on the desk at the far side of the room still flickers in the\n"
        "soft breeze that pushes through the cracks in the walls. Your notebook open on the last page rests heavy on\n"
        "the table. Its been three days since you started to uncover the strange story the old lady at the bar around\n"
        "the corner told you. A woman came to this secluded village about eight days ago, talking about her lost\n"
        "daughter and that she knows about her whereabouts. That someone brought her here. But for what, she does not\n"
        "know. The old lady told you that the woman went of to a small hut in the mountains, but has not been seen since.\n"
        "Noone knows where this hut is or what it looks like, but after reading multiple articles and scanning the \n"
        "local newspaper for the past three days, you have an idea where it could be. \n \n"
        "The snow falls silently against the window, as you push yourself out under the warm blanket and into your cold\n"
        "pants that rest on the back of the wooden chair. You put on your shirt and the slightly ragged jacked your \n"
        "father gave you years ago. This is not what he wanted, but its a case you where looking for for soo long.\n"
        "Grabbing your notebook and a small flashlight you open the door and make your way to the small hut, hoping \n"
        "to find the woman and maybe even here daughter.\n")


def write_story_ending():
    write(
        "The cold wet air seems to creep into every crack in your cloth, letting you shiver all over. It is dark, very\n"
        "dark, as you continue on. The battery of your flashlight seems to have died and you touch ahead. A few turns\n"
        "later you see the soft orange shimmer cast by a torch. The irony smell of blood rushes into your nose and you\n"
        "push back the urge to vomit. As you get closer you can hear the sad whimpering of woman. Pushing forward you \n"
        "enter a brightly lit room. The walls made of white marmor, torches run around the entire hall illuminating \n"
        "everything in their warm orange light. The smell of blood is almost overwhelming as you look around. \n"
        "It is clean in hear, almost too clean. A few shelf line the left and right walls, filled with neatly stacked \n"
        "books. But in the center of the room you see pedestal of black obsidian, like an otherworldly block of \n"
        "nothingness. Its food rests in a pool of blood and in this pool you see an old lady, kneeling on the floor. \n"
        "Her face in her hands and sobbing uncontrollably. Then you realize there is a woman on the block of darkness.\n"
        "A young lady in a once beautiful outfit. The now dark blouse torn apart, the blue jeans ripped at multiple\n"
        "spots and her shoes are gone completely. \n\n"
        "You step closer, looking for anything that might help you uncover what happened here. You examine the body. \n"
        "Several minutes go by, the old lady doesn't even seem to notice you. There seem to be no clues or anything \n"
        "useful. But then you see small pieces of skin stuck under her nails. And what looks like a small piece of paper\n"
        "in her mouth. Written on it in perfectly curly letters you read a single name, like a signature.\n\n"
        "[it]Irine Lestradh[/it]\n\n"
        "You take out a small plastic back and scrape off some of the skin under her nails and place the letter into \n"
        "another bag. Warping the old lady into a warm huge you help her get out of this dark and twisted version of \n"
        "an escape room and go back to the tavern you first heard of this case, hoping that the lady will some day \n"
        "recover from what ever this was. But you are certain that with the evidence you found the police will be able\n"
        "to find whoever did this.\n\n"
        "[b]Five weeks later[/b]\n\n"
        "Its been five weeks working closely with the local police. The skin you found under her nails could be linked\n"
        "to a woman in her mid 40th with the name mathing the signature of the piece of paper you found as well.\n"
        "It seems that Elisabeth, the name of the murdered woman, was able to rip off this piece from one of the books\n"
        "In the maze and hide hit before she was murdered. Her mother is still in rehab, but seems to be doning better\n"
        "every day, but this will take much longer. Everything seems grim and noone was able to find the hut through\n"
        "which you entered the rooms of horror, but at least you know who the murderer is and only need to find her!\n"
    )


class Game:
    def __init__(self, player_name, current_level=0):
        # '_' makes the variable protected and not viewable from outside the game class
        self._player_name = player_name
        self._current_level = current_level
        self._levels_completed = {}
        self._hints_used = {}

        # for storing the game, we need a unique identifier for the json key
        self._unique_identifier = self.generate_unique_identifier()
        self._level_state = {}
        for level in levels.values():
            # str(level) = <function logic_puzzle at 0x000001843C90E5C0>
            # str(level).split(" ") = ["function", "logic_puzzle", "at", "0x000001843C90E5C0"]
            # str(level).split(" ")[1] = "logic_puzzle"
            name = str(level).split(" ")[1]

            # creates dictionary with name as key and an empty dictionary as value
            self._level_state[name] = {"death": False}

    # getter for the level name
    def get_level_name(self, level_ind=-1) -> str:
        if level_ind == -1:
            return str(levels[self._current_level]).split("at")[0].split(" ")[1]
        else:
            return str(levels[level_ind]).split("at")[0].split(" ")[1]

    # getter for the player name
    def get_player_name(self) -> str:
        return self._player_name

    # getter for the current level
    def get_current_level(self) -> int:
        return self._current_level

    # getter for the completed levels
    def get_levels_completed(self) -> dict:
        return self._levels_completed

    # getter for the used hints
    def get_hints_used(self, level_ind=-1) -> list:
        if level_ind == -1:
            return self._hints_used[self.get_level_name(self._current_level)]
        try:
            return self._hints_used[self.get_level_name(level_ind)]
        except KeyError:
            return []

    # setter for the used hints
    def set_hint_used(self, hint: str):
        level = self.get_level_name()
        if level not in self._hints_used.keys():
            self._hints_used[level] = [hint]
        else:
            self._hints_used[level].append(hint)

    # setter for the state of the level
    def set_level_state(self, state: {}):
        name = str(levels[self._current_level]).split(" ")[1].split(" ")[0]
        self._level_state[name] = state

    # getter for the state of the current level
    def get_level_state(self):
        name = str(levels[self._current_level]).split(" ")[1].split(" ")[0]
        return self._level_state[name]

    # This function create a unique identifier by using the player name in lower case and the current date and time
    def generate_unique_identifier(self) -> str:
        return f"{self._player_name.lower()}_{get_date()}"

    def get_levels(self):
        level_list = []
        for level in levels.values():
            level_list.append(str(level).split(" ")[1])
        return level_list

    # store the completed level and update the important information
    def complete_level(self, level: str, time_taken: time):
        if level in self._levels_completed.keys():
            self._levels_completed[level] += time_taken
        else:
            self._levels_completed[level] = time_taken
        # self._hints_used[level] = hints_used
        self._current_level += 1
        self.save_game()

    # save the game
    def save_game(self, filename=default_filename):
        # create dictionary with the needed information
        game_data = {
            'player_name': self._player_name,
            'current_level': self._current_level,
            'levels_completed': self._levels_completed,
            'hints_used': self._hints_used,
            'level_state': self._level_state
        }

        # check if the path of the filename points to an existing file and if so read it and get the information from it
        if os.path.exists(filename):
            # If the file exists, load existing data, only read permissions ('r')
            with open(filename, 'r') as json_file:
                existing_data = json.load(json_file)
        else:
            # If the file doesn't exist, create an empty list
            existing_data = {}

        # Add the current game data to the existing data
        existing_data[self._unique_identifier] = game_data

        # Save the updated data to the file with write permissions 'w'
        with open(filename, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

    # this function lets the user play the game
    def play(self) -> int:
        # as long as the player has not completed all levels run the current puzzle, after that store time and go to
        # the next level. Exit if the player used the exit command
        while self._current_level < len(levels.keys()):
            write(f"[b]Room {self._current_level}[/b]")
            level_time, ex = levels[self._current_level](self)

            # if the player entered the exit command close the play function
            if ex == 1:
                return 1
            # level_name = str(levels[self._current_level]).split("at")[0].split(" ")[1]
            level_name = str(levels[self._current_level]).split(" ")[1]
            self.complete_level(level_name, level_time)

            # this allows the player to move to the next room at his own time
            cinput("Press enter to continue.\n")
            plt.close('all')
            clear_console()

        # write the end of the story if the player solved all puzzles
        write_story_ending()
        write("[b]Thanks for playing our game, we hope you enjoyed it :)[/b]\n")

        # allows the player to directly end the game or go back to the main menu
        inp = cinput("Do you want to go back to the main menu (1) or exit the game (2)?\n")

        # a simple check of the user input to prevent errors
        try:
            inp = int(inp)
            return inp
        except KeyError:
            write("You entered something else, we will move you to the main menu :)\n")
            return 1

    # This function allows us to load the game
    def load_game(self, filename=default_filename):
        # check whether the path of the filename points to an existing file or not
        if not os.path.exists(filename):
            write("[b]No[/b] game has been played yet.", menu_delay)
        else:
            # read the saved games
            with open(filename, 'r') as json_file:
                stored_games = json.load(json_file)
                # check for games with the entered player name
                games = [elem for elem in stored_games.keys() if self._player_name.lower() in elem.lower()]

                if len(games) > 0:
                    # remove games which have been completed, as there is no point in loading them
                    loadable_games = list(filter(lambda key: stored_games[key]['current_level'] != len(levels.keys()),
                                                 games))
                    # Check if the player died any of the states and remove the corresponding state from the loadable
                    # games
                    for id in loadable_games:
                        if 0 < stored_games[id]["current_level"] < 3 and \
                                (stored_games[id]["level_state"]["image_puzzle"]["death"] or
                                 stored_games[id]["level_state"]["number_puzzle"]["death"]):
                            loadable_games.remove(id)

                    # handle the case in which no game can be loaded as all games are either completed or filled with
                    # dead players
                    if len(loadable_games) == 0:
                        write("It seems that all the games with your name are already completed or ended in death.\n", 0)
                        ans = cinput("Do you want to load a different player? (y,n)\n")
                        if "y" in ans:
                            ans = cinput("Which player do you want to load?\n")
                            self._player_name = ans
                            self.load_game()
                        else:
                            return

                    # displays the games that are loadable in a tabular manner
                    display_games(stored_games, loadable_games, self.get_levels())

                    inp = cinput("Which game do you want to load (Index)?\n")
                    # Error handling if the user input is not a number
                    while True:
                        if "ex" in inp:
                            return
                        try:
                            inp = int(inp)
                            break
                        except ValueError:
                            inp = cinput("Please enter just the index number for the save you want to load or enter exit to go back.\n")

                    # get the information from the json file and store them in the current game instance
                    game_data = stored_games[loadable_games[inp]]
                    self._player_name = game_data["player_name"]
                    self._current_level = game_data["current_level"]
                    self._levels_completed = game_data["levels_completed"]
                    self._hints_used = game_data["hints_used"]
                    self._unique_identifier = games[inp]
                    self._level_state = game_data["level_state"]

                    # clear console before running the game
                    clear_console()
                    # start the game after loading the values
                    self.play()

                # Handle the case in which no game with the entered player name exists, but this should not happen as it
                # is handled above
                else:
                    write("There is [b] no [/b] game save with your player name.")
                    ans = cinput("Did you misspell your name? (y,n)?\n")
                    if "y" in ans:
                        ans = cinput("What is your name?\n")
                        self._player_name = ans
                        self.load_game()
