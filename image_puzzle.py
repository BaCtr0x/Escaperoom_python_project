from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import cinput, write, default_commands
import time


def get_color_name(rgb):
    # ein Dictionary mit den Farben und ihren RGB Werten
    colours = {
        'red': (255, 0, 0),
        'orange': (255, 165, 0),
        'yellow': (255, 255, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'purple': (128, 0, 128)
    }

    min_distance = float('inf')
    closest_color = None

    # Wir berechnen die distance zwischen der Eingabe und den gegebenen Farben
    for color, reference_rgb in colours.items():
        distance = sum((a - b) ** 2 for a, b in zip(rgb, reference_rgb)) ** 0.5

        if distance < min_distance:
            min_distance = distance
            closest_color = color

    return closest_color


def play_puzzle(game):

    # Bild laden
    image = cv2.imread('nature_image.jpg')

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

    for _ in range(2):  # Die Schleife wird dreimal durchlaufen
        # colour = cinput("Was ist die dominante Farbe des Bildes: ")
        colour = cinput("What is the dominating colour?\n")

        if colour.lower() == "blue":  # Ignoriere die Groß-/Kleinschreibung
            # Zeige das Bild mit der erkannten Farbe
            highlighted_image = cv2.bitwise_and(image, image,
                                                mask=mask)  # es werden nur die Pixel übernommen, welche der dominanten Farbe entsprechen
            plt.imshow(dominant_color_rgb_normalized)  # Verwende die normalisierten Werte
            plt.title('Dominant colour')
            plt.axis('off')
            plt.show()

            print(f"Gut gemacht! Die gesuchte dominante Farbe ist {colour}.\nDu kannst nun den nächsten Raum betreten.")
            room_status = 1  # Variable, die einen göffnenen Raum zeigt wird auf 1 gesetzt
            return 0  # Beende die Schleife, wenn die richtige Farbe gefunden wurde
        elif "ex" in colour or "hi" in colour or "he" in colour or "_" in colour:
            stop = default_commands(colour, [], 0, game)
            if stop != 0:
                return 1
        else:
            print(f"Die gesuchte dominante Farbe ist leider nicht {colour}. Versuche es erneut.")
            return 0

    # Dieser Code wird nur erreicht, wenn die Schleife dreimal durchlaufen wurde und die richtige Farbe nicht gefunden wurde.
    if room_status == 0:
        print("Du hast alle Versuche aufgebraucht. Der Escape Room bleibt verschlossen.")
        return 0


def image_puzzle(game) -> time:

    # starte den Timer
    start = time.time()

    ex = play_puzzle(game)

    stop = time.time()
    if ex == 0:
        # mache weiter mit den anderen Rätseln
        return round(stop - start, 2), [], 0
    else:
        # stoppe, weil exit eingegeben wurde
        return round(stop - start, 2), [], 1


if __name__ == "__main__":
    image_puzzle()