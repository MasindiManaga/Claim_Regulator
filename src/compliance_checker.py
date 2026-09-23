from datetime import datetime, timedelta


def get_next_business_day(received_at):
    """
    Calculate the first business day after a claim is received.

    Prototype limitation:
    Weekends are excluded, but South African public holidays
    are not yet included in the calculation.
    """

    next_day = received_at + timedelta(days=1)

    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)

    return next_day


def check_claim_recording(claim):
    """
    CR-001:
    Check whether a claim was recorded no later than the
    first business day after initial receipt.
    """

    received_at = datetime.fromisoformat(claim["received_at"])
    recorded_at = datetime.fromisoformat(claim["recorded_at"])

    deadline = get_next_business_day(received_at)

    if recorded_at.date() <= deadline.date():
        status = "COMPLIANT"
        action = "NONE"
    else:
        status = "BREACHED"
        action = "CREATE_COMPLIANCE_INCIDENT"

    result = {
        "claim_id": claim["claim_id"],
        "rule_id": "CR-001",
        "status": status,
        "received_at": claim["received_at"],
        "recorded_at": claim["recorded_at"],
        "deadline": deadline.date().isoformat(),
        "action": action
    }

    return result