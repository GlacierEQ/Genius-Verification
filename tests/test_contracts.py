"""Auto-generated tests for Autonomous Systems Engineering."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from genius_verification.core import ContractEnforcer, OperationReceipt


def test_receipt_hash():
    r = OperationReceipt("op1", "agent", "DEPLOY", "OK")
    assert len(r.sha256) == 64
    assert len(r.short_hash) == 12

def test_enforcer_execute():
    ce = ContractEnforcer()
    receipt = ce.execute("op1", "agent", "BUILD")
    assert receipt.result == "COMPLETED"
    assert len(ce.receipt_chain) == 1

def test_enforcer_precondition_pass():
    ce = ContractEnforcer()
    ce.register_precondition("DEPLOY", lambda ctx: ctx == "ready")
    receipt = ce.execute("op1", "agent", "DEPLOY", context="ready")
    assert receipt.result == "COMPLETED"

def test_enforcer_precondition_fail():
    ce = ContractEnforcer()
    ce.register_precondition("DEPLOY", lambda ctx: ctx == "ready")
    import pytest
    with pytest.raises(ValueError):
        ce.execute("op1", "agent", "DEPLOY", context="not_ready")

def test_chain_integrity():
    ce = ContractEnforcer()
    ce.execute("op1", "a", "STEP1")
    ce.execute("op2", "a", "STEP2")
    assert ce.verify_chain_integrity()

def test_receipt_deterministic():
    r1 = OperationReceipt("op1", "a", "X", "OK", timestamp=1000.0)
    r2 = OperationReceipt("op1", "a", "X", "OK", timestamp=1000.0)
    assert r1.sha256 == r2.sha256


def test_receipt_hash_binds_payload_not_literal_template():
    a = OperationReceipt("op1", "agent", "DEPLOY", "OK", timestamp=1000.0)
    b = OperationReceipt("op2", "agent", "DEPLOY", "OK", timestamp=1000.0)
    c = OperationReceipt("op1", "other", "DEPLOY", "OK", timestamp=1000.0)
    assert a.sha256 != b.sha256
    assert a.sha256 != c.sha256

def test_precondition_failure_names_actual_action():
    ce = ContractEnforcer()
    ce.register_precondition("DEPLOY", lambda _: False)
    import pytest
    with pytest.raises(ValueError, match="Precondition failed for DEPLOY"):
        ce.execute("op1", "agent", "DEPLOY")

def test_receipt_chain_is_cryptographically_linked():
    ce = ContractEnforcer()
    first = ce.execute("op1", "a", "STEP1")
    second = ce.execute("op2", "a", "STEP2")
    assert first.previous_sha256 is None
    assert second.previous_sha256 == first.sha256
    assert ce.verify_chain_integrity()
