import time

from genius_verification import (
    AuditLedger,
    ContractSchemaValidator,
    OperationReceipt,
    ReceiptSigner,
)


def test_crypto_signing_and_verification():
    signer = ReceiptSigner.from_single_key(b"test_secret_key_12345", key_id="v1")
    receipt = OperationReceipt(
        operation_id="op-101",
        operator="apex_engine",
        action="VERIFY_STATE",
        result="PASS",
    )
    sig = signer.sign_receipt(receipt)
    assert sig.startswith("v1:")
    assert signer.verify_signature(receipt, sig) is True

    # Tampered signature
    assert signer.verify_signature(receipt, "v1:badsignature") is False

    # Key rotation support
    multi_signer = ReceiptSigner(
        {"v1": b"old_secret", "v2": b"new_secret"}, active_key_id="v2"
    )
    sig2 = multi_signer.sign_receipt(receipt)
    assert sig2.startswith("v2:")
    assert multi_signer.verify_signature(receipt, sig2) is True


def test_freshness_check():
    signer = ReceiptSigner.from_single_key(b"secret")
    receipt = OperationReceipt(
        operation_id="op-fresh",
        operator="apex",
        action="CHECK",
        result="OK",
        timestamp=time.time() - 5.0,
    )
    assert signer.verify_freshness(receipt, max_age_seconds=10.0) is True
    assert signer.verify_freshness(receipt, max_age_seconds=2.0) is False


def test_audit_ledger_chain_and_persistence(tmp_path):
    ledger = AuditLedger()
    r1 = OperationReceipt("op-1", "user", "init", "OK", previous_sha256=None)
    ledger.append(r1)
    r2 = OperationReceipt("op-2", "user", "step", "OK", previous_sha256=r1.sha256)
    ledger.append(r2)

    valid, idx, _err = ledger.verify_integrity()
    assert valid is True
    assert idx is None

    # Export and import
    export_file = tmp_path / "ledger.jsonl"
    count = ledger.export_jsonl(export_file)
    assert count == 2

    imported = AuditLedger.import_jsonl(export_file)
    assert len(imported) == 2
    assert imported[0].sha256 == r1.sha256
    assert imported[1].sha256 == r2.sha256


def test_schema_validator_semver():
    assert ContractSchemaValidator.is_valid_semver("1.0.0") is True
    assert ContractSchemaValidator.is_valid_semver("2.1.3-beta.1") is True
    assert ContractSchemaValidator.is_valid_semver("invalid-semver") is False


def test_schema_validator_manifest():
    valid_manifest = {
        "name": "genius-foundry",
        "version": "1.0.0",
        "capabilities": ["codegen", "verify"],
    }
    ok, errs = ContractSchemaValidator.validate_capability_manifest(valid_manifest)
    assert ok is True
    assert len(errs) == 0

    bad_manifest = {"name": "incomplete"}
    ok, errs = ContractSchemaValidator.validate_capability_manifest(bad_manifest)
    assert ok is False
    assert len(errs) >= 2


def test_dependency_cycle_detection():
    acyclic_graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    has_cycle, _ = ContractSchemaValidator.detect_dependency_cycles(acyclic_graph)
    assert has_cycle is False

    cyclic_graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
    }
    has_cycle, path = ContractSchemaValidator.detect_dependency_cycles(cyclic_graph)
    assert has_cycle is True
    assert path is not None
