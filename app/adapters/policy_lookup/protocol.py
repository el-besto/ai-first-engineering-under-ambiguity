from typing import Protocol


class PolicyLookupProtocol(Protocol):
    def verify_policy(self, policy_number: str) -> dict: ...
