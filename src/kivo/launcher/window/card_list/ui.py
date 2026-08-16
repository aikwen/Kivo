from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QListView,
    QWidget,
)

from .delegate import CardItemDelegate
from .model import CardListModel


class CardListUI(QListView):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.card_model = CardListModel()
        self.setModel(self.card_model)

        self.card_delegate = CardItemDelegate(self)
        self.setItemDelegate(self.card_delegate)

        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.setMouseTracking(True)
        self.setUniformItemSizes(True)
        self.setSpacing(0)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        self.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(
            """
            QListView {
                background: transparent;
                border: none;
                outline: none;
            }

            QListView::viewport {
                background: transparent;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #BEBEBE;
                min-height: 24px;
                border-radius: 3px;
            }

            QScrollBar::handle:vertical:hover {
                background: #D0D0D0;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )