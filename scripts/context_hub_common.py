#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import getpass
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

KNOWN_PROJECT_HASHTAGS = {
    "#youtube",
    "#video",
    "#tutorial",
    "#aibrief",
    "#audio",
    "#news",
    "#armor",
    "#scripture",
    "#bible",
    "#fighterverses",
    "#harmony",
    "#piano",
    "#music",
    "#conductor",
    "#monitor",
    "#agents",
    "#dashboard",
    "#productivity",
    "#virtualmanager",
    "#visor",
    "#cfa",
}

DOMAIN_TAG_MAP = {
    "youtube.com": ["#youtube", "#video"],
    "youtu.be": ["#youtube", "#video"],
    "substack.com": ["#aibrief", "#news"],
    "x.com": ["#aibrief", "#youtube"],
    "twitter.com": ["#aibrief", "#youtube"],
    "github.com": ["#conductor", "#agents"],
    "arxiv.org": ["#aibrief", "#news"],
    "techcrunch.com": ["#aibrief", "#news"],
}

KEYWORD_TAG_RULES = {
    "keyboard": ["#productivity"],
    "shortcut": ["#productivity"],
    "avatar": ["#youtube"],
    "clone": ["#youtube"],
    "brief": ["#aibrief"],
    "audio": ["#audio"],
    "verse": ["#armor", "#scripture"],
    "bible": ["#armor", "#bible"],
    "fighter": ["#fighterverses", "#armor"],
    "dashboard": ["#dashboard", "#productivity"],
    "restaurant": ["#virtualmanager", "#cfa"],
}

TEXT_EXTENSIONS = {".md", ".txt", ".html", ".htm", ".rtf", ".json", ".csv", ".xml", ".yaml", ".yml"}
URL_EXTENSIONS = {".url", ".webloc"}


@dataclass
class ResolvedPaths:
    user: str
    icloud_root: Path
    repo_root: Path
    riley_root: Path
    context_hub: Path
    runtime_root: Path
    runtime_index_dir: Path
    runtime_context_dir: Path
    lock_dir: Path
    captures_root: Path
    captures_inbox: Path
    captures_processed: Path
    captures_text: Path
    rileyshare_captures: Path | None
    capture_roots: list[Path]
    inbox_roots: list[Path]
    processed_roots: list[Path]
    index_dir: Path
    context_dir: Path
    digest_dir: Path
    archive_dir: Path
    state_json: Path
    index_sqlite: Path
    index_ndjson: Path
    ingest_log: Path
    candidates_md: Path
    promotions_md: Path
    promotions_state: Path
    riley_context: Path

    def as_dict(self) -> dict[str, Any]:
        return {
            "user": self.user,
            "icloud_root": str(self.icloud_root),
            "repo_root": str(self.repo_root),
            "riley_root": str(self.riley_root),
            "context_hub": str(self.context_hub),
            "runtime_root": str(self.runtime_root),
            "runtime_index_dir": str(self.runtime_index_dir),
            "runtime_context_dir": str(self.runtime_context_dir),
            "lock_dir": str(self.lock_dir),
            "captures_root": str(self.captures_root),
            "captures_inbox": str(self.captures_inbox),
            "captures_processed": str(self.captures_processed),
            "captures_text": str(self.captures_text),
            "rileyshare_captures": str(self.rileyshare_captures) if self.rileyshare_captures else None,
            "capture_roots": [str(p) for p in self.capture_roots],
            "inbox_roots": [str(p) for p in self.inbox_roots],
            "processed_roots": [str(p) for p in self.processed_roots],
            "index_dir": str(self.index_dir),
            "context_dir": str(self.context_dir),
            "digest_dir": str(self.digest_dir),
            "archive_dir": str(self.archive_dir),
            "state_json": str(self.state_json),
            "index_sqlite": str(self.index_sqlite),
            "index_ndjson": str(self.index_ndjson),
            "ingest_log": str(self.ingest_log),
            "candidates_md": str(self.candidates_md),
            "promotions_md": str(self.promotions_md),
            "promotions_state": str(self.promotions_state),
            "riley_context": str(self.riley_context),
        }


def now_local() -> datetime:
    return datetime.now().astimezone()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def compute_fingerprint(size: int, mtime: float) -> str:
    return f"{size}:{int(mtime * 1_000_000_000)}"


def file_type_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in TEXT_EXTENSIONS:
        return "text"
    if ext in URL_EXTENSIONS:
        return "url"
    if ext == ".pdf":
        return "pdf"
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic"}:
        return "image"
    if ext in {".mp3", ".wav", ".m4a", ".aac", ".flac"}:
        return "audio"
    if ext in {".mp4", ".mov", ".mkv", ".avi", ".webm"}:
        return "video"
    return "other"


def rel_to_root(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def path_in_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def parse_meta(sidecar: Path) -> dict[str, Any]:
    if not sidecar.exists():
        return {}
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception:
        return {}


def extract_hashtags(text: str) -> set[str]:
    return {tag.lower() for tag in re.findall(r"#[A-Za-z0-9_:-]+", text)}


def canonicalize_url(url: str) -> str:
    raw = (url or "").strip()
    if not raw:
        return ""
    try:
        parts = urlsplit(raw)
    except Exception:
        return raw

    scheme = (parts.scheme or "https").lower()
    netloc = parts.netloc.lower()
    path = parts.path or ""
    if path.endswith("/") and path != "/":
        path = path.rstrip("/")

    query_pairs = parse_qsl(parts.query, keep_blank_values=True)
    query_pairs.sort()
    query = urlencode(query_pairs)

    return urlunsplit((scheme, netloc, path, query, ""))


def infer_tags(path_rel: str, filename: str, text: str, meta_tags: list[str] | None, url: str | None = None) -> list[str]:
    tags: set[str] = set()

    for raw in meta_tags or []:
        if isinstance(raw, str) and raw.strip():
            tag = raw.strip()
            if not tag.startswith("#"):
                tag = f"#{tag}"
            tags.add(tag.lower())

    combined = f"{path_rel} {filename} {text}".lower()

    for found in extract_hashtags(combined):
        tags.add(found)

    for keyword, mapped in KEYWORD_TAG_RULES.items():
        if keyword in combined:
            tags.update(t.lower() for t in mapped)

    if "/rileyprojects/" in path_rel.lower():
        folder_hint = path_rel.lower().split("/rileyprojects/", 1)[1].split("/", 1)[0]
        if "youtube" in folder_hint:
            tags.update({"#youtube", "#video"})
        if "armor" in folder_hint:
            tags.update({"#armor", "#scripture"})
        if "dashboard" in folder_hint:
            tags.update({"#dashboard", "#productivity"})
        if "cfa" in folder_hint:
            tags.update({"#cfa", "#virtualmanager"})

    domain_source = (url or "") + " " + combined
    for domain, mapped in DOMAIN_TAG_MAP.items():
        if domain in domain_source:
            tags.update(t.lower() for t in mapped)

    return sorted(tags)


def _default_runtime_root() -> Path:
    xdg_data_home = os.environ.get("XDG_DATA_HOME", "").strip()
    if xdg_data_home:
        return Path(xdg_data_home).expanduser() / "rileyfile" / "runtime"
    return Path.home() / ".rileyfile" / "runtime"


def resolve_paths(
    require_existing_root: bool = True,
    riley_root: str | Path | None = None,
    runtime_root: str | Path | None = None,
) -> ResolvedPaths:
    user = getpass.getuser()
    repo_root = Path(__file__).resolve().parents[1]
    icloud_root = Path(f"/Users/{user}/Library/Mobile Documents/com~apple~CloudDocs")

    if riley_root is not None:
        selected_root = Path(riley_root).expanduser().resolve()
    else:
        override = os.environ.get("RILEYFILE_ROOT", "").strip()
        selected_root = Path(override).expanduser().resolve() if override else repo_root.resolve()

    if require_existing_root and not selected_root.exists():
        raise FileNotFoundError(f"RileyFile root missing: {selected_root}")

    if runtime_root is not None:
        selected_runtime_root = Path(runtime_root).expanduser().resolve()
    else:
        runtime_override = os.environ.get("RILEYFILE_RUNTIME_ROOT", "").strip()
        selected_runtime_root = (
            Path(runtime_override).expanduser().resolve() if runtime_override else _default_runtime_root().resolve()
        )

    context_hub = selected_root / "CONTEXT_HUB"
    runtime_index_dir = selected_runtime_root / "index"
    runtime_context_dir = selected_runtime_root / "context"
    lock_dir = selected_runtime_root / ".lock"
    captures_root = context_hub / "captures"
    captures_inbox = captures_root / "inbox"
    captures_processed = captures_root / "_processed"
    captures_text = captures_root / "_text"

    rileyshare_captures = selected_root / "RileyShare" / "captures"
    has_rileyshare_captures = rileyshare_captures.exists()

    capture_roots: list[Path] = [captures_root]
    inbox_roots: list[Path] = [captures_inbox]
    processed_roots: list[Path] = [captures_processed]

    if has_rileyshare_captures:
        capture_roots.append(rileyshare_captures)
        inbox_roots.append(rileyshare_captures / "inbox")
        processed_roots.append(rileyshare_captures / "_processed")

    index_dir = context_hub / "index"
    context_dir = context_hub / "context"
    digest_dir = context_dir / "_daily_digest"
    archive_dir = context_dir / "_archive"

    state_json = runtime_context_dir / ".state.json"
    index_sqlite = runtime_index_dir / "RILEY_INDEX.sqlite"
    index_ndjson = runtime_index_dir / "RILEY_INDEX.ndjson"
    ingest_log = context_dir / "_ingest_log.ndjson"
    candidates_md = context_dir / "_candidates.md"
    promotions_md = context_dir / "_promotions.md"
    promotions_state = runtime_context_dir / ".promotions_state.json"

    riley_context = selected_root / "RILEY_CONTEXT.md"

    must_create = [
        context_hub,
        selected_runtime_root,
        runtime_index_dir,
        runtime_context_dir,
        captures_root,
        captures_inbox,
        captures_processed,
        captures_text,
        index_dir,
        context_dir,
        digest_dir,
        archive_dir,
        context_hub / "scripts",
    ]

    if has_rileyshare_captures:
        must_create.extend([
            rileyshare_captures / "inbox",
            rileyshare_captures / "_processed",
        ])

    for p in must_create:
        p.mkdir(parents=True, exist_ok=True)

    if not ingest_log.exists():
        ingest_log.write_text("", encoding="utf-8")
    if not candidates_md.exists():
        candidates_md.write_text("# Context Candidates\n\n- No new ingest entries.\n", encoding="utf-8")
    if not promotions_md.exists():
        promotions_md.write_text("# Context Promotions\n\n- No pending promotions.\n", encoding="utf-8")

    return ResolvedPaths(
        user=user,
        icloud_root=icloud_root,
        repo_root=repo_root,
        riley_root=selected_root,
        context_hub=context_hub,
        runtime_root=selected_runtime_root,
        runtime_index_dir=runtime_index_dir,
        runtime_context_dir=runtime_context_dir,
        lock_dir=lock_dir,
        captures_root=captures_root,
        captures_inbox=captures_inbox,
        captures_processed=captures_processed,
        captures_text=captures_text,
        rileyshare_captures=rileyshare_captures if has_rileyshare_captures else None,
        capture_roots=capture_roots,
        inbox_roots=inbox_roots,
        processed_roots=processed_roots,
        index_dir=index_dir,
        context_dir=context_dir,
        digest_dir=digest_dir,
        archive_dir=archive_dir,
        state_json=state_json,
        index_sqlite=index_sqlite,
        index_ndjson=index_ndjson,
        ingest_log=ingest_log,
        candidates_md=candidates_md,
        promotions_md=promotions_md,
        promotions_state=promotions_state,
        riley_context=riley_context,
    )


def open_db(index_sqlite: Path) -> sqlite3.Connection:
    index_sqlite.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(index_sqlite)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            sha TEXT,
            fingerprint TEXT,
            size INTEGER,
            mtime REAL,
            type TEXT,
            first_seen TEXT,
            last_seen TEXT,
            extracted_text_path TEXT,
            tags_json TEXT,
            note TEXT,
            source_app TEXT,
            captured_at TEXT,
            extraction_error TEXT
        )
        """
    )

    cols = {row[1] for row in conn.execute("PRAGMA table_info(files)").fetchall()}
    if "fingerprint" not in cols:
        conn.execute("ALTER TABLE files ADD COLUMN fingerprint TEXT")

    conn.execute("CREATE INDEX IF NOT EXISTS idx_files_sha ON files(sha)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_files_mtime ON files(mtime)")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )
    conn.commit()
    return conn


def db_get_state(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM state WHERE key=?", (key,)).fetchone()
    return row[0] if row else None


def db_set_state(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO state(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )


def list_files_for_index(root: Path) -> list[Path]:
    out: list[Path] = []
    skip_dirs = {".git", "node_modules", "__pycache__", ".lock"}
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_parts = rel_to_root(current, root).split("/") if current != root else []
        if any(part in skip_dirs for part in rel_parts):
            continue
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in filenames:
            p = current / name
            if p.name.startswith(".") and p.suffix.lower() in {".swp", ".tmp"}:
                continue
            out.append(p)
    out.sort(key=lambda p: p.as_posix())
    return out


def try_import_sqlite() -> bool:
    try:
        import sqlite3  # noqa: F401
        return True
    except Exception:
        return False


def last_24h_cutoff() -> datetime:
    return now_local() - timedelta(hours=24)
