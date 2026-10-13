import json

import pytest

from vitals_monitor.thresholds import DEFAULT_THRESHOLDS, Band, load_thresholds


def test_default_bands_are_in_order():
    for band in DEFAULT_THRESHOLDS.values():
        assert band.critical_low <= band.warning_low <= band.warning_high <= band.critical_high


def test_out_of_order_band_is_rejected():
    with pytest.raises(ValueError):
        Band(warning_low=40, critical_low=50, warning_high=110, critical_high=130)


def test_loader_overrides_one_limit(tmp_path):
    path = tmp_path / "limits.json"
    path.write_text(json.dumps({"heart_rate": {"warning_high": 100}}))
    loaded = load_thresholds(str(path))
    assert loaded["heart_rate"].warning_high == 100
    assert loaded["spo2"] == DEFAULT_THRESHOLDS["spo2"]


def test_loader_rejects_unknown_parameter(tmp_path):
    path = tmp_path / "limits.json"
    path.write_text(json.dumps({"glucose": {"warning_high": 9}}))
    with pytest.raises(ValueError):
        load_thresholds(str(path))


def test_loader_rejects_out_of_order_limits(tmp_path):
    path = tmp_path / "limits.json"
    path.write_text(json.dumps({"heart_rate": {"warning_high": 140}}))
    with pytest.raises(ValueError):
        load_thresholds(str(path))
