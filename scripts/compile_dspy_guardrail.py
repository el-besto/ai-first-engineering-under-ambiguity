import dspy
from dspy.teleprompt import BootstrapFewShot

from app.adapters.safety.dspy_signatures import ExtractPII, pii_metric


def main():
    # Configure DSPy to use the local Ollama instance
    lm = dspy.LM("ollama_chat/llama3.1:8b", api_base="http://localhost:11434", api_key="")
    dspy.settings.configure(lm=lm)

    # 1. Define your training data (Ground Truth)
    # TODO: DEFERRED - Training Data Size - Provide a much larger and more representative
    # dataset of industry-specific PII examples during hardening.
    raw_data = [
        {
            "document": "John Doe passed away on 01/15/2026. The beneficiary is Jane Doe. Policy #123456789.",
            "pii_entities": "John Doe, 01/15/2026, Jane Doe, 123456789",
        },
        {
            "document": "My son, Robert Smith, died from a heart attack. Please contact me at 555-0198.",
            "pii_entities": "Robert Smith, 555-0198",
        },
        {
            "document": "I am writing to report the passing of Mary Johnson (DOB 11/20/1950) on October 4th.",
            "pii_entities": "Mary Johnson, 11/20/1950, October 4th",
        },
        {
            "document": "Policy owner William Blake. Email wblake@example.com for info.",
            "pii_entities": "William Blake, wblake@example.com",
        },
        {
            "document": "The deceased had no known relatives. Name is unknown.",
            "pii_entities": "",
        },
        {
            "document": "Please send the funds to account number 9876543210 at Chase Bank.",
            "pii_entities": "9876543210, Chase Bank",
        },
    ]

    # 2. Convert to DSPy Examples
    dataset = [
        dspy.Example(document=item["document"], pii_entities=item["pii_entities"]).with_inputs("document")
        for item in raw_data
    ]

    # 3. Set up and run the Optimizer
    base_extractor = dspy.Predict(ExtractPII)

    teleprompter = BootstrapFewShot(metric=pii_metric, max_bootstrapped_demos=2, max_labeled_demos=2)

    # 4. Compile the optimized module
    print("Starting compilation. This will prompt the local SLM to optimize the prompt...")
    compiled_extractor = teleprompter.compile(student=base_extractor, trainset=dataset)

    import os

    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "app", "adapters", "safety", "compiled_pii_extractor.json"
    )
    compiled_extractor.save(output_path)
    print(f"Compilation complete! Saved to {output_path}")


if __name__ == "__main__":
    main()
