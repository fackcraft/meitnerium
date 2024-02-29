
import sys
from enum import Enum

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QScrollArea, \
    QLabel
from PySide6.QtGui import QResizeEvent, QVector3D, QQuaternion
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DRender import Qt3DRender


# noinspection PyUnresolvedReferences
import assets.resources


class Aircraft(Qt3DExtras.Qt3DWindow):
    def __init__(self) -> None:
        super().__init__()

        # camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 0, 40))
        self.camera().setViewCenter(QVector3D(0, 0, 0))

        # root entity
        root_entity = Qt3DCore.QEntity()

        # material
        material = Qt3DExtras.QPhongMaterial(root_entity)

        self.setRootEntity(root_entity)

        self.torusEntity = Qt3DCore.QEntity(root_entity)
        self.torusMesh = Qt3DExtras.QTorusMesh()
        self.torusMesh.setRadius(5)
        self.torusMesh.setMinorRadius(1)
        self.torusMesh.setRings(100)
        self.torusMesh.setSlices(20)

        self.torusTransform = Qt3DCore.QTransform()
        self.torusTransform.setScale3D(QVector3D(1.5, 1, 0.5))
        self.torusTransform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(1, 0, 0), 45))

        self.torusEntity.addComponent(self.torusMesh)
        self.torusEntity.addComponent(self.torusTransform)
        self.torusEntity.addComponent(material)


        # aircraft
        entity = Qt3DCore.QEntity(root_entity)
        mesh: Qt3DRender.QMesh = Qt3DRender.QMesh(root_entity)
        mesh.setSource(":aircraft.obj")

        transform = Qt3DCore.QTransform()
        transform.setScale3D(QVector3D(1.5, 1, 0.5))
        transform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(1, 0, 0), 45))

        entity.addComponent(mesh)
        entity.addComponent(transform)
        entity.addComponent(material)


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
        print(self.sidebar.width(), MessageList.MINIMUM_WIDTH_DESKTOP, self.status)
        if self.sidebar.width() <= MessageList.MINIMUM_WIDTH_DESKTOP and self.status == MainWindow.Status.DESKTOP:
            self.main.hide()
            self.sidebar.setMaximumWidth(MessageList.MAXIMUM_WIDTH_MOBILE)
            self.setMaximumWidth(self.width())
            self.status = MainWindow.Status.Lock
        elif self.status == MainWindow.Status.Lock and self.sidebar.width() < MessageList.MAXIMUM_WIDTH_MOBILE:
            self.status = MainWindow.Status.MOBILE
        elif self.sidebar.width() >= MessageList.MAXIMUM_WIDTH_MOBILE and self.status == MainWindow.Status.MOBILE:
            self.main.show()
            self.sidebar.setMaximumWidth(MessageList.MAXIMUM_WIDTH_DESKTOP)
            self.setMaximumWidth(16777215)
            self.status = MainWindow.Status.DESKTOP


if __name__ == '__main__':
    application: QApplication = QApplication(sys.argv)
    main_window: MainWindow = MainWindow()
    main_window.show()
    # aircraft: Aircraft = Aircraft()
    # aircraft.show()
    sys.exit(application.exec())
