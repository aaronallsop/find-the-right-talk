"""The page: two doors onto the same programme, on this laptop only.

    python -m ftrt.page            # then open http://127.0.0.1:8765

Press door: pick one of the outlets, or type what you always cover and what you came to KubeCon
to find; Go runs the match. Vendor door: pick a sponsor, or type what your company does and what
it is showing; the flip (outlets that fit you) comes next. Underneath, the plain search, three ways.
Typed text is used for that one search and never stored or written to any log.
"""
from . import quiet  # noqa: F401  (first: model offline, library chatter off)
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from . import config, engine, flip, match, search, tracing, warm

PAGE_FILE = Path(__file__).with_name("page.html")
THEME_FILE = Path(__file__).with_name("page-theme.css")   # the page's look, kept apart from its workings
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
        out.append({"name": r["name"], "kind": r["kind"], "tier": "sample" if r.get("sample") else r.get("tier"),
                    "startup": bool(r.get("startup")),
                    "track": r.get("track"), "score": r["score"], "passage": passage,
                    "via": r.get("via"), "found_by": r.get("found_by")})
    return out


@app.get("/")
def page():
    return PAGE_FILE.read_text(encoding="utf-8")   # read on every request, so an edit shows on reload


@app.get("/page-theme.css")
def theme():
    """The page's look. If the file is not there, the page keeps its own built-in look."""
    if not THEME_FILE.exists():
        return "", 404
    return THEME_FILE.read_text(encoding="utf-8"), 200, {"Content-Type": "text/css; charset=utf-8"}


@app.get("/api/lists")
def lists():
    """The pickers: the outlets and the sponsors, by name."""
    outlets = client.search(index=config.OUTLETS_INDEX, size=200, source_includes=["record_id", "name", "has_assignment", "sample"],
                            query={"bool": {"filter": [{"term": {"part": "beat"}}, {"term": {"passage_no": 0}}]}})["hits"]["hits"]
    sponsors = client.search(index=config.PROGRAMME_INDEX, size=500, source_includes=["record_id", "name", "tier", "startup"],
                             query={"bool": {"filter": [{"term": {"kind": "sponsor"}}, {"term": {"passage_no": 0}}]}})["hits"]["hits"]
    by_name = lambda hits: sorted((h["_source"] for h in hits), key=lambda s: s["name"].lower())
    return jsonify(engine=engine.where(), elser=search.has_elser(client), rerank=search.rerank_on(),
                   jina=search.has_field(client, config.JINA_FIELD),
                   outlets=by_name(outlets), sponsors=by_name(sponsors))


@app.get("/api/profile")
def profile():
    """The text a pick puts in the first box: an outlet's standing beat, or what a sponsor does. Ids only in the
    address, never typed text."""
    outlet_id, sponsor_id = request.args.get("outlet", "").strip(), request.args.get("sponsor", "").strip()
    try:
        if outlet_id:
            name, parts = match.stored_parts(client, outlet_id)
            return jsonify(name=name, text=parts["beat"]["text"])
        if sponsor_id:
            row = flip.find_sponsor(sponsor_id)
            return jsonify(name=row["name"], text=flip.sponsor_texts(row)["does"])
    except SystemExit as e:   # no such outlet or sponsor
        return jsonify(error=str(e)), 404
    return jsonify(error="Ask for an outlet or a sponsor."), 400


@app.post("/api/match")
def run_match():
    """The press door: a picked outlet, or the two typed boxes."""
    body = request.get_json(silent=True) or {}
    outlet_id, beat, assignment = _text(body, "outlet_id"), _text(body, "beat"), _text(body, "assignment")
    startups = bool(body.get("startups"))   # the start-ups toggle narrows the sponsors; talks and speakers are unaffected
    search.begin_request()
    with tracing.span("press door", outlet=outlet_id or "typed", startups=startups) as root:
        return _run_match(root, outlet_id, beat, assignment, startups)


def _run_match(root, outlet_id, beat, assignment, startups):
    """Matches what the two boxes say. A picked outlet only filled the first box (with its own beat, which the
    visitor may have edited) and names the result; the second box is the visitor's own."""
    name = "Your outlet"
    if outlet_id:
        names = match.outlet_names(client)
        if outlet_id not in names:
            return jsonify(error=f"No outlet {outlet_id!r}."), 404
        name = names[outlet_id]
        if not beat:   # the box was emptied: fall back to the outlet's own beat
            beat = match.stored_parts(client, outlet_id)[1]["beat"]["text"]
    if not beat:
        return jsonify(error="Pick an outlet, or say what you always cover."), 400
    parts = match.typed_parts(beat, assignment)
    if search.has_field(client, config.JINA_FIELD):
        parts = match.with_jina(client, parts)   # Jina asked once per part, shared by the three kinds
    with ThreadPoolExecutor(max_workers=len(match.MATCH_KINDS)) as pool:   # sponsors, talks, speakers at once
        found = dict(zip(match.MATCH_KINDS, pool.map(tracing.carry(
            lambda kind: match.match(client, parts, config.PAGE_RESULTS, kind, startups and kind == "sponsor")), match.MATCH_KINDS)))
    sat_out = search.left_out()   # read once: the trace and the page say the same
    root.set_attribute("left_out", ", ".join(sat_out) or "none")
    results = {kind: {way: _plain(rs) for way, rs in found[kind].items()} for kind in match.MATCH_KINDS}
    on = ("what it always covers and what you came to find (counting double)" if len(parts) == 2
          else "what it always covers")
    return jsonify(title=f"Matches for {name}, on {on}", results=results, startups=startups, left_out=sat_out,
                   kinds=[["sponsor", "Start-up sponsors" if startups else "Sponsors"], ["talk", "Talks"], ["speaker", "Speakers"]])


@app.post("/api/flip")
def run_flip():
    """The vendor door: a picked sponsor, or the two typed boxes, finds the outlets that fit it and the nearest talks."""
    body = request.get_json(silent=True) or {}
    sponsor_id, does, showing = _text(body, "sponsor_id"), _text(body, "does"), _text(body, "showing")
    search.begin_request()
    with tracing.span("vendor door", sponsor=sponsor_id or "typed"):
        return _run_flip(sponsor_id, does, showing)


def _run_flip(sponsor_id, does, showing):
    """Flips what the two boxes say. A picked sponsor only filled the first box (with its own text, which the
    visitor may have edited) and names the result; the second box is the visitor's own."""
    name = "Your company"
    if sponsor_id:
        try:
            row = flip.find_sponsor(sponsor_id)
        except SystemExit as e:   # no such sponsor
            return jsonify(error=str(e)), 404
        name = row["name"]
        if not does:   # the box was emptied: fall back to the sponsor's own text
            does = flip.sponsor_texts(row)["does"]
    if not does:
        return jsonify(error="Pick a sponsor, or say what your company does."), 400
    texts = flip.typed_texts(does, showing)
    parts = match.parts_from_text(texts)
    if search.has_field(client, config.JINA_FIELD):
        parts = match.with_jina(client, parts)   # Jina asked once per part, shared by outlets and talks
    found = flip.flip(client, parts, config.PAGE_RESULTS)
    results = {kind: {way: _plain(rs) for way, rs in ways.items()} for kind, ways in found.items()}
    on = ("what it does and what you are showing at KubeCon (counting double)" if "showing" in parts
          else "what it does")
    return jsonify(title=f"Outlets and talks for {name}, on {on}", results=results, left_out=search.left_out(),
                   kinds=[["outlet", "Outlets"], ["talk", "Talks"]])




@app.post("/api/search")
def run_search():
    """The plain search over the programme: one way, or "compare", every way at once side by side."""
    body = request.get_json(silent=True) or {}
    q, mode, kind = _text(body, "q"), _text(body, "mode") or "blended", _text(body, "kind") or None
    startups = bool(body.get("startups"))
    if startups:   # only sponsors have a tier, so "start-ups only" means start-up sponsors
        kind = "sponsor"
    if not q:
        return jsonify(error="Type something to search for."), 400
    if (mode not in search.MODES and mode != "compare") or kind not in (None, "talk", "event", "speaker", "sponsor"):
        return jsonify(error="Unknown search."), 400
    search.begin_request()
    with tracing.span("plain search", mode=mode, kind=kind or "all", startups=startups):
        return _run_search(q, mode, kind, startups)


def _run_search(q, mode, kind, startups):
    if mode == "compare":   # every way at once; a way that is not here (laptop) or did not answer comes back empty
        found = search.compare_all(client, q, config.PAGE_RESULTS, filt=search.filters(kind, startups))
        return jsonify(ways={way: (None if rs is None else _plain(rs)) for way, rs in found.items()},
                       mode=mode, startups=startups, left_out=search.left_out())
    results = search.MODES[mode](client, q, config.PAGE_RESULTS, filt=search.filters(kind, startups))
    if results is None:   # ELSER or the re-ranker asked for where it is missing or not answering
        return jsonify(error=search.MISSING[mode]), 503
    return jsonify(results=_plain(results), mode=mode, startups=startups, left_out=search.left_out())


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
    print("Traces of each search go to Dash0" if tracing.setup() else
          f"Tracing off (no Dash0 settings in {tracing.SETTINGS_FILE}); everything else works the same")
    # Elastic's models sleep when idle: wake them in the background, so the page opens at once; until they
    # answer, searches go ahead without them and the page says so
    threading.Thread(target=warm.warm, args=(client,), daemon=True).start()
    print(f"Open http://{config.PAGE_HOST}:{config.PAGE_PORT}  (this laptop only; Ctrl-C stops it)")
    app.run(host=config.PAGE_HOST, port=config.PAGE_PORT, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
