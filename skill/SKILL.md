---
name: renew-wise
description: Find upcoming household bill, subscription, insurance, and warranty dates in documents the user authorizes on this UGREEN NAS. Return an evidence-linked review list and flag uncertainty without changing files.
---

# RenewWise

## Goal

Help a household or small-office user find upcoming renewal, payment, and warranty dates in authorized NAS documents. Return a concise list with the source document and supporting text so the user can verify every result.

## When to use

Use when the user asks what bills, subscriptions, policies, or warranties are due or expiring, or asks to review these dates in a named NAS folder. This Skill only prepares a review list. It does not create reminders, contact providers, move files, or alter documents.

## Required inputs

- An authorized NAS folder to search. If the user has not identified one, ask which folder to use; never guess a private location.
- A time window, such as the next 30 days. If omitted, ask for a window or offer a clearly labeled next-30-days view.
- Optional categories: bills, subscriptions, insurance, or warranties. If omitted, search all four.

## Supported capability areas

Use only UGREEN NAS capabilities available through the installed Skill Developer Package:

- **Files:** find and browse documents within the user-authorized folder.
- **Documents:** read documents and extract information from them.

Do not use shell commands, scripts, direct filesystem access, unsupported APIs, or external services. If the installed package does not expose the required Files and Documents capabilities, explain that the search cannot be completed and stop. Do not invent command names or silently substitute another source.

## Workflow and expert review passes

Run these passes in order as one coordinated Skill workflow. Each pass must use the actual folder, file list, or document content returned by the preceding pass; do not refer vaguely to “the earlier results.”

1. **Scope pass:** confirm the folder, time window, and categories. Search only that authorized folder and its descendants. Respect NAS access permissions and skip hidden or inaccessible content unless the user explicitly included it and the tools permit access.
2. **Document-finder pass:** use the Files capability to find candidate bills, invoices, subscription notices, insurance policies, and warranty receipts. Keep the NAS-provided source path for each candidate. If no candidates are found, say so and stop.
3. **Document-reader pass:** use the Documents capability to read the candidate documents and extract only explicitly stated provider/item, date, date meaning, category, and amount/currency when present. Do not infer missing dates, amounts, or renewals from a purchase date alone.
4. **Evidence-review pass:** independently check each extracted date against its source content. Return a date only when a nearby statement supports its meaning, such as “payment due,” “renews on,” “expires,” or “warranty valid until.” Attach a short source excerpt or the nearest relevant text and the source path. Flag unclear date formats, conflicting dates, and uncertain classifications instead of resolving them by guesswork. Interpret unambiguous ISO and month-name dates directly. For ambiguous numeric dates, ask the user which date convention applies or mark the item “date needs confirmation.”
5. **Result pass:** remove duplicate references to the same document and event, sort by date, and include only results in the requested time window. Clearly distinguish upcoming from already overdue items. If a document could not be read, list its filename and the available reason without implying it contains a renewal.

The passes are reasoning roles inside this Skill's single workflow; do not claim that separate external agents or services ran.

## Result format

Return a compact table with: date, date meaning, category, provider/item (if explicit), amount/currency (if explicit), source path, and supporting text. Follow it with a short “Needs review” section for ambiguous or unreadable items. If nothing qualifies, state that no matching items were found in the selected folder and window. Never fabricate a result to fill the table.

## Permissions, model, and data handling

Ask before searching a folder that the user has not authorized. Operate with the invoking user's NAS permissions and use the built-in local Uliya model when available. Do not send document text, paths, or extracted personal information to external models or services. Do not retain extracted text beyond the current request. This Skill is read-only: it must not create, move, rename, tag, overwrite, or delete files. It does not send reminders or share information externally.

## Failure handling

- If the folder is missing, outside the authorized scope, or inaccessible, explain that and ask the user to select an accessible folder.
- If Files or Documents capabilities are unavailable, stop and identify the missing capability; do not fall back to arbitrary commands.
- If no candidate documents are found, say so and stop.
- If a document is unreadable, report it under “Needs review” and continue with other candidates.
- If extracted dates conflict or their meaning is unclear, show the competing evidence and request user review. Do not choose one silently.
- If the search is incomplete because a capability fails, label the result incomplete and name the affected files or step.

## Hackathon implementation and disclosures

The original hackathon functionality is the sequential document-finding, date-extraction, and evidence-review workflow that produces a source-linked renewal list. This Round 1 Skill uses only the Files and Documents capability areas documented in the official UGREEN Starter Kit; exact CLI/tool names are intentionally not asserted here.

Third-party components and open-source libraries: none are bundled or called by this Skill. AI tools: OpenAI Codex ([source](https://openai.com/codex/)) was used to draft the Skill and proposal; it is not a runtime dependency. At runtime the Skill is intended to use UGREEN's built-in local Uliya model. No external model or service is part of the planned workflow. Capability source: [UGREEN Hackathon Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit).
