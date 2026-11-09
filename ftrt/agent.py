"""An Elastic Agent Builder agent over today's two catalogues, set up from this script.

    python -m ftrt.agent setup                 # creates (or replaces) the 3 tools and the agent in Elastic Cloud
    python -m ftrt.agent instructions          # updates only the agent's instructions, in place, from agent_instructions.md
    python -m ftrt.agent ask "Which sponsors and talks fit the Hello World Gazette?"
    python -m ftrt.agent remove                # deletes the 3 tools and the agent again

Agent Builder is Elastic's own way to give a language model tools over Elasticsearch. Ours are three
read-only queries in ES|QL (Elastic's query language), over ftrt-programme and ftrt-outlets only:
search the programme by ELSER's meaning (optionally one kind, optionally start-ups only), read an
outlet's profile, and read a sponsor's profile. The agent's instructions are in agent_instructions.md:
never invent a company, quote the passage behind every pick, and label every answer AI-written.

Cost and privacy: the agent's language model runs on Elastic's hosted inference service (the project's
default, an Anthropic Claude model), so each question, and the passages the tools return, go there and
are billed per use. Elastic Cloud only; the laptop engine has no Agent Builder. Approved by Aaron, 12:41.
The agent is a second, AI-written way in; it does not run this project's own blend or match.
"""
from . import quiet  # noqa: F401  (first: model offline, library chatter off)
import argparse, json, sys, textwrap, urllib.error, urllib.request
from pathlib import Path
from dotenv import dotenv_values
from . import config

PREFIX = "ftrt"   # every tool and agent this script makes starts with this; it touches nothing else
AGENT_ID = "ftrt-find-the-right-talk"
INSTRUCTIONS = Path(__file__).with_name("agent_instructions.md")

TOOLS = [
    {
        "id": "ftrt.search_programme",
        "type": "esql",
        "description": ("Search the KubeCon + CloudNativeCon North America 2026 programme (talks, events, speakers and "
                        "sponsors) by meaning, using Elastic's ELSER model. Returns up to 15 passages, best first, each with "
                        "the record's name, kind (talk, event, speaker or sponsor), sponsor tier, whether it is a start-up, "
                        "and the passage text. A record can appear more than once (one row per matching passage)."),
        "configuration": {
            "query": f"""FROM {config.PROGRAMME_INDEX} METADATA _score
| WHERE MATCH({config.ELSER_FIELD}, ?question)
| WHERE ?kind == "any" OR kind == ?kind
| WHERE ?startups_only == false OR startup == true
| SORT _score DESC
| KEEP name, kind, tier, startup, text
| LIMIT 15""",
            "params": {
                "question": {"type": "string", "description": "What to look for, in plain words (for an outlet: its assignment or beat)."},
                "kind": {"type": "string", "description": 'One of "any", "talk", "speaker", "sponsor", "event". Use "any" for everything.'},
                "startups_only": {"type": "boolean", "description": "true to return only Start-Up tier sponsors; otherwise false."},
            },
        },
    },
    {
        "id": "ftrt.outlet_profile",
        "type": "esql",
        "description": ("Read a media outlet's profile: what it always covers (part 'beat') and, for some outlets, what it came "
                        "to KubeCon to find (part 'assignment'). Outlets marked SAMPLE are invented examples."),
        "configuration": {
            "query": f"""FROM {config.OUTLETS_INDEX}
| WHERE MATCH(name, ?outlet_name)
| KEEP name, part, real_or_sample, text
| LIMIT 10""",
            "params": {"outlet_name": {"type": "string", "description": "The outlet's name, e.g. Hello World Gazette."}},
        },
    },
    {
        "id": "ftrt.sponsor_profile",
        "type": "esql",
        "description": "Read a KubeCon sponsor's own description: its tier, whether it is a start-up, and its text, passage by passage.",
        "configuration": {
            "query": f"""FROM {config.PROGRAMME_INDEX}
| WHERE kind == "sponsor" AND MATCH(name, ?sponsor_name)
| SORT name ASC, passage_no ASC
| KEEP name, tier, startup, text
| LIMIT 8""",
            "params": {"sponsor_name": {"type": "string", "description": "The sponsor's name, e.g. Kedify."}},
        },
    },
]


def _kibana() -> tuple[str, str]:
    """Kibana's address and the key, from the cloud settings file (never printed). In a serverless project
    Kibana sits beside Elasticsearch, its address the same with ".kb." in place of ".es."."""
    v = dotenv_values(config.CLOUD_SETTINGS_FILE)
    es_url, key = (v.get("ES_CLOUD_URL") or "").strip(), (v.get("ES_CLOUD_API_KEY") or "").strip()
    if not es_url or not key:
        raise SystemExit(f"Agent Builder needs Elastic Cloud: {config.CLOUD_SETTINGS_FILE} is missing or not filled in.")
    return (v.get("KIBANA_URL") or es_url.replace(".es.", ".kb.")).strip().rstrip("/"), key


def _call(method: str, path: str, body: dict | None = None, timeout: int = 300):
    url, key = _kibana()
    req = urllib.request.Request(url + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"ApiKey {key}", "kbn-xsrf": "true", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:   # the message from Kibana; it never contains the key
        return e.code, e.read()[:500].decode("utf-8", "replace")


def _ours(object_id: str) -> str:
    if not object_id.startswith(PREFIX):
        raise SystemExit(f"refusing to touch {object_id}: not one of ours")
    return object_id


def remove():
    for path in [f"/api/agent_builder/agents/{_ours(AGENT_ID)}"] + [f"/api/agent_builder/tools/{_ours(t['id'])}" for t in TOOLS]:
        status, _ = _call("DELETE", path)
        print(f"   removed {path.rsplit('/', 1)[1]}" if status == 200 else f"   {path.rsplit('/', 1)[1]}: not there ({status})")


def setup():
    remove()   # start clean, so running it twice gives the same result
    for tool in TOOLS:
        status, body = _call("POST", "/api/agent_builder/tools", {**tool, "id": _ours(tool["id"]), "tags": ["find-the-right-talk"]})
        if status != 200:
            raise SystemExit(f"Could not create tool {tool['id']}: {status} {body}")
        print(f"   tool {tool['id']}: created")
    agent = {"id": _ours(AGENT_ID), "name": "Find the Right Talk",
             "description": "Finds the KubeCon talks, speakers and sponsors that fit a media outlet, quoting the passage behind each pick.",
             "configuration": {"instructions": INSTRUCTIONS.read_text(encoding="utf-8"),
                               "tools": [{"tool_ids": [t["id"] for t in TOOLS]}],
                               # only our three tools: none of Elastic's general ones, which could read any catalogue
                               "enable_elastic_capabilities": False}}
    status, body = _call("POST", "/api/agent_builder/agents", agent)
    if status != 200:
        raise SystemExit(f"Could not create the agent: {status} {body}")
    print(f"   agent {AGENT_ID}: created. In Kibana: Agents, then 'Find the Right Talk'.")


def instructions():
    """Update only the agent's instructions, in place: its tools and every other setting stay as they are."""
    status, current = _call("GET", f"/api/agent_builder/agents/{_ours(AGENT_ID)}")
    if status != 200:
        raise SystemExit(f"The agent is not there ({status}); run setup first.")
    configuration = {**current["configuration"], "instructions": INSTRUCTIONS.read_text(encoding="utf-8")}
    status, body = _call("PUT", f"/api/agent_builder/agents/{AGENT_ID}",
                         {"name": current["name"], "description": current.get("description", ""), "configuration": configuration})
    if status != 200:
        raise SystemExit(f"Could not update the instructions: {status} {body}")
    print(f"   agent {AGENT_ID}: instructions updated ({len(configuration['instructions'])} characters); tools unchanged")


def ask(question: str):
    status, body = _call("POST", "/api/agent_builder/converse", {"agent_id": AGENT_ID, "input": question})
    if status != 200:
        raise SystemExit(f"The agent did not answer: {status} {body}")
    for step in body.get("steps", []):
        if step.get("type") == "tool_call":
            print(f"   tool used: {step.get('tool_id')} {json.dumps(step.get('params', {}))}")
    print("\n--- AI-written answer from Elastic Agent Builder ---\n")
    print(textwrap.indent((body.get("response") or {}).get("message", "(no message)"), "   "))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["setup", "instructions", "ask", "remove"])
    ap.add_argument("question", nargs="?")
    a = ap.parse_args()
    if a.action == "ask" and not a.question:
        sys.exit("ask needs a question in quotes")
    {"setup": setup, "instructions": instructions, "remove": remove, "ask": lambda: ask(a.question)}[a.action]()


if __name__ == "__main__":
    main()
