import math
import sys
import threading
from PyQt5.QtGui import QBrush
from network import Network
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QPushButton
from PyQt5.Qt import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 QGraphicView"
        self.top = 200
        self.left = 500
        self.width = 1000
        self.height = 750
        self.player_snake = snake

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Przycisk odpowiedzialny za ruch w lewy górny róg
        b_q = QPushButton('Lewy Górny', self)
        b_q.move(10, 10)
        b_q.clicked.connect(self.click_q)

        # Przycisk odpowiedzialny za ruch w górę
        b_w = QPushButton('Góra', self)
        b_w.move(110, 10)
        b_w.clicked.connect(self.click_w)

        # Przycisk odpowiedzialny za ruch w prawy górny róg
        b_e = QPushButton('Prawy Górny', self)
        b_e.move(210, 10)
        b_e.clicked.connect(self.click_e)

        # Przycisk odpowiedzialny za ruch w lewy dolny róg
        b_a = QPushButton('Lewy Dolny', self)
        b_a.move(10, 40)
        b_a.clicked.connect(self.click_a)

        # Przycisk odpowiedzialny za ruch w dół
        b_s = QPushButton('Dół', self)
        b_s.move(110, 40)
        b_s.clicked.connect(self.click_s)

        # Przycisk odpowiedzialny za ruch w prawy dolny róg
        b_d = QPushButton('Prawy Dolny', self)
        b_d.move(210, 40)
        b_d.clicked.connect(self.click_d)

        # Inicjalizacja labeli
        my_font = QtGui.QFont()
        my_font.setFamily("Cambria")
        my_font.setPointSize(20)

        self.label_first_snake_points = QtWidgets.QLabel(self)
        self.label_first_snake_points.setFont(my_font)
        self.label_first_snake_points.move(450, 20)
        self.label_first_snake_points.setText(f"Moj wynik: {snake.points}")
        self.label_first_snake_points.adjustSize()

        self.label_second_snake_points = QtWidgets.QLabel(self)
        self.label_second_snake_points.setFont(my_font)
        self.label_second_snake_points.move(450, 70)
        self.label_second_snake_points.setText(f"Wynik przeciwnika: {snake2.points}")
        self.label_second_snake_points.adjustSize()

        self.scene = QGraphicsScene()
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)

        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(3)

        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0, 120, 980, 575)
        # self.createGraphicView()

        # Tworzenie itemow
        w = 0
        k = 0
        idx_counter = 0
        for r in range(-5, 5, 1):
            for c in range(-5, 5, 1):
                he = HexagonItem(6, 30, (-500) + 90 * c, (-300) + r * 50, w, k, idx_counter)
                he.create_poly()
                hex_items.append(he)
                self.scene.addItem(hex_items[idx_counter])
                idx_counter += 1
                k += 2

            w += 1
            k = 1

            for c in range(-5, 5, 1):
                he = HexagonItem(6, 30, (-500) + 45 + (90 * c), (-300) + (r * 50) + 25, w, k, idx_counter)
                he.create_poly()
                hex_items.append(he)
                self.scene.addItem(hex_items[idx_counter])
                idx_counter += 1
                k += 2

            w += 1
            k = 0

        self.show()
        self.force_paint_event()  # watek zwiazany z odswiezaniem

    # Funkcje wiazace przyciski z poruszaniem sie
    def click_q(self):
        self.player_snake.move("Q")

    def click_w(self):
        self.player_snake.move("W")

    def click_e(self):
        self.player_snake.move("E")

    def click_a(self):
        self.player_snake.move("A")

    def click_s(self):
        self.player_snake.move("S")

    def click_d(self):
        self.player_snake.move("D")

    def force_paint_event(self):
        threading.Timer(0.1, self.force_paint_event).start()
        self.paintEvent()

    def paintEvent(self, *args, **kwargs):
        # Aktualizacja informacji dotyczacych drugiego gracza
        # noinspection PyShadowingNames
        snake2 = net.send(snake)

        # Aktualizacja wyniku punktowego
        self.label_first_snake_points.setText(f"Moj wynik: {snake.points}")
        self.label_first_snake_points.adjustSize()
        self.label_second_snake_points.setText(f"Wynik przeciwnika: {snake2.points}")
        self.label_second_snake_points.adjustSize()

        # Mechaniki sprawdzające czy ktorys z graczy nie wykonal nielegalnego ruchu konczacego gre
        # Gdy moj waz najechal na siebie
        if snake.is_ate_himself:
            self.label_first_snake_points.setText(f"Moj wynik: Przegrywasz!")
            self.label_first_snake_points.adjustSize()
            self.label_second_snake_points.setText(f"Przeciwnik wygrywa")
            self.label_second_snake_points.adjustSize()

        # Gdy moj waz wyjechal poza plansze
        if snake.is_moved_outside_board:
            self.label_first_snake_points.setText(f"Moj wynik: Przegrywasz!")
            self.label_first_snake_points.adjustSize()
            self.label_second_snake_points.setText(f"Przeciwnik wygrywa")
            self.label_second_snake_points.adjustSize()

        # Kontrola czy waz najechal na weza
        c = [value for value in snake.snake_pos if value in snake2.snake_pos]
        if len(c) != 0:
            snake.is_moved_on_another_snake = True
        # Moj waz najechal na weza drugiego gracza
        if snake.is_moved_on_another_snake:
            self.label_first_snake_points.setText(f"Moj wynik: Przegrywasz!")
            self.label_first_snake_points.adjustSize()
            self.label_second_snake_points.setText(f"Przeciwnik wygrywa")
            self.label_second_snake_points.adjustSize()

        # Waz przeciwnika najechal na siebie
        if snake2.is_ate_himself:
            self.label_first_snake_points.setText(f"Moj wynik: Wygrywasz!")
            self.label_first_snake_points.adjustSize()
            self.label_second_snake_points.setText(f"Przeciwnik wykonal nieprawidlowy ruch")
            self.label_second_snake_points.adjustSize()

        # Waz przeciwnika wyjechal poza plansze
        if snake2.is_moved_outside_board:
            self.label_first_snake_points.setText(f"Moj wynik: Wygrywasz!")
            self.label_first_snake_points.adjustSize()
            self.label_second_snake_points.setText(f"Przeciwnik wykonal nieprawidlowy ruch")
            self.label_second_snake_points.adjustSize()

        # Waz przeciwnika najechal na mojego weza
        if snake2.is_moved_on_another_snake:
            self.label_first_snake_points.setText(f"Moj wynik: Wygrywasz!")
            self.label_first_snake_points.adjustSize()
            self.label_second_snake_points.setText(f"Przeciwnik wykonal nieprawidlowy ruch")
            self.label_second_snake_points.adjustSize()

        # Moj waz wygral
        if snake.is_winner:
            self.label_first_snake_points.setText(f"Moj wynik: Wygrywasz!")
            self.label_first_snake_points.adjustSize()
            self.label_second_snake_points.setText(f"Przeciwnik byl wolniejszy od Ciebie")
            self.label_second_snake_points.adjustSize()
        # Moj waz przegral
        elif snake2.is_winner:
            self.label_first_snake_points.setText(f"Moj wynik: Przegrywasz")
            self.label_first_snake_points.adjustSize()
            self.label_second_snake_points.setText(f"Przeciwnik byl szybszy od Ciebie")
            self.label_second_snake_points.adjustSize()

        # noinspection PyShadowingNames
        apple_pos = [pos for pos in snake.apple_p if pos in snake2.apple_p]
        snake.apple_p = apple_pos
        snake2.apple_p = apple_pos

        # Zczytanie gdzie znajduja sie weze lub jablko - do rysowania
        counter = 0
        idx_my_snake.clear()
        idx_enemy_snake.clear()
        idx_apple_pos.clear()
        for hex_item in hex_items:
            if [hex_item.w, hex_item.k] in snake.snake_pos:
                idx_my_snake.append(hex_items.index(hex_item))
            elif [hex_item.w, hex_item.k] in snake2.snake_pos:
                idx_enemy_snake.append(hex_items.index(hex_item))
            elif [hex_item.w, hex_item.k] in apple_pos:
                idx_apple_pos.append(hex_items.index(hex_item))

        counter += 1
        self.scene.update()


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
        # print("create")
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
        # print(self.polygon)
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(3)
        self.greenBrush = QtGui.QBrush(QtGui.QColor(100, 255, 100))
        self.redBrush = QtGui.QBrush(QtGui.QColor(255, 100, 100))
        self.blackBrush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))

        QPainter.setPen(self.pen)
        if self.idx in idx_my_snake:
            QPainter.setBrush(self.greenBrush)
        elif self.idx in idx_enemy_snake:
            QPainter.setBrush(self.blackBrush)
        elif self.idx in idx_apple_pos:
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


net = Network()
snake = net.getP()
snake2 = net.send(snake)
apple_pos = [pos for pos in snake.apple_p if pos in snake2.apple_p]

idx_my_snake = []
idx_enemy_snake = []
idx_apple_pos = []
hex_items = []

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
