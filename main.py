import sys

from samples import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('map.ui', self)
        self.obj_name = 'Красная площадь'
        self.ll, self.spn = get_ll_span(self.obj_name)
        self.z = 17
        print(self.ll, self.spn)
        self.show_picture()

    def show_picture(self):
        ll = f"ll={self.ll}"
        self.pixmap = QPixmap(get_map_img(ll, 'map', 'z=' + str(self.z)).name)
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        # self.label = QLabel(self)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.z + 1 <= 17:
                self.z += 1
        elif event.key() == Qt.Key_PageDown:
            if self.z - 1 >= 0:
                self.z -= 1
        self.show_picture()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example_app = MyWidget()
    example_app.show()
    sys.exit(app.exec())
