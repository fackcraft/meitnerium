import sys

from PySide6.QtCore import QByteArray, QJsonValue, QUrl, QJsonDocument
from PySide6.QtWidgets import QApplication, QWidget
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


if __name__ == "__main__":
    application: QApplication = QApplication(sys.argv)
    test: Test = Test()
    test.show()
    sys.exit(application.exec())
