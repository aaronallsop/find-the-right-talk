"""Import this first: it keeps the meaning model offline and silences the libraries' start-up chatter.

The model is already in the local cache, so it is never fetched; without this every command
printed a torch note, "Could not reach the Hub" and a progress bar before its own output.
"""
import logging, os

os.environ.setdefault("HF_HUB_OFFLINE", "1")              # read the model from the local cache; never wait on the wifi
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
os.environ.setdefault("HF_HUB_VERBOSITY", "error")        # the "Could not reach the Hub" note (offline is on purpose)

# the last one is torch's "Redirects are not supported on macOS" note, printed on every start
for _name in ("sentence_transformers", "huggingface_hub", "transformers", "torch",
              "torch.distributed.elastic.multiprocessing.redirects"):
    logging.getLogger(_name).setLevel(logging.ERROR)
