ClaimRegulator

Cloud-Based Insurance Claims Compliance Monitoring System

ClaimRegulator is a Python-based, serverless application deployed on Amazon Web Services (AWS). It is designed to support timely, consistent and auditable insurance claims processing by automatically evaluating claim-recording deadlines and identifying potential compliance breaches.

The project was developed as a practical cloud computing and software development portfolio project, demonstrating the integration of AWS services, Python business logic, API security, automated testing and NoSQL database operations.

Project Status: Functional backend prototype deployed and tested on AWS. Multi-insurer platform development is planned.

1. Problem Statement

Insurance companies process large volumes of claims, making it important to monitor operational deadlines and identify potential compliance failures.

Manual monitoring can introduce delays, inconsistencies and difficulties in tracking incidents.

ClaimRegulator explores how cloud-based automation can support compliance monitoring through consistent rule evaluation, incident detection and structured recordkeeping.

The current implementation uses a prototype compliance rule, CR-001, to evaluate whether a claim was recorded within a configured business-day deadline.

CR-001 is a demonstration rule and should not be interpreted as a verified statutory requirement.

2. Project Objectives

Automate insurance claim-recording compliance checks.
Calculate deadlines using South African business days and public holidays.
Identify compliant and breached claims.
Automatically record detected compliance incidents.
Prevent duplicate incident creation.
Provide a secure API for submitting claims.
Establish a foundation for a future multi-insurer compliance platform.

3. AWS Architecture

The current solution uses a serverless architecture.

Authenticated API Client

          |

          v

Amazon API Gateway

     (AWS IAM)

          |

          v

     AWS Lambda

   (Python 3.13)

          |

          v

Compliance Engine

          |

          +-------------------+

          |                   |

          v                   v

   Compliant Claim       Breached Claim

          |                   |

          v                   v

   Return Result        Amazon DynamoDB

                              |

                              v

                       Store Incident

AWS Services Used

AWS ServicePurposeAWS LambdaExecutes the Python compliance-checking logicAmazon API GatewayExposes the compliance-checking HTTP APIAmazon DynamoDBStores detected compliance incidentsAWS Identity and Access Management (IAM)Controls API invocation and resource permissionsAmazon CloudWatchSupports execution logging and troubleshootingAWS CloudShellProvides an AWS environment for authenticated API testing

4. Implemented Features

Automated Compliance Checking

The compliance engine evaluates claim-recording timestamps against a calculated deadline and returns a compliance outcome.

South African Business-Day Calculations

Deadline calculations account for weekends and South African public holidays using the Python holidays library.

Compliance Incident Creation

When a breach is detected, the AWS Lambda function writes an incident record to Amazon DynamoDB.

Duplicate Incident Prevention

The application uses a deterministic incident identifier and conditional database writes to avoid creating duplicate incidents for the same claim and compliance rule.

IAM-Secured API

The API Gateway endpoint requires AWS IAM authentication. Requests are signed using AWS Signature Version 4.

Automated Testing

Python tests validate business-day calculations and compliance-checking behaviour.

Seven local tests were successfully executed during development.

5. API Overview

Method: POST

Route: /claims/check

Authentication: AWS IAM (Signature Version 4)

Example Request

{

  "claim_id": "CLM008",

  "received_at": "2026-09-23T10:00:00",

  "recorded_at": "2026-09-25T14:00:00"

}

Example Response — Compliant Claim

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

Example Response — Breached Claim

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

Both examples were successfully tested through API Gateway and returned HTTP 200.

The examples use synthetic claim information.

6. Testing and Validation

The following scenarios have been validated:

Test ScenarioResultCompliant claimPassedBreached claimPassedSouth African public-holiday calculationPassedAutomatic DynamoDB incident creationPassedDuplicate incident preventionPassedIAM-authenticated API invocationPassedEnd-to-end API processingPassed

Local Testing

Run the Python tests from the project root:

python -m pytest tests/

Cloud Execution Evidence

CloudWatch logs were used to inspect Lambda execution and compliance-rule processing.

Additional validation was completed through direct Lambda tests, authenticated API Gateway requests and DynamoDB incident inspection.

Verified API examples:

CLM008: COMPLIANT — incident storage not required.
CLM009: BREACHED — compliance incident created.

7. Security Considerations

The current prototype includes:

AWS IAM-based API authentication.
Dedicated permissions for API testing.
IAM policies restricting access to the relevant API route.
Removal of temporary CloudShell permissions after testing.
DynamoDB conditional writes for incident deduplication.
Synthetic test data rather than real customer information.

The application is not yet production-ready.

Additional controls are required before onboarding real insurers, including tenant isolation, insurer-specific authorization, audit logging, secrets management, data protection assessments and operational monitoring.

8. Technology Stack

Programming Language: Python 3.13

Cloud Platform: Amazon Web Services

AWS Services: Lambda, API Gateway, DynamoDB, IAM, CloudWatch and CloudShell

Python Libraries: boto3, holidays, pytest

Development Tools: Visual Studio Code, Git and GitHub

9. Development Roadmap

Phase 1 — Compliance Engine

Completed

Python compliance-checking logic
Business-day and public-holiday calculations
Automated tests

Phase 2 — AWS Backend

Completed

Lambda deployment
API Gateway integration
IAM authentication
DynamoDB incident storage
Duplicate incident prevention
End-to-end testing

Phase 3 — Multi-Insurer Architecture

Planned

Tenant-aware claim processing
Secure insurer identity management
Tenant-level data isolation
Insurer-specific access permissions

Phase 4 — Insurer Portal

Planned

Claims submission interface
Compliance monitoring dashboard
Incident review and management
Historical compliance reporting

Phase 5 — Extended Platform Capabilities

Future Development

Audit trails and operational reporting
Additional configurable compliance rules
Notifications and escalation workflows
Secure claimant verification functionality

10. AWS re/Start Learning Outcomes

ClaimRegulator demonstrates practical experience in:

Developing and deploying serverless applications.
Integrating AWS managed services.
Implementing IAM authentication and least-privilege permissions.
Working with NoSQL databases.
Troubleshooting Lambda execution timeouts.
Testing cloud APIs using signed requests.
Applying Python automated testing.
Managing application source code with Git and GitHub.

A notable troubleshooting activity involved investigating a Lambda execution timeout, adjusting the function's timeout configuration and successfully retesting the deployment.

11. Disclaimer

ClaimRegulator is an educational and proof-of-concept project.

The compliance rules currently implemented are prototype assumptions and have not been validated as comprehensive requirements under South African insurance legislation.

The application is not intended for production regulatory decision-making without further legal validation, security review and operational testing.
