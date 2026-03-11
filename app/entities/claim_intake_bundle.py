from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ClaimIntakeBundle:
    case_id: str
    documents: Mapping[str, str]

    @classmethod
    def load_from_fixture(cls, case_id: str, fixture_dir: Path) -> "ClaimIntakeBundle":
        docs = {}
        if fixture_dir.exists():
            for file_path in fixture_dir.iterdir():
                if file_path.is_file() and not file_path.name.startswith("."):
                    docs[file_path.stem.upper()] = file_path.read_text()
        return cls(case_id=case_id, documents=docs)

    @classmethod
    def _get_base_fixture_dir(cls) -> Path:
        return Path(__file__).parent.parent.parent / "tests" / "acceptance" / "fixtures" / "death_claim"

    @classmethod
    def fake_complete(cls) -> "ClaimIntakeBundle":
        return cls.load_from_fixture("CASE_A_COMPLETE", cls._get_base_fixture_dir() / "case_a_complete")

    @classmethod
    def fake_missing_information(cls) -> "ClaimIntakeBundle":
        return cls.load_from_fixture("CASE_B_MISSING", cls._get_base_fixture_dir() / "case_b_missing_information")

    @classmethod
    def fake_ambiguous(cls) -> "ClaimIntakeBundle":
        return cls.load_from_fixture("CASE_C_AMBIGUOUS", cls._get_base_fixture_dir() / "case_c_ambiguous")
