from app.adapters.review_queue.protocol import ReviewQueueProtocol


class FakeReviewQueue(ReviewQueueProtocol):
    def enqueue(self, task: dict) -> None:
        pass
