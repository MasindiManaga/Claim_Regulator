# ClaimRegulator Regulatory Research

## Scope

ClaimRegulator is a prototype compliance monitoring system designed for
non-life insurance claims in South Africa.

The system is intended to support claims and compliance personnel by
monitoring claims processes, identifying potential compliance exceptions,
maintaining traceability, and supporting human review.

ClaimRegulator does not make final regulatory or claims decisions.

---

## Regulatory vs Business Controls

ClaimRegulator distinguishes between:

- **Regulatory Requirements:** Requirements derived from applicable South
  African insurance legislation, regulations, and regulatory standards.

- **Business Controls:** Internal system controls designed to support
  compliance and reduce operational risk. These controls should not be
  interpreted as regulatory requirements unless explicitly supported by
  an applicable regulatory source.

---

## CR-001: Timely Claim Recording

**Source:**  
South African Policyholder Protection Rules (PPRs) applicable to
short-term/non-life insurance claims — Rule 17.8.7.

**Regulatory Requirement:**  
A claim must be recorded no later than the first business day after the
date on which the claim was initially received.

The recording of a claim must not be delayed until all documentation or
other requirements relating to the claim have been received.

**ClaimRegulator Control:**  
ClaimRegulator will compare the date and time on which a claim was received
with the date and time on which it was recorded.

Where the applicable recording deadline is exceeded, the system will
create a compliance incident requiring investigation and an explanation.

The employee associated with the incident may provide an explanation but
may not resolve their own compliance incident. Resolution must be reviewed
and approved by a different authorised person, such as a supervisor or
compliance officer.

**Data Required:**
- Claim ID
- Received timestamp (`received_at`)
- Recorded timestamp (`recorded_at`)
- Employee responsible
- Compliance status
- Incident ID, where applicable
- Incident explanation
- Reviewer
- Review timestamp
- Resolution status

> The automatic incident and separate review process are ClaimRegulator business controls and are not presented as requirements of Rule 17.8.7.

---

## CR-002: Claim Communication

**Source:**  
South African Policyholder Protection Rules applicable to
short-term/non-life insurance claims — Rule 17 claims management
requirements.

**Regulatory Requirement:**  
The claims process must include appropriate communication with the
claimant. This includes acknowledging receipt of the claim within a
reasonable time and providing relevant information about the claims
process, including applicable contact details, indicative timelines and
outstanding requirements.

Claimants must also be kept adequately informed about the progress of
their claims, including relevant delays, revised timelines and claim
decisions.

Communications must meet applicable plain-language requirements.

**ClaimRegulator Control:**  
ClaimRegulator will maintain a communication history for each claim.

When an outstanding requirement is identified, the system will create a
task requiring the responsible employee to communicate the outstanding
requirement to the claimant.

The system will use progressive escalation:

1. **Task** — an action needs to be completed.
2. **Warning** — an outstanding task has reached a defined escalation
   condition.
3. **Compliance Incident** — a defined compliance escalation condition
   has been reached and formal review is required.

> Where a communication requires a qualitative assessment, such as
determining whether custom wording is sufficiently clear and in plain
language, ClaimRegulator will support human review rather than treating
the assessment as a fully automated compliance decision.

**Data Required:**
- Communication ID
- Claim ID
- Communication type
- Created by
- Created timestamp
- Reviewer, where required
- Review timestamp
- Sent timestamp
- Recipient
- Review status
- Related outstanding requirement
- Task status
- Escalation status

> Exact internal warning and escalation timeframes will not be invented. Where legislation specifies a timeframe, the applicable regulatory timeframe will be used. Where an insurer establishes an internal SLA, it will be identified as a business rule.

---

## CR-003: Investigation and Claim Rejection

**Source:**  
South African Policyholder Protection Rules applicable to
short-term/non-life insurance claims — Rule 17 claims-management
requirements.

**Regulatory Requirement:**  
A claim must not be rejected without a reasonable investigation having
been performed. Where a claim decision is communicated, applicable
requirements concerning the reasons and basis for the decision must also
be followed.

**ClaimRegulator Control:**  
ClaimRegulator will prevent a user from proceeding with a claim rejection
where the required investigation has not been completed.

If rejection is attempted before completion of the investigation:

- The rejection action will be blocked.
- The employee will be informed that the investigation requirement has
  not been completed.
- The attempted action will be recorded in the audit history.

A blocked attempt will not automatically be classified as a compliance
incident because ClaimRegulator prevented the rejection from taking
effect.

Where the investigation has been completed, a claims officer may propose
a rejection. The proposed rejection will enter a `PENDING_DECISION_REVIEW`
status.

A second authorised person must review and approve the proposed rejection
before the rejection is communicated to the claimant.

**Investigation Data Required:**
- Investigation status
- Investigation start timestamp
- Investigation completion timestamp
- Investigator
- Investigation summary
- Supporting evidence reference

**Decision Data Required:**
- Proposed decision
- Proposed by
- Proposal timestamp
- Reason for proposed rejection
- Supporting evidence
- Reviewer
- Review timestamp
- Review outcome
- Final decision status
- Decision communication timestamp

> The second-person approval requirement is a ClaimRegulator business control and is not presented as a regulatory requirement unless a specific applicable regulatory source establishes such a requirement.

---

## Documentation Review Control

ClaimRegulator will maintain a documentation checklist appropriate to the
claim being processed.

Documentation requirements will not be assumed to be identical for every
claim type.

Each required item may be classified as:

- `RECEIVED`
- `OUTSTANDING`
- `NOT APPLICABLE`
- `UNCLASSIFIED`

If an employee attempts to complete the documentation review while one or
more required items remain unclassified, ClaimRegulator will display a
notice.

The employee may return to the checklist or continue.

If the employee continues, the system will record that:
- The notice was displayed.
- Unclassified items remained.
- The employee chose to continue.
- The identity of the employee.
- The timestamp of the action.

This notice is a business control and does not by itself indicate a
regulatory breach.

---

## Human Oversight Principle

ClaimRegulator will automate compliance checks where the underlying
condition can be objectively evaluated from available data.

Where compliance requires qualitative judgement, ClaimRegulator will
support human review rather than automatically declaring the activity
compliant or non-compliant.

Examples include:
- Assessing whether an investigation was reasonable.
- Reviewing custom claimant communications for plain language.
- Reviewing explanations for compliance incidents.
- Approving the resolution of compliance incidents.

The purpose of ClaimRegulator is therefore to support and strengthen human
compliance decision-making rather than replace it.
