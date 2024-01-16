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

        # hier vergleichen wir, ob die aktuelle Farbe besser passt oder nicht, wenn ja, tausche sie als beste Option
        if distance < min_distance:
            min_distance = distance
            closest_color = color

    # gibt die beste Farbwahl zurück
    return closest_color

