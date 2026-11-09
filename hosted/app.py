"""The lean, hosted page: words, Elastic's ELSER and Jina only, Elastic Cloud only, no local meaning model.

gunicorn runs this inside the container (see Dockerfile). It wires the existing page, ftrt/page.py, up for hosting
WITHOUT editing any of ftrt/: it swaps four things on the modules after they are imported.
  1. The engine settings come from two environment variables (ES_CLOUD_URL, ES_CLOUD_API_KEY), which a Kubernetes
     secret supplies; no settings file and no key is in the image. If they are absent, the usual settings file
     (FTRT_CLOUD_ENV) is read instead, which is how a local test run mounts Aaron's file read-only.
  2. The laptop meaning model (sentence-transformers, and torch under it) is left out: its voice is skipped
     everywhere, the same way the page already skips a voice that does not answer. Typed text is not cut into
     passages (that needed the model's tokeniser); it goes whole to words, ELSER and Jina.
  3. The page's HTML loses its "Meaning" buttons and column.
  4. A small per-address limit on searches, because the page has no login and every search is billed to Aaron's
     Elastic project.
"""
import collections, os, re, threading, time
from pathlib import Path

os.environ.setdefault("FTRT_ENGINE", "cloud")   # never the laptop engine

from flask import jsonify, request
from ftrt import config, engine, match, passages, search, warm
from ftrt import page as ftrt_page

# 1. engine settings from the environment (the Kubernetes secret)
_settings_from_file = engine._cloud_settings


def _cloud_settings():
    url, key = os.environ.get("ES_CLOUD_URL", "").strip(), os.environ.get("ES_CLOUD_API_KEY", "").strip()
    return (url, key) if url and key else _settings_from_file()


engine._cloud_settings = _cloud_settings

# 2. no local meaning model
_original_vector_search = search.search_meaning_vector


def _no_meaning(*args, **kwargs):
    return None   # a voice that is not here, as the page already treats ELSER on the laptop


def _vector_search(client, vector, n=10, index=config.PROGRAMME_INDEX, filt=None, field="vector", passages=True):
    if field == "vector":   # the laptop model's stored numbers; Jina's own field goes through as usual
        return None
    return _original_vector_search(client, vector, n, index, filt, field, passages)


def _no_model(*args, **kwargs):
    raise RuntimeError("the laptop meaning model is not part of the hosted page")


def _lean_parts(texts: dict[str, str]) -> dict:
    """Parts from typed text, kept whole: words, ELSER and Jina read the text, so it needs no numbers of its own."""
    return {part: {"text": passages._tidy(text), "vector": None} for part, text in texts.items() if text}


search.embed = match.embed = _no_model
search.search_meaning = _no_meaning
search.MODES["meaning"] = _no_meaning
search.search_meaning_vector = match.search_meaning_vector = _vector_search
search.MISSING["meaning"] = ("The laptop meaning model is not part of this hosted page. "
                             "Use Jina or Elastic's ELSER, which read for meaning in Elastic Cloud.")
match.parts_from_text = _lean_parts

# 3. the page's HTML, without the Meaning way
HTML = Path(ftrt_page.__file__).with_name("page.html").read_text(encoding="utf-8")
HTML = re.sub(r'[ \t]*<button type="button" data-way="meaning"[^>]*>Meaning</button>\n?', "", HTML)
HTML = HTML.replace('["meaning", "Meaning"], ', "").replace("Try Meaning.", "Try Jina or Elastic ELSER.")
ftrt_page.app.view_functions["page"] = lambda: HTML
ftrt_page.app.add_url_rule("/healthz", "healthz", lambda: "ok")   # asks the engine nothing, so it costs nothing
ftrt_page.app.add_url_rule("/readyz", "readyz", lambda: "ok")     # the name Radar's starter manifests probe

# 4. a limit on searches per address (and overall), because every search is billed
RATE_PER_ADDRESS = int(os.environ.get("HOSTED_RATE_PER_MINUTE", "60"))
RATE_OVERALL = int(os.environ.get("HOSTED_RATE_OVERALL_PER_MINUTE", "600"))
_recent, _all, _lock = collections.defaultdict(collections.deque), collections.deque(), threading.Lock()


@ftrt_page.app.before_request
def _limit():
    if request.method != "POST":
        return None
    who = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or request.remote_addr or "?"
    now = time.monotonic()
    with _lock:
        if len(_recent) > 10000:
            _recent.clear()
        mine = _recent[who]
        for q in (mine, _all):
            while q and now - q[0] > 60:
                q.popleft()
        if len(mine) >= RATE_PER_ADDRESS or len(_all) >= RATE_OVERALL:
            return jsonify(error="A lot of searches are running just now. Wait a minute and try again."), 429
        mine.append(now)
        _all.append(now)
    return None


ftrt_page.client = engine.connect()   # fails at start, loudly, if the settings are wrong
threading.Thread(target=warm.warm, args=(ftrt_page.client,), daemon=True).start()   # wake ELSER and the re-ranker
app = ftrt_page.app
