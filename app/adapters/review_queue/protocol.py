from typing import Protocol


class ReviewQueueProtocol(Protocol):
    def enqueue(self, task: dict) -> None: ...
