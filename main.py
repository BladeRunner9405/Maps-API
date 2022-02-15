import sys

from samples import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel


class MyWidget(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('map.ui', self)
        self.obj_name = 'Красная площадь'
        self.ll, self.spn = get_ll_span(self.obj_name)
        print(self.ll, self.spn)
        self.show_picture()


    def show_picture(self):
        ll_spn = f"ll={self.ll}&spn={self.spn}"
        self.pixmap = QPixmap(get_map_img(ll_spn).name)
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        # self.label = QLabel(self)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.label.setPixmap(self.pixmap)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    example_app = MyWidget()
    example_app.show()
    sys.exit(app.exec())
