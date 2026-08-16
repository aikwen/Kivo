from PySide6.QtWidgets import QLineEdit, QWidget


class SearchUI(QLineEdit):
    STYLE = """
        QLineEdit {
            background: transparent;
            color: #f1f3f4;
            border: none;

            padding: 10px 16px;
            font-size: 15px;
        }
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setPlaceholderText("Search cards...")
        self.setStyleSheet(self.STYLE)