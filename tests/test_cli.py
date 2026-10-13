from vitals_monitor.cli import main


def write_csv(tmp_path, rows):
    path = tmp_path / "readings.csv"
    path.write_text("patient_id,timestamp,parameter,value\n" + "\n".join(rows) + "\n")
    return str(path)


def test_exit_code_zero_when_all_normal(tmp_path):
    path = write_csv(tmp_path, ["P-001,2026-01-05T08:00:00,heart_rate,72"])
    assert main([path]) == 0


def test_exit_code_one_for_warning(tmp_path):
    path = write_csv(tmp_path, ["P-001,2026-01-05T08:00:00,spo2,92"])
    assert main([path]) == 1


def test_exit_code_two_for_critical(tmp_path):
    path = write_csv(tmp_path, ["P-001,2026-01-05T08:00:00,spo2,85"])
    assert main([path]) == 2
