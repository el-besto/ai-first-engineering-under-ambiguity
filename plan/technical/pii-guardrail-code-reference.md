# Enterprise AI PII Guardrail - Reference Code

This document contains the core DSPy signatures, evaluation metrics, and Vaultless Python classes required to build the PII guardrail securely.

---

## 1. The DSPy Extraction Signature

This signature defines the exact input and output expectations for the local Small Language Model (SLM), instructing it to extract precise strings without altering the document.

```python
import dspy

class ExtractPII(dspy.Signature):
    """Identify and extract all Personally Identifiable Information (PII) and sensitive entities from the text. Return them as a comma-separated list."""

    document = dspy.InputField(desc="The source document snippet.")
    pii_entities = dspy.OutputField(desc="Comma-separated list of exact string matches of sensitive entities (e.g., names, specific company names, SSNs, financial accounts, dates of birth).")
```

---

## 2. The Custom Evaluation Metric (Recall Optimization)

This metric is used by the DSPy teleprompter during the compilation phase to strictly penalize the model for missing any ground-truth PII (false negatives) while being more forgiving of false positives.

```python
def pii_metric(example, pred, trace=None):
    # Parse the comma-separated strings into cleaned lists
    true_entities = [e.strip().lower() for e in example.pii_entities.split(',')]
    pred_entities = [e.strip().lower() for e in pred.pii_entities.split(',')]

    if not true_entities or true_entities == ['']:
        return 1.0 if not pred_entities else 0.5 # Give partial credit if it hallucinates PII when there is none

    # Calculate True Positives
    true_positives = 0
    for true_ent in true_entities:
        if any(true_ent in pred_ent for pred_ent in pred_entities):
            true_positives += 1

    # Calculate Recall
    recall = true_positives / len(true_entities)

    # Penalize heavily for missing ANY entity (strict security guardrail)
    if recall < 1.0:
        return 0.0 # Return 0 so the optimizer learns missing PII is unacceptable

    return 1.0 # Perfect recall
```

---

## 3. The DSPy Optimizer Compilation Script

This pattern takes your examples, runs the `pii_metric`, and uses `BootstrapFewShot` to bake the optimal instructions into your local SLM.

```python
import dspy
from dspy.teleprompt import BootstrapFewShot

# 1. Define your training data (Ground Truth)
raw_data = [
    {"document": "John Doe passed away on 01/15/2026. The beneficiary is Jane Doe.", "pii_entities": "John Doe, 01/15/2026, Jane Doe"},
    {"document": "Policy #123456789. Cause of death was myocardial infarction.", "pii_entities": "123456789"}
]

# 2. Convert to DSPy Examples
dataset = [
    dspy.Example(document=item["document"], pii_entities=item["pii_entities"]).with_inputs("document")
    for item in raw_data
]
trainset = dataset

# 3. Set up and run the Optimizer
base_extractor = dspy.Predict(ExtractPII)

teleprompter = BootstrapFewShot(
    metric=pii_metric,
    max_bootstrapped_demos=2,
    max_labeled_demos=2
)

# 4. Compile the optimized module
compiled_extractor = teleprompter.compile(student=base_extractor, trainset=trainset)
compiled_extractor.save("compiled_pii_extractor.json")
```

---

## 4. The Vaultless (Format-Preserving Encryption) Guardrail

This production-grade class uses AES-GCM to deterministically encrypt PII into URL-safe base64 tokens.

```python
import base64
import hashlib
import re
import dspy
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class VaultlessPIIGuardrail:
    def __init__(self, hex_secret_key: str, compiled_extractor: dspy.Module):
        # 32 bytes for AES-256
        key_bytes = bytes.fromhex(hex_secret_key)
        self.aesgcm = AESGCM(key_bytes)

        # Your optimized DSPy extractor
        self.extractor = compiled_extractor

    def _deterministic_encrypt(self, plaintext: str) -> str:
        """Encrypts PII so the same input always yields the same token."""
        data = plaintext.encode('utf-8')
        nonce = hashlib.sha256(data).digest()[:12]
        ciphertext = self.aesgcm.encrypt(nonce, data, None)
        token_bytes = base64.urlsafe_b64encode(nonce + ciphertext)
        return f"TOK-{token_bytes.decode('utf-8').rstrip('=')}"

    def _decrypt(self, token: str) -> str:
        """Mathematically reverses the token back to original PII."""
        try:
            raw_token = token.replace("TOK-", "")
            padding = '=' * (4 - (len(raw_token) % 4))
            decoded = base64.urlsafe_b64decode(raw_token + padding)

            nonce = decoded[:12]
            ciphertext = decoded[12:]

            plaintext = self.aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode('utf-8')
        except Exception:
            return token

    def anonymize(self, text: str):
        """Replaces PII with mathematical tokens."""
        prediction = self.extractor(document=text)
        entities = [e.strip() for e in prediction.pii_entities.split(',')]

        safe_text = text
        for entity in entities:
            if entity and entity in text:
                token = self._deterministic_encrypt(entity)
                safe_text = safe_text.replace(entity, token)

        return safe_text

    def de_anonymize(self, agent_output: str):
        """Scans the LLM output for tokens and decrypts them."""
        tokens_found = set(re.findall(r"TOK-[a-zA-Z0-9_\-]+", agent_output))

        clear_text = agent_output
        for token in tokens_found:
            original_entity = self._decrypt(token)
            clear_text = clear_text.replace(token, original_entity)

        return clear_text
```
