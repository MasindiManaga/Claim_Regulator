# ClaimRegulator

**Cloud-Based Insurance Claims Compliance Monitoring System**

ClaimRegulator is a Python-based, serverless prototype deployed on Amazon Web Services (AWS). It evaluates claim-recording deadlines, identifies potential compliance breaches, and records incidents for review.

> **Status:** AWS backend prototype deployed and tested. Multi-insurer support and the insurer-facing portal are planned, not yet implemented.

## Problem statement

Insurance claims operations need consistent deadline monitoring and traceable records of potential compliance failures. ClaimRegulator explores how serverless cloud services can automate checks and maintain structured incident records.

The current **CR-001** rule is a **prototype-configured business rule**, not a verified legal requirement under South African insurance legislation.

## Architecture

```text
IAM-authenticated API client
           |
           v
Amazon API Gateway (POST /claims/check)
           |
           v
AWS Lambda (Python 3.13)
           |
           v
Compliance checker
      /           \
 COMPLIANT       BREACHED
     |               |
 Return result   DynamoDB incident record
                     |
                Return result
```

| AWS service | Purpose |
| --- | --- |
| AWS Lambda | Runs Python compliance logic |
| Amazon API Gateway | Exposes the HTTP endpoint with AWS IAM authorization |
| Amazon DynamoDB | Stores compliance incidents |
| AWS IAM | Controls API invocation and service permissions |
| Amazon CloudWatch | Captures Lambda execution logs |
| AWS CloudShell | Used for authenticated API testing |

## Implemented features

- Checks claim-recording timestamps against a configured business-day deadline.
- Skips weekends and South African public holidays using the Python `holidays` package.
- Returns `COMPLIANT` or `BREACHED` with a calculated deadline.
- Creates DynamoDB incident records for breaches.
- Prevents duplicate incidents for the same claim and rule using a deterministic identifier and conditional writes.
- Accepts requests through an AWS IAM-protected API Gateway endpoint.
- Includes automated Python tests for business-day and compliance logic.

## API example

**Endpoint:** `POST /claims/check`  
**Authentication:** AWS Signature Version 4 (IAM)

Example request (synthetic data):

```json
{
  "claim_id": "CLM008",
  "received_at": "2026-09-23T10:00:00",
  "recorded_at": "2026-09-25T14:00:00"
}
```

Example compliant response:

```json
{
  "claim_id": "CLM008",
  "rule_id": "CR-001",
  "status": "COMPLIANT",
  "received_at": "2026-09-23T10:00:00",
  "recorded_at": "2026-09-25T14:00:00",
  "deadline": "2026-09-25",
  "action": "NONE",
  "incident_storage": "NOT_REQUIRED"
}
```

Example breached response:

```json
{
  "claim_id": "CLM009",
  "rule_id": "CR-001",
  "status": "BREACHED",
  "received_at": "2026-09-23T10:00:00",
  "recorded_at": "2026-09-28T09:00:00",
  "deadline": "2026-09-25",
  "action": "CREATE_COMPLIANCE_INCIDENT",
  "incident_storage": "CREATED"
}
```

Both examples returned HTTP `200` during authenticated API Gateway testing.

## Testing and evidence

The following scenarios have been tested:

| Scenario | Result |
| --- | --- |
| Compliant claim | Passed |
| Breached claim | Passed |
| South African public-holiday handling | Passed |
| DynamoDB incident creation | Passed |
| Duplicate incident prevention | Passed |
| IAM-authenticated API invocation | Passed |

Seven local Python tests passed during development. Run the tests from the project root with:

```bash
python -m pytest tests/
```

### Cloud execution evidence

Amazon CloudWatch logs were used to inspect CR-001 processing for compliant and breached synthetic claims. Direct Lambda tests, API Gateway responses, and DynamoDB records provided additional validation.

**Preserve or reinsert your existing CloudWatch screenshot links below this paragraph:**

<!-- Existing CloudWatch evidence screenshots go here. -->

## Security and limitations

- API requests require AWS IAM authentication.
- A dedicated test identity was configured with restricted API invocation permissions.
- Temporary AWS CloudShell permissions were removed after testing.
- Development and demonstration use synthetic claim data.
- The current backend does **not** yet enforce separation between different insurers.

**Not production-ready:** Tenant isolation, insurer-specific authorization, broader audit controls, monitoring, data-protection review, and legal validation remain necessary before handling real claims.

## Technology stack

- **Language:** Python 3.13
- **AWS:** Lambda, API Gateway, DynamoDB, IAM, CloudWatch, CloudShell
- **Python packages:** `boto3`, `holidays`, `pytest`
- **Development:** Visual Studio Code, Git, GitHub

## Development roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| 1 | Python compliance engine and automated tests | Completed |
| 2 | Lambda, API Gateway, IAM, DynamoDB integration and end-to-end tests | Completed |
| 3 | Multi-insurer tenant identity, authorization and data isolation | Planned |
| 4 | Insurer claim submission and incident management portal | Planned |
| 5 | Audit reporting, notifications and secure claimant verification | Future |

## AWS re/Start portfolio learning outcomes

This project demonstrates hands-on experience with serverless deployment, managed AWS services, IAM-based API authentication, NoSQL persistence, Python testing, Git version control, and cloud troubleshooting.

One troubleshooting exercise involved a Lambda invocation that exceeded its initial three-second timeout. After adjusting the timeout and retesting, the function successfully processed the claims.

## Disclaimer

ClaimRegulator is an educational proof of concept. Its current compliance rules are prototype assumptions, not a comprehensive or legally verified interpretation of South African insurance regulation. It must not be used for real regulatory decision-making without legal review, security hardening, and operational validation.
