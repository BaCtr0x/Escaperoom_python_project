import time
import re
from utils import write, cinput, default_commands


# TODO: Muss noch fertig gestellt werden und Klassen für logic und cipher puzzle erstellen, wahrscheinlich keine Zeit für
class Puzzle:
    def __init__(self, puzzle_name: str, game, hints: list, answers: list, intro: str, outro: str, error_messages: list,
                 input_formats: list, hint_count=0, solving_time=0):
        self._name = puzzle_name
        self._game = game
        self._hints = hints
        self._hint_count = hint_count
        self._answers = answers
        self._start_time = 0
        self._stop_time = 0
        self._solving_time = solving_time
        self._intro = intro + "\n"
        self._outro = outro + "\n"
        self._error_messages = error_messages
        self._input_formats = input_formats

    def get_name(self) -> str:
        return self._name

    def write_intro(self):
        write(self._intro)

    def write_outro(self):
        write(self._outro)

    def get_hint(self, pos=None) -> str:
        if pos is not None:
            return self._hints[pos]
        else:
            return self._hints[self._hint_count]

    def set_hint_count(self, num: int):
        self._hint_count = num

    def increase_hint_count(self, bonus=0):
        self._hint_count += 1 + bonus

    def help_text(self):
        write("[c]You can either do type the answer. Be aware, that it will require you to enter the answer\n"
              "as stated by the prompt. The other options are: \n"
              "- 'hint', to get a hint for the current puzzle\n"
              "- 'exit', to get back to the main menu.\n"
              "- 'old_hints' if you loaded a game you can get your hints back[/c]\n")

    def handle_input(self, inp: str):
        if "ex" in inp:
            self._stop_time = time.time()
            self._game.save_game()
            self._solving_time = self._stop_time - self._start_time
        elif "he" in inp:
            self.help_text()
        elif "o_h" in inp:
            old_hints = '\n'.join(self._game.get_hints_used())
            write(f"[y]{old_hints}[/y]\n")
        elif "hi" in inp:
            hint = self.get_hint()
            write(hint, 0)
            self._game.set_hint_used(hint)
            self.increase_hint_count(len(self._game.get_hints_used(self._game.get_current_level())))
        else:
            if self.check_answer(inp):
                self.write_outro()
            else:
                write()

    def __check_answer_format(self, answer: str, format: str):
        if format == 'a,b,c,d':
            # Check if the input is in the form 'a,b,c,d' with any number of occurrences
            pattern = re.compile(r'^[a-d](,[a-d])*$')
            return bool(pattern.match(answer))

        elif format == 'a':
            # Check if the input is a single letter 'a'
            pattern = re.compile(r'^[a]$', re.IGNORECASE)
            return bool(pattern.match(answer))

        elif format == 'number':
            # Check if the input is a number
            pattern = re.compile(r'^\d+$')
            return bool(pattern.match(answer))

        else:
            # Unsupported format type
            return False

    def check_answer(self, answer: str) -> bool:
        if self.__check_answer_format(answer, self._input_formats[0]):
            return answer in self._answers
        else:
            write(f"Your answer does not match the input format of {self._input_formats[0]}")
            return False
