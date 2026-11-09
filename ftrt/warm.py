"""Wake Elastic's models before a demo: ELSER and, if it is switched on, the re-ranker.

    python -m ftrt.warm

Both sleep when nobody has used them for a while, and the first question after that waits while
they wake (81 s measured once). A search never waits that long: it gives them a few seconds, then
answers without them and says so. Run this a few minutes before presenting (the page also runs it
in the background when it starts) and the first search has everything.
"""
from . import quiet  # noqa: F401  (first: model offline, library chatter off)
from . import config, search
from .engine import connect


def warm(client) -> None:
    for name, wake, why_not in ((config.ELSER_NAME, search.wake_elser, "not in this catalog (it needs Elastic Cloud and a load there)"),
                                (config.RERANK_NAME, search.wake_rerank, "switched off, or not on this engine")):
        try:
            took = wake(client)
            print(f"{name}: awake ({took:.0f} s)" if took is not None else f"{name}: {why_not}")
        except Exception as e:   # the page and searches still work without it
            print(f"{name}: did not wake ({type(e).__name__}); searches will go ahead without it")


def main():
    warm(connect())


if __name__ == "__main__":
    main()
