# Vitals Monitor (demo)

A small Python library and command-line tool that checks patient vital-sign readings against alert thresholds. It is a demonstration project for practicing with Ketryx. It is not a medical device and must not be used for clinical decisions.

## What it does

- Reads vital-sign readings (heart rate, SpO2, respiratory rate, temperature) from a CSV file.
- Rejects readings with a missing patient ID, an unknown parameter or a non-numeric value.
- Compares each reading with warning and critical thresholds and raises an alert.
- Lets thresholds be changed through a JSON file, and rejects files whose limits are out of order.
- Detects a sustained decline in a parameter over a rolling window of readings.
- Records every alert in a tamper-evident audit log, where each entry is chained to the one before it.
- Returns an exit code from the command line: 0 for no alerts, 1 for warnings, 2 for critical alerts.

## Layout

| Path | Purpose |
|---|---|
| `src/vitals_monitor/models.py` | Reading and alert data classes, with input validation |
| `src/vitals_monitor/thresholds.py` | Default thresholds and the JSON loader |
| `src/vitals_monitor/evaluator.py` | Classifies a reading as normal, warning or critical |
| `src/vitals_monitor/trend.py` | Rolling average and sustained decline check |
| `src/vitals_monitor/audit.py` | Hash-chained audit log |
| `src/vitals_monitor/cli.py` | Command-line entry point |
| `tests/` | Automated tests (pytest) |
| `data/sample_readings.csv` | Example input |

## Run it

    pip install -r requirements.txt
    pytest
    python -m vitals_monitor.cli data/sample_readings.csv

Run the last command with `PYTHONPATH=src` if the package is not installed.

## Default thresholds

| Parameter | Warning | Critical |
|---|---|---|
| Heart rate (bpm) | below 50 or above 110 | at or below 40, or at or above 130 |
| SpO2 (%) | below 94 | at or below 90 |
| Respiratory rate (breaths/min) | below 10 or above 22 | at or below 8, or at or above 28 |
| Temperature (C) | below 36.0 or above 38.0 | at or below 35.0, or at or above 39.5 |
