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
CONNECTIONS = 32            # requests to the engine at once; a page Go asks about two dozen side by side (the default is 10)

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
ELSER_NAME = "Elastic's ELSER"
RERANK_NAME = "Elastic's re-ranker"
ELSER_FIELD = "text_elser"  # the passage's text again, which Elastic turns into ELSER's own terms at load time
ELSER_TIMEOUT = 300         # seconds a load, or a deliberate wake-up, may wait on it
ELSER_SEARCH_LIMIT = 4      # seconds a search waits for it; slower, and the results come without it (and say so)
ELSER_REST = 60             # after it misses a search, seconds before searches ask it again (it is probably waking)

# Jina embeddings (Aaron, 13:27): one more meaning voice, Elastic Cloud only. Every passage's 1,024 Jina numbers are
# fetched from Elastic's hosted inference service at load (passages sent there, billed per use) BEFORE anything is
# rebuilt, so a refusal changes nothing; each search's question is sent there too. 10 passages took 0.65-0.75 s,
# one question 0.38 s (13:31).
JINA_ENDPOINT = ".jina-embeddings-v3"
JINA_NAME = "Jina embeddings"
JINA_FIELD = "vector_jina"
JINA_SIZE = 1024
JINA_BATCH = 16             # passages per request at load (the service accepts at most 16)
JINA_PARALLEL = 8           # requests at a time at load
JINA_SEARCH_LIMIT = 4       # seconds a search waits for the question's numbers; slower, and it is left out (and says so)
JINA_REST = 60              # after a miss, seconds before searches ask it again

# Elastic's re-ranker (Aaron's item 6): reads the question and each of the blended top results' passages
# together and puts them in a new order. Elastic Cloud only; left out if it does not answer. The in-project
# ".rerank-v1-elasticsearch" would not start (12:18-12:21, "no ML nodes with sufficient capacity"), so, on Aaron's
# yes (12:30), this is Elastic's HOSTED Jina re-ranker: for the re-ranked view, the search text and the top
# passages go to Elastic's inference service, outside the project, billed per use. 0.32-0.53 s a call (12:30).
# Set to None to switch it off.
RERANK_ENDPOINT = ".jina-reranker-v3"
RERANK_TOP = 20             # how many of the blended results it re-orders; the rest keep the blended order
RERANK_SEARCH_LIMIT = 4     # seconds a search waits for it; slower, and the blended order stands (and says so)
RERANK_REST = 60            # after it misses, seconds before it is asked again (so the page does not wait on it)

# The match (M2): an outlet's profile searches the programme.
MATCH_WEIGHTS = {"assignment": 2.0, "beat": 1.0,   # the assignment's votes count double (Aaron, 8 November)
                 "showing": 2.0, "does": 1.0}      # the flip mirrors it: what a sponsor shows at KubeCon counts double
                                                   # (Aaron, 9 November, 12:20, through Saturn)
MATCH_WORDS_TERMS = 25      # words search by profile: how many of its most telling words to search for

# The page (M3). Port 5000 is taken by macOS itself (AirPlay Receiver); 5055-5057 may be in use too; and browsers
# refuse 5060 and 5061 outright (the internet-phone ports, on Chrome's, Safari's and Firefox's blocked lists).
PAGE_HOST = "127.0.0.1"     # this laptop only: the page has no login
PAGE_PORT = 8765
PAGE_RESULTS = 10           # results of each kind shown on the page
PAGE_MAX_TYPED = 4000       # characters accepted in any one box (a picked sponsor's own text runs to 3,678)

# The fit check: AI-written sentences on why the top sponsors may suit the outlet, asked for after the results show.
FITCHECK_ENDPOINT = "openai-chat_completion-k563qy9gg9"   # a chat model already set up in the Elastic project's inference service
FITCHECK_MODEL_NAME = "OpenAI's gpt-4.1"   # said on the page beside what it wrote
FITCHECK_TOP = 3                # how many of the top sponsors it writes about
FITCHECK_LIMIT = 12             # seconds it may take; slower, and the page simply shows no fit check
FITCHECK_PASSAGE_CHARS = 4000   # of each sponsor's own text sent to it (the longest runs to 3,678)
FITCHECK_MAX_TOKENS = 400       # the most it may write in all
FITCHECK_MAX_WORDS = 70         # a longer piece about any one sponsor is not shown
