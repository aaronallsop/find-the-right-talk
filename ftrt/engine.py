"""One way to reach Elasticsearch, in the cloud or on this laptop.

Two settings files live OUTSIDE this folder and are never copied into it:
  ~/elastic-cloud/.env          ES_CLOUD_URL and ES_CLOUD_API_KEY for the Elastic Cloud serverless project
  ~/elastic-start-local/.env    ES_LOCAL_URL and ES_LOCAL_PASSWORD, written by Elastic's start-local installer
If the cloud file is filled in, the cloud is used; otherwise the local engine. FTRT_ENGINE=local or
FTRT_ENGINE=cloud in the environment forces one or the other (the laptop is the demo's fallback).
FTRT_CLOUD_ENV=/path/to/.env reads another cloud project's settings file instead of ~/elastic-cloud/.env.
"""
import os, sys
from elasticsearch import Elasticsearch
from dotenv import dotenv_values, load_dotenv
from . import config


def _cloud_settings() -> tuple[str, str] | None:
    if not config.CLOUD_SETTINGS_FILE.exists():
        return None
    values = dotenv_values(config.CLOUD_SETTINGS_FILE)
    url, key = (values.get("ES_CLOUD_URL") or "").strip(), (values.get("ES_CLOUD_API_KEY") or "").strip()
    return (url, key) if url and key else None


def where() -> str:
    """'cloud' or 'local': which engine the next connect() will use."""
    forced = os.environ.get("FTRT_ENGINE", "").lower()
    if forced in ("cloud", "local"):
        return forced
    return "cloud" if _cloud_settings() else "local"


def connect() -> Elasticsearch:
    mode = where()
    if mode == "cloud":
        settings = _cloud_settings()
        if not settings:
            raise SystemExit(f"FTRT_ENGINE=cloud but {config.CLOUD_SETTINGS_FILE} is missing or not filled in.")
        url, key = settings
        client = Elasticsearch(url, api_key=key, request_timeout=120, connections_per_node=config.CONNECTIONS)
        label = "Elastic Cloud serverless"
    else:
        load_dotenv(config.ENGINE_SETTINGS_FILE)
        password = os.environ.get("ES_LOCAL_PASSWORD")
        if not password:
            raise SystemExit(f"No engine password found in {config.ENGINE_SETTINGS_FILE}. Is Elasticsearch installed with start-local?")
        url = os.environ.get("ES_LOCAL_URL", config.ENGINE_DEFAULT_URL)
        client = Elasticsearch(url, basic_auth=(config.ENGINE_USER, password), request_timeout=120, connections_per_node=config.CONNECTIONS)
        label = f"local engine at {url}"
    try:
        client.info()
    except Exception as e:  # the message names the cause, never the key or password
        raise SystemExit(f"Could not reach the {label}: {type(e).__name__}. Check it is running and the settings file is right.")
    print(f"Engine: {label}", file=sys.stderr)
    return client
