"""Turn one spreadsheet row into a record and its passages.

A record's text is written out as plain sentences, then cut into passages of about
PASSAGE_PIECES word-pieces (the meaning model's own units) on sentence boundaries, so the model
reads every word of every passage. Short leftovers are folded into the passage before them, so
one-line fields never become passages of their own. Every passage begins with the record's name,
so a passage read on its own still says what it is about.
"""
import re
from . import config

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_tokeniser = None


def pieces(text: str) -> int:
    """How many word-pieces the meaning model sees in this text (without its two markers)."""
    global _tokeniser
    if _tokeniser is None:
        from transformers import AutoTokenizer
        _tokeniser = AutoTokenizer.from_pretrained(config.MODEL_NAME)
    return len(_tokeniser.tokenize(text))


def split_list(cell: str) -> list[str]:
    return [p.strip() for p in cell.split(config.LIST_SEPARATOR) if p.strip()] if cell else []


def _sentence(label: str, value: str) -> str:
    """A labelled sentence, or nothing if the value is empty."""
    value = (value or "").strip()
    if not value:
        return ""
    # a list cell ("Platform teams; Security teams" or "Product A.; Product B.") reads as sentences
    value = re.sub(r"\.?;\s+", ". ", value)
    if value[-1] not in ".!?":
        value += "."
    return f"{label}: {value}" if label else value


def _tidy(text: str) -> str:
    """Remove the doubled punctuation that joining cells makes ("Now What?. Track", "Registry:. Lens")."""
    text = re.sub(r"[:\s]+\.(?=\s|$)", ".", text)           # "Product:." and "Product: ." -> "Product."
    text = re.sub(r"(?<=\w)\.\.(?=\s|$)", ".", text)          # "organizer.." -> "organizer." (an ellipsis stays)
    return re.sub(r"([?!])\.(?=\s|$)", r"\1", text)          # "Now What?." -> "Now What?"


def _real(value: str) -> str:
    """The cell's value, or nothing if it is a placeholder ("TODO", "none", ".")."""
    value = (value or "").strip()
    return "" if value.lower() in config.PLACEHOLDERS or len(value) < 3 else value


def cut(text: str, budget: int = config.PASSAGE_PIECES, min_tail: int = config.MIN_TAIL_PIECES,
        limit: int = config.MODEL_MAX_PIECES) -> list[str]:
    """Cut text into passages of at most `budget` word-pieces, on sentence boundaries.

    A short leftover is folded into the passage before it only if the two together stay within
    `limit`, so no passage ever runs past what the model reads."""
    sentences = [s for s in _SENTENCE_END.split(text.strip()) if s]
    passages, sizes, current, count = [], [], [], 0

    def close():
        nonlocal current, count
        if current:
            passages.append(" ".join(current)); sizes.append(count)
        current, count = [], 0

    for s in sentences:
        n = pieces(s)
        if n > budget:  # one very long sentence: cut it by words, each piece within the budget
            close()
            for w in s.split():
                m = pieces(w)
                if count + m > budget and current:
                    close()
                current.append(w); count += m
            continue
        if count + n > budget and current:
            close()
        current.append(s); count += n
    close()
    if len(passages) > 1 and sizes[-1] < min_tail and sizes[-2] + sizes[-1] <= limit:
        passages[-2:] = [" ".join(passages[-2:])]
    return passages or [""]


def _with_name(name: str, body: str) -> list[str]:
    """Cut the body so that each passage, with the name in front, still fits what the model reads."""
    name = name.strip()
    lead = name if name[-1:] in ".!?" else f"{name}."
    room = config.MODEL_MAX_PIECES - pieces(lead)
    body = _tidy(body)
    return [_tidy(f"{lead} {p}".strip()) for p in cut(body, min(config.PASSAGE_PIECES, room), limit=room)]


def session_record(row: dict) -> dict:
    """A talk or an event from sessions.csv."""
    speakers = split_list(row["speakers"]); companies = split_list(row["companies"]); topics = split_list(row["topics"])
    body = " ".join(filter(None, [
        _sentence("Track", row["track"]),
        _sentence("When", f"{row['day']}, {row['time']}" if row["day"] and row["time"] else row["day"]),
        _sentence("Speakers", ", ".join(speakers)) if speakers else "",
        _sentence("Companies", ", ".join(companies)) if companies else "",
        _sentence("Topics", ", ".join(topics)) if topics else "",
        _sentence("", row["description"]),
    ]))
    return {
        "record_id": row["id"], "kind": row["kind"], "name": row["title"],
        "passages": _with_name(row["title"], body),
        "track": row["track"], "day": row["day"], "date": row["date"], "time": row["time"],
        "room": row["room"], "level": row["level"],
        "speakers": speakers, "companies": companies, "topics": topics,
    }


def speaker_record(row: dict) -> dict:
    companies = split_list(row["companies"]); talks = split_list(row["talks"])
    job = _real(row["job"])
    if job.lower() == row["name"].strip().lower():   # two speakers' job cells hold their own name
        job = ""
    body = " ".join(filter(None, [
        _sentence("", f"{job} at {', '.join(companies)}" if job and companies else job or (", ".join(companies))),
        _sentence("Speaking on", "; ".join(talks)) if talks else "",
        _sentence("", _real(row["bio"])),
    ]))
    return {
        "record_id": row["id"], "kind": "speaker", "name": row["name"],
        "passages": _with_name(row["name"], body),
        "job": job, "companies": companies, "talks": talks,
    }


def sponsor_record(row: dict) -> dict:
    topics = split_list(row["conference_topics"])
    tier = row["tier"]
    body = " ".join(filter(None, [
        _sentence("", f"A {tier} sponsor" + (f" at booth {row['booth']}" if row["booth"] else "")),
        _sentence("Conference topics", ", ".join(topics)) if topics else "",
        _sentence("", row["conference_description"]),
        _sentence("", row["ai_what_they_do"]),
        _sentence("Who it is for", row["ai_who_its_for"]),
        _sentence("Industries", row["ai_industries"]),
        _sentence("Problems solved", row["ai_problems_solved"]),
        _sentence("Products", row["ai_products"]),
        _sentence("Open source", row["ai_open_source"]),
        _sentence("At KubeCon", row["ai_at_kubecon"]),
    ]))
    return {
        "record_id": row["id"], "kind": "sponsor", "name": row["name"],
        "passages": _with_name(row["name"], body),
        "tier": tier, "startup": tier.lower().startswith("start"), "booth": row["booth"],
        "topics": topics, "website": row["website"], "source_quality": row["ai_source_quality"],
    }


def outlet_records(row: dict) -> list[dict]:
    """An outlet gives one record for its standing beat and, if it has one, one for its assignment."""
    common = {
        "record_id": row["id"], "kind": "outlet", "name": row["name"],
        "real_or_sample": row["real_or_sample"], "sample": row["real_or_sample"].upper().startswith("SAMPLE"),
        "has_assignment": bool(row["kubecon_assignment"].strip()),
        "website": row["website"], "written_by": row["written_by"],
    }
    beat = " ".join(filter(None, [
        _sentence("", row["what_they_cover"]),
        _sentence("Beat", row["beat"]),
        _sentence("Audience", row["audience"]),
        _sentence("Formats", row["formats"]),
        _sentence("Shows and sections", row["shows_or_sections"]),
        _sentence("Region", row["region"]),
    ]))
    records = [{**common, "part": "beat", "passages": _with_name(row["name"], beat)}]
    if common["has_assignment"]:
        records.append({**common, "part": "assignment",
                        "passages": _with_name(row["name"], _sentence("KubeCon assignment", row["kubecon_assignment"]))})
    return records
