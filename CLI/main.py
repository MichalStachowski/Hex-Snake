# === Stachowski Michal ===
# Przygotowano podstawową planszę hex. Wykorzystano klasy Snake, HexField, HexBoard.
# Tak przygotowana plansza jest wyrysowana w konsoli.
#
# Użyto kolorów - S jest oznaczony kolorem zielonym, natomiast owoc A (jabłko) kolorem czerwonym
#
# Zaimplementowano reguły środowiska i mechanikę poruszania się.
# Wąż porusza się po heksagonalnej siatce i zjada owoc wygenerowany w losowej pozycji. Po jego zjedzeniu wąż wydłuża się, a gracz zdobywa punkt. W przypadku najechania na # samego siebie nastepuje koniec gry.
# To samo dzieje sie gdy wyjdziemy poza pole.
#
# Zaimplementowano możliwość poruszania się za pomocą klawiszy "qweasd" wczytanych standardowym input
# Kierunki: Q = lewy górny, W = górny, E = prawy górny, A = lewy dolny, S = dolny, D = prawy dolny 
#
# W grze bierze udział dwóch graczy. Rozgrywka nie jest jednoczesna - najpierw po planszy porusza się Gracz1, a następnie generowana jest plansza dla Gracz2.
# Na koniec następuje podsumowanie wyniku punktowego i wyłonienie zwycięzcy.

from termcolor import colored
import os
import fileinput
import random
import time
os.system('color')


class Snake:
    def __init__(self, head):
        self.head = head
        self.snake_pos = [self.head]
        self.points = 0

    def move(self, direction, player_turn, apple_pos, random_hex_field):
        """
        Funkcja odpowiada za poruszanie się wężem.
        :param direction: Kierunek podany za pomocą input z linii polecen
        :param player_turn: my_turn lub enemy_turn. Jeżeli wystąpi nieprawidłowy ruch to zmieniane na False
        :param apple_pos: Pozycja na której znajduje się jabłko
        :param random_hex_field: Obiekt klasy HexField wylosowany w funkcji game.
        :return: player_turn: Zmienna logiczna określająca czy gra powinna trwać dalej.
        """
        illegal_move = False  # jezeli nieprawidlowy ruch to brak reakcji
        x = self.snake_pos[0][0]
        y = self.snake_pos[0][1]

        # Kierunek: Lewy Górny
        if direction == "Q" or direction == "q":
            self.snake_pos.insert(0, [x - 1, y - 1])

        # Kierunek: Góra
        elif direction == "W" or direction == "w":
            self.snake_pos.insert(0, [x - 2, y])

        # Kierunek: Prawy Górny
        elif direction == "E" or direction == "e":
            self.snake_pos.insert(0, [x - 1, y + 1])

        # Kierunek: Lewy Dolny
        elif direction == "A" or direction == "a":
            self.snake_pos.insert(0, [x + 1, y - 1])

        # Kierunek: Dół
        elif direction == "S" or direction == "s":
            self.snake_pos.insert(0, [x + 2, y])

        # Kierunek: Prawy Dolny
        elif direction == "D" or direction == "d":
            self.snake_pos.insert(0, [x + 1, y + 1])

        # Decyzja o koncu gry
        elif direction == "K" or direction == "k":
            player_turn = False

        # Zadne z powyzszych
        else:
            print("Nieprawidlowy ruch")
            illegal_move = True

        # Jezeli wykonano poprawny ruch sprawdzam czy na docelowym polu znajduje sie jablko.
        # Jesli tak to odpowiednio nalezy podliczyc punkty oraz "wydluzyc" weza.
        if illegal_move:
            pass
        else:
            x = self.snake_pos[0][0]
            y = self.snake_pos[0][1]

            if [x, y] == apple_pos and random_hex_field.is_apple:
                random_hex_field.is_apple = False
                random_hex_field.is_snake = True
                apple_pos[0] = -1
                apple_pos[1] = -1
                self.points += 1
            else:
                del self.snake_pos[-1]

            # Mechanizm kontroli czy wąż nie wjechał na siebie
            unique = list(set(map(tuple, self.snake_pos)))
            if len(unique) != len(self.snake_pos):
                print("NIEPRAWIDLOWY RUCH! KONIEC GRY")
                player_turn = False

            # Mechanizm kontroli czy wąż nie wyszedł poza planszę
            if x < 0 or x > rows_num*2 - 1 or y < 0 or y > cols_num*2 - 2:
                print("Wyjscie poza plansze - niedozwolony ruch")
                player_turn = False

        return player_turn


class HexField:
    def __init__(self, r, c):
        self.is_snake = False
        self.is_apple = False
        self.w = r
        self.k = c


class HexBoard:
    def __init__(self, rows_n, cols_n):
        self.rows_num = rows_n
        self.cols_num = cols_n
        self.f = None

    def draw_pure_board(self, rows, cols):
        """
        Wypisanie heksagonalnej siatki
        :param rows: Liczba wierszy
        :param cols: Liczba heksagonów w wierczu
        :return:
        """
        self.f = open("board.txt", "a")
        self.f.truncate(0)
        for _ in range(rows):
            for _ in range(cols):
                print("/ \\_", end='', file=self.f)

            print(file=self.f)
            for _ in range(cols):
                print("\\_/ ", end='', file=self.f)

            print(file=self.f)
        self.f.close()

    def draw_snake_on_board(self, snake, apple_pos):
        """
        Modyfikacja wyrysowanej siatki
        :param snake: Obiekt klasy Snake
        :param apple_pos: Polozenie jablka na planszy
        :return:
        """
        self.draw_pure_board(self.rows_num, self.cols_num)

        # Oznaczenie na planszy gdzie jest waz
        for pos in snake.snake_pos:
            with open("board.txt", "r") as f:
                file = f.readlines()
            with open("board.txt", "w") as f:
                for line_number in range(len(file)):
                    if line_number == pos[0]:
                        line_1 = file[line_number][0:pos[1] * 2] + '/S\\' + file[line_number][2 * pos[1] + 3:]
                        print(line_1, file=f, end='')
                    else:
                        line = file[line_number]
                        print(line, file=f, end='')

        # Oznaczenie na planszy gdzie jest jabłko
        if apple_pos != [-1, -1]:
            with open("board.txt", "r") as f:
                file = f.readlines()
            with open("board.txt", "w") as f:
                for line_number in range(len(file)):
                    if line_number == apple_pos[0]:
                        line_1 = file[line_number][0:apple_pos[1] * 2] + '/A\\' + file[line_number][
                                                                                  2 * apple_pos[1] + 3:]
                        print(line_1, file=f, end='')
                    else:
                        line = file[line_number]
                        print(line, file=f, end='')

        # Przepisuje board.txt do green_board.txt
        with open("board.txt") as f:
            with open("green_board.txt", "w") as f1:
                for line in f:
                    f1.write(line)

        # Zamiana snake na zielony kolor
        with fileinput.FileInput("green_board.txt", inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace("S", colored('S', 'green')), end='')

        # Zamiana jablka na czerwony kolor
        with fileinput.FileInput("green_board.txt", inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace("A", colored('A', 'red')), end='')

        # Wyswietlenie planszy
        f = open("green_board.txt", "r")
        print(f.read())
        f.close()


def game(player_snake, player_turn, player_name, player_board):
    """
    Właściwa mechanika rozgrywki
    :param player_snake: Obiekt klasy snake.
    :param player_turn: Jeżeli gracz wykona niedozwoloną akcję, zmienna ustawiana jest na False co onzacza koniec gry.
    :param player_name: Nazwa gracza wyswietlana w konsoli.
    :param player_board: Obiekt klasy HexBoard. Plansza na której rozgrywa się gra.
    :return:
    """
    # Wykorzysuje liste instancji i szukam w niej czy waz pokrywa sie z polem
    # Parametr is_snake zmienia sie wtedy na True
    for field in hex_fields:
        if (field.w, field.k) in player_snake.snake_pos:
            field.is_snake = True

    # losuje hex field i to hex field bedzie jako pozycja jablka
    random_hex_field = random.choice(hex_fields)
    # Mechanizm zeby wylosowal pole ktore nie jest wezem
    while random_hex_field.is_snake:
        random_hex_field = random.choice(hex_fields)
    random_hex_field.is_apple = True

    apple_pos = [random_hex_field.w, random_hex_field.k]

    player_board.draw_snake_on_board(player_snake, apple_pos)
    stop_cond = ["k", "K"]
    sn_dir = ""
    while sn_dir not in stop_cond and player_turn:
        # Wykorzysuje liste instancji i szukam w niej czy waz pokrywa sie z polem
        # Parametr is_snake zmienia sie wtedy na True
        # Wywoluje sie za kazdym razem bo waz zmienia polozenie
        for field in hex_fields:
            if (field.w, field.k) in player_snake.snake_pos:
                field.is_snake = True

        # Losowanie jabłka odbywa się gdy poprzednie jabłko zostało już wzięte
        if apple_pos == [-1, -1]:
            # losuje hex field i to hex field bedzie jako pozycja jablka
            random_hex_field = random.choice(hex_fields)
            # Mechanizm zeby wylosowal pole na którym nie znajduje się wąż
            while random_hex_field.is_snake:
                random_hex_field = random.choice(hex_fields)
            random_hex_field.is_apple = True
            apple_pos = [random_hex_field.w, random_hex_field.k]

        sn_dir = input()
        os.system('cls')
        print("{}: ".format(player_name))
        player_turn = player_snake.move(sn_dir, player_turn, apple_pos, random_hex_field)
        if player_turn:
            print("Zdobytych punktow: ", player_snake.points)
            player_board.draw_snake_on_board(player_snake, apple_pos)
        else:
            print("Koniec tury {}.".format(player_name))
            print("Zdobytych punktów: ", player_snake.points)
            time.sleep(3)
            os.system('cls')


def remove_files():
    try:
        os.remove("board.txt")
        os.remove("green_board.txt")
        os.remove("green_board.txt.bak")
    except FileNotFoundError:
        pass


cols_num = 10
rows_num = 5

# Tworze obiekt klasy HexBoard
board = HexBoard(rows_num, cols_num)

# Przypisuje odpowiednie indeksy polom i tworze obiekty ktore maja przypisane takie wartosci
# Pozniej na podstawie tych wartosci koloruje odpowiednie pola
# Tworzenie listy instancji Klasy HexField
hex_fields = []
for i in range(rows_num * 2 - 1):
    if i % 2 == 0:
        k = -2
    else:
        k = -1

    if i % 2 == 0:
        for j in range(cols_num):
            w = i
            k += 2
            hex_fields.append(HexField(w, k))
    else:
        for j in range(cols_num - 1):
            w = i
            k += 2
            hex_fields.append(HexField(w, k))


# Tworze obiekty klasy Snake
my_snake = Snake([1, 1])
enemy_snake = Snake([rows_num*2 - 3, cols_num*2 - 3])

# Rozgrywka
my_turn, enemy_turn = True, True
game(my_snake, my_turn, "Gracz 1", board)
game(enemy_snake, enemy_turn, "Gracz 2", board)

# Podsumowanie wyników i wyłonienie zwycięzcy
print("PODSUMOWANIE")
print("Gracz 1: ", my_snake.points)
print("Gracz 2: ", enemy_snake.points)
if my_snake.points > enemy_snake.points:
    print("Wygrywa Gracz 1")
elif my_snake.points < enemy_snake.points:
    print("Wygrywa Gracz 2")
else:
    print("Remis")

remove_files()
