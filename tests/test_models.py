from datetime import datetime

import pytest

from vitals_monitor.models import Reading

NOW = datetime(2026, 1, 5, 8, 0, 0)


def test_valid_reading_is_accepted():
    reading = Reading("P-001", NOW, "heart_rate", 72)
    assert reading.value == 72


def test_empty_patient_id_is_rejected():
    with pytest.raises(ValueError):
        Reading("", NOW, "heart_rate", 72)


def test_unknown_parameter_is_rejected():
    with pytest.raises(ValueError):
        Reading("P-001", NOW, "glucose", 5.5)


def test_nan_value_is_rejected():
    with pytest.raises(ValueError):
        Reading("P-001", NOW, "spo2", float("nan"))
