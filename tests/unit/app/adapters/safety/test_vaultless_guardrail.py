from unittest.mock import patch

import pytest
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.adapters.safety.vaultless_guardrail import VaultlessPIIGuardrail


@pytest.fixture
def secret_key_hex():
    return AESGCM.generate_key(bit_length=256).hex()


@pytest.fixture
def guardrail(secret_key_hex, tmp_path):
    # Create a dummy compiled model file to satisfy the existence check
    dummy_model_path = tmp_path / "compiled_pii_extractor.json"
    dummy_model_path.write_text("{}")

    with patch("dspy.Predict.load"):
        yield VaultlessPIIGuardrail(secret_key_hex, str(dummy_model_path))


class FakePrediction:
    def __init__(self, entities):
        self.pii_entities = entities


def test_vaultless_guardrail_initialization_requires_key():
    with pytest.raises(ValueError, match="LLM_GUARDRAIL_SECRET_KEY is required"):
        VaultlessPIIGuardrail("", "dummy")


def test_vaultless_guardrail_initialization_validates_key_length():
    with pytest.raises(ValueError, match="Key must be 32 bytes"):
        VaultlessPIIGuardrail("deadbeef", "dummy")


@patch("dspy.Predict.__call__")
def test_tokenize_replaces_pii_entities_with_deterministic_tokens(mock_predict, guardrail):
    mock_predict.return_value = FakePrediction("John Doe, 555-1234")

    raw_input = "My name is John Doe and my number is 555-1234."
    safe_input, token_map = guardrail.tokenize(raw_input)

    assert "John Doe" not in safe_input
    assert "555-1234" not in safe_input

    # Check that there are two distinct TOK- strings in the safe_input
    assert safe_input.count("TOK-") == 2

    # 2 tokens should be returned in the map
    assert len(token_map) == 2


@patch("dspy.Predict.__call__")
def test_tokenize_is_deterministic(mock_predict, guardrail):
    mock_predict.return_value = FakePrediction("Jane Doe")

    _raw1, map1 = guardrail.tokenize("Hello Jane Doe")
    _raw2, map2 = guardrail.tokenize("Goodbye Jane Doe")

    # Extract the token for Jane Doe
    token1 = next(iter(map1.keys()))
    token2 = next(iter(map2.keys()))

    assert token1 == token2


@patch("dspy.Predict.__call__")
def test_detokenize_reverses_tokens(mock_predict, guardrail):
    mock_predict.return_value = FakePrediction("Alice, 123 Main St")

    raw_input = "Alice lives at 123 Main St."
    safe_input, token_map = guardrail.tokenize(raw_input)

    assert "Alice" not in safe_input

    # Now detokenize
    cleartext = guardrail.detokenize(safe_input, token_map)
    assert cleartext == raw_input


def test_detokenize_ignores_invalid_tokens(guardrail):
    # A fake token that isn't encrypted by our key or lacks proper padding
    fake_token = "TOK-invalid_base64_payload_that_fails"
    safe_input = f"Contact at {fake_token}"

    cleartext = guardrail.detokenize(safe_input, {})
    assert cleartext == safe_input
