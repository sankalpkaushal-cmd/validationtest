from vitals_monitor.audit import AuditLog


def test_new_log_verifies():
    assert AuditLog().verify() is True


def test_appended_events_verify():
    log = AuditLog()
    log.append({"message": "a"})
    log.append({"message": "b"})
    assert len(log) == 2
    assert log.verify() is True


def test_changed_event_is_detected():
    log = AuditLog()
    log.append({"message": "a"})
    log.append({"message": "b"})
    log._entries[0]["event"]["message"] = "changed"
    assert log.verify() is False


def test_removed_entry_is_detected():
    log = AuditLog()
    log.append({"message": "a"})
    log.append({"message": "b"})
    del log._entries[0]
    assert log.verify() is False
