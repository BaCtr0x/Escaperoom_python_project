from utils import cinput, write, default_commands
import time


class Zahlenfolgenraetsel:
    def __init__(self, *args, **kwargs):
        self.length = kwargs.get('length', 5)
        self.guesses = 3
        self.sequence = []
        self.user_guess = []

    def fibonacci_generator(self):
        a, b = 1, 1
        for _ in range(self.length):
            yield a
            a, b = b, a + b

    def play_game(self, game):
        # create the fibonacci generator
        generator = self.fibonacci_generator()
        # run generator and store result in a list
        self.sequence = [next(generator) for _ in range(self.length)]
        write("\nAs you reach the bottom of the staircase, you enter a barely lit room. The smell of moss and wet stone\n"
            "lingers in the air. The rough walls to your right and left are similar to the ones in the previous room. \n"
            "But the wall opposite of you is clean, smooth and seems to have been made with modern tools. You step \n"
            "closer and let the cone of light from your flashlight wander of the dark surface. As you go from left to\n"
            "right you see an sequence of seemingly random numbers:\n"
            f"[c]{self.sequence[:self.length - 1]}[/c]\n"
            "At the end of the sequence you see an empty spot. So you look around to find any hint of what to do next.\n"
            "On the right you see a small table with a few numbers made of stone, which seem to fit perfectly into the \n"
            "notch in the wall. \n"
        )

        # handle the user interaction and limit the number of guesses to the set number of guesses in self.guesses
        for i in range(self.guesses):
            inp = cinput("Which combination of numbers will you enter?\n")

            # check the input to be the last number of the sequence
            if inp == str(self.sequence[self.length-1]):
                write(
                    f"\nYou enter {inp} you see the sequence blink from left to right in a bright yellow light and you \n"
                    "hear a loud crackling sound as the wall breaks open to form an opening to another dark corridor\n"
                    "with no end in sight. [it]What is going on here?[/it] you think to yourself as you continue.\n"
                    "As you walk down the corridor you feel the cold air brush over you bare skin of your neck and \n"
                    "you start to shiver. At the same time you see your flashlight flicker. Hopefully the battery will\n"
                    "hold till the end of this case. The thought of traversing these corridors in complete darkness\n"
                    "puts you on the edge."
                )
                return 0

            # handling default commands like exiting the game, using help, hint and old_hint
            elif "ex" in colour or "hi" in colour or "he" in colour or "_" in colour:
                stop = default_commands(colour, [], 0, game)
                if type(stop) == float:
                    return 1

            # print the text of entering a wrong answer
            else:
                write("\n You see the sequence of numbers flash red once. This is not a good sine. Lets better get\n"
                      "better get this right. You don't want to know what happens if you are wrong too many times.\n")

        # This section is only reached if all guesses have been used.
        # set the level state to death, such that the game can not be loaded later on
        game.set_level_state({"death": True})
        # save the game
        game.save_game()
        write("You see the sequence of number flash in red once more, but this time it does not go back to the cyan\n"
              "color as it did before. Panic start to rise in your chest as you feel warms flowing down on you from \n"
              "the ceiling. [it]What is happening[/it]. You look around...\n"
              "The door behind you is gone! You run back, scanning the wall, trying to find even the smallest crack\n"
              "in the perfectly smooth wall. But there is nothing, no nook you fingers can get a hold of, as you feel\n"
              "the warms from the top getting warmer and warmer. Your chest tightens further as you realise that this\n"
              "there is no escape anymore. You missed you chance to get out of here alive. \n"
              "A loud crackling sound crashes down on you, as you see a wide [o]crack[/o] forming at the ceiling and\n"
              "and orange light pushing through it. The heat radiating from it is starting to burn your skin as\n"
              "as you see magma bubbling into your room and feel the sweat on your skin evaporating.\n\n")
        write("[r][b]You died![/b][/r]\n\n"
              "Thank you for playing our game, we wish you better luck next time :)\n\n")
        cinput("Press enter to go back to the main menu.\n")
        return 1


# not pretty, but since all other puzzles are not a class themselves this is the easiest way to keep the structure
def number_puzzle(game):
    # create a puzzle instance, comment out one of the following puzzles
    # Using **kwargs
    puzzle = Zahlenfolgenraetsel(length=8)
    # Using *args
    # puzzle = Zahlenfolgenraetsel(10)

    # take time before starting the puzzle
    start = time.time()

    # start the game
    res = puzzle.play_game(game)

    # tatke the time after the puzzle
    stop = time.time()

    # return time and exit code for further handeling.
    return round(stop - start, 2), res

