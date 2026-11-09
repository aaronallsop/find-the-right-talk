"""The flip: a sponsor finds the outlets that fit it, and the talks nearest to it.

    python -m ftrt.flip "Kedify"                                  # blended: outlets, then talks
    python -m ftrt.flip --mode compare "Kedify"
    python -m ftrt.flip --list                                    # the 226 sponsors
    options: --mode words|meaning|elser|jina|blended|reranked|compare, -n 5 (how many talks; every outlet is ranked)

The match turned round. A sponsor has two parts: what it does (its own description, what it
makes, who it is for, the problems it solves) and what it is showing at KubeCon (empty for most
sponsors). Each part searches the outlets, by meaning, by its most telling words and, in Elastic
Cloud, by Elastic's ELSER, and the rankings are merged by reciprocal rank fusion, the KubeCon part
counting double as the outlet's assignment does in the match. Each outlet comes with its own
passage that matched. A sponsor with nothing for KubeCon is matched on what it does alone.
"""
from . import quiet  # noqa: F401  (first: model offline, library chatter off)
import argparse
from concurrent.futures import ThreadPoolExecutor
from . import config, load, match, passages, tracing
from .engine import connect

TALKS = "talk"


def sponsor_rows() -> dict[str, dict]:
    return {r["id"]: r for r in load.read_csv("sponsors")}


def find_sponsor(wanted: str) -> dict:
    """A sponsor's row, from its id or any part of its name (an exact name wins)."""
    rows = sponsor_rows()
    if wanted in rows:
        return rows[wanted]
    exact = [r for r in rows.values() if r["name"].lower() == wanted.lower()]
    hits = exact or [r for r in rows.values() if wanted.lower() in r["name"].lower()]
    if len(hits) != 1:
        names = ", ".join(r["name"] for r in hits[:8])
        raise SystemExit(f"{'No' if not hits else 'More than one'} sponsor matches {wanted!r}{': ' + names if hits else ''}. Try --list.")
    return hits[0]


def sponsor_texts(row: dict) -> dict[str, str]:
    """A sponsor's two parts, in the same sentences the loader writes for it."""
    does = " ".join(filter(None, [
        passages._sentence("", row["conference_description"]),
        passages._sentence("", row["ai_what_they_do"]),
        passages._sentence("Who it is for", row["ai_who_its_for"]),
        passages._sentence("Problems solved", row["ai_problems_solved"]),
        passages._sentence("Products", row["ai_products"]),
    ]))
    return {"does": does, "showing": passages._sentence("At KubeCon", row["ai_at_kubecon"])}


def typed_texts(does: str, showing: str = "") -> dict[str, str]:
    """The vendor door's two boxes."""
    return {"does": passages._sentence("", does), "showing": passages._sentence("At KubeCon", showing)}


def flip(client, parts: dict, n_talks: int = 10) -> dict[str, dict[str, list[dict]]]:
    """{"outlet": {way: [...]}, "talk": {way: [...]}}: every outlet ranked, and the nearest talks."""
    every_outlet = 100   # far more than there are; the outlets catalogue is small
    with ThreadPoolExecutor(max_workers=2) as pool:   # the two are independent: ask both at once
        outlets = pool.submit(tracing.carry(match.match), client, parts, every_outlet, "outlet", index=config.OUTLETS_INDEX)
        talks = pool.submit(tracing.carry(match.match), client, parts, n_talks, TALKS)
        return {"outlet": outlets.result(), TALKS: talks.result()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sponsor", nargs="?", help="a sponsor's name (any part of it) or id")
    ap.add_argument("--mode", choices=["words", "meaning", "elser", "jina", "blended", "reranked", "compare"], default="blended")
    ap.add_argument("-n", type=int, default=5, help="how many talks (1 to 50)")
    ap.add_argument("--list", action="store_true", help="list the sponsors and stop")
    a = ap.parse_args()
    if a.list or not a.sponsor:
        for r in sorted(sponsor_rows().values(), key=lambda r: r["name"].lower()):
            print(f"   {r['name']}  ({r['tier']})")
        return
    row = find_sponsor(a.sponsor)
    client = connect()
    parts = match.parts_from_text(sponsor_texts(row))
    print(f"\nFlipping {row['name']} ({row['tier']}), on " + (
        "what it does and what it is showing at KubeCon (counting double)" if "showing" in parts else
        "what it does alone (it says nothing about what it is showing at KubeCon)"))
    results = flip(client, parts, min(max(a.n, 1), 50))
    for kind, label in (("outlet", "outlets"), (TALKS, "talks")):
        res = results[kind]
        voices = len([w for w in ("words", "meaning", "elser", "jina") if w in res])
        for mode in (("words", "meaning", "elser", "jina", "blended", "reranked") if a.mode == "compare" else (a.mode,)):
            if mode not in res:
                print(f"\n=== {mode.upper()} === ({match.MISSING[mode]})")
                continue
            lists = len(parts) * (voices if mode == "blended" else 1)
            rows = [{**r, "tier": "sample" if r.get("sample") else r.get("tier")} for r in res[mode]]
            match.show(f"=== {mode.upper()} === {label} for {row['name']}", rows, lists)


if __name__ == "__main__":
    main()
