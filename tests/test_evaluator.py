from datetime import datetime

from vitals_monitor.evaluator import evaluate, evaluate_all
from vitals_monitor.models import Reading

NOW = datetime(2026, 1, 5, 8, 0, 0)


def reading(parameter, value):
    return Reading("P-001", NOW, parameter, value)


def test_normal_reading_raises_no_alert():
    assert evaluate(reading("heart_rate", 80)) is None


def test_low_spo2_raises_warning():
    assert evaluate(reading("spo2", 92)).severity == "warning"


def test_very_low_spo2_raises_critical():
    assert evaluate(reading("spo2", 90)).severity == "critical"


def test_high_temperature_raises_critical():
    assert evaluate(reading("temp_c", 39.6)).severity == "critical"


def test_alert_message_names_parameter_and_severity():
    alert = evaluate(reading("heart_rate", 120))
    assert alert.message == "heart_rate 120 is warning"


def test_evaluate_all_keeps_input_order():
    alerts = evaluate_all([reading("heart_rate", 125), reading("spo2", 85), reading("spo2", 98)])
    assert [a.parameter for a in alerts] == ["heart_rate", "spo2"]
