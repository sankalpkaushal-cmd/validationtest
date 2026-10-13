"""Alert thresholds, with defaults and a JSON loader."""
from __future__ import annotations

import json
from dataclasses import dataclass

from .models import VALID_PARAMETERS

INF = float("inf")


@dataclass(frozen=True)
class Band:
    """Limits for one parameter.

    The limits must be in order: critical_low <= warning_low <=
    warning_high <= critical_high. Use infinity for a side with no limit.
    """

    warning_low: float
    critical_low: float
    warning_high: float
    critical_high: float

    def __post_init__(self) -> None:
        if not (
            self.critical_low <= self.warning_low <= self.warning_high <= self.critical_high
        ):
            raise ValueError("thresholds are out of order")


DEFAULT_THRESHOLDS = {
    "heart_rate": Band(warning_low=50, critical_low=40, warning_high=110, critical_high=130),
    "spo2": Band(warning_low=94, critical_low=90, warning_high=INF, critical_high=INF),
    "resp_rate": Band(warning_low=10, critical_low=8, warning_high=22, critical_high=28),
    "temp_c": Band(warning_low=36.0, critical_low=35.0, warning_high=38.0, critical_high=39.5),
}


def load_thresholds(path: str) -> dict[str, Band]:
    """Load thresholds from a JSON file.

    Parameters missing from the file keep their default limits. A parameter
    that is not recognized, or limits that are out of order, raise ValueError.
    """
    with open(path, encoding="utf-8") as handle:
        raw = json.load(handle)

    thresholds = dict(DEFAULT_THRESHOLDS)
    for parameter, limits in raw.items():
        if parameter not in VALID_PARAMETERS:
            raise ValueError(f"unknown parameter: {parameter}")
        merged = {**_as_dict(DEFAULT_THRESHOLDS[parameter]), **limits}
        thresholds[parameter] = Band(**merged)
    return thresholds


def _as_dict(band: Band) -> dict[str, float]:
    return {
        "warning_low": band.warning_low,
        "critical_low": band.critical_low,
        "warning_high": band.warning_high,
        "critical_high": band.critical_high,
    }
