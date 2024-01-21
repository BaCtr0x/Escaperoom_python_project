from Game import *
from utils import write, clear_console, change_typing_speed, cinput, default_commands
from visuallize import show_stats


# This is the main file in which the outer structure of the game is going to be placed


def launch_game() -> bool:
    clear_console()

    # create a game instance, based in the name enter
    name = cinput("What is your name?:\n")
    game = Game(name)
    clear_console()

    # print the main story
    write_main_story()

    # calls puzzles in order and stores the returned time in the dictionary

    cont = game.play()

    if cont == 1:
        return False
    else:
        return True


def load_game() -> bool:
    write("[b] Load a game [/b]\n", menu_delay)
    name = cinput("What is your name?\n")
    if "exit" in name:
        return False
    game = Game(name)
    game.load_game()
    return False


def show_option_menu(clear=False):
    if clear:
        clear_console()

    write("[b]Options[/b]\n", menu_delay)

    write("1. Change writing speed\n"
          "2. Delete a specific save state\n"
          "3. Delete all save states\n"
          "4. Exit", menu_delay)


def options() -> bool:
    options_func = {
        1: change_typing_speed,
        2: delete_specific_safe_state,
        3: delete_all_safe_states
    }
    show_option_menu(True)
    op = cinput("What do you want to do?\n").lower()
    while True:
        try:
            op = int(op)
        except ValueError:
            if "change" in op:
                op = 1
            elif "specific" in op:
                op = 2
            elif "all" in op:
                op = 3
            elif "ex" in op:
                return False
        try:
            if op == 4:
                return False
            options_func[op]()
            show_option_menu(True)
            op = cinput("What do you want to do\n")
        except KeyError:
            op = cinput("Please enter a valid number or operation name.\n")


def exit_game():
    # TODO: check if unsaved information is still running, save them end the programm,
    #  i think we dont need this function anymore
    return True


def main_menu_selection(inp: str) -> int:
    # options the user could input
    options = ["play", "load", "show", "options", "exit"]

    # remove '.' and make input lower case
    inp = inp.lower().replace(".", "")

    # check if the input made by the user contains any of the options given above
    elems = [element for element in options if element in inp]

    # extract the number in the input string of the user using a regular expression
    num = re.search(r'[1-5]', inp)

    # error handling and returning the selected number
    if 0 != len(elems):
        return options.index(elems[0]) + 1
    elif num is not None:
        return int(num.string)
    else:
        return -1


def main_menu():
    clear_console()
    game_dic = {
        1: launch_game,
        2: load_game,
        3: show_stats,
        4: options,
        5: exit_game
    }
    load_writing_speed()

    # helper variable for displaying menu
    run = 0
    user_inp = -1
    bexit = False
    while not bexit:
        if run == 0:
            write("[b]Main menu[/b]\n\n"
                  "1. Play game \n"
                  "2. Load game \n"
                  "3. Show stats \n"
                  "4. Options \n"
                  "5. Exit game\n"
                  "\n\n You can navigate the menus by either entering the corresponding number or typing the name of "
                  "the operation you want to select. An confirm your input by pressing 'enter'.\n\n"
                  "You can always type 'help', to see what you can do.\n", menu_delay)
            user_inp = main_menu_selection(cinput("What do you want to do?\n"))
        if user_inp != -1:
            clear_console()
            bexit = game_dic[user_inp]()
            clear_console()
            run = 0
        else:
            write("Please enter either a number between 1 and 5 or for example 'Play Game'", menu_delay)
            user_inp = main_menu_selection(cinput(""))
            run = 1


# for debugging
if __name__ == "__main__":
    main_menu()
