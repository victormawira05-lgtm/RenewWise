# RenewWise backend

Read-only local prototype for the standalone RenewWise UGREEN AI NAS Skill idea. It scans an explicitly authorized folder and returns source-linked renewal, bill, subscription, insurance, and warranty date candidates.

## Run locally

```powershell
cd renewwise/backend
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
New-Item -ItemType Directory -Force authorized_documents
python app.py
```

The prototype reads `RENEWWISE_DATA_ROOT` from the process environment; it does not load `.env` automatically. Set it before launch if you want a different root:

```powershell
$env:RENEWWISE_DATA_ROOT = (Resolve-Path .\authorized_documents).Path
python app.py
```

Check `GET http://127.0.0.1:5050/api/health`, then analyze the root with:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5050/api/analyze -ContentType 'application/json' -Body '{"folder":"."}'
```

Supported input: text, Markdown, CSV, text-based PDF, and DOCX. Scanned image-only PDFs are reported as unreadable by extraction and need OCR support added after checking the UGREEN package. Numeric dates are interpreted as day/month/year. The initial prototype uses deterministic local extraction, without external AI calls or persistent storage.

This is a local development backend, not yet a UGREEN NAS Skill package. Before submission, map the read/search capabilities to the official Skill Developer Package and its supported agent/tool workflow.
