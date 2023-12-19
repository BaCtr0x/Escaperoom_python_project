import re

from cesar_puzzle import cesar_puzzle
from logic_puzzle import logic_puzzle
from utils import write, clear_console, change_typing_speed, cinput
# This is supposed to be the main file in which the outer structure of the game is going to be placed


def launch_game():
    clear_console()
    # print the main story
    write("You wake up slowly. The comfort of your dreams vanishes into mist and you feel the cold air of the room\n"
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
    # calls puzzles in order and stores the returned time in the dictionary
    times = {
        "logic_puzzle": logic_puzzle(),
        "cesar_puzzle": cesar_puzzle()
    }


def load_game():
    print("moin")


def show_stats():
    print("moin")


def options():
    write("[b]Options[/b]\n", 0)
    write("If you want to cahnge the typing speed enter a value between 0 and 10, where 10 is instant and 0 very slow. Otherwise type 'back'.\n", 0)
    speed = cinput().lower()
    if speed == "back":
        return
    else:
        change_typing_speed(speed)
    write("This is an example to show you the typing speed you entered.\n")

    while True:
        write("Is this good? (y,n)\n", 0)
        ans = cinput().lower()
        if ans == "y":
            return
        else:
            write("Please enter a new value: \n", 0)
            speed = cinput().lower()
            change_typing_speed(speed)
            write("This is an example to show you the typing speed you entered.\n")


def exit():
    # check if unsaved information is still running, save them end the programm
    return True


def main_menu_selection(inp: str) -> int:
    options = ["play", "load", "show", "options", "exit"]
    inp = inp.lower().replace(".", "")
    elems = [element for element in options if element in inp]
    if len(elems) == 1:
        return options.index(elems[0]) + 1
    elif len(elems) > 1:
        return -1
    try:
        num = int(re.search(r'(\d+(\.\d+)?)', inp).string)
        if num < 1 or num > 5:
            return -1
    except KeyError:
        return -1


def main_menu():
    clear_console()
    game_dic = {
        1: launch_game,
        2: load_game,
        3: show_stats,
        4: options,
        5: exit
    }
    write("[b]Main menu[/b]\n", 0)
    write("1. Play game \n", 0)
    write("2. Load Game \n", 0)
    write("3. Show stats \n", 0)
    write("4. Options \n", 0)
    write("5. Exit game\n", 0)

    user_inp = main_menu_selection(cinput("What do you want to do?\n"))
    while True:
        #clear_console()
        if user_inp != -1:
            game_dic[user_inp]()
        else:
            write("Please enter either a number between 1 and 5 or for example 'Play Game'", 0)
            main_menu_selection(cinput(""))




if __name__ == "__main__":
    main_menu()
