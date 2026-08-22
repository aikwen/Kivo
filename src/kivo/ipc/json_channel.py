import json
from typing import Any, TextIO


class JsonChannel:
    def __init__(
        self,
        reader: TextIO,
        writer: TextIO,
    ) -> None:
        self._reader = reader
        self._writer = writer

    def send(self, data: Any) -> None:
        message = json.dumps(
            data,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        self._writer.write(message)
        self._writer.write("\n")
        self._writer.flush()

    def recv(self) -> Any | None:
        line = self._reader.readline()

        if not line:
            return None

        return json.loads(line)