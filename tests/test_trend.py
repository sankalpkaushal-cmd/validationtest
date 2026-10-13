import pytest

from vitals_monitor.trend import rolling_average, sustained_decline


def test_rolling_average_of_full_windows():
    assert rolling_average([1, 2, 3, 4], window=2) == [1.5, 2.5, 3.5]


def test_rolling_average_rejects_zero_window():
    with pytest.raises(ValueError):
        rolling_average([1, 2, 3], window=0)


def test_decline_is_detected():
    assert sustained_decline([98, 98, 98, 95, 95, 95]) is True


def test_flat_series_is_not_a_decline():
    assert sustained_decline([97, 97, 97, 97, 97, 97]) is False


def test_too_few_values_is_not_a_decline():
    assert sustained_decline([98, 95, 92]) is False
