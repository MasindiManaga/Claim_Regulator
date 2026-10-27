
from datetime import datetime

from src.compliance_checker import get_next_business_day


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
