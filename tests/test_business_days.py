
from datetime import datetime

from src.compliance_checker import (
    get_next_business_day,
    check_claim_recording
)

def test_normal_weekday():
    received_at = datetime(2026, 10, 19, 9, 0)
    deadline = get_next_business_day(received_at)

    assert deadline.date().isoformat() == "2026-10-20"


def test_weekend():
    received_at = datetime(2026, 10, 23, 9, 0)
    deadline = get_next_business_day(received_at)

    assert deadline.date().isoformat() == "2026-10-26"


def test_public_holiday():
    received_at = datetime(2026, 9, 23, 9, 0)
    deadline = get_next_business_day(received_at)

    assert deadline.date().isoformat() == "2026-09-25"

def test_claim_recorded_after_public_holiday():
    # prepare claim
    claim = {
        "claim_id": "CLM006",
        "received_at": "2026-09-23T09:00:00",
        "recorded_at": "2026-09-28T10:00:00"
    }

    # check compliance
    result = check_claim_recording(claim)

    # verify results
    assert result["deadline"] == "2026-09-25"
    assert result["status"] == "BREACHED"
    assert result["action"] == "CREATE_COMPLIANCE_INCIDENT"