# find-the-right-talk

**Which talks and sponsors at KubeCon should a given media outlet cover?** Pick an outlet and this
ranks the programme (talks, speakers and sponsors) by how well each fits what that outlet covers,
and shows the passage that made each one match. Turn the same engine round and a sponsor finds the
outlets and talks that fit it. Start-ups can be shown on their own, so a small company with the
right story surfaces beside the big names.

It runs on Elastic Cloud serverless, searches the programme by words and by meaning, and in the
cloud adds Elastic's own ELSER model and Elastic's hosted re-ranker as further voices. All the code
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
- **Words, meaning, and Elastic's voice.** On the page, "Compare all" shows five
  columns side by side (words, meaning, Elastic's ELSER, blended, re-ranked), and a switch picks
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
- **Elastic's hosted re-ranker** (Jina, through Elastic's inference service) re-orders the blended
  top 20 in the "Re-ranked" view (cloud only). For that view only, the search text (or the outlet's
  or sponsor's profile) and those 20 passages are sent to Elastic's hosted inference service, which
  is outside your own Elastic Cloud project and is billed per use. Every other view stays inside
  your own Elastic Cloud project, and the re-ranker is not used on the laptop engine. About half a
  second is added to a search and 1 to 1.5 seconds to a page "Go" (measured 9 November).
- **Elastic Agent Builder** runs an AI agent, "Find the Right Talk" (in Kibana: Agents), with three
  read-only tools over today's two catalogues only. It is a second, AI-written way in, not the
  engine: it does not run the project's own blend. Its answers are written by a language model on
  Elastic's hosted inference service (Anthropic's Claude Sonnet 4.5, the project's default), so the
  questions and the passages it reads go there, billed per use. Every answer ends "AI-written by the
  Find the Right Talk agent (Elastic Agent Builder). Check each quoted passage before you rely on it."
  On Elastic's trial it answers about one long question every 7 minutes. Titan measured one
  Gazette answer in 41 seconds on 9 November and checked all 14 of its quotations word for word
  against the programme; Cassini's check of it is still to come.
- **The blend is this project's own code:** each ranked list votes (reciprocal rank fusion), so it
  takes any number of voices.
- **Geo queries are not used:** the data has no coordinates (rooms in one building and a region
  word per outlet), so a map would be decoration.

## What Elastic asked entrants to use

Status at 13:30 on 9 November, one line each:

1. **Elastic Cloud serverless:** done. Everything runs on a serverless Elasticsearch project.
2. **Ingesting data:** done. The programme, speakers, sponsors and outlets are loaded as 2,250
   passages into two catalogues.
3. **Jina models for embeddings:** half done. Elastic's hosted Jina re-ranker is used to re-order the
   blended top 20 (the "Re-ranked" view). Jina embeddings as a further voice are being tried and are
   not in yet.
4. **An Agent Builder agent with custom tools:** done. "Find the Right Talk" has three tools of our
   own over the two catalogues.
5. **Elastic Workflows:** not used.

**The five main code files, so you can see Elasticsearch is the core** (each is in `ftrt/`):

- `engine.py`: the one way the code reaches Elasticsearch, in Elastic Cloud or on a laptop.
- `load.py`: loads the spreadsheets into two new catalogues, one document per passage, each holding
  the words, 384 numbers for its meaning, and (in the cloud) Elastic's ELSER reading of it.
- `search.py`: the searches: words, meaning, Elastic's ELSER, the blend (reciprocal rank fusion, in
  this project's own code) and the re-ranked view.
- `match.py`: an outlet's own profile searches the programme (the press door); `flip.py` does the
  same the other way round (the vendor door).
- `agent.py`: sets up the Agent Builder agent and its three tools in Elastic Cloud from a script.

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
- **Meaning finds the topic, not the stance:** re-ranked, the GPU search puts vCluster (which
  shares GPUs) above Edera (which isolates them); the re-ranker cannot tell the stance either.
- **It never says "nothing fits":** meaning always returns the nearest thing.
- **The fit check, an AI judgement of the top results, was not built.** The Agent Builder agent is a
  different thing: it answers in words, and it is slow (41 seconds for one answer when measured).

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
  Elastic model never blanks the page, and the warm-up command; 12:32 Elastic's hosted re-ranker; 12:46 the Agent Builder agent; 13:22 a code review by Sonar's Gitar, and its one finding fixed.
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
  deployment, not on a separate service. The optional "Re-ranked" view is an exception: it sends
  the search text and the top 20 passages to Elastic's hosted re-ranking service (see above). The
  Agent Builder agent is the other: its answers are written by Anthropic's Claude Sonnet 4.5 on
  Elastic's hosted inference service, and are labelled as AI-written.
- **Sonar's Gitar** reviewed all of today's code on a review pull request that was never merged: it
  approved with suggestions. Its one finding was confirmed and fixed (the start-ups switch could
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
3. Install Python 3.11, then this project's pieces:
   `python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt`
4. Load the data: `.venv/bin/python -m ftrt.load`. It takes 470 seconds to Elastic Cloud, because
   Elastic's ELSER model reads every passage as it loads, and 12 seconds on the laptop engine
   (`FTRT_ENGINE=local .venv/bin/python -m ftrt.load`); both were measured on 9 November. The first
   run downloads the small meaning model (about 90 MB) once; later runs work offline. It reads the
   four spreadsheets it needs (sessions, speakers, sponsors, outlets), cuts the text into 2,250
   passages (2,225 for the programme and 25 for the outlets: 501 talks, 100 events, 715 speakers,
   226 sponsors and 14 outlets), turns each into 384 numbers with the meaning model (in Elastic
   Cloud, Elastic's ELSER model also reads each one), and fills two new catalogues,
   `ftrt-programme` and `ftrt-outlets`. A search of the loaded text for email addresses finds none.
   Run it again any time: it rebuilds both from scratch.
5. Start the page: `.venv/bin/python -m ftrt.page`, and open http://127.0.0.1:8765 (on this laptop
   only; Ctrl-C stops it).

The same commands, from Terminal, as they were run on 9 November (Elastic Cloud by default; put
`FTRT_ENGINE=local` in front of any of them for the laptop engine, or `FTRT_CLOUD_ENV=/path/to/.env`
to read another Elastic Cloud settings file):

- **Search:** `.venv/bin/python -m ftrt.search --mode compare --kind sponsor -n 5 "SLSA Level 3"`.
  The ways are `words`, `meaning`, `elser`, `reranked`, the default blended, and `compare`, which
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
