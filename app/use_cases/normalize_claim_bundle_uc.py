from app.entities.claim_intake_bundle import ClaimIntakeBundle
from app.use_cases.protocols import LoggerProtocol


class NormalizeClaimBundleUseCase:
    def __init__(self, logger: LoggerProtocol):
        self.logger = logger.bind(use_case=self.__class__.__name__)

    def execute(self, bundle: ClaimIntakeBundle) -> ClaimIntakeBundle:
        self.logger.info("started")
        self.logger.info("completed")
        return bundle
