
import os
import json
import hashlib
import boto3

from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError


# initialise DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(
    os.environ["INCIDENTS_TABLE_NAME"]
)


def get_next_business_day(received_at):
    # calculate next business day
    next_day = received_at + timedelta(days=1)

    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)

    return next_day


def check_claim_recording(claim):
    # check CR-001
    received_at = datetime.fromisoformat(claim["received_at"])
    recorded_at = datetime.fromisoformat(claim["recorded_at"])

    deadline = get_next_business_day(received_at)

    if recorded_at.date() <= deadline.date():
        status = "COMPLIANT"
        action = "NONE"
    else:
        status = "BREACHED"
        action = "CREATE_COMPLIANCE_INCIDENT"

    return {
        "claim_id": claim["claim_id"],
        "rule_id": "CR-001",
        "status": status,
        "received_at": claim["received_at"],
        "recorded_at": claim["recorded_at"],
        "deadline": deadline.date().isoformat(),
        "action": action
    }


def create_compliance_incident(result):
    # generate stable incident identifier
    incident_key = f"{result['claim_id']}:{result['rule_id']}"
    incident_id = hashlib.sha256(
        incident_key.encode("utf-8")
    ).hexdigest()[:24]

    incident = {
        "incident_id": incident_id,
        "claim_id": result["claim_id"],
        "rule_id": result["rule_id"],
        "compliance_status": "BREACHED",
        "incident_status": "OPEN",
        "received_at": result["received_at"],
        "recorded_at": result["recorded_at"],
        "deadline": result["deadline"],
        "detected_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        table.put_item(
            Item=incident,
            ConditionExpression="attribute_not_exists(incident_id)"
        )
        return "CREATED"

    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code == "ConditionalCheckFailedException":
            return "ALREADY_EXISTS"

        raise

def lambda_handler(event, context):
    # parse request
    if "body" in event:
        body = event["body"]

        if event.get("isBase64Encoded"):
            import base64
            body = base64.b64decode(body).decode("utf-8")

        try:
            claim = json.loads(body) if isinstance(body, str) else body
        except (json.JSONDecodeError, TypeError):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Invalid JSON request body"})
            }
    else:
        claim = event

    # validate claim
    required_fields = ["claim_id", "received_at", "recorded_at"]
    if not isinstance(claim, dict) or any(
        field not in claim for field in required_fields
    ):
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Missing required claim fields"})
        }

    # check compliance
    try:
        result = check_claim_recording(claim)

        if result["status"] == "BREACHED":
            result["incident_storage"] = create_compliance_incident(result)
        else:
            result["incident_storage"] = "NOT_REQUIRED"

    except (ValueError, TypeError):
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Invalid claim date format"})
        }

    print(json.dumps(result))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }