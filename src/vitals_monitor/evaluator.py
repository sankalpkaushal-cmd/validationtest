"""Classify readings against thresholds and raise alerts."""
from __future__ import annotations

from .models import Alert, Reading
from .thresholds import DEFAULT_THRESHOLDS, Band


def classify(value: float, band: Band) -> str | None:
    """Return 'critical', 'warning' or None for a value and its limits."""
    if value <= band.critical_low or value >= band.critical_high:
        return "critical"
    if value < band.warning_low or value > band.warning_high:
        return "warning"
    return None


def evaluate(reading: Reading, thresholds: dict[str, Band] | None = None) -> Alert | None:
    """Return an alert for a reading, or None if the reading is normal."""
    limits = thresholds or DEFAULT_THRESHOLDS
    severity = classify(reading.value, limits[reading.parameter])
    if severity is None:
        return None
    return Alert(
        patient_id=reading.patient_id,
        timestamp=reading.timestamp,
        parameter=reading.parameter,
        severity=severity,
        message=f"{reading.parameter} {reading.value:g} is {severity}",
    )


def evaluate_all(
    readings: list[Reading], thresholds: dict[str, Band] | None = None
) -> list[Alert]:
    """Evaluate every reading and return the alerts, in input order."""
    alerts = []
    for reading in readings:
        alert = evaluate(reading, thresholds)
        if alert is not None:
            alerts.append(alert)
    return alerts
