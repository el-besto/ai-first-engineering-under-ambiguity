from types import SimpleNamespace

from app.adapters.safety.dspy_signatures import pii_metric


def test_pii_metric_perfect_recall():
    example = SimpleNamespace(pii_entities="John Doe, 01/15/2026")
    pred = SimpleNamespace(pii_entities="John Doe, 01/15/2026")
    assert pii_metric(example, pred) == 1.0


def test_pii_metric_partial_false_positives():
    example = SimpleNamespace(pii_entities="John Doe")
    pred = SimpleNamespace(pii_entities="John Doe, Jane Doe")
    assert pii_metric(example, pred) == 1.0


def test_pii_metric_missing_entity_penalized():
    example = SimpleNamespace(pii_entities="John Doe, 01/15/2026")
    pred = SimpleNamespace(pii_entities="John Doe")
    assert pii_metric(example, pred) == 0.0


def test_pii_metric_no_ground_truth_no_prediction():
    example = SimpleNamespace(pii_entities="")
    pred = SimpleNamespace(pii_entities="")
    assert pii_metric(example, pred) == 1.0


def test_pii_metric_no_ground_truth_with_hallucinated_prediction():
    example = SimpleNamespace(pii_entities="")
    pred = SimpleNamespace(pii_entities="John Doe")
    assert pii_metric(example, pred) == 0.5


def test_pii_metric_empty_string_handling():
    example = SimpleNamespace(pii_entities=" ")
    pred = SimpleNamespace(pii_entities=" ")
    assert pii_metric(example, pred) == 1.0
