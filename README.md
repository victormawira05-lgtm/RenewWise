# RenewWise

**A private, evidence-linked renewal and warranty review Skill for UGREEN AI NAS.**

RenewWise searches a folder the user authorizes, finds likely bills, subscriptions, insurance policies, and warranty documents, then returns dates with source paths and supporting text. Ambiguous or conflicting details are flagged for review. The Skill is read-only and does not send reminders or transmit document content to external services.

## Project status

This repository contains the original Round 1 Skill draft, proposal, and a separate local extraction prototype. The pre-test package is a draft based on UGREEN's published Files and Documents capability descriptions. It still needs review with the official Skill Developer Package and checker, then validation on UGREEN NAS if selected as a finalist.

The Flask backend is a **local prototype only**. It is not the NAS Skill runtime and is not included in the pre-test ZIP. The actual submission ZIP follows the Skill-only package requirements.

## Repository layout

```text
renewwise/
├── backend/       Read-only local extraction API prototype
├── skill/         SKILL.md and user-facing Skill README
├── submission/    Round 1 proposal PDF and pre-test Skill ZIP
├── proposal.md    Editable proposal source
└── README.md
```

## Local backend prototype

See [backend/README.md](backend/README.md) for setup. The prototype scans a configured authorized folder and extracts renewal-date candidates from text, Markdown, CSV, text-based PDF, and DOCX files. Scanned PDFs need OCR support, which is not implemented. Results are generated per request and are not persisted.

## UGREEN Skill

Read [skill/SKILL.md](skill/SKILL.md) for the trigger, required inputs, supported capability areas, workflow, permissions, and failure handling. The Skill uses the Files capability to find candidates and the Documents capability to read and extract information. Exact tool names must be confirmed against the official developer package before release.

## Round 1 files

- [Project proposal](submission/RenewWise_Project_Proposal.pdf)
- [Pre-test Skill package](submission/RenewWise_Pretest_Skill_Package.zip)

The proposal's ten substantive responses are under the 500-word limit. Both files are within the stated file-size limits. Follow the current Devpost listing for the final submission checklist and upload deadline.
