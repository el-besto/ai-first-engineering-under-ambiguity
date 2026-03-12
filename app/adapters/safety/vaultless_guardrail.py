import base64
import hashlib
import os
import re
from typing import Any

import dspy
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.adapters.safety.dspy_signatures import ExtractPII
from app.adapters.safety.protocol import PIIGuardrailAdapter
from app.infrastructure.telemetry.logger import get_logger, log_exception


class VaultlessPIIGuardrail(PIIGuardrailAdapter):
    """
    Production-grade Vaultless PII Guardrail.
    Uses DSPy to extract PII entities and AES-GCM to deterministically encrypt them
    into format-preserving tokens (TOK-...) to maintain referential integrity.
    """

    def __init__(
        self,
        secret_key_hex: str,
        compiled_model_path: str,
        api_base: str = "http://localhost:11434",
        api_key: str = "local-dev",
        model_name: str = "ollama/llama3.1:8b",
    ):
        self.logger = get_logger(__name__).bind(adapter=self.__class__.__name__)
        if not secret_key_hex:
            raise ValueError("LLM_GUARDRAIL_SECRET_KEY is required for VaultlessPIIGuardrail")

        # Initialize AES-GCM
        try:
            key = bytes.fromhex(secret_key_hex)
            if len(key) != 32:
                raise ValueError("Key must be 32 bytes (64 hex characters)")
        except ValueError as e:
            raise ValueError(f"Invalid LLM_GUARDRAIL_SECRET_KEY: {e}") from e

        self._aesgcm = AESGCM(key)

        # TODO: DEFERRED [015] Remove local DSPy configuration in VaultlessPIIGuardrail
        # once global threadpool issue in Streamlit is fixed
        # Explicitly configure DSPy locally inside this instance to survive ThreadPoolExecutor boundaries
        # that commonly bite Frameworks like Streamlit and LangGraph.
        lm = dspy.LM(model_name, api_base=api_base, api_key=api_key)
        dspy.settings.configure(lm=lm)

        # Load DSPy Extractor
        self._extractor = dspy.Predict(ExtractPII)
        if os.path.exists(compiled_model_path):
            self._extractor.load(compiled_model_path)

        self._token_prefix = "TOK-"
        self._token_pattern = re.compile(rf"{self._token_prefix}[A-Za-z0-9_\-]+")

    def _deterministic_encrypt(self, plaintext: str) -> str:
        # Create a deterministic 12-byte nonce by hashing the plaintext
        nonce = hashlib.sha256(plaintext.encode("utf-8")).digest()[:12]

        # Encrypt the plaintext
        ciphertext = self._aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

        payload = nonce + ciphertext
        encoded = base64.urlsafe_b64encode(payload).decode("utf-8").rstrip("=")
        return f"{self._token_prefix}{encoded}"

    def _decrypt(self, token: str) -> str:
        if not token.startswith(self._token_prefix):
            return token

        try:
            encoded = token[len(self._token_prefix) :]
            padding = "=" * (4 - (len(encoded) % 4))
            payload = base64.urlsafe_b64decode(encoded + padding)

            if len(payload) < 12:
                return token

            nonce = payload[:12]
            ciphertext = payload[12:]

            plaintext = self._aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode("utf-8")
        except Exception:
            return token

    def tokenize(self, raw_input: str) -> tuple[str, dict[str, Any]]:
        log = self.logger.bind(operation="tokenize")
        if not raw_input.strip():
            log.debug("completed", input_chars=0, token_count=0)
            return raw_input, {}

        log.info("started", input_chars=len(raw_input))
        try:
            # 1. Ask DSPy to extract PII.
            prediction = self._extractor(document=raw_input)
            pii_entities_str = prediction.pii_entities

            if not pii_entities_str:
                log.info("completed", token_count=0)
                return raw_input, {}

            # 2. Parse the comma-separated strings.
            entities = [e.strip() for e in pii_entities_str.split(",") if e.strip()]

            if not entities:
                log.info("completed", token_count=0)
                return raw_input, {}

            entities.sort(key=len, reverse=True)

            # 3. Encrypt and replace.
            safe_input = raw_input
            token_map = {}

            for entity in entities:
                if len(entity) < 2:
                    continue

                token = self._deterministic_encrypt(entity)
                safe_input = safe_input.replace(entity, token)
                token_map[token] = entity

            log.info("completed", token_count=len(token_map))
            return safe_input, token_map
        except Exception as e:
            log_exception(log, "failed", e, input_chars=len(raw_input))
            raise

    def detokenize(self, safe_input: str, token_map: dict[str, Any]) -> str:
        log = self.logger.bind(operation="detokenize")
        tokens = self._token_pattern.findall(safe_input)

        cleartext = safe_input
        for token in set(tokens):
            decrypted = self._decrypt(token)
            if decrypted != token:
                cleartext = cleartext.replace(token, decrypted)

        log.debug("completed", token_count=len(tokens))
        return cleartext
