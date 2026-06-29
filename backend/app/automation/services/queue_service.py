from collections import deque
from typing import Any


class QueueService:
    def __init__(self) -> None:
        self._queue: deque[dict[str, Any]] = deque()

    def enqueue(self, item: dict[str, Any]) -> None:
        self._queue.append(item)

    def dequeue(self) -> dict[str, Any] | None:
        if not self._queue:
            return None
        return self._queue.popleft()

    def size(self) -> int:
        return len(self._queue)

