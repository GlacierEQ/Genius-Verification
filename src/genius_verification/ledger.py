from __future__ import annotations

import json
from pathlib import Path

from .core import OperationReceipt


class AuditLedger:
    def __init__(self) -> None:
        self._entries: list[OperationReceipt] = []

    def append(self, receipt: OperationReceipt) -> int:
        if self._entries:
            expected_prev = self._entries[-1].sha256
            if receipt.previous_sha256 != expected_prev:
                raise ValueError(
                    f"Receipt previous_sha256 mismatch: expected {expected_prev}, got {receipt.previous_sha256}"
                )
        elif receipt.previous_sha256 is not None:
            raise ValueError(f"Initial receipt must have previous_sha256=None, got {receipt.previous_sha256}")
        self._entries.append(receipt)
        return len(self._entries)

    def verify_integrity(self) -> tuple[bool, int | None, str | None]:
        if not self._entries:
            return True, None, None

        prev_hash: str | None = None
        for idx, item in enumerate(self._entries):
            if item.previous_sha256 != prev_hash:
                return False, idx, f"Hash link broken at index {idx}: expected {prev_hash}, got {item.previous_sha256}"
            prev_hash = item.sha256
        return True, None, None

    def export_jsonl(self, file_path: str | Path) -> int:
        p = Path(file_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with open(p, "w", encoding="utf-8") as f:
            for entry in self._entries:
                payload = entry.canonical_payload()
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
                count += 1
        return count

    @classmethod
    def import_jsonl(cls, file_path: str | Path) -> AuditLedger:
        ledger = cls()
        p = Path(file_path)
        if not p.is_file():
            raise FileNotFoundError(f"Ledger file not found: {file_path}")
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                receipt = OperationReceipt(
                    operation_id=data["operation_id"],
                    operator=data["operator"],
                    action=data["action"],
                    result=data["result"],
                    timestamp=data["timestamp"],
                    previous_sha256=data.get("previous_sha256"),
                )
                ledger.append(receipt)
        return ledger

    def __len__(self) -> int:
        return len(self._entries)

    def __getitem__(self, idx: int) -> OperationReceipt:
        return self._entries[idx]
