from src.compliance_checker import check_claim_recording


def test_claim_recorded_within_deadline():
    claim = {
        "claim_id": "TEST001",
        "received_at": "2026-09-18T16:00:00",
        "recorded_at": "2026-09-21T10:30:00"
    }

    result = check_claim_recording(claim)

    assert result["status"] == "COMPLIANT"
    assert result["action"] == "NONE"
    assert result["deadline"] == "2026-09-21"


def test_claim_recorded_after_deadline():
    claim = {
        "claim_id": "TEST002",
        "received_at": "2026-09-18T16:00:00",
        "recorded_at": "2026-09-22T10:30:00"
    }

    result = check_claim_recording(claim)

    assert result["status"] == "BREACHED"
    assert result["action"] == "CREATE_COMPLIANCE_INCIDENT"
    assert result["deadline"] == "2026-09-21"


def test_claim_recorded_same_day():
    claim = {
        "claim_id": "TEST003",
        "received_at": "2026-09-21T08:30:00",
        "recorded_at": "2026-09-21T11:00:00"
    }

    result = check_claim_recording(claim)

    assert result["status"] == "COMPLIANT"
    assert result["action"] == "NONE"