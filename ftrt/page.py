"""The page: two doors onto the same programme, on this laptop only.

    python -m ftrt.page            # then open http://127.0.0.1:8765

Press door: pick one of the outlets, or type what you always cover and what you came to KubeCon
to find; Go runs the match. Vendor door: pick a sponsor, or type what your company does and what
it is showing; the flip (outlets that fit you) comes next. Underneath, the plain search, three ways.
Typed text is used for that one search and never stored or written to any log.
"""
from . import quiet  # noqa: F401  (first: model offline, library chatter off)
from pathlib import Path
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from . import config, engine, match, search

PAGE_FILE = Path(__file__).with_name("page.html")
app = Flask(__name__)
client = None


def _text(body: dict, key: str) -> str:
    return str(body.get(key) or "").strip()[:config.PAGE_MAX_TYPED]


def _plain(results: list[dict]) -> list[dict]:
    """What the page shows of each result: no numbers beyond the score, and the name taken off the
    front of the passage (it is shown as the heading)."""
    out = []
    for r in results:
        prefix = f"{r['name']}. "
        passage = r["passage"][len(prefix):] if r["passage"].startswith(prefix) else r["passage"]
        out.append({"name": r["name"], "kind": r["kind"], "tier": r.get("tier"), "startup": bool(r.get("startup")),
                    "track": r.get("track"), "score": r["score"], "passage": passage,
                    "via": r.get("via"), "found_by": r.get("found_by")})
    return out


@app.get("/")
def page():
    return PAGE_FILE.read_text(encoding="utf-8")   # read on every request, so an edit shows on reload


@app.get("/api/lists")
def lists():
    """The pickers: the outlets and the sponsors, by name."""
    outlets = client.search(index=config.OUTLETS_INDEX, size=200, source_includes=["record_id", "name", "has_assignment", "sample"],
                            query={"bool": {"filter": [{"term": {"part": "beat"}}, {"term": {"passage_no": 0}}]}})["hits"]["hits"]
    sponsors = client.search(index=config.PROGRAMME_INDEX, size=500, source_includes=["record_id", "name", "tier"],
                             query={"bool": {"filter": [{"term": {"kind": "sponsor"}}, {"term": {"passage_no": 0}}]}})["hits"]["hits"]
    by_name = lambda hits: sorted((h["_source"] for h in hits), key=lambda s: s["name"].lower())
    return jsonify(engine=engine.where(), elser=search.has_elser(client), outlets=by_name(outlets), sponsors=by_name(sponsors))


@app.post("/api/match")
def run_match():
    """The press door: a picked outlet, or the two typed boxes."""
    body = request.get_json(silent=True) or {}
    outlet_id, beat, assignment = _text(body, "outlet_id"), _text(body, "beat"), _text(body, "assignment")
    if outlet_id:
        try:
            name, parts = match.stored_parts(client, outlet_id)
        except SystemExit as e:   # no such outlet in the catalogue
            return jsonify(error=str(e)), 404
    elif beat:
        name, parts = "Your outlet", match.typed_parts(beat, assignment)
    else:
        return jsonify(error="Pick an outlet, or say what you always cover."), 400
    results = {kind: {way: _plain(rs) for way, rs in match.match(client, parts, config.PAGE_RESULTS, kind).items()}
               for kind in match.MATCH_KINDS}
    return jsonify(name=name, parts=list(parts), results=results)


@app.post("/api/flip")
def run_flip():
    """The vendor door. The flip (a sponsor finds its outlets) is the next piece to be built."""
    return jsonify(pending=True, message="The flip, outlets that fit your company, is the next piece to be built.")


@app.post("/api/search")
def run_search():
    """The plain search: words, meaning or blended, over the programme."""
    body = request.get_json(silent=True) or {}
    q, mode, kind = _text(body, "q"), _text(body, "mode") or "blended", _text(body, "kind") or None
    if not q:
        return jsonify(error="Type something to search for."), 400
    if mode not in search.MODES or kind not in (None, "talk", "event", "speaker", "sponsor"):
        return jsonify(error="Unknown search."), 400
    results = search.MODES[mode](client, q, config.PAGE_RESULTS, filt=search.filters(kind))
    if results is None:   # ELSER asked for where it is missing or not answering
        return jsonify(error=search.ELSER_MISSING), 503
    return jsonify(results=_plain(results), mode=mode)


@app.errorhandler(Exception)
def trouble(e):
    """Any other failure (usually the engine not answering): a plain message, never the details."""
    if isinstance(e, HTTPException):   # a wrong address or method keeps its own answer
        return e
    return jsonify(error=f"The search engine did not answer ({type(e).__name__}). Is it running?"), 503


def main():
    global client
    client = engine.connect()
    search.embed("warm up")   # load the meaning model now, not on the first search
    try:
        woke = search.wake_elser(client)   # Elastic's ELSER sleeps when idle; wake it now, not on the first search
        if woke is not None:
            print(f"Elastic's ELSER model is awake ({woke:.0f}s)")
    except Exception as e:   # the page still works without it: searches leave ELSER out until it answers
        print(f"Elastic's ELSER model did not wake ({type(e).__name__}); searches will leave it out until it answers")
    print(f"Open http://{config.PAGE_HOST}:{config.PAGE_PORT}  (this laptop only; Ctrl-C stops it)")
    app.run(host=config.PAGE_HOST, port=config.PAGE_PORT, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
