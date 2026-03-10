from app.entities.claim_intake_bundle import ClaimIntakeBundle


class NormalizeClaimBundleUseCase:
    def execute(self, bundle: ClaimIntakeBundle) -> ClaimIntakeBundle:
        return bundle
