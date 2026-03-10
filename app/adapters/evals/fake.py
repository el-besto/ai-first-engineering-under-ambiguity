from app.adapters.evals.protocol import EvaluationRecorderProtocol


class FakeEvaluationRecorder(EvaluationRecorderProtocol):
    def __init__(self):
        self.recorded_cases = []

    def record_case(self, case_type: str) -> bool:
        self.recorded_cases.append(case_type)
        return True

    def has_recorded_case(self, case_type: str) -> bool:
        return case_type in self.recorded_cases
