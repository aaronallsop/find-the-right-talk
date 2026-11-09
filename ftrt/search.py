"""Search the programme from Terminal: by words, by meaning, by Elastic's own model (ELSER), or blended.

    python -m ftrt.search "SLSA Level 3"                     # blended (the default)
    python -m ftrt.search --mode words "SLSA Level 3"
    python -m ftrt.search --mode meaning "surviving a Black Friday traffic spike"
    python -m ftrt.search --mode elser "..."                 # Elastic Cloud only
    python -m ftrt.search --mode reranked "..."              # blended, top 20 re-ordered by Elastic's re-ranker (cloud only)
    python -m ftrt.search --mode compare "..."               # the same search, every way side by side
    options: -n 10 (how many), --kind sponsor|talk|speaker|event, --startups (Start-Up sponsors only)

Every result is a record (a talk, speaker or sponsor) with the passage that made it match.
Words search can come back empty, which is information; meaning search always returns the
nearest thing. ELSER is a second, larger meaning model that Elastic runs inside the cloud project;
on the laptop engine it is skipped. Blended merges the ranked lists (two on the laptop, three in the
cloud), one vote each, by reciprocal rank fusion, in our own code.
"""
from . import quiet  # noqa: F401  (first: model offline, library chatter off)
import argparse, contextvars, sys, textwrap, threading, time
from concurrent.futures import ThreadPoolExecutor
from elasticsearch import ApiError, TransportError
from . import config, engine, tracing
from .engine import connect

_model = None
_model_lock = threading.Lock()   # searches now run side by side; only one of them loads the model


def embed(text: str) -> list[float]:
    """The query's 384 meaning numbers, from the same model that read the catalogue."""
    global _model
    with _model_lock:
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
                    "passage": s.get("text"), "_id": h["_id"], "_index": h["_index"],
                    "tier": s.get("tier"), "startup": s.get("startup"), "track": s.get("track"),
                    "companies": s.get("companies"), "part": s.get("part"), "sample": s.get("sample")})
        if len(out) >= n:
            break
    return out


_FIELDS = ["record_id", "kind", "name", "text", "tier", "startup", "track", "companies", "part", "sample"]
_LIST_FIELDS = [f for f in _FIELDS if f != "text"]   # long lists come back without the passages' text (most of the weight)


def _fields(passages: bool) -> list[str]:
    return _FIELDS if passages else _LIST_FIELDS


def with_passages(client, results: list[dict]) -> list[dict]:
    """Fill in the passage text of results that came back without it, in one request. Only the results that are
    shown, or handed to the re-ranker, need it; the long lists that are merged do not."""
    missing = [r for r in results if r.get("passage") is None]
    if missing:
        got = client.mget(docs=[{"_index": r["_index"], "_id": r["_id"]} for r in missing], source_includes=["text"])["docs"]
        for r, d in zip(missing, got):
            r["passage"] = d["_source"]["text"]
    return results


def search_words(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None,
                 passages: bool = True) -> list[dict]:
    body = {"bool": {"must": {"match": {"text": {"query": query, "minimum_should_match": config.WORDS_MIN_MATCH}}},
                     "filter": filt or []}}
    r = client.search(index=index, query=body, size=_fetch_size(n), source_includes=_fields(passages))
    return _group(r["hits"]["hits"], n)


def search_meaning_vector(client, vector: list[float], n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None,
                          field: str = "vector", passages: bool = True) -> list[dict]:
    """Meaning search from numbers already in hand (the match reuses this with an outlet's numbers; Jina with its own)."""
    k = _fetch_size(n)
    knn = {"field": field, "query_vector": vector, "k": k, "num_candidates": max(config.MEANING_CANDIDATES, k)}
    if filt:
        knn["filter"] = {"bool": {"filter": filt}}
    r = client.search(index=index, knn=knn, size=k, source_includes=_fields(passages))
    return _group(r["hits"]["hits"], n)


def search_meaning(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None,
                   passages: bool = True) -> list[dict]:
    return search_meaning_vector(client, embed(query), n, index, filt, passages=passages)


ELSER_MISSING = ("Elastic's own model, ELSER, did not answer or is not in this catalogue (it runs only in Elastic "
                 "Cloud, after a load there with python -m ftrt.load). Skipped.")
_elser_resting_until = 0.0   # after a failure, searches leave ELSER alone until this time


def has_field(client, field: str, index: str = config.PROGRAMME_INDEX) -> bool:
    """Whether this catalogue holds this field. Asked afresh each time (one small request), so a running page
    notices a reload."""
    props = client.indices.get_mapping(index=index)[index]["mappings"].get("properties", {})
    return field in props


def has_elser(client, index: str = config.PROGRAMME_INDEX) -> bool:
    """Whether this catalogue holds ELSER's reading of each passage (Elastic Cloud only; the laptop skips it)."""
    return has_field(client, config.ELSER_FIELD, index)


JINA_MISSING = ("Jina embeddings are not in this catalogue or did not answer (they need Elastic Cloud and a load "
                "there). Skipped.")
_jina_resting_until = 0.0


def jina_question(client, query: str) -> list[float] | None:
    """The question's Jina numbers from Elastic's hosted service, or None if it is resting or does not answer in time."""
    global _jina_resting_until
    if time.time() < _jina_resting_until:
        _left_out(config.JINA_NAME)
        return None
    try:
        r = client.options(request_timeout=config.JINA_SEARCH_LIMIT, max_retries=0).inference.text_embedding(
            inference_id=config.JINA_ENDPOINT, input=[query], timeout=f"{config.JINA_SEARCH_LIMIT}s")
        return r.body["text_embedding"][0]["embedding"]
    except (ApiError, TransportError) as e:
        _jina_resting_until = time.time() + config.JINA_REST
        _left_out(config.JINA_NAME)
        print(f"Jina did not answer within {config.JINA_SEARCH_LIMIT} s ({type(e).__name__}); left out, and not asked "
              f"again for {config.JINA_REST} s.", file=sys.stderr)
        return None


def search_jina(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None,
                vector: list[float] | None = None, passages: bool = True) -> list[dict] | None:
    """Search by the meaning Jina's model finds: the question's numbers come from Elastic's hosted service, then the
    nearest passages by their stored Jina numbers. None on the laptop, or if it is slow, so callers skip this voice."""
    if not has_field(client, config.JINA_FIELD, index):
        return None
    vector = vector or jina_question(client, query)
    if vector is None:
        return None
    return search_meaning_vector(client, vector, n, index, filt, field=config.JINA_FIELD, passages=passages)


def search_elser(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None,
                 passages: bool = True) -> list[dict] | None:
    """Search by the meaning Elastic's own model, ELSER, finds. None where the catalogue has no ELSER field
    (the laptop engine) or ELSER does not answer (it may be waking up), so callers skip this voice rather than fail."""
    global _elser_resting_until
    if time.time() < _elser_resting_until:
        _left_out(config.ELSER_NAME)
        return None
    try:
        if not has_elser(client, index):
            return None
        body = {"bool": {"must": {"semantic": {"field": config.ELSER_FIELD, "query": query}}, "filter": filt or []}}
        r = client.options(request_timeout=config.ELSER_SEARCH_LIMIT, max_retries=0).search(
            index=index, query=body, size=_fetch_size(n), source_includes=_fields(passages))
    except (ApiError, TransportError) as e:
        _elser_resting_until = time.time() + config.ELSER_REST
        _left_out(config.ELSER_NAME)
        print(f"ELSER did not answer within {config.ELSER_SEARCH_LIMIT} s ({type(e).__name__}); left out, and not "
              f"asked again for {config.ELSER_REST} s.", file=sys.stderr)
        return None
    return _group(r["hits"]["hits"], n)


def wake_elser(client) -> float | None:
    """Wake ELSER (it sleeps when idle; waking took 81 s once). Seconds taken, or None if this catalogue has none."""
    if not has_elser(client):
        return None
    t = time.time()
    client.options(request_timeout=config.ELSER_TIMEOUT).inference.inference(
        inference_id=config.ELSER_ENDPOINT, input=["wake up"], timeout=f"{config.ELSER_TIMEOUT}s")
    return time.time() - t


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


def every_way(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None) -> dict:
    """Each way asked once, at the same time, ranked to the fixed depth: {"words": [...], "meaning": [...],
    "elser": [...] or None, "jina": [...] or None}."""
    depth = max(n, config.BLEND_DEPTH)   # fixed, so the blend does not change with how many are shown
    ways = (("words", search_words), ("meaning", search_meaning), ("elser", search_elser), ("jina", search_jina))
    def ask(way):   # each way a step of its own in the trace
        with tracing.span(f"{way[0]} search") as s:
            found = way[1](client, query, depth, index, filt, passages=False)
            tracing.note(s, found)
            return found
    with ThreadPoolExecutor(max_workers=len(ways)) as pool:
        return dict(zip((w for w, _ in ways), pool.map(tracing.carry(ask), ways)))


def blend(found: dict, n: int) -> list[dict]:
    """Words and meaning, and Elastic's models where they answered, one vote each, merged in a fixed order."""
    return fuse([(found[w], 1.0) for w in ("words", "meaning", "elser", "jina") if found.get(w) is not None], n)


def search_blended(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None) -> list[dict]:
    return with_passages(client, blend(every_way(client, query, n, index, filt), n))


def compare_all(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None) -> dict:
    """Every way side by side, each asked once: the blended and re-ranked columns come from the same answers."""
    found = every_way(client, query, n, index, filt)
    with tracing.span("fetch passages"):
        blended = with_passages(client, blend(found, max(n, config.RERANK_TOP)))   # the re-ranker reads these passages
    with tracing.span("re-rank") as s:
        reordered = rerank(client, query, blended)
        tracing.note(s, reordered)
    return {**{w: (None if rs is None else with_passages(client, rs[:n])) for w, rs in found.items()},
            "blended": blended[:n], "reranked": None if reordered is None else reordered[:n]}


RERANK_MISSING = ("Elastic's re-ranker runs only in Elastic Cloud, and only when it answers. Skipped.")


_rerank_resting_until = 0.0   # after a failure, the re-ranker is left alone until this time


def rerank_on() -> bool:
    """The re-ranker is used only in Elastic Cloud, and only when an endpoint is set (config.RERANK_ENDPOINT)."""
    return bool(config.RERANK_ENDPOINT) and engine.where() == "cloud"


_sat_out = contextvars.ContextVar("sat_out", default=None)   # this request's models that were left out


def begin_request() -> None:
    """Start counting, for this request only, which of Elastic's models sit it out."""
    _sat_out.set(set())


def _left_out(name: str) -> None:
    got = _sat_out.get()
    if got is not None:
        got.add(name)


def left_out() -> list[str]:
    """Which of Elastic's models sat this request out (resting, or slow to answer), as recorded while it ran."""
    return sorted(_sat_out.get() or ())


def wake_rerank(client) -> float | None:
    """Wake the re-ranker, waiting as long as it takes. Seconds taken, or None if it is switched off."""
    if not rerank_on():
        return None
    t = time.time()
    client.options(request_timeout=config.ELSER_TIMEOUT).inference.rerank(
        inference_id=config.RERANK_ENDPOINT, query="wake up", input=["wake up"], timeout=f"{config.ELSER_TIMEOUT}s")
    return time.time() - t


def rerank(client, question: str, results: list[dict], top: int = config.RERANK_TOP) -> list[dict] | None:
    """Elastic's re-ranker reads the question with each of the top results' passages and re-orders them;
    the rest keep their order. None on the laptop engine, or if it does not answer, so callers skip it."""
    global _rerank_resting_until
    if not rerank_on() or not results:
        return None
    if time.time() < _rerank_resting_until:
        _left_out(config.RERANK_NAME)
        return None
    head = results[:top]
    try:
        out = client.options(request_timeout=config.RERANK_SEARCH_LIMIT, max_retries=0).inference.rerank(
            inference_id=config.RERANK_ENDPOINT, query=question, input=[r["passage"] for r in head],
            timeout=f"{config.RERANK_SEARCH_LIMIT}s")
    except (ApiError, TransportError) as e:
        _rerank_resting_until = time.time() + config.RERANK_REST
        _left_out(config.RERANK_NAME)
        print(f"The re-ranker did not answer within {config.RERANK_SEARCH_LIMIT} s ({type(e).__name__}); left out, "
              f"and not asked again for {config.RERANK_REST} s.", file=sys.stderr)
        return None
    order = sorted(out.body["rerank"], key=lambda o: -o["relevance_score"])
    return [{**head[o["index"]], "score": round(o["relevance_score"], 4)} for o in order] + results[top:]


MISSING = {"elser": ELSER_MISSING, "jina": JINA_MISSING, "reranked": RERANK_MISSING}


def search_reranked(client, query: str, n: int = 10, index: str = config.PROGRAMME_INDEX, filt: list | None = None) -> list[dict] | None:
    """The blended results, with the top ones re-ordered by Elastic's re-ranker (Elastic Cloud only)."""
    reordered = rerank(client, query, search_blended(client, query, max(n, config.RERANK_TOP), index, filt))
    return None if reordered is None else reordered[:n]


MODES = {"words": search_words, "meaning": search_meaning, "elser": search_elser, "jina": search_jina, "blended": search_blended,
         "reranked": search_reranked}


def show(title: str, results: list[dict], width: int = 100):
    print(f"\n{title}")
    if not results:
        print("   (nothing: no record has enough of these words)" if title.startswith("=== WORDS") else "   (nothing matches these filters)")
    for i, r in enumerate(results, start=1):
        tag = r["kind"] + (f", {r['tier']}" if r.get("tier") else "")
        extra = f"  [found by {r['found_by']} lists]" if (r.get("found_by") or 0) > 1 else ""
        print(f"{i:3d}. {r['name']}  ({tag})  score {r['score']:.4f}{extra}")
        prefix = f"{r['name']}. "
        passage = r["passage"][len(prefix):] if r["passage"].startswith(prefix) else r["passage"]
        print(textwrap.fill("found because: " + passage, width=width, initial_indent="       ", subsequent_indent="       ", max_lines=2, placeholder=" …"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--mode", choices=["words", "meaning", "elser", "jina", "blended", "reranked", "compare"], default="blended")
    ap.add_argument("-n", type=int, default=10, help=f"how many results (1 to {config.BLEND_DEPTH})")
    ap.add_argument("--kind", choices=["talk", "event", "speaker", "sponsor"])
    ap.add_argument("--startups", action="store_true", help="Start-Up tier sponsors only")
    a = ap.parse_args()
    a.n = min(max(a.n, 1), config.BLEND_DEPTH)
    client = connect()
    filt = filters(a.kind, a.startups)
    if a.mode == "compare":
        lists = {m: MODES[m](client, a.query, a.n, filt=filt) for m in ("words", "meaning", "elser", "jina", "blended", "reranked")}
        for m, res in lists.items():
            if res is None:
                print(f"\n=== {m.upper()} ===  ({MISSING[m]})")
            else:
                show(f"=== {m.upper()} ===  {a.query!r}", res)
        tops = {m: (res[0]["name"] if res else ("skipped" if res is None else "nothing")) for m, res in lists.items()}
        print(f"\nTop result: words → {tops['words']} | meaning → {tops['meaning']} | ELSER → {tops['elser']} | Jina → {tops['jina']} | "
              f"blended → {tops['blended']} | re-ranked → {tops['reranked']}")
        if not lists["words"] and not lists["meaning"]:
            print("Nothing matches: check the filters.")
        elif not lists["words"]:
            print("Words found nothing; meaning answered anyway (it always returns the nearest thing).")
        else:
            print("Words and meaning " + ("AGREE" if tops["words"] == tops["meaning"] else "DISAGREE") + " on the top result.")
    else:
        res = MODES[a.mode](client, a.query, a.n, filt=filt)
        if res is None:
            raise SystemExit(MISSING[a.mode])
        show(f"=== {a.mode.upper()} ===  {a.query!r}", res)


if __name__ == "__main__":
    main()
