class Zahlenfolgenraetsel:
    def __init__(self, *args, **kwargs):
        self.length = kwargs.get('length', 5)
        self.sequence = []
        self.user_guess = []

    def fibonacci_generator(self):
        a, b = 1, 1
        for _ in range(self.length):
            yield a
        a, b = b, a + b

    def play_game(self):
        generator = self.fibonacci_generator()
        self.sequence = [next(generator) for _ in range(self.length)]
        print("Willkommen beim Zahlenfolgenrätsel!")
        print(f"Errate die Fortsetzung der Zahlenfolge: {self.sequence}")
        for i in range(self.length):
            guess = int(input(f"Nächstes Element in der Zahlenfolge: "))
            self.user_guess.append(guess)
        if self.user_guess == self.sequence:
            print("Herzlichen Glückwunsch! Du hast die Zahlenfolge korrekt erraten.")
        else:
            print(f"Leider ist die Zahlenfolge falsch. Die richtige Fortsetzung wäre: {self.sequence}")


# Beispiel für die Verwendung der Klasse mit Args und Kwargs
raetsel1 = Zahlenfolgenraetsel(length=8)  # Verwendung von Kwargs für die Länge der Zahlenfolge
raetsel1.play_game()
raetsel2 = Zahlenfolgenraetsel(10)  # Verwendung von Args für die Länge der Zahlenfolge
raetsel2.play_game()
