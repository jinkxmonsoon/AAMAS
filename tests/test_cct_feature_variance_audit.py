import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = ROOT / "scripts/audit_cct_feature_variance.py"


def _load_audit_module():
    spec = importlib.util.spec_from_file_location("audit_cct_feature_variance", AUDIT_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_cct_feature_variance_audit_reports_descriptive_warnings():
    subprocess.run([sys.executable, "scripts/build_cct_graphs_full_trace.py"], cwd=ROOT, check=True)
    module = _load_audit_module()

    audit = module.audit_feature_variance()
    module.write_reports(audit)

    assert audit["feature_row_count"] == 2100
    assert "output_token_count" in audit["high_variance_features"]
    assert "feature_schema_version" in audit["constant_features"]
    assert audit["graph_count_summary"]["node_count_unique"] == [5]
    assert audit["graph_count_summary"]["edge_count_unique"] == [12]
    assert audit["readiness_decision"] == "ready_with_shortcut_warnings"
    assert not audit["blocker_reasons"]
    assert (ROOT / "results/reports/journal_v1_full_trace_cct/cct_feature_variance_report.md").is_file()
    assert (ROOT / "results/reports/journal_v1_full_trace_cct/cct_structural_shortcut_risk_report.md").is_file()
    assert (ROOT / "results/reports/journal_v1_full_trace_cct/cct_feature_readiness_gate.md").is_file()
