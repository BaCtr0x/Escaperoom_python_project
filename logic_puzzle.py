import time
from utils import write, cinput, default_commands
from Game import *

hints = [
    "The stones are jade, saphire, ruby and obsidian.",
    "Obsidian is last.",
    "Jade is next to saphire.",
    "Saphire is first."
]


# TODO: Puzzle umbauen mit puzzle class, wenn Zeit und Lust :D
def logic_puzzle(game) -> time:
    puzzle_symbols = ["jade", "sapphire", "ruby", "obsidian"]
    solution = "saphire,jade,ruby,obsidian"

    write(
        "A cold shiver runs down your spine as you walk through the sick blizzard that pushes down the mountain side.\n"
        "You can not put a finger on it, but everything around you seems to be off somehow, as you see the dark wood \n"
        "of an old small hut. Smoke streams from the small chimney and you can see the warm orange flicker of the fire\n"
        "inside. As you open the door with a loud creaking sound you are instantly enveloped in warm smell of a good \n"
        "olf stew. Your heavy boots stump on the wooden floor as you close the door behind you and look around. \n \n"
        "The room is small, not much bigger than an average student dorm room. The table in the center is decked with\n"
        "A bowl of nicely smelling mushroom stew that seems to bee still warm, judging by the steam coming from it.\n"
        "A kitchen corner at the right side is filled with pots of simmering broth and the crackling fire across the\n"
        "room makes you feel like you entered one of those skivacation huts you could rent for a relaxing time off. \n"
        "You continue to look around, but nothing of interest seems to be placed around the room. No hint of anyone \n"
        "being still here, except from the comfortable food. Just as you sit at the table to write down some immediate\n"
        "thoughts, you see the corner of a note protruding from under the bowl. You carefully pull out the note and \n"
        "read the beautifully written words: \n\n"
        "'I've been stuck at this hut for days. There is nothing here. Nothing that gives me even the slightest hint to\n"
        "where my daughter is. But at least it keeps me warm. All I could find are these weird symbols that pop up on\n"
        "the wall when a candle gets close, but I can't seem to find any meaning behind them. I will give them another\n"
        "try tomorrow.'\n\n"
        "Immediately you take the candle on the table and scan the walls with it. And there it is on the wall opposite\n"
        "the door shimmers as you get closer. Four strange symbols appear, as if they are being carved into the wood.\n"
        "Looking closer they seem to shimmer in different colors, [g]green[/g], [c]cyan[/c], [r]red[/r] and [lp]purple[/lp].\n"
        "and resemble different kinds of stones.\n"
        "As you touch on of them they seem follow your hand and can be rearranged. You look for clues and see a \n"
        "letter poking our from behind the sideboard of the kitchen corner. You put your shoulder against it and push\n"
        "it out of the way to reveal three lines of scribbled words:\n"
        "- Jade isn't in spot 3.\n"
        "- Ruby isn't next to saphire.\n"
        "- Obsidian isn't next to either jade or saphire.\n \n")

    hint_count = len(game.get_hints_used(game.get_current_level()))
    start = time.time()

    while True:
        ans = cinput("Which order do you choose? 'a,b,c,d'\n").replace(" ", "").replace(".", ",").lower()
        if ans == solution:
            stop = time.time()
            write("\nYou move the symbols around and with a quite 'click' they lock in place. The fireplace instantly \n"
                  "extinguishes. And with the sound of splitting wood, you see in the flickering light of your candle\n"
                  "a door forming in the wall. You push your fingers behind the small gap that appeared, the slight\n"
                  "pain of a small splinter that gets stuck in your index finger lets you revolt shortly. But you\n"
                  "continue opening the light door. A short hall opens in front of you that terminates in another room.\n"
                  "The smell is old and musty and you get the feeling that this won't be such a simple case, as you\n"
                  "continue on.\n \n")

            return round(stop - start, 2), 0
        elif "ex" in ans or "hi" in ans or "he" in ans or "_" in ans:
            stop = default_commands(ans, hints, hint_count, game)
            # in case of entering 'hint'
            if type(stop) == int:
                hint_count = stop
            # case of entering 'exit'
            elif type(stop) == float:
                return round(stop - start, 2), 1
        # check whether the cinput is in the correct form or not
        elif bool([element for element in ans if element not in puzzle_symbols]):
            write("Please write your answer in the form of: a,b,c,d or did you misspell?\n"
                  "Nonetheless nothing seems to happen.\n")
        else:
            write("Nothing seems to happen, maybe the order is not correct yet.\n")
