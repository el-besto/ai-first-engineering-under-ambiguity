from app.adapters.evals.protocol import EvaluationRecorderProtocol


class FakeEvaluationRecorder(EvaluationRecorderProtocol):
    def __init__(self):
        self.recorded_cases = []

    def record_case(self, case_type: str) -> bool:
        return case_type in self.recorded_cases
