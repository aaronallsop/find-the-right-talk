"""Every constant in one place. Change a number here, nowhere else."""
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

# The model reads only about the first 180 words of anything, so long text is cut into passages.
PASSAGE_WORDS = 120      # aim for passages of about this many words
MIN_TAIL_WORDS = 40      # a leftover shorter than this is folded into the passage before it

# Where the engine is and how to get in. The password is read from this file and never written anywhere.
ENGINE_SETTINGS_FILE = Path.home() / "elastic-start-local" / ".env"
ENGINE_DEFAULT_URL = "http://localhost:9200"
ENGINE_USER = "elastic"

# Search settings (used from B2 on).
WORDS_MIN_MATCH = "2<75%"   # one or two words typed: all must be present; more: three quarters
MEANING_CANDIDATES = 200    # how many stored passages the engine re-checks at full detail
FETCH_FLOOR = 120           # passages fetched per search before grouping into records, at least
FETCH_CAP = 2000            # and at most (the engine's window is 10,000)
RRF_K = 60                  # reciprocal rank fusion constant, from the original paper
