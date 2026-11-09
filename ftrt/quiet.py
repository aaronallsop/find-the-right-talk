"""Import this first: it keeps the meaning model offline once it is on this machine, and silences the
libraries' start-up chatter.

On a machine that has never run this, the first command fetches the model (about 90 MB, once) from
Hugging Face. After that the model is read from the local cache and the internet is never asked, so
flaky venue wifi cannot stall a search. Without the silencing every command printed a torch note,
"Could not reach the Hub" and a progress bar before its own output.
"""
import logging, os
from pathlib import Path

_MODEL_CACHE = "models--sentence-transformers--all-MiniLM-L6-v2"   # the cache folder of config.MODEL_NAME


def _model_is_cached() -> bool:
    hub = os.environ.get("HF_HUB_CACHE") or Path(os.environ.get("HF_HOME") or Path.home() / ".cache" / "huggingface") / "hub"
    snapshots = Path(hub).expanduser() / _MODEL_CACHE / "snapshots"
    # the whole model, not just the small tokeniser files that splitting text into passages fetches first
    return all(any(snapshots.glob(f"*/{name}")) for name in ("model.safetensors", "modules.json", "1_Pooling/config.json"))


if _model_is_cached():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")          # read the model from the local cache; never wait on the wifi
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
os.environ.setdefault("HF_HUB_VERBOSITY", "error")        # the "Could not reach the Hub" note (offline is on purpose)
# The Elasticsearch library traces its own requests once tracing is on, with the engine's full address in each; only
# this project's named steps go to Dash0 (ftrt/tracing.py), so the library's own tracing stays off.
os.environ["OTEL_PYTHON_INSTRUMENTATION_ELASTICSEARCH_ENABLED"] = "false"
os.environ["OTEL_PYTHON_INSTRUMENTATION_ELASTICSEARCH_CAPTURE_SEARCH_QUERY"] = "omit"

# the last one is torch's "Redirects are not supported on macOS" note, printed on every start
for _name in ("sentence_transformers", "huggingface_hub", "transformers", "torch",
              "torch.distributed.elastic.multiprocessing.redirects"):
    logging.getLogger(_name).setLevel(logging.ERROR)
