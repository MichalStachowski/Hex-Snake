class Snake:
    def __init__(self, head):
        self.head = head
        self.snake_pos = [self.head]
        self.points = 0
        self.apple_p = [[10, 8], [2, 10], [11, 17], [10, 2], [14, 16], [18, 14], [15, 7], [10, 4], [12, 0], [10, 6],
                        [17, 7], [13, 17], [6, 10], [18, 10], [4, 12], [6, 12], [6, 14], [5, 15], [8, 10], [17, 1]]
        self.is_ate_himself = False
        self.is_moved_outside_board = False
        self.is_moved_on_another_snake = False
        self.is_winner = False

    def move(self, direction):
        """
        Mechanika poruszania się Węża
        :param direction: Kierunek przekazany poprzez kliknięcie w odpowiedni button
        """
        x = self.snake_pos[0][0]
        y = self.snake_pos[0][1]

        # Kierunek: Lewy Górny
        if direction == "Q":
            self.snake_pos.insert(0, [x - 1, y - 1])

        # Kierunek: Góra
        elif direction == "W":
            self.snake_pos.insert(0, [x - 2, y])

        # Kierunek: Prawy Górny
        elif direction == "E":
            self.snake_pos.insert(0, [x - 1, y + 1])

        # Kierunek: Lewy Dolny
        elif direction == "A":
            self.snake_pos.insert(0, [x + 1, y - 1])

        # Kierunek: Dół
        elif direction == "S":
            self.snake_pos.insert(0, [x + 2, y])

        # Kierunek: Prawy Dolny
        elif direction == "D":
            self.snake_pos.insert(0, [x + 1, y + 1])

        # Mechanika kontroli czy wąż stanął na polu z jabłkiem
        x = self.snake_pos[0][0]
        y = self.snake_pos[0][1]

        if [x, y] in self.apple_p:
            # aktualizacja listy z owocami
            self.apple_p.remove([x, y])

            # Aktualizacja wyniku punktowego
            self.points += 1
        else:
            del self.snake_pos[-1]  # usuwam ostatnią pozycję na jakiej znalazł się wąż

        # Mechanizm kontroli czy wąż nie wjechał na siebie
        unique = list(set(map(tuple, self.snake_pos)))
        if len(unique) != len(self.snake_pos):
            print("NIEPRAWIDLOWY RUCH! KONIEC GRY")
            self.is_ate_himself = True

        # Mechanizm kontroli czy wąż nie wyszedł poza planszę
        if x < 0 or x > 19 or y < 0 or y > 19:
            self.is_moved_outside_board = True

        # Mechanizm wyłonienia zwycięzcy po zdobyciu 10 punktów
        if self.points == 10:
            self.is_winner = True
