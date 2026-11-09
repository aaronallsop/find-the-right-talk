# find-the-right-talk

**Which talks and sponsors at KubeCon should a given media outlet cover?** Pick an outlet and
this ranks the programme — talks, speakers and sponsors — by how well each fits what that outlet
covers, and says why each one matched. Search the programme by words, by meaning,
or both (in Elastic Cloud, with Elastic's own ELSER model as one more voice). It runs on Elastic Cloud serverless; a local Elasticsearch in Docker is the alternative.

Built at the WeMakeDevs Cloud Native Hackathon, Elasticsearch track, Salt Lake City,
9 November 2026, by Aaron Allsop.

## Set it up

[Exact steps, tested on the day from a fresh copy of this repository into an empty folder:]
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
4. Load the data: `.venv/bin/python -m ftrt.load`. Takes about 12 seconds on the laptop engine
   and 470 seconds to Elastic Cloud, because Elastic's ELSER model reads every passage as it loads
   (both measured 9 November). The first run downloads the small meaning model (about 90 MB) once; later runs work offline. It reads the four spreadsheets it needs (sessions, speakers, sponsors, outlets), cuts the text into passages (2,225 for the programme and 25 for the outlets), turns each into
   384 numbers with the meaning model (in Elastic Cloud, Elastic's ELSER model also reads each one), and fills two new catalogues, `ftrt-programme` and
   `ftrt-outlets`. Run it again any time: it rebuilds both from scratch.
5. Start the page: `.venv/bin/python -m ftrt.page`, and open http://127.0.0.1:8765 (on this laptop
   only; Ctrl-C stops it).

You can also search from Terminal: `.venv/bin/python -m ftrt.search --mode compare "SLSA Level 3"`
shows one search all ways with the passage that made each result match: four in Elastic Cloud
(words, meaning, Elastic's ELSER, blended), three on the laptop engine, which skips ELSER and says
so. `--mode words`, `--mode meaning`, `--mode elser` or the default blended show one way; add
`--kind sponsor` or `--startups` to narrow it.

To see the match for an outlet from Terminal:
`.venv/bin/python -m ftrt.match --mode compare --kind sponsor -n 10 "Breach Chronicle"`;
`--list` lists the 14 outlets.

To flip it round, so a sponsor finds the outlets that fit it:
`.venv/bin/python -m ftrt.flip "Kedify"` ranks every outlet and then the nearest talks;
`.venv/bin/python -m ftrt.flip --mode compare "Edera"` shows it all ways; `--list` lists the 226
sponsors. On the page this is the "I'm a vendor" door.

Elastic's ELSER sleeps when idle and can take about 80 seconds to wake. The page wakes it when it
starts; if it does not answer, searches go ahead without it.

On Elastic Cloud it needs the internet and your project's own key; the local alternative needs no
internet once set up. No other key [unless the fit check is built].

## How it works

[Five boxes, from the cheat sheet: data → catalogue → three searches → the match → the page.]

## What existed before the day, and what was built on it

- **Before 9 November (allowed under rules 1 and 2):** the idea; notes and research (`notes/`);
  the public programme, copied once with credit; the sponsor and outlet profiles in `data/`,
  including six invented sample outlets, labelled, two of them test cases whose answer keys were
  written in advance (`notes/answer-keys.md`). Aaron built the same search pattern for his own
  video library the week before, as a separate private project; none of its code is in this
  repository. This project was rebuilt from scratch on the day.
- **On 9 November, after 11:00:** all of the code — loading, the three searches, the match,
  the page. The commit history starts at the beginning of the hackathon. This first commit holds
  no code: only the data, the notes, the rulebook (`CLAUDE.md`), the licence, the ignore list and
  this README.

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
  deployment, not on a separate service.
- [If built: the fit check sends the top results to Claude through Anthropic's API.]
- [If used: Gemini (Google) read the README as a newcomer would and answered questions; it
  wrote none of the code.]
- [If used: Jules (Google) checked the README's claims against the code at the feature freeze;
  it changed nothing.]

## Checked by Aaron

[One line per check Aaron did himself on the day, and what he saw.]

## Tools and data

- Elasticsearch and Kibana (Elastic), Elastic Cloud serverless (or the same engine locally in
  Docker), Elastic's ELSER model (in the cloud), Python, Flask, sentence-transformers, all-MiniLM-L6-v2.
- **Data:** KubeCon + CloudNativeCon North America 2026 programme, The Linux Foundation,
  CC BY 3.0, as of 4 November 2026. See `data/CREDITS.md`. Logos and photos are not included.

## Licence

MIT, for the code. The programme data remains under its own licence, CC BY 3.0.
