"""Data models for readings and alerts."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

VALID_PARAMETERS = ("heart_rate", "spo2", "resp_rate", "temp_c")


@dataclass(frozen=True)
class Reading:
    """One measurement for one patient.

    A reading is rejected if the patient ID is empty, the parameter is not
    one of VALID_PARAMETERS, or the value is not a number.
    """

    patient_id: str
    timestamp: datetime
    parameter: str
    value: float

    def __post_init__(self) -> None:
        if not self.patient_id:
            raise ValueError("patient_id is required")
        if self.parameter not in VALID_PARAMETERS:
            raise ValueError(f"unknown parameter: {self.parameter}")
        if self.value != self.value:  # NaN is the only value not equal to itself
            raise ValueError("value must be a number")


@dataclass(frozen=True)
class Alert:
    """An alert raised for a reading. Severity is 'warning' or 'critical'."""

    patient_id: str
    timestamp: datetime
    parameter: str
    severity: str
    message: str
