from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QLocalServer, QLocalSocket


class InstanceServer(QObject):
    activated = Signal()

    def __init__(
        self,
        name: str,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self._name = name
        self._server = QLocalServer(self)

        self._server.newConnection.connect(
            self._on_new_connection
        )

    def acquire(self) -> bool:
        if self._server.listen(self._name):
            return True

        if self._notify_existing_instance():
            return False

        QLocalServer.removeServer(self._name)

        if self._server.listen(self._name):
            return True

        raise RuntimeError(
            f"Failed to acquire Kivo instance server: "
            f"{self._server.errorString()}"
        )

    def _notify_existing_instance(self) -> bool:
        socket = QLocalSocket()

        socket.connectToServer(self._name)

        if not socket.waitForConnected(200):
            return False

        socket.write(b"activate\n")

        if not socket.waitForBytesWritten(200):
            socket.disconnectFromServer()
            return True

        socket.disconnectFromServer()

        return True

    def _on_new_connection(self) -> None:
        while self._server.hasPendingConnections():
            socket = self._server.nextPendingConnection()

            if socket is None:
                continue

            socket.readyRead.connect(
                lambda socket=socket: self._read_message(
                    socket
                )
            )
            socket.disconnected.connect(
                socket.deleteLater
            )

    def _read_message(
        self,
        socket: QLocalSocket,
    ) -> None:
        message = bytes(
            socket.readAll()
        ).strip()

        if message == b"activate":
            self.activated.emit()