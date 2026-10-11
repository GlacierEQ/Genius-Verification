"""Evidence-bound verification primitives for Genius-Verification."""
from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OperationReceipt:
    """Immutable, hash-bound receipt for a verified operation."""

    operation_id: str
    operator: str
    action: str
    result: str
    timestamp: float = field(default_factory=time.time)
    previous_sha256: str | None = None

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "operation_id": self.operation_id,
            "operator": self.operator,
            "previous_sha256": self.previous_sha256,
            "result": self.result,
            "timestamp": self.timestamp,
        }

    @property
    def sha256(self) -> str:
        raw = json.dumps(
            self.canonical_payload(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @property
    def short_hash(self) -> str:
        return self.sha256[:12]


class ContractEnforcer:
    """Enforce action preconditions and preserve a cryptographically linked receipt chain."""

    def __init__(self) -> None:
        self._receipts: list[OperationReceipt] = []
        self._preconditions: dict[str, Callable[[Any], bool]] = {}

    def register_precondition(self, action: str, check: Callable[[Any], bool]) -> None:
        action = str(action).strip()
        if not action:
            raise ValueError("action must be non-empty")
        if not callable(check):
            raise TypeError("precondition check must be callable")
        self._preconditions[action] = check

    def execute(
        self,
        operation_id: str,
        operator: str,
        action: str,
        context: Any = None,
    ) -> OperationReceipt:
        operation_id = str(operation_id).strip()
        operator = str(operator).strip()
        action = str(action).strip()
        if not operation_id:
            raise ValueError("operation_id must be non-empty")
        if not operator:
            raise ValueError("operator must be non-empty")
        if not action:
            raise ValueError("action must be non-empty")

        check = self._preconditions.get(action)
        if check is not None and not check(context):
            raise ValueError(f"Precondition failed for {action}")

        previous = self._receipts[-1].sha256 if self._receipts else None
        receipt = OperationReceipt(
            operation_id=operation_id,
            operator=operator,
            action=action,
            result="COMPLETED",
            previous_sha256=previous,
        )
        self._receipts.append(receipt)
        return receipt

    @property
    def receipt_chain(self) -> list[OperationReceipt]:
        return list(self._receipts)

    def verify_chain_integrity(self) -> bool:
        previous_hash: str | None = None
        previous_timestamp: float | None = None
        for receipt in self._receipts:
            if receipt.previous_sha256 != previous_hash:
                return False
            if previous_timestamp is not None and receipt.timestamp < previous_timestamp:
                return False
            previous_hash = receipt.sha256
            previous_timestamp = receipt.timestamp
        return True
