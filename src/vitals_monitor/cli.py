"""Command-line entry point: read a CSV of readings and print alerts."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime

from .audit import AuditLog
from .evaluator import evaluate_all
from .models import Reading
from .thresholds import DEFAULT_THRESHOLDS, load_thresholds


def read_readings(path: str) -> list[Reading]:
    """Read readings from a CSV with columns patient_id, timestamp, parameter, value."""
    readings = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            readings.append(
                Reading(
                    patient_id=row["patient_id"],
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    parameter=row["parameter"],
                    value=float(row["value"]),
                )
            )
    return readings


def main(argv: list[str] | None = None) -> int:
    """Run the tool. Return 0 for no alerts, 1 for warnings, 2 for critical alerts."""
    parser = argparse.ArgumentParser(description="Check vital-sign readings against thresholds.")
    parser.add_argument("readings", help="CSV file of readings")
    parser.add_argument("--thresholds", help="JSON file that overrides default thresholds")
    args = parser.parse_args(argv)

    thresholds = load_thresholds(args.thresholds) if args.thresholds else DEFAULT_THRESHOLDS
    alerts = evaluate_all(read_readings(args.readings), thresholds)

    log = AuditLog()
    for alert in alerts:
        print(f"{alert.severity.upper():8} {alert.patient_id} {alert.message}")
        log.append({"patient_id": alert.patient_id, "message": alert.message,
                    "severity": alert.severity})

    if any(a.severity == "critical" for a in alerts):
        return 2
    return 1 if alerts else 0


if __name__ == "__main__":
    raise SystemExit(main())
