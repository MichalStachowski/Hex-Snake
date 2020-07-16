import sys, math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QMessageBox
import random


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.player_snake = my_snake

        # Zmienne wykorzystywane do przechowywania owoców
        self.apple_pos_list = []
        self.idx_apple_pos = []

        # noinspection PyArgumentList
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(100, 100, 1000, 800)  # wymiary okna
        self.init_buttons()  # Obsługa przycisków w GUI

        # Obsługa labeli w GUI
        self.label_first_snake_points = QtWidgets.QLabel(self)
        self.label_second_snake_points = QtWidgets.QLabel(self)
        self.label_whose_turn = QtWidgets.QLabel(self)
        self.init_labels()

        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))  # Kolor pisaka - czarny
        self.pen.setWidth(3)  # ustawienie grubosci pisaka
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))  # ustawianie wypełnienia figur

        board.init_board()  # Inicjalizacja planszy

    def init_buttons(self):
        """
        Obsługa przycisków w GUI
        """
        # Przycisk odpowiedzialny za nową grę
        b_new_game = QPushButton('Nowa Gra', self)
        b_new_game.move(100, 50)
        b_new_game.clicked.connect(self.click_new_game)

        # Przycisk odpowiedzialny za wyjście
        b_exit = QPushButton('Wyjscie', self)
        b_exit.move(200, 50)
        b_exit.clicked.connect(self.click_exit)

        # Przycisk odpowiedzialny za ruch w lewy górny róg
        b_q = QPushButton('Lewy Górny', self)
        b_q.move(100, 700)
        b_q.clicked.connect(self.click_q)

        # Przycisk odpowiedzialny za ruch w górę
        b_w = QPushButton('Góra', self)
        b_w.move(200, 700)
        b_w.clicked.connect(self.click_w)

        # Przycisk odpowiedzialny za ruch w prawy górny róg
        b_e = QPushButton('Prawy Górny', self)
        b_e.move(300, 700)
        b_e.clicked.connect(self.click_e)

        # Przycisk odpowiedzialny za ruch w lewy dolny róg
        b_a = QPushButton('Lewy Dolny', self)
        b_a.move(100, 750)
        b_a.clicked.connect(self.click_a)

        # Przycisk odpowiedzialny za ruch w dół
        b_s = QPushButton('Dół', self)
        b_s.move(200, 750)
        b_s.clicked.connect(self.click_s)

        # Przycisk odpowiedzialny za ruch w prawy dolny róg
        b_d = QPushButton('Prawy Dolny', self)
        b_d.move(300, 750)
        b_d.clicked.connect(self.click_d)

    def init_labels(self):
        """
        Obsługa labeli w GUI
        """
        my_font = QtGui.QFont()
        my_font.setFamily("Cambria")
        my_font.setPointSize(20)

        # Konfiguracja labela dotyczacego wyniku punktowego pierwszego gracza
        self.label_first_snake_points.setFont(my_font)
        self.label_first_snake_points.move(450, 20)
        self.label_first_snake_points.setText(f"Gracz1: {my_snake.points}")
        self.label_first_snake_points.adjustSize()

        # Konfiguracja labela dotyczacego wyniku punktowego drugiego gracza
        self.label_second_snake_points.setFont(my_font)
        self.label_second_snake_points.move(450, 70)
        self.label_second_snake_points.setText(f"Gracz2: {enemy_snake.points}")
        self.label_second_snake_points.adjustSize()

        # Konfiguracja labela dotyczacego informacji czyja teraz kolej na ruch
        self.label_whose_turn.setFont(my_font)
        self.label_whose_turn.move(700, 55)
        if self.player_snake == my_snake:
            self.label_whose_turn.setText("Tura: Gracz1")
        else:
            self.label_whose_turn.setText("Tura: Gracz2")
        self.label_whose_turn.adjustSize()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        board.draw_board(painter)

    def change_player_snake(self):
        """
        Zmiana gracza wykorzystywana w grze turowej
        """
        if self.player_snake == my_snake:
            self.player_snake = enemy_snake
            self.label_whose_turn.setText("Tura: Gracz2")
        else:
            self.player_snake = my_snake
            self.label_whose_turn.setText("Tura: Gracz1")

    # Funkcje związane z obsługą przycisków
    def click_new_game(self):
        """
        Zresetowanie parametrów gry w celu możliwości rozpoczęcia jej na nowo
        """
        my_snake.points = 0
        enemy_snake.points = 0
        my_snake.snake_pos = [[2, 2]]
        enemy_snake.snake_pos = [[17, 17]]
        self.player_snake = my_snake
        self.apple_pos_list = []
        self.idx_apple_pos = []
        self.label_first_snake_points.setText(f"Gracz1: {my_snake.points}")
        self.label_second_snake_points.setText(f"Gracz2: {enemy_snake.points}")
        self.label_whose_turn.setText("Tura: Gracz1")
        self.update()

    def click_exit(self):
        sys.exit(app.exec_())

    def click_q(self):
        self.player_snake.move("Q", self.apple_pos_list, self.idx_apple_pos)
        self.change_player_snake()

    def click_w(self):
        self.player_snake.move("W", self.apple_pos_list, self.idx_apple_pos)
        self.change_player_snake()

    def click_e(self):
        self.player_snake.move("E", self.apple_pos_list, self.idx_apple_pos)
        self.change_player_snake()

    def click_a(self):
        self.player_snake.move("A", self.apple_pos_list, self.idx_apple_pos)
        self.change_player_snake()

    def click_s(self):
        self.player_snake.move("S", self.apple_pos_list, self.idx_apple_pos)
        self.change_player_snake()

    def click_d(self):
        self.player_snake.move("D", self.apple_pos_list, self.idx_apple_pos)
        self.change_player_snake()

    def snake_eat_himself_popup(self):
        """
        Funkcja wywołująca okienko w przypadku najechania węża na samego siebie
        """
        msg = QMessageBox()
        msg.setWindowTitle("Niedozwolony ruch")
        msg.setText("Wąż nie może najechać na swój ogon")
        msg.setIcon(QMessageBox.Critical)  # Warning / Critical / Information / Question
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText("Koniec gry")

        if self.player_snake == my_snake:
            msg.setDetailedText("Wygrywa Gracz 2")
        else:
            msg.setDetailedText("Wygrywa Gracz 1")

        msg.buttonClicked.connect(self.exit_snake)
        x = msg.exec_()  # this shows the message

    def snake_moved_outside_board_popup(self):
        """
        Funkcja wywołująca okienko w przypadku wyjścia węża poza planszę gry
        """
        msg = QMessageBox()
        msg.setWindowTitle("Niedozwolony ruch")
        msg.setText("Wąż wyszedł poza pole gry")
        msg.setIcon(QMessageBox.Critical)  # Warning / Critical / Information / Question
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText("Koniec gry")

        if self.player_snake == my_snake:
            msg.setDetailedText("Wygrywa Gracz 2")
        else:
            msg.setDetailedText("Wygrywa Gracz 1")

        msg.buttonClicked.connect(self.exit_snake)
        x = msg.exec_()  # this shows the message

    def snake_on_snake_popup(self):
        """
        Funkcja wywołująca okienko w przypadku najechania węża na węża drugiego gracza
        """
        msg = QMessageBox()
        msg.setWindowTitle("Niedozwolony ruch")
        msg.setText("Wąż najechał na węża przeciwnika")
        msg.setIcon(QMessageBox.Critical)  # Warning / Critical / Information / Question
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText("Koniec gry")

        if self.player_snake == my_snake:
            msg.setDetailedText("Wygrywa Gracz 2")
        else:
            msg.setDetailedText("Wygrywa Gracz 1")

        msg.buttonClicked.connect(self.exit_snake)
        x = msg.exec_()  # this shows the message

    def player_won_popup(self):
        """
        Funkcja wywołująca okienko w przypadku zwycięstwa jednego z graczy (regulaminowe zdobycie 10 punktów)
        """
        msg = QMessageBox()
        msg.setWindowTitle("Wygrana!")
        if self.player_snake == my_snake:
            msg.setText("Gracz 1 zdobył 10 punktów")
        else:
            msg.setText("Gracz 2 zdobył 10 punktów")
        msg.setIcon(QMessageBox.Information)  # Warning / Critical / Information / Question
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText("Gratulacje!")
        msg.buttonClicked.connect(self.exit_snake)
        x = msg.exec_()  # this shows the message

    def exit_snake(self, i):
        exit()

    def update_points_label(self):
        """
        Aktualizacja informacji tekstowych dotyczących liczby punktów graczy
        """
        self.label_first_snake_points.setText(f"Gracz1: {my_snake.points}")
        self.label_second_snake_points.setText(f"Gracz2: {enemy_snake.points}")


class HexField:
    def __init__(self, r, c, idx):
        self.is_snake = False
        self.is_apple = False
        self.w = r
        self.k = c
        self.idx = idx

    def update_is_snake(self, player_snake):
        """
        Jeżeli na danym polu znajduje się wąż ustawia parametr is_snake na True
        :param player_snake: Wąż sterowany przez gracza w danej turze
        """
        if [self.w, self.k] in player_snake.snake_pos:
            self.is_snake = True
            self.is_apple = False
        else:
            self.is_snake = False

    # Przy losowaniu jabłka
    def update_into_apple(self):
        """
        Przy losowaniu jabłka nie można dopuścić do sytuacji by wylosowane jabłko znalazło się na polu na którym
        znajduje się wąż. Jeżeli na wylosowanym polu nie znajduje się wąż, parametr is_apple obiektu zamieniane jest
        na True.
        """
        if self.is_snake or self.is_apple:
            return False
        else:
            self.is_apple = True
            return True


class Snake:
    def __init__(self, head):
        self.head = head
        self.snake_pos = [self.head]
        self.points = 0

    def move(self, direction, apple_pos, idx_apple_pos):
        """
        Mechanika poruszania się Węża
        :param direction: Kierunek przekazany poprzez kliknięcie w odpowiedni button
        :param apple_pos: Lista współrzędnych położenia jabłka
        :param idx_apple_pos: indeks obiektu HexField, który ma parametr is_apple=True
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
        if [x, y] in apple_pos:
            # aktualizacja listy z owocami
            idx_to_remove = apple_pos.index([x, y])
            apple_pos.remove([x, y])
            del idx_apple_pos[idx_to_remove]

            # aktualizacja ze na danym polu znajduje się snake
            for hex_field in hex_fields:
                hex_field.update_is_snake(self)

            # Aktualizacja wyniku punktowego
            self.points += 1
            widget.update_points_label()
        else:
            del self.snake_pos[-1]  # usuwam ostatnią pozycję na jakiej znalazł się wąż

        # Mechanizm kontroli czy wąż nie wjechał na siebie
        unique = list(set(map(tuple, self.snake_pos)))
        if len(unique) != len(self.snake_pos):
            print("NIEPRAWIDLOWY RUCH! KONIEC GRY")
            widget.snake_eat_himself_popup()

        # Mechanizm kontroli czy wąż nie wyszedł poza planszę
        if x < 0 or x > 19 or y < 0 or y > 19:
            widget.snake_moved_outside_board_popup()  # popup z informacją o błędnym ruchu

        # Mechanizm kontroli czy doszło do kolizji węży
        if snake_on_snake_event():
            widget.snake_on_snake_popup()

        # Mechanizm wyłonienia zwycięzcy po zdobyciu 10 punktów
        if self.points == 10:
            widget.player_won_popup()

        widget.update()


class HexBoard:
    def __init__(self, rows_n, cols_n):
        self.rows_num = rows_n
        self.cols_num = cols_n
        self.w = 0
        self.k = 0
        self.idx_counter = 0
        self.polygon = None

    def init_board(self):
        """
        Generowanie planszy oraz listy instancji obiektów
        """
        for r in range(-5, 5, 1):
            for c in range(-5, 5, 1):
                self.polygon = self.draw_hexagon(6, 30, 90 * c, r * 50)
                polygons_list.append(self.polygon)
                hex_fields.append(HexField(self.w, self.k, self.idx_counter))
                self.idx_counter += 1
                self.k += 2

            self.w += 1
            self.k = 1

            for c in range(-5, 5, 1):
                self.polygon = self.draw_hexagon(6, 30, 45 + (90 * c), (r * 50) + 25)
                polygons_list.append(self.polygon)
                hex_fields.append(HexField(self.w, self.k, self.idx_counter))
                self.idx_counter += 1
                self.k += 2

            self.w += 1
            self.k = 0

    def draw_hexagon(self, n, rad, pos_x, pos_y):
        """
        Wyrysowanie pojedynczego pola
        :param n: Liczba wierzchołków
        :param rad: Promień sześciokąta
        :param pos_x: Współrzędna x środka sześciokąta
        :param pos_y: Współrzędna x środka sześciokąta
        """
        polygon = QtGui.QPolygonF()
        w = 360 / n  # kąt o jaki przesunięte są wierzchołki

        # Wyznaczanie punktów
        for i in range(n):
            t = w * i
            x = rad * math.cos(math.radians(t))
            y = rad * math.sin(math.radians(t))
            polygon.append(QtCore.QPointF(pos_x + (1000 / 2 + x), pos_y + (800 / 2 + y)))

        return polygon

    def draw_board(self, painter):
        """
        Wyrysowanie planszy w każdej iteracji
        :param painter: Pisak wykorzystywany do rysowania (zdefiniowany w init klasy MyWidget)
        """
        counter = 0  # licznik który wykorzystywany jest do rysowania

        # Patrze na których polach znajduje się wąż
        idx_mysnake_pos = []
        idx_enemysnake_pos = []
        for hex_field in hex_fields:
            hex_field.update_is_snake(my_snake)  # czy na tym polu jest waz
            if hex_field.is_snake:  # jezeli jest
                idx_mysnake_pos.append(hex_fields.index(hex_field))

            # dla weza przeciwnika (zeby oddzielic je kolorem)
            hex_field.update_is_snake(enemy_snake)
            if hex_field.is_snake:
                idx_enemysnake_pos.append(hex_fields.index(hex_field))

        # LOSOWANIE OWOCÓW
        if not widget.apple_pos_list:
            for _ in range(5):
                random_index = random.randint(0, len(hex_fields))
                for hex_field in hex_fields:
                    if hex_field.idx == random_index:
                        # jezeli na danym polu nie znajduje się snake na polu bedzie jablko
                        flag_random_apple = hex_field.update_into_apple()
                        if flag_random_apple:
                            widget.apple_pos_list.append([hex_field.w, hex_field.k])
                            widget.idx_apple_pos.append(hex_field.idx)

        # Wypełnienie sześciokąta kolorem odpowiednim dla danego obiektu
        for polygon in polygons_list:
            if counter in idx_mysnake_pos:
                self.brush = QtGui.QBrush(QtGui.QColor(100, 255, 100))  # Kolor zielony - Wąż nr 1
                painter.setBrush(self.brush)
            elif counter in idx_enemysnake_pos:
                self.brush = QtGui.QBrush(QtGui.QColor(10, 10, 10))  # Kolor czarny - Wąż nr 2
                painter.setBrush(self.brush)
            elif counter in widget.idx_apple_pos:
                self.brush = QtGui.QBrush(QtGui.QColor(255, 100, 100))  # Czerwony kolor - Jabłko
                painter.setBrush(self.brush)
            else:
                self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))  # Biały kolor - Puste pole
                painter.setBrush(self.brush)
            painter.drawPolygon(polygon)

            counter += 1


def snake_on_snake_event():
    """
    Funkcja wykrywająca czy wąż najechal na weża drugiego gracza.
    Odbywa się to poprzez znajdowanie cześci wspólnej dwóch list.
    :return: Jeżeli znaleziona zostanie część wspólna oznacza to że wąż najechał na węża
    """
    c = [value for value in my_snake.snake_pos if value in enemy_snake.snake_pos]
    if len(c) != 0:
        return True


hex_fields = []
polygons_list = []
my_snake = Snake([2, 2])
enemy_snake = Snake([17, 17])
board = HexBoard(10, 10)

app = QtWidgets.QApplication(sys.argv)

widget = MyWidget()
widget.show()

sys.exit(app.exec_())
