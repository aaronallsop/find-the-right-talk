"""Search the programme three ways from Terminal: by words, by meaning, or both blended.

    python -m ftrt.search "SLSA Level 3"                     # blended (the default)
    python -m ftrt.search --mode words "SLSA Level 3"
    python -m ftrt.search --mode meaning "surviving a Black Friday traffic spike"
    python -m ftrt.search --mode compare "..."               # the same search, all three ways side by side
    options: -n 10 (how many), --kind sponsor|talk|speaker|event, --startups (Start-Up sponsors only)

Every result is a record (a talk, speaker or sponsor) with the passage that made it match.
Words search can come back empty, which is information; meaning search always returns the
nearest thing. Blended merges the two ranked lists by reciprocal rank fusion, in our own code.
"""
import os
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import argparse, textwrap
from . import config
from .engine import connect

_model = None


def embed(text: str) -> list[float]:
    """The query's 384 meaning numbers, from the same model that read the catalogue."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(config.MODEL_NAME)
    return _model.encode([text], normalize_embeddings=True)[0].tolist()


def filters(kind: str | None = None, startups: bool = False, part: str | None = None) -> list[dict]:
    f = []
    if kind:
        f.append({"term": {"kind": kind}})
    if startups:
        f.append({"term": {"startup": True}})
    if part:
        f.append({"term": {"part": part}})
    return f


def _fetch_size(n: int) -> int:
    """How many passages to ask the engine for: enough to fill n records after grouping, fixed at a
    floor so the same question gives the same answer whether 3 or 30 results are shown, and capped
    at the engine's window."""
    return min(max(n * 6, config.FETCH_FLOOR), config.FETCH_CAP)


def _group(hits: list[dict], n: int) -> list[dict]:
    """Passages come back ranked; keep the best passage of each record, in order, up to n records."""
    out, seen = [], set()
    for h in hits:
        s = h["_source"]
        if s["record_id"] in seen:
            continue
        seen.add(s["record_id"])
        out.append({"record_id": s["record_id"], "kind": s["kind"], "name": s["name"], "score": h["_score"],
                    "passage": s["text"], "tier": s.get("tier"), "startup": s.get("startup"), "track": s.get("track"),
                    "companies": s.get("companies"), "part": s.get("part")})
        if len(out) >= n:
            break
    return out


_FIELDS = ["record_id", "kind", "name", "text", "tier", "startup", "track", "companies", "part"]


def search_words(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None) -> list[dict]:
    body = {"bool": {"must": {"match": {"text": {"query": query, "minimum_should_match": config.WORDS_MIN_MATCH}}},
                     "filter": filt or []}}
    r = client.search(index=index, query=body, size=_fetch_size(n), source_includes=_FIELDS)
    return _group(r["hits"]["hits"], n)


def search_meaning_vector(client, vector: list[float], n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None) -> list[dict]:
    """Meaning search from numbers already in hand (the match reuses this with an outlet's numbers)."""
    k = _fetch_size(n)
    knn = {"field": "vector", "query_vector": vector, "k": k, "num_candidates": max(config.MEANING_CANDIDATES, k)}
    if filt:
        knn["filter"] = {"bool": {"filter": filt}}
    r = client.search(index=index, knn=knn, size=k, source_includes=_FIELDS)
    return _group(r["hits"]["hits"], n)


def search_meaning(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None) -> list[dict]:
    return search_meaning_vector(client, embed(query), n, index, filt)


def fuse(ranked_lists: list[tuple[list[dict], float]], n: int = 10, k: int = config.RRF_K) -> list[dict]:
    """Reciprocal rank fusion. Each list votes: a record gets weight / (k + position) from every list
    it appears in, and the totals decide the order. Lists are (results, weight); weight 1 is one vote."""
    totals, best = {}, {}
    for results, weight in ranked_lists:
        for pos, rec in enumerate(results, start=1):
            rid = rec["record_id"]
            totals[rid] = totals.get(rid, 0.0) + weight / (k + pos)
            best.setdefault(rid, []).append((pos, rec))
    fused = []
    for rid, total in sorted(totals.items(), key=lambda kv: -kv[1]):
        pos, rec = min(best[rid], key=lambda pr: pr[0])
        fused.append({**rec, "score": round(total, 5), "found_by": len(best[rid])})
    return fused[:n]


def search_blended(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None) -> list[dict]:
    words = search_words(client, query, n * 2, index, filt)
    meaning = search_meaning(client, query, n * 2, index, filt)
    return fuse([(words, 1.0), (meaning, 1.0)], n)


MODES = {"words": search_words, "meaning": search_meaning, "blended": search_blended}


def show(title: str, results: list[dict], width: int = 100):
    print(f"\n{title}")
    if not results:
        print("   (nothing: no record has enough of these words)" if title.startswith("=== WORDS") else "   (nothing matches these filters)")
    for i, r in enumerate(results, start=1):
        tag = r["kind"] + (f", {r['tier']}" if r.get("tier") else "")
        extra = f"  [also found by the other list]" if r.get("found_by") == 2 else ""
        print(f"{i:3d}. {r['name']}  ({tag})  score {r['score']:.4f}{extra}")
        prefix = f"{r['name']}. "
        passage = r["passage"][len(prefix):] if r["passage"].startswith(prefix) else r["passage"]
        print(textwrap.fill("found because: " + passage, width=width, initial_indent="       ", subsequent_indent="       ", max_lines=2, placeholder=" …"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--mode", choices=["words", "meaning", "blended", "compare"], default="blended")
    ap.add_argument("-n", type=int, default=10, help="how many results (1 to 200)")
    ap.add_argument("--kind", choices=["talk", "event", "speaker", "sponsor"])
    ap.add_argument("--startups", action="store_true", help="Start-Up tier sponsors only")
    a = ap.parse_args()
    a.n = min(max(a.n, 1), 200)
    client = connect()
    filt = filters(a.kind, a.startups)
    if a.mode == "compare":
        lists = {m: MODES[m](client, a.query, a.n, filt=filt) for m in ("words", "meaning", "blended")}
        for m, res in lists.items():
            show(f"=== {m.upper()} ===  {a.query!r}", res)
        tops = {m: (res[0]["name"] if res else "nothing") for m, res in lists.items()}
        print(f"\nTop result: words → {tops['words']} | meaning → {tops['meaning']} | blended → {tops['blended']}")
        if not lists["words"] and not lists["meaning"]:
            print("Nothing matches: check the filters.")
        elif not lists["words"]:
            print("Words found nothing; meaning answered anyway (it always returns the nearest thing).")
        else:
            print("Words and meaning " + ("AGREE" if tops["words"] == tops["meaning"] else "DISAGREE") + " on the top result.")
    else:
        show(f"=== {a.mode.upper()} ===  {a.query!r}", MODES[a.mode](client, a.query, a.n, filt=filt))


if __name__ == "__main__":
    main()
