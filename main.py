import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QResizeEvent


class Main(QWidget):
    MINIMUM_WIDTH = 740

    def __init__(self) -> None:
        super().__init__()

        layout: QVBoxLayout = QVBoxLayout()

        button = QPushButton("A")
        layout.addWidget(button)

        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setLayout(layout)


class Sidebar(QWidget):
    MINIMUM_WIDTH_DESKTOP = 150
    MAXIMUM_WIDTH_DESKTOP = 250
    MAXIMUM_WIDTH_MOBILE = MINIMUM_WIDTH_DESKTOP + Main.MINIMUM_WIDTH

    def __init__(self) -> None:
        super().__init__()

        layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(layout)

        self.setMinimumWidth(self.MINIMUM_WIDTH_DESKTOP)
        self.setMaximumWidth(self.MAXIMUM_WIDTH_DESKTOP)

        button: QPushButton = QPushButton("New session")
        layout.addWidget(button)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        widget: QWidget = QWidget(self)
        layout: QHBoxLayout = QHBoxLayout()
        widget.setLayout(layout)

        self.sidebar: Sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        self.main: Main = Main()
        layout.addWidget(self.main)

        self.mobile: bool = False
        self.lock: bool = False

        self.setMinimumHeight(640)
        self.setGeometry(0, 0, Sidebar.MAXIMUM_WIDTH_DESKTOP + Main.MINIMUM_WIDTH, 640)
        self.setCentralWidget(widget)

    def resizeEvent(self, event: QResizeEvent):
        if self.sidebar.width() <= Sidebar.MINIMUM_WIDTH_DESKTOP and not self.mobile:
            self.main.hide()
            self.sidebar.setMaximumWidth(Sidebar.MAXIMUM_WIDTH_MOBILE)
            self.setMaximumWidth(self.width())
            self.mobile, self.lock = True, True
        elif self.lock and self.sidebar.width() < Sidebar.MAXIMUM_WIDTH_MOBILE:
            self.lock = False
        elif self.sidebar.width() >= Sidebar.MAXIMUM_WIDTH_MOBILE and self.mobile and not self.lock:
            self.main.show()
            self.sidebar.setMaximumWidth(Sidebar.MAXIMUM_WIDTH_DESKTOP)
            self.setMaximumWidth(16777215)
            self.mobile = False


if __name__ == '__main__':
    application: QApplication = QApplication(sys.argv)
    main_window: MainWindow = MainWindow()
    main_window.show()
    sys.exit(application.exec())
