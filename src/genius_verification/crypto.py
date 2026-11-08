from __future__ import annotations

import hashlib
import hmac
import time

from .core import OperationReceipt


class ReceiptSigner:
    def __init__(self, secret_keys: dict[str, bytes], active_key_id: str) -> None:
        if not secret_keys:
            raise ValueError("secret_keys must not be empty")
        if active_key_id not in secret_keys:
            raise ValueError(f"active_key_id {active_key_id} not found in secret_keys")
        self._keys = dict(secret_keys)
        self._active_key_id = active_key_id

    @classmethod
    def from_single_key(cls, key: bytes, key_id: str = "k1") -> ReceiptSigner:
        return cls({key_id: key}, active_key_id=key_id)

    def sign_receipt(self, receipt: OperationReceipt) -> str:
        key = self._keys[self._active_key_id]
        digest = hmac.new(key, receipt.sha256.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"{self._active_key_id}:{digest}"

    def verify_signature(self, receipt: OperationReceipt, signature: str) -> bool:
        if ":" not in signature:
            return False
        key_id, sig = signature.split(":", 1)
        key = self._keys.get(key_id)
        if key is None:
            return False
        expected = hmac.new(key, receipt.sha256.encode("utf-8"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected)

    def verify_freshness(self, receipt: OperationReceipt, max_age_seconds: float) -> bool:
        age = time.time() - receipt.timestamp
        return 0 <= age <= max_age_seconds
