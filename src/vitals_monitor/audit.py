"""Tamper-evident audit log. Each entry is chained to the one before it."""
from __future__ import annotations

import hashlib
import json

GENESIS = "0" * 64


class AuditLog:
    """An append-only list of events, linked by SHA-256 hashes."""

    def __init__(self) -> None:
        self._entries: list[dict] = []

    def append(self, event: dict) -> str:
        """Add an event and return its hash."""
        previous = self._entries[-1]["hash"] if self._entries else GENESIS
        digest = self._digest(previous, event)
        self._entries.append({"event": event, "previous": previous, "hash": digest})
        return digest

    def verify(self) -> bool:
        """Return True if no entry has been changed, removed or reordered."""
        previous = GENESIS
        for entry in self._entries:
            if entry["previous"] != previous:
                return False
            if entry["hash"] != self._digest(previous, entry["event"]):
                return False
            previous = entry["hash"]
        return True

    def __len__(self) -> int:
        return len(self._entries)

    @staticmethod
    def _digest(previous: str, event: dict) -> str:
        body = json.dumps(event, sort_keys=True, default=str)
        return hashlib.sha256((previous + body).encode("utf-8")).hexdigest()
