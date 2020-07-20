import math
import random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView,  QGraphicsPolygonItem, \
    QPushButton, QMessageBox, QGraphicsPixmapItem
from PyQt5.QtGui import QBrush, QPixmap
from PyQt5.Qt import Qt
import sys
import rsc


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.player_snake = my_snake

        # Zmienne wykorzystywane do przechowywania owoców
        self.apple_pos_list = []
        self.idx_apple_pos = []

        self.title = "PyQt5 QGraphicView"
        self.top = 200
        self.left = 500
        self.width = 1200
        self.height = 800

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGraphicView()

        # Przycisk odpowiedzialny za nową grę
        b_new_game = QPushButton('Nowa Gra', self)
        b_new_game.move(10, 10)
        b_new_game.clicked.connect(self.click_new_game)

        # Przycisk odpowiedzialny za wyjście
        b_exit = QPushButton('Wyjscie', self)
        b_exit.move(110, 10)
        b_exit.clicked.connect(self.click_exit)

        # Przycisk odpowiedzialny za ruch w lewy górny róg
        b_q = QPushButton('Lewy Górny', self)
        b_q.move(10, 70)
        b_q.clicked.connect(self.click_q)

        # Przycisk odpowiedzialny za ruch w górę
        b_w = QPushButton('Góra', self)
        b_w.move(110, 70)
        b_w.clicked.connect(self.click_w)

        # Przycisk odpowiedzialny za ruch w prawy górny róg
        b_e = QPushButton('Prawy Górny', self)
        b_e.move(210, 70)
        b_e.clicked.connect(self.click_e)

        # Przycisk odpowiedzialny za ruch w lewy dolny róg
        b_a = QPushButton('Lewy Dolny', self)
        b_a.move(10, 100)
        b_a.clicked.connect(self.click_a)

        # Przycisk odpowiedzialny za ruch w dół
        b_s = QPushButton('Dół', self)
        b_s.move(110, 100)
        b_s.clicked.connect(self.click_s)

        # Przycisk odpowiedzialny za ruch w prawy dolny róg
        b_d = QPushButton('Prawy Dolny', self)
        b_d.move(210, 100)
        b_d.clicked.connect(self.click_d)

        # noinspection PyAttributeOutsideInit
        self.label_first_snake_points = QtWidgets.QLabel(self)
        # noinspection PyAttributeOutsideInit
        self.label_second_snake_points = QtWidgets.QLabel(self)
        # noinspection PyAttributeOutsideInit
        self.label_whose_turn = QtWidgets.QLabel(self)
        self.init_labels()

        self.show()

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

    # noinspection PyAttributeOutsideInit
    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)

        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(3)

        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(50, 150, 1000, 600)

        # osobna scena zeby wyswietlic zdjecie korzystajac QGraphicsItem
        self.scene_img = QGraphicsScene()
        graphicView_img = QGraphicsView(self.scene_img, self)
        graphicView_img.setGeometry(1000, 10, 120, 120)

        self.shapes()

    def shapes(self):
        """
        Tworzę itemy
        :return:
        """
        w = 0
        k = 0
        idx_counter = 0

        for r in range(-5, 5, 1):
            for c in range(-5, 5, 1):
                he = HexagonItem(6, 30, (-500) + 90*c, (-300) + r*50, w, k, idx_counter)
                he.create_poly()
                hex_items.append(he)
                self.scene.addItem(hex_items[idx_counter])
                idx_counter += 1
                k += 2

            w += 1
            k = 1

            for c in range(-5, 5, 1):
                he = HexagonItem(6, 30, (-500) + 45 + (90*c), (-300) + (r*50) + 25, w, k, idx_counter)
                he.create_poly()
                hex_items.append(he)
                self.scene.addItem(hex_items[idx_counter])
                idx_counter += 1
                k += 2

            w += 1
            k = 0

        # Użycie resources za pomoca QGraphicsPixmapItem do wyświetlania grafik
        im_qrc = QGraphicsPixmapItem()
        path = QPixmap(":/mojqrc/sn_img.jpg")
        im_qrc.setPixmap(path)
        self.scene_img.addItem(im_qrc)

    # noinspection PyAttributeOutsideInit
    def paintEvent(self, *args, **kwargs):
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(3)
        self.greenBrush = QtGui.QBrush(QtGui.QColor(100, 255, 100))
        self.redBrush = QtGui.QBrush(QtGui.QColor(255, 100, 100))
        self.blackBrush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))

        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        # Losuje jablka
        if not self.apple_pos_list:
            for _ in range(5):
                random_idx = random.randint(0, len(hex_items)-1)
                a_x = hex_items[random_idx].w
                a_y = hex_items[random_idx].k
                if [a_x, a_y] in my_snake.snake_pos or [a_x, a_y] in enemy_snake.snake_pos:
                    pass
                else:
                    self.apple_pos_list.append([a_x, a_y])
                    self.idx_apple_pos.append(random_idx)

        # Dobranie odpowiedniego wypelnienia
        counter = 0
        idx_my_snake.clear()
        idx_enemy_snake.clear()
        for hex_item in hex_items:
            if [hex_item.w, hex_item.k] in my_snake.snake_pos:
                idx_my_snake.append(hex_items.index(hex_item))
            elif [hex_item.w, hex_item.k] in enemy_snake.snake_pos:
                idx_enemy_snake.append(hex_items.index(hex_item))

        counter += 1
        self.scene.update()

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
        self.scene.update()

    # noinspection PyMethodMayBeStatic
    def click_exit(self):
        sys.exit(App.exec_())

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
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText("Koniec gry")

        if self.player_snake == my_snake:
            msg.setDetailedText("Wygrywa Gracz 2")
        else:
            msg.setDetailedText("Wygrywa Gracz 1")

        msg.buttonClicked.connect(self.exit_snake)
        x = msg.exec_()

    def snake_moved_outside_board_popup(self):
        """
        Funkcja wywołująca okienko w przypadku wyjścia węża poza planszę gry
        """
        msg = QMessageBox()
        msg.setWindowTitle("Niedozwolony ruch")
        msg.setText("Wąż wyszedł poza pole gry")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText("Koniec gry")

        if self.player_snake == my_snake:
            msg.setDetailedText("Wygrywa Gracz 2")
        else:
            msg.setDetailedText("Wygrywa Gracz 1")

        msg.buttonClicked.connect(self.exit_snake)
        x = msg.exec_()

    def snake_on_snake_popup(self):
        """
        Funkcja wywołująca okienko w przypadku najechania węża na węża drugiego gracza
        """
        msg = QMessageBox()
        msg.setWindowTitle("Niedozwolony ruch")
        msg.setText("Wąż najechał na węża przeciwnika")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText("Koniec gry")

        if self.player_snake == my_snake:
            msg.setDetailedText("Wygrywa Gracz 2")
        else:
            msg.setDetailedText("Wygrywa Gracz 1")

        msg.buttonClicked.connect(self.exit_snake)
        x = msg.exec_()

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
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText("Gratulacje!")
        msg.buttonClicked.connect(self.exit_snake)
        x = msg.exec_()

    # noinspection PyMethodMayBeStatic
    def exit_snake(self, i):
        exit()

    def update_points_label(self):
        """
        Aktualizacja informacji tekstowych dotyczących liczby punktów graczy
        """
        self.label_first_snake_points.setText(f"Gracz1: {my_snake.points}")
        self.label_second_snake_points.setText(f"Gracz2: {enemy_snake.points}")


class HexagonItem(QGraphicsPolygonItem):
    """
    Klasa ktora definiuje kazde pole na planszy. Tworzenie createpoly i rysowanie paint
    """
    def __init__(self, n, rad, pos_x, pos_y, w, k, idx_counter):
        super().__init__()
        self.n = n
        self.rad = rad
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.w = w
        self.k = k
        self.idx = idx_counter
        self.polygon = None
        self.is_snake = False
        self.is_apple = False

    def create_poly(self):
        self.polygon = QtGui.QPolygonF()
        w = 360 / self.n  # kąt o jaki przesunięte są wierzchołki

        # Wyznaczanie punktów
        for i in range(self.n):
            t = w * i
            x = self.rad * math.cos(math.radians(t))
            y = self.rad * math.sin(math.radians(t))
            self.polygon.append(QtCore.QPointF(self.pos_x + (1000 / 2 + x), self.pos_y + (600 / 2 + y)))

        return self.polygon

    # noinspection PyAttributeOutsideInit
    def paint(self, QPainter, QStyleOptionGraphicsItem, widget=None):
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(3)
        self.greenBrush = QtGui.QBrush(QtGui.QColor(100, 255, 100))
        self.redBrush = QtGui.QBrush(QtGui.QColor(255, 100, 100))
        self.blackBrush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        QPainter.setPen(self.pen)

        # Wybranie odpowiedniego wypelnienia przy rysowaniu
        if self.idx in idx_my_snake:
            QPainter.setBrush(self.greenBrush)
        elif self.idx in idx_enemy_snake:
            QPainter.setBrush(self.blackBrush)
        elif self.idx in window.idx_apple_pos:
            QPainter.setBrush(self.redBrush)

        QPainter.drawPolygon(self.polygon)

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
    """
    Klasa definiująca węża - gracza
    """
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
            for hex_field in hex_items:
                hex_field.update_is_snake(self)

            # Aktualizacja wyniku punktowego
            self.points += 1
            window.update_points_label()
        else:
            del self.snake_pos[-1]  # usuwam ostatnią pozycję na jakiej znalazł się wąż

        # Mechanizm kontroli czy wąż nie wjechał na siebie
        unique = list(set(map(tuple, self.snake_pos)))
        if len(unique) != len(self.snake_pos):
            print("NIEPRAWIDLOWY RUCH! KONIEC GRY")
            window.snake_eat_himself_popup()

        # Mechanizm kontroli czy wąż nie wyszedł poza planszę
        if x < 0 or x > 19 or y < 0 or y > 19:
            window.snake_moved_outside_board_popup()  # popup z informacją o błędnym ruchu

        # Mechanizm kontroli czy doszło do kolizji węży
        if snake_on_snake_event():
            window.snake_on_snake_popup()

        # Mechanizm wyłonienia zwycięzcy po zdobyciu 10 punktów
        if self.points == 10:
            window.player_won_popup()


def snake_on_snake_event():
    """
    Funkcja wykrywająca czy wąż najechal na weża drugiego gracza.
    Odbywa się to poprzez znajdowanie cześci wspólnej dwóch list.
    :return: Jeżeli znaleziona zostanie część wspólna oznacza to że wąż najechał na węża
    """
    c = [value for value in my_snake.snake_pos if value in enemy_snake.snake_pos]
    if len(c) != 0:
        return True


hex_items = []
idx_my_snake = []
idx_enemy_snake = []
my_snake = Snake([2, 2])
enemy_snake = Snake([17, 17])
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
