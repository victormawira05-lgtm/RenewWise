# RenewWise — Round 1 Project Proposal

**Track:** Automate Your Workflow

1. **What does your Skill do?** RenewWise finds upcoming household bill, subscription, insurance, and warranty dates in user-authorized NAS documents and returns an evidence-linked review list.
2. **Target user and problem:** People managing household or small-office paperwork have due dates and warranty expirations scattered across invoices, policy documents, and receipts.
3. **Solution:** Search a chosen NAS folder, extract explicit dates and related details, and show each result beside its source file and supporting text.
4. **Main user flow:** The user names an authorized folder, date window, and optional categories; RenewWise finds candidate documents, reads them, checks each date against its context, then presents a sorted list and flags uncertain items.
5. **Difference:** Results include source paths and evidence, and ambiguous or conflicting dates are flagged instead of guessed. The workflow stays within the user's NAS and does not send reminders or alter files.
6. **UGREEN NAS features and steps:** Files find/browse locates candidate documents in the chosen folder; Documents read/extract retrieves dates and context. The built-in local Uliya model is planned for interpretation. No file-writing capability is required.
7. **Technical approach:** One Skill coordinates sequential finder, reader, and evidence-review passes, using each tool's actual previous output. Inputs are the authorized folder, time window, and optional categories. It honors the invoking user's permissions, uses the local model, and returns source-linked results without persistent storage or external transmission. No unsupported command names or direct filesystem access are assumed.
8. **Built/not built/testing:** A read-only local extractor prototype and the initial Skill workflow have been drafted. The prototype is not the submitted Skill runtime. Mapping to the official Skill Creation Tool and NAS capability calls, validation with its checker, and device testing remain. No NAS testing has occurred.
9. **Finalist test plan:** Core case 1: extract an explicitly stated warranty end date and return its receipt source. Core case 2: find a bill due date and amount across multiple authorized documents. Edge case: conflicting or ambiguous numeric dates must be flagged for review, not guessed.
10. **Limits, risks, dependencies:** Scanned/unreadable files and unsupported formats may be missed; extracted results require user verification. Availability of Files and Documents capabilities and the local model depends on the official UGREEN package and NAS version. No third-party runtime dependency is planned.

**Disclosure (outside the 500-word response limit):** No third-party components or open-source libraries are bundled in this Skill. OpenAI Codex (https://openai.com/codex/) was used to draft the materials; it is not a runtime dependency. The planned runtime uses UGREEN's built-in local Uliya model. The original hackathon work is the source-linked renewal review workflow. Capability documentation: https://ai.ugreen.com/pages/hackathon-starter-kit
