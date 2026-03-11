from app.adapters.evals.protocol import EvaluationRecorderProtocol
from app.infrastructure.telemetry.logger import get_logger


class FakeEvaluationRecorder(EvaluationRecorderProtocol):
    def __init__(self):
        self.recorded_cases = []
        self.logger = get_logger(__name__).bind(adapter=self.__class__.__name__)

    def record_case(self, case_type: str) -> bool:
        self.logger.bind(operation="record_case").info("completed", case_type=case_type)
        self.recorded_cases.append(case_type)
        return True

    def has_recorded_case(self, case_type: str) -> bool:
        return case_type in self.recorded_cases
