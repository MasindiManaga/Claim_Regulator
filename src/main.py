import json
from pathlib import Path

from src.compliance_checker import check_claim_recording


def load_claims():
    """
    Load synthetic claims from the project's JSON dataset.
    """

    project_root = Path(__file__).resolve().parent.parent
    data_file = project_root / "data" / "sample_claims.json"

    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    claims = load_claims()

    print("=== ClaimRegulator Compliance Check ===\n")

    for claim in claims:
        result = check_claim_recording(claim)

        print(f"Claim: {result['claim_id']}")
        print(f"Rule: {result['rule_id']}")
        print(f"Status: {result['status']}")
        print(f"Deadline: {result['deadline']}")
        print(f"Action: {result['action']}")
        print("-" * 40)


if __name__ == "__main__":
    main()