"""Traces of the page's searches, sent to Dash0 with OpenTelemetry when its settings file is filled in.

The settings file lives OUTSIDE this folder, is filled in by Aaron, and is never printed or committed:
    ~/dash0/.env
        DASH0_AUTH_TOKEN=...                                   the Dash0 auth token
        DASH0_ENDPOINT=https://ingress.<region>.aws.dash0.com  the OTLP (HTTP) endpoint Dash0's settings show
        DASH0_DATASET=default                                  optional
FTRT_DASH0_ENV=/path/to/.env in front of a command reads another file instead. With no file, or no token,
tracing is off and nothing else changes.

What a trace holds: the name of each step (the press door's match, each way of searching, ELSER, Jina, the
re-ranker, fetching the passages), how long each took, how many results it found, and which of Elastic's models
were left out; for a picked outlet or sponsor, its id. Never the text anyone typed, and never the search question.
"""
import contextlib, contextvars, os
from pathlib import Path
from dotenv import dotenv_values
from opentelemetry import trace
from opentelemetry.trace import StatusCode

SETTINGS_FILE = Path(os.environ.get("FTRT_DASH0_ENV") or Path.home() / "dash0" / ".env").expanduser()
SERVICE_NAME = "find-the-right-talk"
tracer = trace.get_tracer("ftrt")   # until setup() succeeds this records nothing


def setup() -> bool:
    """Send traces to Dash0 if its settings file is filled in. True if tracing is on."""
    if not SETTINGS_FILE.exists():
        return False
    v = dotenv_values(SETTINGS_FILE)
    token, endpoint = (v.get("DASH0_AUTH_TOKEN") or "").strip(), (v.get("DASH0_ENDPOINT") or "").strip().rstrip("/")
    if not token or not endpoint:
        return False
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    headers = {"Authorization": f"Bearer {token}"}
    if (v.get("DASH0_DATASET") or "").strip():
        headers["Dash0-Dataset"] = v["DASH0_DATASET"].strip()
    provider = TracerProvider(resource=Resource.create({"service.name": SERVICE_NAME}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces", headers=headers)))
    trace.set_tracer_provider(provider)
    return True


@contextlib.contextmanager
def span(name: str, **attributes):
    """One step of a search, with its own timing. Attributes must never hold typed text or a question."""
    with tracer.start_as_current_span(name, attributes={k: v for k, v in attributes.items() if v is not None},
                                      record_exception=False, set_status_on_exception=False) as s:
        try:
            yield s
        except BaseException as e:   # only the kind of error: its message can name the engine's address
            s.set_status(StatusCode.ERROR, type(e).__name__)
            raise


def carry(fn):
    """The same function, run inside the current request's context even on another thread (the searches run side by
    side): its trace, and its list of the models that sat this request out."""
    parent = contextvars.copy_context()
    def run(*args, **kwargs):
        return parent.copy().run(fn, *args, **kwargs)   # a fresh copy each time: one context cannot run twice at once
    return run


def note(s, results) -> None:
    """Record on a step how many results it found, or that it was left out."""
    s.set_attribute("results", -1 if results is None else len(results))
    s.set_attribute("left_out", results is None)
