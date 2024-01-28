import random
import time
from utils import write, cinput, default_commands
from Game import *

hints_cypher = [
    "The encryption seems to follow a famous roman emperor.",
    "The encryption is a cesar cipher.",
    "To solve this use a letter frequency attack."
    "The key is a number between 0 and 26."
    "Use the brute force version by trying every possible key."
]

hints_action = [
    "You can enter an action like push button.",
    "You can pull on something.",
    "Just pull the dagger."
]


def cesar_enc(key: int, plaintext: str):
    encrypted_text = ""

    for char in plaintext:
        if char.isalpha():
            is_upper = char.isupper()

            # Konvertiere Character zu ASCII Code
            ascii_code = ord(char)

            # Shifte den Character entsprechend des Keys
            encrypted_code = (ascii_code - ord('A' if is_upper else 'a') + key) % 26

            # Konvertiere den ASCII Code zurück zu Character
            encrypted_char = chr(encrypted_code + ord('A' if is_upper else 'a'))

            # Füge den Character zum Ergebnisstring hinzu
            encrypted_text += encrypted_char
        # else:
        #     # Wenn der Character kein Buchstabe ist, füge ihn so hinzu
        #     encrypted_text += char

    return encrypted_text


def cesar_dec(key: int, cypher: str):
    decrypted_text = ""

    for char in cypher:
        if char.isalpha():
            is_upper = char.isupper()

            # Konvertiere Character zu ASCII Code
            ascii_code = ord(char)

            # Shifte den Character entsprechend des Keys
            encrypted_code = (ascii_code - ord('A' if is_upper else 'a') - key) % 26

            # Konvertiere den ASCII Code zurück zu Character
            encrypted_char = chr(encrypted_code + ord('A' if is_upper else 'a'))

            # Füge den Character zum Ergebnisstring hinzu
            decrypted_text += encrypted_char
        # else:
        #     # Wenn der Character kein Buchstabe ist, überspringe ihn.
        #     decrypted_text += char

    return decrypted_text


def cesar_puzzle(game) -> time:
    note = (
        "You have found my note. Finally. With this you can continue to my grave, where you will find my murderer. \n"
        "There is a small lever disguised as a dagger that was plunged into my chest. \n"
        "If you remove it a door will open, follow the path behind it. \n"
        "Good luck!\n")

    # hint_count = len(game.get_hints_used(game.get_current_level()))
    level_state = game.get_level_state()

    if level_state == {"death": False}:
        # Could also be between 0 and 24, but 0 and 26 are boring as nothing happens, so we create a small buffer of 3
        skey = random.randint(3, 23)
        enc_note = cesar_enc(skey, note.upper())

        # TODO: store enc_done in state to get correct hints
        state = {
            "solution": skey,
            "cypher": enc_note
        }

        game.set_level_state(state)
    else:
        # load information from save state
        skey = level_state["solution"]
        enc_note = level_state["cypher"]

    write("You enter the next room. Its dark and the air is filled with the smell of laurel wrath and grapes. \n"
          "A marmor recliner stands in the center, a red thick blanket on top. At the other end of the recliner rests\n"
          "a comfortable looking pillow of red velvet with a note on top of it. With slightly trembling fingers you \n"
          "pick up the note and read the scribbled message: \n\n"
          f"[o]{enc_note}[/o]")

    write("\nOn the small counter beside the recliner resides a nightstand on which a small machine is placed. \n"
          "This machine, spattered with blood shows to options: Decrypt and Encrypt. A stack of paper lies beside it,\n"
          "as well as a dark pen. It seems that you can use the machine to decode the note, but the correct key is missing. \n"
          "Maybe you can use the machine by writing [c]'encrypt: text'[/c] or [c]'decrypt: key'[/c].\n")

    ans = ""
    # start timer
    start = time.time()

    enc_done = False

    enc_hint_counter = 0
    action_hint_counter = 0

    # count the number of hints for enc hint and action hint of the loaded game
    for hint in game.get_hints_used(game.get_current_level()):
        if hint in hints_cypher:
            enc_hint_counter += 1
        else:
            action_hint_counter += 1

    while True:
        ans = cinput("What do you want to do?:\n")
        # check if input follows input convention for encrypt and decrypt
        try:
            if ":" in ans:
                inp = ans.split(":")[1]
            else:
                inp = ans.split(" ")[1]
            splitable = True
        except IndexError:
            splitable = False
        if "encrypt" in ans and splitable:
            write(f"{cesar_enc(skey, inp)}\n")
        elif "decrypt" in ans and splitable:
            key = int(inp)
            # saves some computation by not doing the decryption
            if key == skey:
                write(f"{note}\n")
                enc_done = True
            else:
                write(cesar_dec(key, enc_note))
        # just as fallback to present the project so we don't need to obtain the key manually
        elif "olaf" in ans:
            write(str(skey), 0)
        elif "ex" in ans or "hi" in ans or "he" in ans or "_" in ans:
            # checking if the encryption is done so that the new hints can be displayed when asked for
            if enc_done:
                stop = default_commands(ans, hints_action, action_hint_counter, game)
                if type(stop) == int:
                    action_hint_counter = stop
                # case of entering 'exit'
                elif type(stop) == float:
                    return round(stop - start, 2), 1
            else:
                stop = default_commands(ans, hints_cypher, enc_hint_counter, game)
                if type(stop) == int:
                    enc_hint_counter = stop
                # case of entering 'exit'
                elif type(stop) == float:
                    return round(stop - start, 2), 1
        elif "dagger" in ans:
            break
        else:
            write(f"You {ans}.\n"
                  f"nothing seems to happen\n")

    # stop timer
    stop = time.time()

    write("With a scraping noise you pull the dagger out of the white statue on the far wall of the room. \n"
          "Dust falls silently to the ground and you hear a dark rumbling noise, as an old mechanism starts to grind \n"
          "on the old stone floor. A small portion of the wall opens and makes way into a cavern that smells of rotten\n"
          "wood, moss and what seems to be blood. You continue on slowly. The hair on you neck stand up and a cold \n"
          "shudder runs down you spine.\n")

    return round(stop - start, 2), 0
