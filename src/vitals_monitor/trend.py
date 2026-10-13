"""Trend checks over a series of values."""
from __future__ import annotations


def rolling_average(values: list[float], window: int) -> list[float]:
    """Return the average of each full window of consecutive values."""
    if window < 1:
        raise ValueError("window must be at least 1")
    return [
        sum(values[i : i + window]) / window for i in range(len(values) - window + 1)
    ]


def sustained_decline(values: list[float], window: int = 3, min_drop: float = 2.0) -> bool:
    """Return True if the latest window averages at least min_drop below the one before.

    At least two full windows of values are needed. With fewer, the answer is False.
    """
    if len(values) < 2 * window:
        return False
    latest = sum(values[-window:]) / window
    previous = sum(values[-2 * window : -window]) / window
    return (previous - latest) >= min_drop
