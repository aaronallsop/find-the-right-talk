# find-the-right-talk

**Which talks and sponsors at KubeCon should a given media outlet cover?** Pick an outlet and this
ranks the programme (talks, speakers and sponsors) by how well each fits what that outlet covers,
and shows the passage that made each one match. Turn the same engine round and a sponsor finds the
outlets and talks that fit it. Start-ups can be shown on their own, so a small company with the
right story surfaces beside the big names.

It runs on Elastic Cloud serverless, searches the programme by words and by meaning, and in the
cloud adds Elastic's own ELSER model, Jina's embedding model and Elastic's hosted re-ranker as
further voices. It also has an Elastic Agent Builder agent, a code review by Gitar, tracing
in Dash0, and a hosted copy on Radar. All the code
was written on 9 November 2026, at the WeMakeDevs Cloud Native Hackathon, Elasticsearch track, Salt
Lake City, by Claude Code under the direction of Aaron Allsop.

## What you can see

- **Two doors on one page.** "I'm press": pick an outlet, or type what it always covers and what
  it came to KubeCon to find, and get the talks, speakers and sponsors that fit, each with the
  passage that matched and the part of the outlet's profile that found it. "I'm a vendor" (the
  flip): pick a sponsor, or describe your company, and get the outlets whose beat and KubeCon
  assignment fit it, each with the outlet's own passage, and the talks nearest to what you do.
  What a sponsor is showing at KubeCon, like an outlet's assignment, counts double.
- **The start-up flag.** A "Start-ups only" switch narrows every sponsor list to the 32 start-ups
  among the 226 sponsors, and switching it off brings the full lists back.
- **Words, meaning, and Elastic's voice.** On the page, "Compare all" shows six
  columns side by side (words, meaning, Elastic's ELSER, Jina's embeddings, blended, re-ranked), and a switch picks
  one; in Terminal, compare mode runs one search every way. Either way you can watch them disagree. Words win on an exact name ("SLSA
  Level 3"); meaning wins when no one uses your words ("scale up for a traffic spike and back down
  afterwards" finds the start-up Kedify, where words find nothing).
- **A "Re-ranked" view.** Elastic's re-ranking model re-orders the blended top twenty, so the list
  can be shown before and after.

## Where Elastic is used

- **Elastic Cloud serverless** holds every talk, speaker, sponsor and outlet in two catalogues,
  cut into short passages; each passage is stored as words and as a list of 384 numbers that
  capture its meaning.
- **Elasticsearch** does the words search, the meaning (vector) search and the filters in one place.
- **Elastic's own ELSER model**, running inside the project, reads every passage as it loads and
  every search's text, and gets one vote in the blend (cloud only).
- **Jina's embedding model** (`.jina-embeddings-v3`, through Elastic's hosted inference service)
  also reads every passage at load time, and gets one vote in the blend and one column in Compare
  all (cloud only; left out on the laptop engine). All 2,250 passages are sent to that hosted
  service once at load, and each search's question when it runs, billed per use.
- **Elastic's hosted re-ranker** (Jina, through Elastic's inference service) re-orders the blended
  top 20 in the "Re-ranked" view (cloud only). For that view only, the search text (or the outlet's
  or sponsor's profile) and those 20 passages are sent to Elastic's hosted inference service, which
  is outside your own Elastic Cloud project and is billed per use. The re-ranker is not used on
  the laptop engine. Only the ELSER, words and meaning views stay inside your own Elastic Cloud
  project; Jina's embeddings (above), the re-ranker and the agent use Elastic's hosted service. About half a
  second is added to a search and 1 to 1.5 seconds to a page "Go" (measured 9 November).
- **Elastic Agent Builder** runs an AI agent, "Find the Right Talk" (in Kibana: Agents), with three
  read-only tools over today's two catalogues only. It is a second, AI-written way in, not the
  engine: it does not run the project's own blend. Its answers come from a language model reached
  through Elastic's AI connector in the project: since about 14:20 on 9 November that is an OpenAI
  model (gpt-4.1) through an endpoint the author created; before that it was the project's default
  model, Anthropic's Claude Sonnet 4.5 on Elastic's hosted inference service. Elastic's own models do
  the searching; the connector's model only writes the answer. The questions and the passages the
  agent reads go to that model, billed per use. Every answer ends "AI-written by the Find the Right
  Talk agent (Elastic Agent Builder). Check each quoted passage before you rely on it." The agent
  must quote the programme's own passage for every company or talk it suggests. Checked on 9 November:
  on the earlier model, all 14 quotations in one Gazette answer were word for word (Titan); on the
  OpenAI model one answer took 7 seconds, and 2 of its 13 quotations were not word for word (Cassini).
  The author is deciding how to proceed, so this is an open limit.
- **The blend is this project's own code:** each ranked list votes (reciprocal rank fusion), so it
  takes any number of voices.
- **Geo queries are not used:** the data has no coordinates (rooms in one building and a region
  word per outlet), so a map would be decoration.

## What Elastic asked entrants to use

Status at 14:05 on 9 November, one line each:

1. **Elastic Cloud serverless:** done. Everything runs on a serverless Elasticsearch project.
2. **Ingesting data:** done. The programme, speakers, sponsors and outlets are loaded as 2,250
   passages into two catalogues.
3. **Jina models for embeddings:** done. Jina's embedding model is one more voice in the blend, and
   Elastic's hosted Jina re-ranker re-orders the blended top 20 (the "Re-ranked" view).
4. **An Agent Builder agent with custom tools:** done. "Find the Right Talk" has three tools of our
   own over the two catalogues, and its answers come from the model behind Elastic's AI connector.
5. **Elastic Workflows:** not used. The plan was to try it only if everything else was done by 15:00,
   with a 45-minute cap; at 14:05 it had not been started.

**The main code files, so you can see Elasticsearch is the core** (all in `ftrt/` unless said):

- `engine.py`: the one way the code reaches Elasticsearch: Elastic Cloud serverless by default, the
  laptop engine as the fallback.
- `load.py`: rebuilds the two catalogues from the spreadsheets, one document per passage, each with
  its words, 384 numbers from the small model, Elastic's ELSER reading and 1,024 Jina numbers (all the
  numbers are gathered first, so a failure never leaves a half-built catalogue).
- `search.py`: the ways of searching (words, meaning, Elastic's ELSER, Jina), the blend (reciprocal
  rank fusion, in this project's own code), the re-ranked view and Compare all.
- `match.py` and `flip.py`: the press door (an outlet's beat and KubeCon assignment search the
  programme, the assignment counting double) and the vendor door (a sponsor finds its outlets and
  nearest talks).
- `agent.py` (with `agent_instructions.md`): sets up the Elastic Agent Builder agent and its three
  read-only tools from a script.
- `page.py` and `page.html`: the two-door page on this laptop, with Compare all and the start-ups
  switch.
- `tracing.py`: sends a trace of each search to Dash0 with OpenTelemetry (step names and timings
  only, never the typed text or the question).
- `hosted/app.py` (with `hosted/Dockerfile` and `hosted/radar/deployment.yaml`): the lean hosted page
  (words, ELSER and Jina), meant to be served through Radar once the Argo CD step is applied.

## The other sponsor tools

Status at 14:05 on 9 November:

- **Gitar:** done. It reviewed all of today's code; its one finding was confirmed and fixed, and
  Gitar now says "Approved" (the start-ups switch could leave an older answer on screen); see
  "Who did what, and how AI was used". Nothing it wrote was merged.
- **Dash0:** done and confirmed. The author's Dash0 dashboard shows one service (the page) with three
  operations (press door, vendor door, plain search), traces from about 14:01 to 14:05 and at about 14:20, the slowest about 2.9 seconds, and no errors. It traces the laptop page only; the hosted Radar copy is not traced. Tracing: when a Dash0 settings file (`~/dash0/.env`, with
  `DASH0_AUTH_TOKEN` and `DASH0_ENDPOINT`, kept outside the project and never committed) is filled
  in, the page sends a trace of each search to Dash0 using OpenTelemetry. Without the file, tracing
  is off and nothing else changes. What goes to Dash0: the names of the steps (the match, each way
  of searching, the re-rank, fetching passages), how long each took, how many results each found,
  which of Elastic's models were left out, and the id of a picked outlet or sponsor. What never
  goes: the text anyone typed, or the search question. Error messages are kept out of the traces
  too, so the cloud address does not travel with them.
- **Radar:** done, and live (Dione checked it from the public address, and Saturn opened it in a browser). A hosted copy runs at
  https://caiv.cnh.radarhq.io on Radar's Kubernetes cluster, deployed by GitOps (Argo CD) from
  github.com/aaronallsop/caiv-radar. It leaves out the laptop's own meaning model, so its rankings can
  differ slightly from the laptop page: it offers Blended, Words, ELSER, Jina, Re-ranked and Compare
  all, and no plain Meaning way, by design. Opened in a real browser, it showed 14 outlets and 226
  sponsors, and the Hello World Gazette's match came back with Docker, Momentic and JetBrains first,
  each with its passage. The cluster is deleted on 13 November. The hosted copy uses
  the author's own Elastic Cloud project through a cluster secret, so a visitor's search is run, and
  billed per use, on that project, and the text of a search goes to Elastic's models (and, in the
  Re-ranked view, to Elastic's hosted service) as described above. It limits each visitor to 20
  requests a minute and the whole page to 120 a minute.

## Where it falls short

Measured on 9 November against two test outlets whose answer keys were written beforehand
(`notes/answer-keys.md`; the scoring is in `notes/checks.md`):

- **The Hello World Gazette** (a sample outlet, invented and labelled) finds its hidden gem,
  mirrord, and two of its three must-find companies in the top ten. Faros, a tool a manager uses to
  see what coding agents cost, comes 13th, so it misses the answer key by one company.
- **The Breach Chronicle** (also a labelled sample, not used in the demo) misses: none of its
  must-finds is in its top ten, because its wording is about attacks while its companies talk about
  vulnerabilities and sandboxes. It stays in the data as a reported miss.
- **The flip** (a sponsor finds outlets) puts its outlets in a weak order, because the scores bunch
  close together; the talks it finds are on target.
- **The ranking is not exactly repeatable at places 9 and 10.** In 13 runs of the Gazette at the same
  settings the blended top eight and the re-ranked top nine never changed, but places 9 and 10 flipped
  between two versions (Cosmonic and Syntasso, or Syntasso and Dash0), because Jina's scores differ in
  the fourth decimal in some runs. Words, meaning and ELSER never changed.
- **Meaning finds the topic, not the stance:** re-ranked, the GPU search puts vCluster (which
  shares GPUs) above Edera (which isolates them); the re-ranker cannot tell the stance either.
- **It never says "nothing fits":** meaning always returns the nearest thing.
- **The fit check, an AI judgement of the top results, was not built.** The Agent Builder agent is a
  different thing: it answers in words, and in a check on 9 November 2 of 13 quotations in one answer were not word
  for word, so check each quoted passage against the programme.

## What existed before the day, and what was built on it

- **Before 9 November (allowed under rules 1 and 2):** the idea; notes and research (`notes/`);
  the public programme, copied once with credit; the sponsor and outlet profiles in `data/`,
  including six invented sample outlets, labelled, two of them test cases whose answer keys were
  written in advance (`notes/answer-keys.md`). Aaron built the same search pattern for his own
  video library the week before, as a separate private project; none of its code is in this
  repository. This project was rebuilt from scratch on the day.
- **On 9 November, after 11:00:** all of the code, saved one piece at a time (the time is the save):
  11:00 the repository, no code; 11:04 the loader; 11:07 search three ways from Terminal; 11:21 the
  Elastic Cloud connection (laptop engine as fallback); 11:47 passages fit what the meaning model
  reads; 11:48 the match; 11:54 the page; 11:56 steadier results; 12:12 Elastic's ELSER as a further
  voice; 12:14 the page moves to port 8765; 12:17 the flip; 12:25 the start-ups switch; 12:29 a slow
  Elastic model never blanks the page, and the warm-up command; 12:32 Elastic's hosted re-ranker; 12:46 the Agent Builder agent; 13:22 a code review by Gitar, and its one finding fixed;
  13:44 Jina's embeddings as a further voice; 13:49 Dash0 tracing; 14:00 the hosted copy for Radar, live by about 14:15.
  The commit history starts at the beginning of the hackathon: the first commit holds no code, only
  the data, the notes, the rulebook (`CLAUDE.md`), the licence, the ignore list and this README.

## Who did what, and how AI was used

- **Aaron Allsop:** the idea; the two test outlets, the Hello World Gazette and the Breach
  Chronicle (their names, audiences, beats and KubeCon assignments); every product decision; and
  the checks listed below.
- **Claude Code (Anthropic):** wrote the code, under Aaron's direction, during the hackathon:
  Claude Fable 5.1 for the first hour, then Claude Opus 5.5, with Claude Sonnet 5.5 keeping the
  to-do board, checking results and minding the engine. Every commit it made says so.
- **Before the day,** Claude also drafted the sponsor profiles (from each company's website, or
  its conference listing where the site could not be read) and the real outlets' profiles (from
  their own pages), and wrote up the sample outlets: four it invented, two from Aaron's briefs.
  Each is labelled in the data.
- **The meaning search** uses all-MiniLM-L6-v2, a small open-source model that runs on this
  laptop and generates no text. In Elastic Cloud, every passage, and the text of every search, is
  also read by Elastic's own ELSER model, which runs inside the project's own Elastic Cloud
  deployment, not on a separate service. The "Re-ranked" view and Jina's embeddings are exceptions: the first sends
  the search text and the top 20 passages to Elastic's hosted re-ranking service, the second sends
  every passage once at load and each search's question when it runs to Elastic's hosted inference
  service (see above). The
  Agent Builder agent is the other: its answers are written by an OpenAI model (gpt-4.1) reached
  through Elastic's AI connector, so its questions and the passages it reads go to OpenAI, billed to
  the author; they are labelled as AI-written.
- **Gitar** reviewed all of today's code on a review pull request that was never merged: it
  first approved with suggestions, and now says "Approved" with its one finding closed. The finding was confirmed and fixed (the start-ups switch could
  leave an older answer on screen when switching doors or mid-search; every answer now re-runs if the
  setting changed). A second note, that the loader rebuilds both catalogues from the spreadsheets,
  is by design. Nothing Gitar wrote was merged.
- [If used: Gemini (Google) read the README as a newcomer would and answered questions; it
  wrote none of the code.]

## Checked by Aaron

[One line per check Aaron did himself on the day, and what he saw.]

## Set it up

You do not need to run it to judge it. To run it yourself, from a fresh copy of this repository
(the steps below were followed from a clean clone into an empty folder at 11:53 on 9 November; the
test passed, and the fixes it called for have since been made to this README):

1. Create your own Elastic Cloud serverless Elasticsearch project at cloud.elastic.co. The author's
   project and key are not in this repository and cannot be used; you need your own.
2. Make a file `~/elastic-cloud/.env` with two lines, `ES_CLOUD_URL=` the project's endpoint and
   `ES_CLOUD_API_KEY=` an API key for it. When that file is filled in, every command below uses
   Elastic Cloud. It is never copied into this repository. To use a settings file kept somewhere
   else, put `FTRT_CLOUD_ENV=/path/to/.env` in front of a command.
   **Alternative, on your laptop only:** install Docker Desktop and start it, then install
   Elasticsearch and Kibana locally with Elastic's start-local script, **run from your home
   folder**: `cd ~ && curl -fsSL https://elastic.co/start-local | sh` (it creates `~/elastic-start-local`
   with the password in its `.env` file; this project reads the password from there and never stores it).
   Without the cloud file, every command uses that local engine; with it, `FTRT_ENGINE=local` in
   front of a command uses the local engine instead.
3. Install Python 3.11, then this project's pieces (this also installs the OpenTelemetry packages
   used for the optional Dash0 tracing):
   `python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt`
4. Load the data: `.venv/bin/python -m ftrt.load`. It takes 66 seconds to Elastic Cloud (measured 13:35; Elastic's ELSER and Jina's models
   read every passage as it loads), and 12 seconds on the laptop engine
   (`FTRT_ENGINE=local .venv/bin/python -m ftrt.load`); both were measured on 9 November. The first
   run downloads the small meaning model (about 90 MB) once; later runs work offline. It reads the
   four spreadsheets it needs (sessions, speakers, sponsors, outlets), cuts the text into 2,250
   passages (2,225 for the programme and 25 for the outlets: 501 talks, 100 events, 715 speakers,
   226 sponsors and 14 outlets), turns each into 384 numbers with the meaning model (in Elastic
   Cloud, Elastic's ELSER and Jina's models also read each one), and fills two new catalogues,
   `ftrt-programme` and `ftrt-outlets`. A search of the loaded text for email addresses finds none.
   Run it again any time: it rebuilds both from scratch.
5. Start the page: `.venv/bin/python -m ftrt.page`, and open http://127.0.0.1:8765 (on this laptop
   only; Ctrl-C stops it).

The same commands, from Terminal, as they were run on 9 November (Elastic Cloud by default; put
`FTRT_ENGINE=local` in front of any of them for the laptop engine, or `FTRT_CLOUD_ENV=/path/to/.env`
to read another Elastic Cloud settings file):

- **Search:** `.venv/bin/python -m ftrt.search --mode compare --kind sponsor -n 5 "SLSA Level 3"`.
  The ways are `words`, `meaning`, `elser`, `jina`, `reranked`, the default blended, and `compare`, which
  shows one search all ways with the passage that made each result match: four in Elastic Cloud
  (words, meaning, Elastic's ELSER, blended), three on the laptop engine, which skips ELSER and says
  so. Add `--startups` to narrow it to the start-ups.
- **Match** (an outlet finds the talks, speakers and sponsors that fit it):
  `.venv/bin/python -m ftrt.match --mode compare --kind sponsor -n 10 "Hello World Gazette"`;
  `.venv/bin/python -m ftrt.match --list` shows the 14 outlets.
- **Flip** (a sponsor finds the outlets that fit it, then the nearest talks):
  `.venv/bin/python -m ftrt.flip "Kedify"`; `.venv/bin/python -m ftrt.flip --list` shows the 226
  sponsors. On the page this is the "I'm a vendor" door.
- **Warm up before a demo:** `.venv/bin/python -m ftrt.warm`.
- **The Agent Builder agent:** `.venv/bin/python -m ftrt.agent setup` creates the 3 tools and the agent in
  Elastic Cloud; `.venv/bin/python -m ftrt.agent ask "Which sponsors and talks at KubeCon fit the Hello
  World Gazette?"` asks it; `.venv/bin/python -m ftrt.agent remove` deletes them.

Elastic's ELSER sleeps when idle and can take about 80 seconds to wake. Starting the page wakes it
in the background, and the warm-up command wakes it on demand and says how long it took ("awake
(0 s)" means it was already awake). A search waits at most 4 seconds for it; if it is still waking,
the results come without it and the page says so.

On Elastic Cloud it needs the internet and your project's own key; the local alternative needs no
internet once set up. No other key.

## Tools and data

- Elasticsearch and Kibana (Elastic), Elastic Cloud serverless (or the same engine locally in
  Docker), Elastic's ELSER model and hosted re-ranker (in the cloud), Python, Flask,
  sentence-transformers, all-MiniLM-L6-v2.
- **Data:** KubeCon + CloudNativeCon North America 2026 programme, The Linux Foundation,
  CC BY 3.0, as of 4 November 2026. See `data/CREDITS.md`. Logos and photos are not included.

## Licence

MIT, for the code. The programme data remains under its own licence, CC BY 3.0.
