import sys
from enum import Enum

from PySide6.QtCore import QByteArray, QJsonValue, QUrl, QJsonDocument
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QScrollArea, \
    QLabel
from PySide6.QtGui import QResizeEvent
from PySide6.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply


class Test(QWidget):
    def __init__(self) -> None:
        super().__init__()

        json: dict[str, QJsonValue] = {
            "model": "gemma",
            "prompt": "please say 'hello world'",
        }
        document: QJsonDocument = QJsonDocument()
        document.setObject(json)
        data: QByteArray = document.toJson()

        url: QUrl = QUrl("http://localhost:11434/api/generate")
        request: QNetworkRequest = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_response)
        self.network_manager.post(request, data)

    def handle_response(self, reply: QNetworkReply) -> None:
        print(str(reply.readAll(), 'utf-8'))


class Message(QWidget):
    def __init__(self) -> None:
        super().__init__()


class Main(QWidget):
    MINIMUM_WIDTH = 740

    def __init__(self) -> None:
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        layout: QVBoxLayout = QVBoxLayout()

        scroll_area: QScrollArea = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        scroll_content_widget: QWidget = QWidget()
        scroll_area.setWidget(scroll_content_widget)

        scroll_content_widget_layout: QHBoxLayout = QHBoxLayout()
        scroll_content_widget.setLayout(scroll_content_widget_layout)

        label = QLabel("Hello World")
        scroll_content_widget_layout.addWidget(label)

        self.setMinimumWidth(self.MINIMUM_WIDTH)
        self.setLayout(layout)


class MessageList(QWidget):
    MINIMUM_WIDTH_DESKTOP = 150
    MAXIMUM_WIDTH_DESKTOP = 250
    MAXIMUM_WIDTH_MOBILE = MINIMUM_WIDTH_DESKTOP + Main.MINIMUM_WIDTH

    def __init__(self) -> None:
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        layout: QVBoxLayout = QVBoxLayout()

        scroll_area: QScrollArea = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        scroll_content_widget: QWidget = QWidget()
        scroll_area.setWidget(scroll_content_widget)

        scroll_content_widget_layout: QHBoxLayout = QHBoxLayout()
        scroll_content_widget.setLayout(scroll_content_widget_layout)

        button: QPushButton = QPushButton("New session")
        scroll_content_widget_layout.addWidget(button)

        self.setLayout(layout)
        self.setMinimumWidth(self.MINIMUM_WIDTH_DESKTOP)
        self.setMaximumWidth(self.MAXIMUM_WIDTH_DESKTOP)


class MainWindow(QMainWindow):
    class Status(Enum):
        MOBILE: int = 0
        DESKTOP: int = 1
        Lock: int = 3

    def __init__(self) -> None:
        super().__init__()

        widget: QWidget = QWidget(self)
        layout: QHBoxLayout = QHBoxLayout()
        widget.setLayout(layout)

        self.sidebar: MessageList = MessageList()
        layout.addWidget(self.sidebar)

        self.main: Main = Main()
        layout.addWidget(self.main)

        self.status: MainWindow.Status = MainWindow.Status.DESKTOP

        self.setMinimumHeight(640)
        self.setGeometry(0, 0, MessageList.MAXIMUM_WIDTH_DESKTOP + Main.MINIMUM_WIDTH, 640)
        self.setCentralWidget(widget)

    def resizeEvent(self, event: QResizeEvent):
        if self.sidebar.width() <= MessageList.MINIMUM_WIDTH_DESKTOP and self.status == MainWindow.Status.DESKTOP:
            self.main.hide()
            self.sidebar.setMaximumWidth(MessageList.MAXIMUM_WIDTH_MOBILE)
            self.setMaximumWidth(self.width())
            self.status = MainWindow.Status.Lock
            return
        if self.status == MainWindow.Status.Lock and self.sidebar.width() < MessageList.MAXIMUM_WIDTH_MOBILE:
            self.status = MainWindow.Status.MOBILE
            return
        if self.sidebar.width() >= MessageList.MAXIMUM_WIDTH_MOBILE and self.status == MainWindow.Status.MOBILE:
            self.main.show()
            self.sidebar.setMaximumWidth(MessageList.MAXIMUM_WIDTH_DESKTOP)
            self.setMaximumWidth(16777215)
            self.status = MainWindow.Status.DESKTOP


if __name__ == '__main__':
    application: QApplication = QApplication(sys.argv)
    main_window: MainWindow = MainWindow()
    main_window.show()
    sys.exit(application.exec())
