"""Every constant in one place. Change a number here, nowhere else."""
import os
from pathlib import Path

# The two catalogues this project owns. Names are new on purpose: anything else on the
# engine belongs to someone else and is never touched.
PROGRAMME_INDEX = "ftrt-programme"   # talks, events, speakers and sponsors, told apart by `kind`
OUTLETS_INDEX = "ftrt-outlets"       # the media outlets, their standing beat and KubeCon assignment
OWN_PREFIX = "ftrt-"                 # the loader refuses to delete any catalogue not starting with this

# The data, read as UTF-8 with a byte-order mark; lists inside a cell are separated by "; ".
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LIST_SEPARATOR = "; "

# The meaning model: small, open source, runs on the laptop, produces 384 numbers per passage.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_SIZE = 384

# The model reads only its first 256 word-pieces (its own tokeniser's units; technical text runs about
# 1.5 per word) and ignores the rest, so long text is cut into passages, measured in those pieces.
MODEL_MAX_PIECES = 254   # 256 less the two markers the model adds; no passage, name included, may be longer
PASSAGE_PIECES = 180     # aim for passages of about this many pieces (about 120 words), before the name
MIN_TAIL_PIECES = 60     # a leftover shorter than this is folded into the passage before it, if that still fits

# Speaker cells that hold no information: dropped, not loaded as text.
PLACEHOLDERS = {"todo", "tbd", "tba", "none", "n/a", "na", "-", "--", ".", "null"}

# Where the engine is and how to get in. Both files live outside this folder; nothing in them is
# ever written anywhere else. The cloud file wins when it is filled in (see engine.py).
# FTRT_CLOUD_ENV=/path/to/.env in front of a command uses another cloud project's settings file instead.
CLOUD_SETTINGS_FILE = Path(os.environ.get("FTRT_CLOUD_ENV") or Path.home() / "elastic-cloud" / ".env").expanduser()  # ES_CLOUD_URL, ES_CLOUD_API_KEY
ENGINE_SETTINGS_FILE = Path.home() / "elastic-start-local" / ".env"  # ES_LOCAL_URL, ES_LOCAL_PASSWORD
ENGINE_DEFAULT_URL = "http://localhost:9200"
ENGINE_USER = "elastic"

# Search settings (used from B2 on).
WORDS_MIN_MATCH = "2<75%"   # one or two words typed: all must be present; more: three quarters
MEANING_CANDIDATES = 200    # how many stored passages the engine re-checks at full detail
FETCH_FLOOR = 120           # passages fetched per search before grouping into records, at least
FETCH_CAP = 2000            # and at most (the engine's window is 10,000)
RRF_K = 60                  # reciprocal rank fusion constant, from the original paper
BLEND_DEPTH = 100           # every list is ranked this deep before blending, however many results are shown,
                            # so the order never depends on the number asked for (up to this many)

# Elastic's own meaning model, ELSER, as a further voice: Elastic Cloud only (the laptop engine skips it).
# The in-project endpoint runs inside Aaron's serverless project; ".elser-2-elastic" would instead send the
# text to Elastic's separate inference service. It scales down to nothing when idle, so the first call after
# a quiet spell waits while it wakes (81 s measured at 11:58); the page warms it up when it starts.
ELSER_ENDPOINT = ".elser-2-elasticsearch"
ELSER_FIELD = "text_elser"  # the passage's text again, which Elastic turns into ELSER's own terms at load time
ELSER_TIMEOUT = 300         # seconds a load or search may wait on it (waking up included)

# The match (M2): an outlet's profile searches the programme.
MATCH_WEIGHTS = {"assignment": 2.0, "beat": 1.0}   # the assignment's votes count double (Aaron, 8 November)
MATCH_WORDS_TERMS = 25      # words search by profile: how many of its most telling words to search for

# The page (M3). Port 5000 is taken by macOS itself (AirPlay Receiver); 5055-5057 may be in use too; and browsers
# refuse 5060 and 5061 outright (the internet-phone ports, on Chrome's, Safari's and Firefox's blocked lists).
PAGE_HOST = "127.0.0.1"     # this laptop only: the page has no login
PAGE_PORT = 8765
PAGE_RESULTS = 10           # results of each kind shown on the page
PAGE_MAX_TYPED = 2000       # characters accepted in any one box
