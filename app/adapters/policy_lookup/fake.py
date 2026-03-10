from app.adapters.policy_lookup.protocol import PolicyLookupProtocol


class FakePolicyLookup(PolicyLookupProtocol):
    def verify_policy(self, policy_number: str) -> dict:
        return {}
