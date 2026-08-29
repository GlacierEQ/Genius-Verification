from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_identity_contract_file_exists():
    assert (ROOT / "GENIUS.yaml").is_file()


def test_validator_passes_on_repository_root():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
