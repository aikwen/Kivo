import sys

from PySide6.QtCore import Qt, Signal,QPoint
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from kivo.components.popup_menu.main import PopupMenu
from kivo.resources.loader import resource_path

from .ui import TitleBarUI


class TitleBar(TitleBarUI):
    settings_requested = Signal()
    hide_requested = Signal()
    exit_requested = Signal()

    def __init__(
        self,
        title: str,
        settings_enabled: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            title=title,
            parent=parent,
        )

        self.popup_menu = PopupMenu(
            settings_enabled=settings_enabled
        )

        self.more_button.clicked.connect(
            self._show_popup_menu
        )

        self.popup_menu.settings_requested.connect(
            self.settings_requested.emit
        )
        self.popup_menu.hide_requested.connect(
            self.hide_requested.emit
        )
        self.popup_menu.exit_requested.connect(
            self.exit_requested.emit
        )

    def set_title(
        self,
        title: str,
    ) -> None:
        self.title_label.setText(title)

    def mousePressEvent(
        self,
        event: QMouseEvent,
    ) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.popup_menu.hide()

            window = self.window()
            handle = window.windowHandle()

            if handle is not None:
                handle.startSystemMove()

        super().mousePressEvent(event)

    def _show_popup_menu(self) -> None:
        self.popup_menu.show_for(
            self.more_button
        )


if __name__ == "__main__":
    class DemoCard(QWidget):
        resize_margin = 6

        def __init__(self) -> None:
            super().__init__()

            self.setMouseTracking(True)

        def mousePressEvent(
            self,
            event: QMouseEvent,
        ) -> None:
            if event.button() != Qt.MouseButton.LeftButton:
                super().mousePressEvent(event)
                return

            edges = self._resize_edges(
                event.position().toPoint()
            )

            if edges:
                handle = self.windowHandle()

                if handle is not None:
                    handle.startSystemResize(edges)
                    return

            super().mousePressEvent(event)

        def mouseMoveEvent(
            self,
            event: QMouseEvent,
        ) -> None:
            edges = self._resize_edges(
                event.position().toPoint()
            )

            if edges in (
                Qt.Edge.LeftEdge | Qt.Edge.TopEdge,
                Qt.Edge.RightEdge | Qt.Edge.BottomEdge,
            ):
                cursor = Qt.CursorShape.SizeFDiagCursor

            elif edges in (
                Qt.Edge.RightEdge | Qt.Edge.TopEdge,
                Qt.Edge.LeftEdge | Qt.Edge.BottomEdge,
            ):
                cursor = Qt.CursorShape.SizeBDiagCursor

            elif edges & (
                Qt.Edge.LeftEdge | Qt.Edge.RightEdge
            ):
                cursor = Qt.CursorShape.SizeHorCursor

            elif edges & (
                Qt.Edge.TopEdge | Qt.Edge.BottomEdge
            ):
                cursor = Qt.CursorShape.SizeVerCursor

            else:
                cursor = Qt.CursorShape.ArrowCursor

            self.setCursor(cursor)

            super().mouseMoveEvent(event)

        def _resize_edges(
            self,
            position: QPoint,
        ) -> Qt.Edge:
            edges = Qt.Edge(0)

            if position.x() <= self.resize_margin:
                edges |= Qt.Edge.LeftEdge

            elif position.x() >= (
                self.width() - self.resize_margin
            ):
                edges |= Qt.Edge.RightEdge

            if position.y() <= self.resize_margin:
                edges |= Qt.Edge.TopEdge

            elif position.y() >= (
                self.height() - self.resize_margin
            ):
                edges |= Qt.Edge.BottomEdge

            return edges

    app = QApplication(sys.argv)

    window = DemoCard()
    window.resize(
        560,
        360,
    )
    window.setMinimumSize(
        360,
        240,
    )

    window.setWindowFlags(
        Qt.WindowType.Tool
        | Qt.WindowType.FramelessWindowHint
        | Qt.WindowType.WindowStaysOnTopHint
    )

    with resource_path(
        "icons",
        "tray.ico",
    ) as icon_path:
        window.setWindowIcon(
            QIcon(str(icon_path))
        )

    window.setObjectName(
        "card"
    )

    window.setStyleSheet(
        """
        QWidget#card {
            background: #FFFFFF;
        }

        QLabel#content {
            color: #636366;
        }
        """
    )

    root_layout = QVBoxLayout(window)
    root_layout.setContentsMargins(
        0,
        0,
        0,
        0,
    )
    root_layout.setSpacing(0)

    title_bar = TitleBar(
        title="JSON Formatter",
        settings_enabled=True,
    )

    content = QWidget()

    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(
        16,
        16,
        16,
        16,
    )

    content_label = QLabel(
        "这里是 Card 的内容区域"
    )
    content_label.setObjectName(
        "content"
    )

    content_layout.addWidget(
        content_label
    )
    content_layout.addStretch()

    root_layout.addWidget(
        title_bar
    )
    root_layout.addWidget(
        content,
        1,
    )

    title_bar.settings_requested.connect(
        lambda: print("设置")
    )

    title_bar.hide_requested.connect(
        lambda: print("隐藏")
    )

    title_bar.exit_requested.connect(
        app.quit
    )

    window.show()

    sys.exit(app.exec())