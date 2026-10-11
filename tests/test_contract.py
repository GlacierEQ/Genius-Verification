import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_identity_contract_file_exists():
    assert (ROOT / "GENIUS.yaml").is_file()


def test_validator_passes_on_repository_root():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_composition_exports_verified_receipt_and_counterevidence_capabilities():
    data = yaml.safe_load(
        (ROOT / "interfaces" / "COMPOSITION.yaml").read_text(encoding="utf-8")
    )
    provided = {item["id"]: item for item in data["provides"]}
    receipt = provided["verification.evidence.receipt"]
    counterevidence = provided["verification.counterevidence.first-class"]

    assert receipt["stage"] == "verified"
    assert receipt["interface"] == "src/genius_verification/core.py"
    assert receipt["evidence_refs"]
    assert counterevidence["stage"] == "verified"
    assert counterevidence["evidence_refs"]


def test_github_ci_executes_runtime_verification_suite():
    workflow = (
        ROOT / ".github" / "workflows" / "validate.yml"
    ).read_text(encoding="utf-8")
    assert "pytest" in workflow
    assert "python -m compileall" in workflow
    assert "python tools/validate.py ." in workflow


def test_all_github_ci_paths_install_required_dependencies():
    for name in ["ci.yml", "validate.yml"]:
        workflow = (
            ROOT / ".github" / "workflows" / name
        ).read_text(encoding="utf-8")
        assert "pyyaml" in workflow.casefold()
        assert "pytest" in workflow.casefold()
        assert "python -m compileall" in workflow
