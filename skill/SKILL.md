# RenewWise

# Goal

Help a household or small-office user find upcoming bill, subscription, insurance, and warranty dates in documents inside one NAS folder they explicitly authorize. Return a concise, source-linked review list and identify uncertainty so the user can verify each result.

# Required input

- The exact NAS folder to search, provided or explicitly confirmed by the user. Never guess a folder or broaden scope to another share.
- A date window, such as the next 30 days. If it is missing, ask for it before searching.
- Optional categories: bills, subscriptions, insurance, or warranties. If omitted, use all four.

# Generation-time capability evidence

- `ug-filesystem` → `file-agent`
- `ug-document` → `document-agent`

The public capability catalog maps `ug-filesystem` to `file-agent` and documents its read-only `find` Action, which accepts a required `path` plus optional `pattern`, `type`, `max-depth`, and `limit`. It maps `ug-document` to `document-agent` and documents its read-only `extract` Action, which accepts a required `query`, repeated `file` values, and optional `schema`, `content-scope`, `max-files`, `body-cap`, and `dedupe`. Use only those catalogued capabilities. Base user-facing results on completed delegate results, not assumptions about these Actions.

# Orchestration

This Skill is read-only. It finds likely source files and extracts renewal facts; it never writes, moves, renames, deletes, tags, or shares files, creates reminders, contacts providers, or performs payment actions. Do not use shell commands, direct filesystem access, unsupported APIs, or external services. Do not transmit document contents or personal information outside the NAS. If the available document-processing capability would require external transmission, stop and explain that the request cannot be completed under this Skill's data-handling boundary.

1. Confirm the exact authorized folder, date window, and category scope. Ask for missing required input before delegating. Keep the search within that folder and its descendants; respect platform permissions and do not include hidden or inaccessible content unless the user explicitly requested it and the capability permits it.
2. Delegate the candidate-file search to the registered expert using only this CLI's mapped agent:

   `delegate --target file-agent --instruction 'Use ug-filesystem find to locate candidate bills, invoices, subscription notices, insurance policies, and warranty receipts within the exact NAS folder authorized by the user. Search only that folder and its descendants. Return actual matching file paths, filenames, and the operation status. Do not read unrelated files or modify, move, rename, delete, or share anything.'`

3. Continue only if the file-agent returns status `completed` and actual candidate file paths. If the result set is empty, report the empty result and stop; never substitute similar documents or widen the folder scope. If it returns partial results, preserve the partial status and do not imply the search was complete. Do not invent or reconstruct file paths.
4. Delegate extraction using only paths actually returned by the completed file-agent result:

   `delegate --target document-agent --instruction 'Use ug-document extract on only the actual candidate file paths returned by the completed file-agent result. Extract explicitly stated provider or item, renewal or payment date, date meaning, category, amount and currency if present, and a short supporting excerpt with its source path. Check the user requested date window and categories: include qualifying events and separately flag overdue or ambiguous events. Do not infer a renewal from a purchase date, resolve ambiguous numeric dates by guesswork, read other files, or modify or share content. Return extraction coverage, unreadable-file reasons, and the operation status.'`

5. Continue to synthesis only when the document-agent returns status `completed`. Use the real result returned by file-agent as the input to document-agent; use only the actual extracted facts, coverage, and failures from that downstream result as the sole source for the review list. Never state an event was verified when its evidence is absent, and never conceal partial coverage.
6. Review each proposed date against the returned supporting excerpt. Include a date only when nearby text establishes its meaning, such as “payment due,” “renews on,” “expires,” or “warranty valid until.” Interpret clear ISO and month-name dates. Mark ambiguous numeric dates as needing confirmation. Preserve conflicting dates for the user to review. Deduplicate the same event, sort by date, restrict results to the requested window, and distinguish overdue items from future items.

# Completion and failure

Handle every delegation status explicitly:

- `completed`: use only the actual result returned by that expert and proceed to the next required step.
- `failed`: report which step failed and the available error; do not report a successful review.
- `cancelled`: state that the operation was cancelled and stop.
- `waiting_user`: ask only for the missing answer or permission, then resume only after the user responds.
- `waiting_approval`: explain the pending approval and wait. This Skill does not authorize or perform write actions.

If the folder is missing or inaccessible, ask the user to select an authorized folder. If a required capability is unavailable, say which step is unsupported and stop; never substitute direct file access, another data source, or an external service. If an individual document is unreadable, report its filename and the returned reason under “Needs review” while clearly labeling coverage partial if applicable. If no candidates or no qualifying events are found, say so and stop without inventing similar results.

# Result format

Return a compact table with date, date meaning, category, provider or item, amount/currency if stated, source path, and supporting excerpt. Add a “Needs review” section for ambiguous dates, conflicting evidence, unreadable files, or incomplete coverage. State explicitly when no matching documents or no qualifying events were found. Never fabricate a result.

For a short user-facing overview, see [README](references/README.md).

# Permissions and data handling

Search only the explicitly authorized folder using the invoking user's NAS permissions. Request the minimum file-read scope needed. Do not retain document text beyond the current request. This Skill does not use external models, APIs, or services and does not disclose or transmit document content, paths, or extracted personal information externally. If a delegated capability cannot meet that boundary, stop and tell the user. No credentials, scripts, binaries, or third-party libraries are included in this Skill package.

# Source and development disclosure

The original RenewWise workflow and Skill text are developed for this project. OpenAI Codex was used to help draft and review the Skill; it is not a runtime dependency. The `ug-filesystem` and `ug-document` names and Actions are drawn from the official UGREEN Skill Creation Tool's public capability catalog (version 2.0.0). No UGREEN endorsement or certification is claimed. The local Flask API prototype is separate from this orchestration Skill and is not part of the Skill package. SkillHub license selection remains a publisher choice and must be completed truthfully during upload.
