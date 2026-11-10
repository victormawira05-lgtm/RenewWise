"""RenewWise read-only document analysis API.

The service only reads files beneath RENEWWISE_DATA_ROOT. It does not modify,
move, upload, or delete documents. Extracted results are computed per request
and are not persisted.
"""
from __future__ import annotations

import io
import os
import re
import zipfile
from datetime import date, datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from flask import Flask, jsonify, request
from pypdf import PdfReader

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024

ROOT = Path(os.environ.get("RENEWWISE_DATA_ROOT", "./authorized_documents")).expanduser().resolve()
MAX_FILES = int(os.environ.get("RENEWWISE_MAX_FILES", "300"))
MAX_FILE_BYTES = int(os.environ.get("RENEWWISE_MAX_FILE_MB", "12")) * 1024 * 1024
SUPPORTED = {".txt", ".md", ".csv", ".pdf", ".docx"}

DATE_PATTERNS = [
    ("iso", re.compile(r"\b(20\d{2})-(0?[1-9]|1[0-2])-(0?[1-9]|[12]\d|3[01])\b")),
    ("month_first", re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?[,]?\s+(20\d{2})\b", re.I)),
    ("day_first", re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)[,]?\s+(20\d{2})\b", re.I)),
    # Kenyan documents commonly use DD/MM/YYYY; this interpretation is stated in the API response.
    ("numeric_dmy", re.compile(r"\b(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/(20\d{2})\b")),
]
MONTHS = {name.lower(): i for i, name in enumerate(("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"), 1)}
DATE_TERMS = re.compile(r"\b(due|renew(?:al|s|ed)?|expir(?:y|es|ation)|valid\s+until|warrant(?:y|ies)|coverage\s+ends|payment\s+date|service\s+through)\b", re.I)
KIND_TERMS = {
    "warranty": re.compile(r"\bwarrant(?:y|ies)\b", re.I),
    "subscription": re.compile(r"\bsubscription|membership|plan renew|auto.?renew\b", re.I),
    "bill": re.compile(r"\bbill|invoice|payment due|utility\b", re.I),
    "insurance": re.compile(r"\binsurance|policy|premium\b", re.I),
}
MONEY = re.compile(r"\b(KES|KSh|USD|EUR|GBP|\$|€|£)\s?([\d,]+(?:\.\d{1,2})?)\b", re.I)


def _inside_root(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT)
        return True
    except (ValueError, OSError):
        return False


def _resolve_folder(relative: str) -> Path:
    # Reject absolute paths and traversal before resolving to reduce ambiguity.
    candidate_part = Path(relative or ".")
    if candidate_part.is_absolute() or ".." in candidate_part.parts:
        raise ValueError("folder must be a relative path inside the authorized root")
    target = (ROOT / candidate_part).resolve()
    if not _inside_root(target) or not target.is_dir():
        raise ValueError("folder was not found inside the authorized root")
    return target


def _read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    return " ".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))


def _extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if not text.strip():
            raise ValueError("PDF contains no selectable text; OCR support is not enabled")
        return text
    if suffix == ".docx":
        return _read_docx(path)
    return path.read_text(encoding="utf-8", errors="replace")


def _parse_date(kind: str, match: re.Match[str]) -> date | None:
    try:
        if kind == "iso":
            year, month, day = (int(part) for part in match.groups())
        elif kind == "month_first":
            month, day, year = MONTHS[match.group(1).lower()], int(match.group(2)), int(match.group(3))
        elif kind == "day_first":
            day, month, year = int(match.group(1)), MONTHS[match.group(2).lower()], int(match.group(3))
        else:
            day, month, year = (int(part) for part in match.groups())
        return date(year, month, day)
    except (ValueError, KeyError):
        return None


def _analyze_text(text: str, filename: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for pattern_kind, pattern in DATE_PATTERNS:
        for match in pattern.finditer(text):
            parsed = _parse_date(pattern_kind, match)
            if not parsed:
                continue
            start, end = match.span()
            context = text[max(0, start - 100):min(len(text), end + 100)]
            if not DATE_TERMS.search(context):
                continue
            key = (filename, parsed.isoformat())
            if key in seen:
                continue
            seen.add(key)
            kind = next((label for label, regex in KIND_TERMS.items() if regex.search(context)), "renewal")
            nearby_money = MONEY.search(context)
            amount = None
            if nearby_money:
                amount = {"currency": nearby_money.group(1).upper(), "value": nearby_money.group(2).replace(",", "")}
            found.append({
                "date": parsed.isoformat(), "category": kind,
                "source": filename, "matched_text": match.group(0),
                "context": re.sub(r"\s+", " ", context).strip()[:240],
                "amount": amount, "status": "overdue" if parsed < date.today() else "upcoming",
            })
    return found


def _list_files(folder: Path) -> tuple[list[Path], int]:
    collected: list[Path] = []
    skipped = 0
    for current, dirs, filenames in os.walk(folder, followlinks=False):
        current_path = Path(current)
        dirs[:] = [name for name in dirs if not name.startswith(".") and not (current_path / name).is_symlink()]
        for filename in filenames:
            path = current_path / filename
            if filename.startswith(".") or path.is_symlink() or path.suffix.lower() not in SUPPORTED:
                continue
            if not _inside_root(path):
                skipped += 1
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    skipped += 1
                    continue
            except OSError:
                skipped += 1
                continue
            collected.append(path)
            if len(collected) >= MAX_FILES:
                return collected, skipped
    return collected, skipped


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "renewwise", "read_only": True, "root_configured": ROOT.is_dir()})


@app.post("/api/analyze")
def analyze():
    body = request.get_json(silent=True) or {}
    try:
        folder = _resolve_folder(str(body.get("folder", ".")))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    files, skipped = _list_files(folder)
    items: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for path in files:
        relative_name = path.relative_to(folder).as_posix()
        try:
            items.extend(_analyze_text(_extract_text(path), relative_name))
        except (OSError, ValueError, zipfile.BadZipFile, KeyError) as exc:
            reason = str(exc) if isinstance(exc, ValueError) else f"Could not read this file ({type(exc).__name__})."
            errors.append({"source": relative_name, "reason": reason})
        except Exception as exc:
            # A corrupt/unsupported document should not fail the whole folder scan.
            errors.append({"source": relative_name, "reason": f"Could not analyze this file ({type(exc).__name__})."})
    items.sort(key=lambda item: item["date"])
    return jsonify({
        "folder": "." if folder == ROOT else folder.relative_to(ROOT).as_posix(),
        "documents_scanned": len(files), "items": items, "read_errors": errors,
        "files_skipped": skipped, "read_only": True,
        "date_note": "Numeric dates are interpreted as DD/MM/YYYY. Confirm each result against its source document.",
        "privacy_note": "Documents are processed locally for this request; results are not stored or sent to an AI service.",
    })


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Request body is too large."}), 413


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    app.run(host=os.environ.get("RENEWWISE_HOST", "127.0.0.1"), port=int(os.environ.get("RENEWWISE_PORT", "5050")), debug=False)
