# Find the Right Talk

> **Built for the press. When a conference plan falls apart, Find the Right Talk shows a media
> outlet its next story in seconds: the talks, speakers and companies that fit what it covers.**

It is a tool for media outlets covering a conference. An outlet's profile is matched against the
whole programme, and the same engine turned round lets a company on the show floor find the
outlets that would want its story. This build uses KubeCon + CloudNativeCon North America 2026 as
its example; any conference with a programme and a sponsor list would work the same way.

**Try it:** https://caiv.cnh.radarhq.io (hosted on Radar's cluster until 13 November).

## What it does

I'm a video producer, and I have covered a lot of conferences as press. You arrive with a plan, and
on the first day it usually falls through. An interview cancels, and now you have a free hour, a
crew standing around, and hundreds of talks and booths to choose from. The best story in the
building could be two aisles over and you would never know.

- **I'm press.** Pick an outlet and type what it came to the conference to find. You get the talks,
  speakers and sponsors that fit, each with the exact passage that made it match.
- **The fit check.** For the top three sponsors, an AI model writes one sentence on why each may
  suit the outlet, with the passage it read behind a click. The search decides the order, not the AI.
- **I'm a vendor.** The same engine turned round: pick a sponsor, or describe your company, and get
  the outlets whose beat fits your story.
- **Start-ups only.** One switch narrows any sponsor list to the start-ups, so a small company with
  the right story shows up beside the big names.
- **How these were found.** One link shows the same search six ways, side by side: words, meaning,
  Elastic's ELSER, Jina's embeddings, blended and re-ranked.

It is loaded with the KubeCon programme: 501 talks, 715 speakers, 226 sponsors and 14 outlet
profiles (8 real media partners and 6 labelled samples). Another conference means another four
spreadsheets in the same layout.

## Where Elastic is used

- **Elastic Cloud serverless** holds the programme and the outlets as short passages, in two
  catalogues.
- **Elasticsearch** runs the keyword search, the vector search and the filters in one place. This
  project's own code blends the ranked lists (reciprocal rank fusion).
- **Elastic's ELSER model and Jina's embedding model**, both through Elastic, read every passage
  and each get a vote in the blend.
- **Elastic's hosted re-ranker** re-orders the blended top 20 in the "Re-ranked" view.
- **An Elastic inference connector** reaches OpenAI's gpt-4.1 for the fit check.
- **An Elastic Agent Builder agent** with three custom read-only tools answers questions over the
  same two catalogues.

Of the five things Elastic asked entrants to use, four are done: serverless, ingesting data, Jina
embeddings, and an Agent Builder agent with custom tools. Workflows is not used.

## The other sponsor tools

- **Radar** hosts the live page above, deployed by Argo CD.
- **Dash0** traces each search on the laptop page with OpenTelemetry: step names and timings only,
  never the text anyone typed.
- **Gitar**, an AI code reviewer, reviewed the code. Its one finding was fixed; nothing it wrote
  was merged.

## Set it up

You do not need to run it to judge it. To run it yourself:

1. Create your own Elastic Cloud serverless Elasticsearch project. Put its endpoint and an API key
   in a file `~/elastic-cloud/.env`, as two lines: `ES_CLOUD_URL=` and `ES_CLOUD_API_KEY=`. The
   file stays outside this repository.
2. Install: `python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt`
3. Load the data: `.venv/bin/python -m ftrt.load`
4. Start the page: `.venv/bin/python -m ftrt.page` and open http://127.0.0.1:8765

The fit check needs a chat-completion inference endpoint in your Elastic project, with the name set
in `ftrt/config.py`. Without one the page works as before and the fit check box stays hidden.

## AI disclosure

- **Aaron Allsop:** the idea, the two test outlets, every product decision, and the checks.
- **Claude Code (Anthropic)** wrote all of the code, under Aaron's direction, on 9 November 2026,
  after the hackathon's 11:00 start. Every commit says so, and the commit history starts with no
  code in it. Before the day there were only data and notes: the public programme, and the sponsor
  and outlet profiles in `data/`, which Claude drafted from public pages (each labelled; six of
  the outlets are invented samples).
- **In the product,** the search models (all-MiniLM-L6-v2, Elastic's ELSER, Jina) rank text and
  write none. The only AI-written words are the fit check and the Agent Builder agent's answers,
  both from OpenAI's gpt-4.1 through Elastic, and both labelled as AI-written. The fit check is sent
  the outlet's two texts and the three sponsors' own text, nothing else.

What was measured on the day, including the misses, is in `notes/evidence.md`.

## Data and licence

KubeCon + CloudNativeCon North America 2026 programme, The Linux Foundation, CC BY 3.0, as of
4 November 2026. See `data/CREDITS.md`. Logos and photos are not included. The code's licence is in
`LICENSE`.
