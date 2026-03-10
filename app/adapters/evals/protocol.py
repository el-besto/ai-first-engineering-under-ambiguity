from typing import Protocol


class EvaluationRecorderProtocol(Protocol):
    def record_case(self, case_type: str) -> bool: ...
