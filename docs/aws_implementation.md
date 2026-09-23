# AWS Implementation

## Overview

ClaimRegulator uses AWS services to demonstrate how insurance claims compliance controls can be implemented using a cloud-based architecture.

The project is being developed incrementally. AWS services are introduced when they serve a specific application requirement rather than being included only for demonstration purposes.

## Current AWS Architecture

At the current implementation stage, ClaimRegulator uses:

- AWS Lambda for serverless execution of compliance logic.
- Amazon CloudWatch Logs for monitoring Lambda executions and application logs.
- AWS Identity and Access Management (IAM) for controlling the permissions available to the Lambda function.

Current flow:

Claim Event
    |
    v
AWS Lambda
    |
    v
CR-001 Compliance Check
    |
    +---- COMPLIANT ----> No action required
    |
    +---- BREACHED -----> Compliance incident required
    |
    v
Amazon CloudWatch Logs

## AWS Lambda

### Purpose

AWS Lambda is used as the serverless compute layer for ClaimRegulator.

The Lambda function receives claim information as a JSON event and executes the project's Python compliance logic without requiring a continuously running server.

The current Lambda function is:

`claimregulator-compliance-checker`

### CR-001 Implementation

The first cloud-deployed compliance control is CR-001: Timely Claim Recording.

The function evaluates:

- when the initial claim notification was received
- when the claim was recorded
- the calculated recording deadline

The current prototype calculates the first business day after receipt by excluding weekends.

> Prototype limitation: South African public holidays are not yet included in the business-day calculation.

The function returns one of two outcomes:

- `COMPLIANT` with action `NONE`
- `BREACHED` with action `CREATE_COMPLIANCE_INCIDENT`

The `CREATE_COMPLIANCE_INCIDENT` result currently represents the required next action. Persistent incident creation will be implemented in a later development stage.

## Lambda Handler

AWS invokes the application through the Lambda handler:

`lambda_handler(event, context)`

The `event` parameter contains the JSON claim information supplied to the function.

The handler passes the claim to the compliance checking logic and returns the result to the caller.

## Testing

Two synthetic claim scenarios were used to test the deployed Lambda function.

### Test 1: Compliant Claim

Claim: `CLM001`

Result:

- Rule: `CR-001`
- Status: `COMPLIANT`
- Action: `NONE`

### Test 2: Breached Claim

Claim: `CLM002`

Result:

- Rule: `CR-001`
- Status: `BREACHED`
- Action: `CREATE_COMPLIANCE_INCIDENT`

Both scenarios executed successfully in AWS Lambda.

## Amazon CloudWatch

Amazon CloudWatch Logs is used to capture Lambda execution information and application-generated logs.

The application logs the claim identifier, compliance rule, result and required action.

Example:

`ClaimRegulator CR-001 | Claim=CLM002 | Status=BREACHED | Action=CREATE_COMPLIANCE_INCIDENT`

This provides operational visibility into how the compliance checker processes claims.

## IAM

The Lambda function uses an AWS IAM execution role.

At the current stage, the role provides the permissions required for the Lambda function to send execution logs to Amazon CloudWatch.

As additional AWS services are introduced, permissions will be added according to the principle of least privilege.

## Current Architecture Status

Implemented:

- Python compliance logic
- Automated tests with pytest
- AWS Lambda deployment
- Compliant claim Lambda test
- Breached claim Lambda test
- CloudWatch logging
- IAM Lambda execution role

Planned:

- Persistent claim/compliance incident storage
- DynamoDB integration
- Least-privilege DynamoDB permissions
- API-based Lambda invocation
- Additional compliance controls
