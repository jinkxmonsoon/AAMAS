from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_corpus_plan_keys_and_counts_present() -> None:
    text = (ROOT / "configs/corpus_plan.yaml").read_text(encoding="utf-8")
    for key in [
        "dataset_version: BRACIS-Journal-v1",
        "scenario_group_count: 7",
        "clean_cases_per_group: 12",
        "total_clean_cases: 84",
        "total_perturbation_variants: 336",
        "total_main_controlled_traces: 420",
    ]:
        assert key in text


def test_label_rubric_sections_present() -> None:
    text = (ROOT / "configs/label_rubric.yaml").read_text(encoding="utf-8")
    for key in ["label_semantics:", "label_provenance_fields:", "anti_leakage_rules:", "acceptance_criteria:"]:
        assert key in text
