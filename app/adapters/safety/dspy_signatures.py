import dspy


class ExtractPII(dspy.Signature):
    """
    You are an enterprise Vaultless PII Guardrail. Your goal is to identify and extract all Personally
    Identifiable Information (PII) and sensitive entities from the document text.

    Process Steps:
    1. Read the document text carefully.
    2. Identify sensitive entities: names, SSNs, financial accounts, dates of birth, phone numbers, emails.
    3. Return them exactly as they appear in the text, as a comma-separated list.

    Decision Rules:
    - If no PII is found, return an empty string.
    - Do NOT rephrase names or dates. Use exact string matches.
    """

    document = dspy.InputField(
        desc="Extract all Personally Identifiable Information (PII) from the input document. "
        "Return a comma-separated list of the exact substrings that represent sensitive entities "
        "(e.g., names, specific company names, SSNs, financial accounts, dates of birth)."
    )
    pii_entities = dspy.OutputField(
        desc="Comma-separated list of exact string matches of sensitive entities "
        "(e.g., names, specific company names, SSNs, financial accounts, dates of birth)."
    )


def pii_metric(example, pred, trace=None):
    # Parse the comma-separated strings into cleaned lists
    true_entities = [e.strip().lower() for e in example.pii_entities.split(",") if e.strip()]
    pred_entities = [e.strip().lower() for e in pred.pii_entities.split(",") if e.strip()]

    if not true_entities:
        return 1.0 if not pred_entities else 0.5  # Give partial credit if it hallucinates PII when there is none

    # Calculate True Positives
    true_positives = 0
    for true_ent in true_entities:
        if any(true_ent in pred_ent for pred_ent in pred_entities):
            true_positives += 1

    # Calculate Recall
    recall = true_positives / len(true_entities)

    # Penalize heavily for missing ANY entity (strict security guardrail)
    if recall < 1.0:
        return 0.0  # Return 0 so the optimizer learns missing PII is unacceptable

    return 1.0  # Perfect recall
