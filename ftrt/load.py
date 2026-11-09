"""Load the spreadsheets into two new, empty catalogues.

    python -m ftrt.load            # rebuilds both catalogues from data/
    python -m ftrt.load --check    # only prints the counts and the email check, loads nothing

Each record is cut into passages; each passage becomes one document holding the passage's
words and its 384 meaning numbers, plus the record's details, so a search can report the
record and the passage that made it match.
"""
from . import quiet  # noqa: F401  (first: model offline, library chatter off)
import argparse, csv, re, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from elasticsearch import helpers
from . import config, engine, passages
from .engine import connect


def read_csv(name: str) -> list[dict]:
    with open(config.DATA_DIR / f"{name}.csv", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_records() -> tuple[list[dict], list[dict]]:
    programme = [passages.session_record(r) for r in read_csv("sessions")]
    programme += [passages.speaker_record(r) for r in read_csv("speakers")]
    programme += [passages.sponsor_record(r) for r in read_csv("sponsors")]
    outlets = [rec for r in read_csv("outlets") for rec in passages.outlet_records(r)]
    return programme, outlets


def mapping() -> dict:
    keyword = {"type": "keyword"}
    cloud = engine.where() == "cloud"
    # Elastic Cloud serverless manages shards itself and refuses these settings; the laptop engine wants them.
    settings = {} if cloud else {"settings": {"number_of_shards": 1, "number_of_replicas": 0}}
    # In the cloud, each passage also goes to Elastic's own meaning model (ELSER), which Elastic runs at load time,
    # and carries its Jina numbers, fetched from Elastic's hosted inference service before the load.
    elser = {config.ELSER_FIELD: {"type": "semantic_text", "inference_id": config.ELSER_ENDPOINT},
             config.JINA_FIELD: {"type": "dense_vector", "dims": config.JINA_SIZE, "index": True, "similarity": "cosine"}} if cloud else {}
    return {
        **settings,
        "mappings": {"properties": {
            "record_id": keyword, "kind": keyword, "part": keyword,
            "name": {"type": "text", "analyzer": "english", "fields": {"keyword": {"type": "keyword"}}},
            "passage_no": {"type": "integer"}, "passage_count": {"type": "integer"},
            # the passage itself: searched by words (analysed) and kept whole (raw) so absence can be proven
            "text": {"type": "text", "analyzer": "english", "fields": {"raw": {"type": "keyword", "ignore_above": 8000}}},
            "vector": {"type": "dense_vector", "dims": config.VECTOR_SIZE, "index": True, "similarity": "cosine"},
            # record details
            "track": keyword, "day": keyword, "date": keyword, "time": keyword, "room": keyword, "level": keyword,
            "speakers": keyword, "companies": keyword, "topics": keyword, "talks": keyword, "job": keyword,
            "tier": keyword, "startup": {"type": "boolean"}, "booth": keyword, "website": keyword, "source_quality": keyword,
            "real_or_sample": keyword, "sample": {"type": "boolean"}, "has_assignment": {"type": "boolean"}, "written_by": keyword,
            **elser,
        }},
    }


def documents(records: list[dict], vectors, elser: bool = False, jina: list | None = None) -> list[dict]:
    docs, i = [], 0
    for rec in records:
        details = {k: v for k, v in rec.items() if k != "passages"}
        for n, text in enumerate(rec["passages"]):
            suffix = f"#{rec['part']}" if "part" in rec else ""
            docs.append({"_id": f"{rec['record_id']}{suffix}#{n}", **details, "passage_no": n,
                         "passage_count": len(rec["passages"]), "text": text, "vector": vectors[i].tolist(),
                         **({config.ELSER_FIELD: text} if elser else {}),
                         **({config.JINA_FIELD: jina[i]} if jina else {})})
            i += 1
    return docs


def jina_vectors(client, texts: list[str]) -> list[list[float]]:
    """Every passage's Jina numbers, from Elastic's hosted inference service, in batches. Any refusal stops the
    load here, before a catalogue is deleted."""
    batches = [texts[i:i + config.JINA_BATCH] for i in range(0, len(texts), config.JINA_BATCH)]
    def one(batch):
        r = client.options(request_timeout=120).inference.text_embedding(
            inference_id=config.JINA_ENDPOINT, input=batch, timeout="120s")
        return [e["embedding"] for e in r.body["text_embedding"]]
    with ThreadPoolExecutor(max_workers=config.JINA_PARALLEL) as pool:   # results come back in batch order
        out = [v for got in pool.map(one, batches) for v in got]
    assert len(out) == len(texts) and len(out[0]) == config.JINA_SIZE
    return out


def recreate(client, index: str):
    if not index.startswith(config.OWN_PREFIX):
        raise SystemExit(f"refusing to touch {index}: not one of ours")
    if client.indices.exists(index=index):
        client.indices.delete(index=index)
    client.indices.create(index=index, **mapping())


def email_check(client, index: str) -> int:
    """Search the loaded passages for an email address. Returns how many passages hold one.

    Asks the engine for every passage containing an @ sign, then tests each for the shape of
    an email address (speakers' social handles like @jbaruch are not addresses and are fine).
    """
    with_at = client.search(index=index, query={"wildcard": {"text.raw": {"value": "*@*"}}}, size=500)["hits"]["hits"]
    email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
    found = [h for h in with_at if email.search(h["_source"]["text"])]
    for h in found[:5]:
        print(f"   FOUND in {h['_source']['name']}: {h['_source']['text'][:200]}")
    print(f"   ({len(with_at)} passages contain an @ sign, as social handles or phrasing)")
    return len(found)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="print the counts and run the email check; load nothing")
    args = ap.parse_args()
    started = time.time()

    programme, outlets = build_records()
    kinds = Counter(r["kind"] for r in programme)
    print("Records read from the spreadsheets:")
    for kind in ("talk", "event", "speaker", "sponsor"):
        print(f"   {kinds[kind]:5d} {kind}s, in {sum(len(r['passages']) for r in programme if r['kind']==kind)} passages")
    outlet_ids = {r["record_id"] for r in outlets}
    print(f"   {len(outlet_ids):5d} outlets ({sum(1 for r in outlets if r['part']=='assignment')} with a KubeCon assignment), in {sum(len(r['passages']) for r in outlets)} passages")

    client = connect()
    elser = engine.where() == "cloud"
    if elser and not args.check:   # ELSER sleeps when idle: wake it BEFORE anything is deleted, so a failure changes nothing
        t = time.time()
        client.options(request_timeout=config.ELSER_TIMEOUT).inference.inference(
            inference_id=config.ELSER_ENDPOINT, input=["wake up"], timeout=f"{config.ELSER_TIMEOUT}s")
        print(f"Elastic's ELSER model is awake ({time.time()-t:.0f}s); it reads each passage as it loads, which takes some minutes")
    if not args.check:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(config.MODEL_NAME)
        prepared = []   # everything is computed first; only then is any catalogue deleted and rebuilt
        for index, records in ((config.PROGRAMME_INDEX, programme), (config.OUTLETS_INDEX, outlets)):
            texts = [p for r in records for p in r["passages"]]
            t = time.time()
            vectors = model.encode(texts, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
            assert vectors.shape == (len(texts), config.VECTOR_SIZE)
            print(f"Turned {len(texts)} passages into {config.VECTOR_SIZE} numbers each for {index} in {time.time()-t:.0f}s")
            jina = None
            if elser:
                t = time.time()
                jina = jina_vectors(client, texts)
                print(f"Fetched {len(texts)} passages' {config.JINA_SIZE} Jina numbers from Elastic's hosted service in {time.time()-t:.0f}s")
            prepared.append((index, records, texts, vectors, jina))
        for index, records, texts, vectors, jina in prepared:
            recreate(client, index)
            ok, errors = helpers.bulk(client.options(request_timeout=config.ELSER_TIMEOUT), documents(records, vectors, elser, jina),
                                      index=index, chunk_size=100 if elser else 500, max_retries=3, initial_backoff=5,
                                      raise_on_error=False, stats_only=False)
            if errors:   # a partial catalogue would quietly change every result: stop and say so
                raise SystemExit(f"{len(errors)} of {len(texts)} passages failed to load into {index}; first: {str(errors[0])[:300]}. Run the loader again.")
            client.indices.refresh(index=index)

    print("Now in the engine:")
    for index in (config.PROGRAMME_INDEX, config.OUTLETS_INDEX):
        if not client.indices.exists(index=index):
            print(f"   {index}: does not exist yet")
            continue
        total = client.count(index=index)["count"]
        by_kind = client.search(index=index, size=0, aggs={"k": {"terms": {"field": "kind"}, "aggs": {"records": {"cardinality": {"field": "record_id", "precision_threshold": 40000}}}}})
        parts = ", ".join(f"{b['records']['value']} {b['key']}s in {b['doc_count']} passages" for b in by_kind["aggregations"]["k"]["buckets"])
        print(f"   {index}: {total} passages: {parts}")
        print(f"   email addresses found in {index}: {email_check(client, index)}")
    print(f"Done in {time.time()-started:.0f}s")


if __name__ == "__main__":
    main()
