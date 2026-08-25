import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from kivo.utils.path import app_data_dir


class Log:
    max_bytes = 10 * 1024 * 1024
    backup_count = 1

    @classmethod
    def kivo(cls) -> logging.Logger:
        path = (
            app_data_dir("Kivo")
            / "kivo.log"
        )

        return cls._create_logger(
            name="kivo",
            path=path,
        )

    @classmethod
    def card(
        cls,
        card_id: str,
    ) -> logging.Logger:
        path = (
            app_data_dir("Kivo")
            / "cards"
            / card_id
            / "card.log"
        )

        return cls._create_logger(
            name=f"kivo.card.{card_id}",
            path=path,
        )

    @classmethod
    def _create_logger(
        cls,
        name: str,
        path: Path,
    ) -> logging.Logger:
        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        handler = RotatingFileHandler(
            path,
            maxBytes=cls.max_bytes,
            backupCount=cls.backup_count,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s "
            "[%(process)d] "
            "%(levelname)s "
            "%(message)s"
        )

        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False

        return logger