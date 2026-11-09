"""The fit check: one or two AI-written sentences on why each of the top sponsors, talks or speakers may suit this outlet.

It is asked for separately, after the results are already on the page, so a slow or absent model never holds
a result up: any trouble here means only that no fit check is shown. It changes no ranking.

The model is one the Elastic project already offers through its inference service, reached with the same
connection the searches use: there is no extra key. What is sent to it: what the outlet always covers, what
it came to find, and the chosen items' own text from the catalogue. Nothing else, and nothing is stored.
The instructions it is given are in fitcheck_instructions.md, beside this file.
"""
import json, re
from pathlib import Path
from . import config, engine, tracing

INSTRUCTIONS_FILE = Path(__file__).with_name("fitcheck_instructions.md")
_LINE = re.compile(r"^\s*(\d+)\s*[:.)]\s*(.+?)\s*$")


KINDS = {"sponsor": "SPONSOR", "talk": "TALK", "speaker": "SPEAKER"}   # what the fit check can be asked about


def item_texts(client, kind: str, ids: list[str]) -> dict[str, dict]:
    """Each item's own text, read from the catalogue by its id (never taken from the page; names can repeat):
    its name, whether it is a start-up (sponsors only), and its passages in order."""
    hits = client.search(index=config.PROGRAMME_INDEX, size=200, sort=[{"passage_no": "asc"}],
                         source_includes=["record_id", "name", "text", "startup", "passage_no"],
                         query={"bool": {"filter": [{"term": {"kind": kind}}, {"terms": {"record_id": ids}}]}})["hits"]["hits"]
    found = {}
    for s in (h["_source"] for h in hits):
        rec = found.setdefault(s["record_id"], {"name": s["name"], "startup": bool(s.get("startup")), "pieces": {}})
        prefix = f"{s['name']}. "   # every passage starts with the name; the page shows it as the heading
        rec["pieces"].setdefault(s["passage_no"], s["text"][len(prefix):] if s["text"].startswith(prefix) else s["text"])
    return {rid: {"name": rec["name"], "startup": rec["startup"],
                  "passage": " ".join(rec["pieces"][n] for n in sorted(rec["pieces"]))[:config.FITCHECK_PASSAGE_CHARS]}
            for rid, rec in found.items()}


def _question(beat: str, assignment: str, kind: str, ids: list[str], texts: dict[str, dict]) -> str:
    lines = ["WHAT THE OUTLET ALWAYS COVERS:", beat, "", "WHAT IT CAME TO THIS CONFERENCE TO FIND:", assignment or "(nothing given)", ""]
    for i, rid in enumerate(ids, 1):
        t = texts[rid]
        start_up = (" (a start-up)" if t["startup"] else " (not a start-up)") if kind == "sponsor" else ""
        lines += [f"{KINDS[kind]} {i}: {t['name']}{start_up}", t["passage"], ""]
    return "\n".join(lines)


def _said(stream: str) -> str:
    """The model's words, put back together from Elastic's streamed answer."""
    words = []
    for line in stream.splitlines():
        line = line.lstrip("﻿")
        if not line.startswith("data:") or line[5:].strip() in ("", "[DONE]"):
            continue
        for choice in json.loads(line[5:]).get("choices") or []:
            words.append((choice.get("delta") or {}).get("content") or "")
    return "".join(words)


def _ask_model(client, question: str) -> str:
    headers = {"accept": "application/vnd.elasticsearch+json; compatible-with=9",
               "content-type": "application/vnd.elasticsearch+json; compatible-with=9"}
    answer = client.options(request_timeout=config.FITCHECK_LIMIT, max_retries=0).perform_request(
        "POST", f"/_inference/chat_completion/{config.FITCHECK_ENDPOINT}/_stream", headers=headers,
        body={"messages": [{"role": "system", "content": INSTRUCTIONS_FILE.read_text(encoding="utf-8")},
                           {"role": "user", "content": question}],
              "temperature": 0, "max_completion_tokens": config.FITCHECK_MAX_TOKENS})
    return _said(str(answer.body))


def _sentences(said: str, count: int) -> list[str] | None:
    """The answer, one piece per sponsor in order; None unless it is exactly what was asked for."""
    by_number = {}
    for line in said.splitlines():
        m = _LINE.match(line)
        if m:
            by_number.setdefault(int(m.group(1)), m.group(2))
    out = [by_number.get(i) for i in range(1, count + 1)]
    if len(by_number) != count or not all(out) or any(len(s.split()) > config.FITCHECK_MAX_WORDS for s in out):
        return None
    return out


def check(client, beat: str, assignment: str, kind: str, ids: list[str]) -> list[dict] | None:
    """Why each of these sponsors, talks or speakers (by id, in the search's order) may suit this outlet:
    [{id, name, startup, why, passage}], or None when there is nothing safe to show (no model here, an item not
    in the catalogue, a slow or malformed answer)."""
    ids = list(dict.fromkeys(i for i in ids if i))[:config.FITCHECK_TOP]
    if kind not in KINDS or engine.where() != "cloud" or not beat or not ids:   # the laptop's own engine has no model
        return None
    with tracing.span("fit check: passages", kind=kind):
        texts = item_texts(client, kind, ids)
    if any(rid not in texts for rid in ids):
        return None
    with tracing.span("fit check: model", kind=kind):
        said = _ask_model(client, _question(beat, assignment, kind, ids, texts))
    sentences = _sentences(said, len(ids))
    if not sentences:
        return None
    return [{"id": rid, "name": texts[rid]["name"], "startup": kind == "sponsor" and texts[rid]["startup"], "why": why,
             "passage": texts[rid]["passage"]} for rid, why in zip(ids, sentences)]
