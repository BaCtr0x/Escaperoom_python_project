import time
from utils import write, cinput
from Game import *

hints = [
    "The encryption seems to follow a famous roman emperor.",
    "The encryption is a cesar cipher.",
    "To solve this use a letter frequency attack."
    "The key is a number between 0 and 26."
    "Use the brute force version by trying every possible key."
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
    enc_note = cesar_enc(14, note)
    write("You enter the next room. Its dark and the air is filled with the smell of laurel wrath and grapes. \n"
          "A marmor recliner stands in the center, a red thick blanket on top. At the other end of the recliner rests\n"
          "a comfortable looking pillow of red velvet with a note on top of it. With slightly trembling fingers you \n"
          "pick up the note and read the scribbled message: \n"
          f"{enc_note}")

    write("\nOn the small counter beside the recliner resides a nightstand on which a small machine is placed. \n"
          "This machine, spattered with blood shows to options: Decrypt and Encrypt. A stack of paper lies beside it,\n"
          "as well as a dark pen. It seems that you can use the machine to decode the note, but the correct key is missing. \n"
          "Maybe you can use the machine by writing 'encrypt: text' or 'decrypt: key'.\n")

    answer = ""

    hint_count = 0
    # start timer
    start = time.time()

    while "dagger" not in answer:
        answer = cinput("What do you want to do?:\n")
        if "encrypt" in answer:
            plaintext = answer.split(":")[1]
            print(f"{cesar_enc(14, plaintext)}\n")
        elif "decrypt" in answer:
            inp = answer.split(":")[1]
            key = int(inp)
            if key == 14:
                write(f"{note}\n")
            else:
                write(cesar_dec(key, enc_note))
        elif answer == "exit":
            game.save_game()
            return
        elif answer == "hint":
            write(f"{hints[hint_count]}\n")
            game.set_hint_used(hints[hint_count])
            hint_count += 1
        else:
            print(f"You {answer}.\n")

    # stop timer
    stop = time.time()

    write("With a scraping noise you pull the dagger out of the white statue on the far wall of the room. \n"
          "Dust falls silently to the ground and you hear a dark rumbling noise, as an old mechanism starts to grind \n"
          "on the old stone floor. A small portion of the wall opens and makes way into a cavern that smells of rotten\n"
          "wood, moss and what seems to be blood. You continue on slowly. The hair on you neck stand up and a cold \n"
          "shudder runs down you spine.\n")

    return round(stop - start, 2), 0


if __name__ == "__main__":
    print(f"It took {cesar_puzzle()} seconds to solve the puzzle")
