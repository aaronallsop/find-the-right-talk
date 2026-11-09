"""The match: an outlet's own profile searches the programme.

    python -m ftrt.match "Breach Chronicle"                          # blended: top sponsors, talks and speakers
    python -m ftrt.match --mode compare --kind sponsor -n 10 "Hello World Gazette"
    python -m ftrt.match --list                                      # the 14 outlets
    options: --mode words|meaning|elser|jina|blended|reranked|compare, -n 5 (how many of each kind), --kind sponsor|talk|speaker, --startups

An outlet has a standing beat (what it always covers) and, for six of them, a KubeCon assignment
(what it came to find). Each part searches the programme on its own, by meaning with the part's
stored numbers, by words with its text, and (in Elastic Cloud) by Elastic's own model, ELSER, with
its text; the rankings are merged by reciprocal rank fusion,
the assignment's votes counting double (Aaron, 8 November). An outlet with no assignment is
matched on its beat alone. Events (coffee breaks, registration) are left out: they are not stories.
"""
from . import quiet  # noqa: F401  (first: model offline, library chatter off)
import argparse, textwrap
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from . import config, passages, tracing
from .engine import connect
from .search import ELSER_MISSING, MISSING, RERANK_MISSING, _fetch_size, _fields, _group, embed, filters, fuse, jina_question, rerank, search_elser, search_jina, search_meaning_vector, with_passages

MATCH_KINDS = ("sponsor", "talk", "speaker")


def _mean(vectors) -> list[float]:
    """One set of numbers for a part that was cut into several passages: their average, rescaled."""
    v = np.mean(np.asarray(vectors, dtype=float), axis=0)
    return (v / np.linalg.norm(v)).tolist()


def outlet_names(client) -> dict[str, str]:
    r = client.search(index=config.OUTLETS_INDEX, size=200, source_includes=["record_id", "name"])
    return {h["_source"]["record_id"]: h["_source"]["name"] for h in r["hits"]["hits"]}


def find_outlet(client, wanted: str) -> str:
    """An outlet's id, from its id or any part of its name."""
    names = outlet_names(client)
    if wanted in names:
        return wanted
    hits = [rid for rid, name in names.items() if wanted.lower() in name.lower()]
    if len(hits) != 1:
        raise SystemExit(f"{'No' if not hits else 'More than one'} outlet matches {wanted!r}. Try --list.")
    return hits[0]


def stored_parts(client, outlet_id: str) -> tuple[str, dict]:
    """The outlet's name and its parts as loaded: {"beat": {...}, "assignment": {...}}, each with the
    part's words (without the name in front) and one set of meaning numbers."""
    r = client.search(index=config.OUTLETS_INDEX, query={"term": {"record_id": outlet_id}}, size=50,
                      source={"exclude_vectors": False}, sort=[{"passage_no": "asc"}])
    hits = [h["_source"] for h in r["hits"]["hits"]]
    if not hits:
        raise SystemExit(f"No outlet {outlet_id!r} in {config.OUTLETS_INDEX}. Run the loader first.")
    name, parts = hits[0]["name"], {}
    for part in ("beat", "assignment"):
        mine = [h for h in hits if h["part"] == part]
        if mine:
            prefix = f"{name}. "
            text = " ".join(h["text"][len(prefix):] if h["text"].startswith(prefix) else h["text"] for h in mine)
            parts[part] = {"text": text, "vector": _mean([h["vector"] for h in mine])}
    return name, parts


def parts_from_text(texts: dict[str, str]) -> dict:
    """Parts from plain text ({"beat": ..., "assignment": ...}, or the flip's {"does": ..., "showing": ...}),
    cut and turned into numbers as the loader does it. Empty parts are left out. The text is used for
    this one search and not kept anywhere."""
    parts = {}
    for part, text in texts.items():
        if text:
            cut = passages.cut(passages._tidy(text))
            parts[part] = {"text": " ".join(cut), "vector": _mean([embed(p) for p in cut])}
    return parts


def typed_parts(beat: str, assignment: str = "") -> dict:
    """The match's parts from the page's two press boxes."""
    return parts_from_text({"beat": passages._sentence("", beat),
                            "assignment": passages._sentence("KubeCon assignment", assignment)})


def match(client, parts: dict, n: int = 10, kind: str | None = None, startups: bool = False,
          index: str = config.PROGRAMME_INDEX) -> dict[str, list[dict]]:
    """Rank the programme for these parts: {"words": [...], "meaning": [...], "elser": [...], "jina": [...], "blended": [...]}.
    "elser" and "jina" (with the part's text as the question) are there only in Elastic Cloud.
    Each result carries `via`: which part, and which way, gave it its best position."""
    filt = filters(kind, startups)
    if not kind:
        filt.append({"terms": {"kind": list(MATCH_KINDS)}})
    depth = max(n, config.BLEND_DEPTH)   # fixed, so the order does not change with how many are shown
    # the long lists come back without passage text; only the results kept get theirs (with_passages, below)
    ways = {"words": lambda p: search_words_loose(client, p["text"], depth, index, filt, passages=False),
            "meaning": lambda p: search_meaning_vector(client, p["vector"], depth, index, filt, passages=False),
            "elser": lambda p: search_elser(client, p["text"], depth, index, filt, passages=False),
            "jina": lambda p: search_jina(client, p["text"], depth, index, filt, vector=p.get("jina"), passages=False)}
    # every part asks every way at the same time (they do not depend on each other); the lists are then put
    # together in a fixed order, so the result is exactly what asking one after another gives, only sooner
    jobs = [(part, way) for part in parts for way in ways]
    def ask(job):   # one part, one way: a step of its own in the trace
        with tracing.span(f"{job[1]} search", part=job[0], kind=kind or "all") as s:
            found = ways[job[1]](parts[job[0]])
            tracing.note(s, found)
            return found
    with tracing.span("match", kind=kind or "all", parts=len(parts), startups=startups), \
         ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        answers = dict(zip(jobs, pool.map(tracing.carry(ask), jobs)))
    lists = {way: [] for way in ways}
    for part, way in jobs:
        results = answers[(part, way)]
        if results is not None:   # ELSER is skipped on the laptop engine
            lists[way].append(([{**r, "via": f"{PART_NAMES[part]}, by {WAY_NAMES[way]}"} for r in results], config.MATCH_WEIGHTS[part]))
    with tracing.span("fetch passages", kind=kind or "all"):
        out = {way: with_passages(client, fuse(ls, n)) for way, ls in lists.items() if ls}
        blended = with_passages(client, fuse([l for ls in lists.values() for l in ls], max(n, config.RERANK_TOP)))
    out["blended"] = blended[:n]
    # Elastic's re-ranker reads the profile (its KubeCon part first) against each of the blended top passages
    question = " ".join(parts[p]["text"] for p in sorted(parts, key=lambda p: -config.MATCH_WEIGHTS[p]))
    with tracing.span("re-rank", kind=kind or "all") as s:
        reordered = rerank(client, question, blended)
        tracing.note(s, reordered)
    if reordered is not None:   # Elastic Cloud only, and only when it answers
        out["reranked"] = [{**r, "via": "Elastic's re-ranker"} for r in reordered[:n]]
    return out


WAY_NAMES = {"words": "words", "meaning": "meaning", "elser": "Elastic's ELSER", "jina": "Jina embeddings"}


def with_jina(client, parts: dict) -> dict:
    """The parts with each one's Jina numbers asked for once, so the several kinds of one match share them.
    Kept only for this request; a part Jina does not answer for simply has none (Jina is then left out)."""
    with tracing.span("jina question", parts=len(parts)), ThreadPoolExecutor(max_workers=len(parts)) as pool:
        vectors = dict(zip(parts, pool.map(tracing.carry(lambda part: jina_question(client, parts[part]["text"])), parts)))
    return {part: {**p, "jina": vectors[part]} for part, p in parts.items()}
PART_NAMES = {"beat": "what it always covers", "assignment": "its KubeCon assignment",
              "does": "what it does", "showing": "what it shows at KubeCon"}


def search_words_loose(client, text: str, n: int, index: str, filt: list, passages: bool = True) -> list[dict]:
    """Words search with a whole profile as the question. A profile is long, so requiring most of
    its words (as the typed search does) would find nothing. Elasticsearch's "more like this" picks
    the profile's most telling words (frequent in it, rare in the programme) and searches for those."""
    like = {"more_like_this": {"fields": ["text"], "like": text, "min_term_freq": 1,
                               "max_query_terms": config.MATCH_WORDS_TERMS, "min_doc_freq": 2}}
    body = {"bool": {"must": like, "filter": filt}}
    r = client.search(index=index, query=body, size=_fetch_size(n), source_includes=_fields(passages))
    return _group(r["hits"]["hits"], n)


def show(title: str, results: list[dict], lists: int, width: int = 100):
    print(f"\n{title}")
    if not results:
        print("   (nothing matches these filters)")
    for i, r in enumerate(results, start=1):
        tag = r["kind"] + (f", {r['tier']}" if r.get("tier") else "")
        print(f"{i:3d}. {r['name']}  ({tag})  score {r['score']:.4f}  [best: {r['via']}; found by {r['found_by']} of {lists} lists]")
        prefix = f"{r['name']}. "
        passage = r["passage"][len(prefix):] if r["passage"].startswith(prefix) else r["passage"]
        print(textwrap.fill("found because: " + passage, width=width, initial_indent="       ",
                            subsequent_indent="       ", max_lines=2, placeholder=" …"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outlet", nargs="?", help="an outlet's name (any part of it) or id")
    ap.add_argument("--mode", choices=["words", "meaning", "elser", "jina", "blended", "reranked", "compare"], default="blended")
    ap.add_argument("-n", type=int, default=5, help="how many of each kind (1 to 50)")
    ap.add_argument("--kind", choices=list(MATCH_KINDS))
    ap.add_argument("--startups", action="store_true", help="Start-Up tier sponsors only")
    ap.add_argument("--list", action="store_true", help="list the outlets and stop")
    a = ap.parse_args()
    client = connect()
    if a.list or not a.outlet:
        for rid, name in sorted(outlet_names(client).items(), key=lambda kv: kv[1].lower()):
            print(f"   {name}  ({rid})")
        return
    a.n = min(max(a.n, 1), 50)
    name, parts = stored_parts(client, find_outlet(client, a.outlet))
    print(f"\nMatching {name}, on its {' and '.join(parts)}" + (" (the assignment counting double)" if len(parts) == 2 else " alone (it has no KubeCon assignment)"))
    for kind in ([a.kind] if a.kind else (["sponsor"] if a.startups else list(MATCH_KINDS))):
        results = match(client, parts, a.n, kind, a.startups)
        voices = len([w for w in ("words", "meaning", "elser", "jina") if w in results])
        for mode in (("words", "meaning", "elser", "jina", "blended", "reranked") if a.mode == "compare" else (a.mode,)):
            if mode not in results:
                print(f"\n=== {mode.upper()} === ({MISSING[mode]})")
                continue
            lists = len(parts) * (voices if mode == "blended" else 1)
            show(f"=== {mode.upper()} === {kind}s for {name}", results[mode], lists)


if __name__ == "__main__":
    main()
