from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt


class CardListModel(QAbstractListModel):
    def __init__(self, cards: list[str] | None = None) -> None:
        super().__init__()
        self._cards = cards or []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._cards)

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return self._cards[index.row()]

        return None

    def set_cards(self, cards: list[str]) -> None:
        self.beginResetModel()
        self._cards = cards
        self.endResetModel()

    def card(self, index: QModelIndex) -> str | None:
        if not index.isValid():
            return None

        row = index.row()
        if row < 0 or row >= len(self._cards):
            return None

        return self._cards[row]