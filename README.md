# RenewWise

**A private, evidence-linked paperwork review Skill for UGREEN AI NAS.**

RenewWise helps households and small offices find bill due dates, subscription renewals, insurance dates, and warranty expirations hidden in their documents. The user chooses an authorized NAS folder and a time window. RenewWise returns a sorted review list with each date's source file and supporting text, and flags unclear results instead of guessing.

The Skill is designed to be read-only. It does not move or edit files, create reminders, contact providers, or send document content to external services.

## Project status

This repository contains the Round 1 Skill draft, proposal, and a separate local extraction API prototype. The Skill workflow uses the Files capability to find candidate documents and the Documents capability to read and extract details. Exact tool names still need confirmation against UGREEN's official Skill Developer Package and checker. NAS validation has not yet occurred.

The Flask backend is for local prototyping. It is **not** the UGREEN NAS Skill runtime and is not included in the pre-test Skill ZIP.

## Repository contents

| Path | Contents |
| --- | --- |
| [`skill/SKILL.md`](skill/SKILL.md) | Skill entry point, workflow, permissions, and failure handling |
| [`skill/README.md`](skill/README.md) | Short user-facing Skill description |
| [`backend/`](backend/README.md) | Read-only local document extraction API prototype |
| [`proposal.md`](proposal.md) | Editable source for the Round 1 proposal |
| [`submission/`](submission/README.md) | Proposal PDF and pre-test Skill ZIP |

## Run the local prototype

The backend reads files only beneath `RENEWWISE_DATA_ROOT`. Start it from this repository directory:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
New-Item -ItemType Directory -Force authorized_documents
$env:RENEWWISE_DATA_ROOT = (Resolve-Path .\authorized_documents).Path
python backend/app.py
```

The service binds to `127.0.0.1:5050` by default. It reads the root path from the process environment; it does not load `.env` automatically. See [backend/README.md](backend/README.md) for details.

Check that it is running:

```powershell
Invoke-RestMethod http://127.0.0.1:5050/api/health
```

Analyze the authorized root folder:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:5050/api/analyze `
  -ContentType 'application/json' `
  -Body '{"folder":"."}'
```

The response includes candidate dates, categories, source filenames, nearby text, possible amounts, unreadable files, and a note that numeric dates are interpreted as DD/MM/YYYY.

## Prototype limits

- Supported files: TXT, Markdown, CSV, text-based PDF, and DOCX.
- Image-only scanned PDFs need OCR, which is not implemented.
- Date detection is deterministic and may miss unusual wording or formats; verify each result against its source.
- The prototype does not call an AI model or save analysis results.
- This local API does not replace UGREEN's supported NAS Skill tools.

## Round 1 submission files

- [Project proposal PDF](submission/RenewWise_Project_Proposal.pdf)
- [Pre-test Skill package ZIP](submission/RenewWise_Pretest_Skill_Package.zip)

The proposal contains 363 words across its ten substantive answers. Check the current [UGREEN Hackathon Devpost page](https://ugreenhackathon.devpost.com/) for submission requirements and deadlines.
