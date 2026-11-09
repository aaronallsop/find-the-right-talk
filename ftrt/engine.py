"""One way to reach Elasticsearch. Reads the password from the settings file outside this folder."""
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from . import config


def connect() -> Elasticsearch:
    load_dotenv(config.ENGINE_SETTINGS_FILE)
    password = os.environ.get("ES_LOCAL_PASSWORD")
    if not password:
        raise SystemExit(f"No engine password found in {config.ENGINE_SETTINGS_FILE}. Is Elasticsearch installed with start-local?")
    url = os.environ.get("ES_LOCAL_URL", config.ENGINE_DEFAULT_URL)
    client = Elasticsearch(url, basic_auth=(config.ENGINE_USER, password), request_timeout=120)
    if not client.ping():
        raise SystemExit(f"The engine at {url} is not answering. Start it (see README) and try again.")
    return client
