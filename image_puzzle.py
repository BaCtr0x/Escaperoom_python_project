from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import cinput, write, default_commands
import time


def play_puzzle(game):
    write(
        "The stone corridor opens up into a small room, hammered roughly out of the black rock. The sound of dropping\n"
        "water echoes through the room and paints an image of ancient stonework. The smell of wet stone lingers in the\n"
        "air. The static feeling of an electrical field lets the hair on your arms stand up. It is cold compared to\n"
        "the warm room before. You look around with the cone of white light coming from your flashlight and walk\n"
        "further into the room. A bright flash blinds you and you immediately take a step back as a large image hovers\n"
        "on the wall opposite of you. In crackly chiseled letters you read a simple question below the image:\n"
        "[b]What is the dominant colour of this image?[/b]\n\n"
        "Hammer and chisel lie slightly to the right of the question on the floor, dusted in stone powder, as if they\n"
        "have been used recently.\n"
    )

    # Bild laden
    # Bild von https://www.vecteezy.com/photo/22896126-a-fantasy-world-in-alien-landscape-surreal-ultra-detailed-stunning-colorful-digital-art-creative-generative-ai
    image = cv2.imread('puzzle_image.JPG')

    # Konvertiere das Bild in den HSV-Farbraum
    # HSV: Hue (Farbton), Saturation (Sättigung), Value (Helligkeit).
    # Dieser Farbraum erleichtert die Analyse von Farbinformationen.
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Berechne das Histogramm
    hist = cv2.calcHist([hsv_image], [0], None, [256], [0, 256])
    # [0] gibt an, dass der erste von den drei Kanälen des HSV-Farbraums verwendet wird, also der Farbton
    # None gibt an, dass keine Maske verwendet wird, um nur bestimmte Ausschnitte des Bildes zu berücksichtigen
    # [256] gibt die Anzahl der Klassen in dem Histogramm an. RGB hat 256 Stufen (0 - 255).

    # Finde die dominante Farbe & Umwandlung in RGB

    # max. Wert im Histogramm, also der dominante Farbton
    dominant_color_hue = np.argmax(hist)
    # Numpy-Array, der eine Farbe im HSV-Farbraum repräsentiert. Farbton, max. Sättigungswert, max. Helligkeitswert
    dominant_color = np.array([[dominant_color_hue, 255, 255]], dtype=np.uint8)
    # Umformen zu einem 1x1x3-Array; Konvertierungscode zur Umwandlung von HSV zu RGB
    dominant_color_rgb = cv2.cvtColor(dominant_color.reshape(1, 1, 3), cv2.COLOR_HSV2RGB)

    # Filtere nur die dominante Farbe
    mask = cv2.inRange(hsv_image, dominant_color, dominant_color)

    # Zeige das Originalbild
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original image')
    plt.axis('off')  # Deaktiviert die Achsenbeschriftungen für den ersten Subplot

    # Normalisiere die Werte auf den Bereich von 0 bis 1
    dominant_color_rgb_normalized = dominant_color_rgb / 255.0

    # Zeige das Originalbild
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original image')
    plt.axis('off')
    plt.ion()  # Erlaubt dem User weiter eingaben zu machen. (Aktiviert interaktiven Modus)
    plt.show()

    # Variable, die den Raumstatus anzeigt (offen = 1 oder geschlossen = 0)
    room_status = 0

    for _ in range(3):  # Die Schleife wird dreimal durchlaufen
        # colour = cinput("Was ist die dominante Farbe des Bildes: ")
        colour = cinput("")  # Kein Prompt, da die Frage oben schon steht. Der User soll nur die Farbe eingeben.

        if colour.lower() == "red":  # Ignoriere die Groß-/Kleinschreibung
            # Zeige das Bild mit der erkannten Farbe
            highlighted_image = cv2.bitwise_and(image, image,
                                                mask=mask)  # es werden nur die Pixel übernommen, welche der dominanten Farbe entsprechen
            plt.imshow(dominant_color_rgb_normalized)  # Verwende die normalisierten Werte
            plt.title('Dominant colour')
            plt.axis('off')
            plt.show()

            # print(f"Gut gemacht! Die gesuchte dominante Farbe ist {colour}.\nDu kannst nun den nächsten Raum betreten.")
            write(f"As you enter the {colour} you see another image appear beside the original one. A simple square\n"
                  "the colour of your answer. Shortly after that they both start to flicker and vanish, leaving a\n"
                  "dark hole in the wall. Spiderwebs hang across the small dark corridor. One by one your see torches\n"
                  "bursting to light, illuminating the staircase that spirals down deeper into the mountain. Each step\n"
                  "you take echoes around you making you nervous, as if someone is following you, but you press on.\n"
                  "Several minutes go by until you finally reach the next room of what ever this dark and twisted\n"
                  "labyrinth is. But you still hope to find the answers you are looking for.\n")
            room_status = 1  # Variable, die einen göffnenen Raum zeigt wird auf 1 gesetzt
            return 0  # Beende die Schleife, wenn die richtige Farbe gefunden wurde
        # handhaben von eingaben wie hint, help, exit and old hint
        elif "ex" in colour or "hi" in colour or "he" in colour or "_" in colour:
            stop = default_commands(colour, [], 0, game)
            if type(stop) == float:
                return 1
        else:
            # write ist wie print, nur mit einem schreib Effekt.
            write(
                f"The room shakes gloomily as you enter {colour}. You get the feeling that this was not the answer.\n")

    # Dieser Code wird nur erreicht, wenn die Schleife dreimal durchlaufen wurde und die richtige Farbe nicht gefunden
    # wurde.
    if room_status == 0:
        # fugen den aktuellen Status des Spielers hinzu
        game.set_level_state({"death": True})
        # save the game as you died
        game.save_game()
        write(
            "You enter your third guess as feel the ground start to rumble under your feet. Dust starts to fall from\n"
            "the ceiling and into your face. It burns in your eyes and you revolt back. A thunderous bang rolls\n"
            "over you from the wall behind you. You spin around and see the door shut. You run over, trying to push\n"
            "open the door. Pulling and pressing as hard as you can, but the damn door wont budge an inch. You feel\n"
            "the walls pressing in from either side of you. Slowly, agonisingly slowly and you know there is\n"
            "nothing left for you to do but to stare death right in the eyes and accept your faith.\n \n")
        write("[r][b]You died![/b][/r]\n\n"
              "Thank you for playing our game, we wish you better luck next time :)\n\n")
        cinput("Press enter to go back to the main menu.\n")
        return 1


def image_puzzle(game) -> time:
    # starte den Timer
    start = time.time()

    ex = play_puzzle(game)

    stop = time.time()
    # mache weiter mit den anderen Rätseln, wenn ex == 0, wenn ex == 1 stoppe und gehe zum hauptmenü
    return round(stop - start, 2), ex
