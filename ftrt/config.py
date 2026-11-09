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
