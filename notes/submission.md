# Submission paragraph, final draft for Aaron to read, Monday 9 November 2026

Written by Rhea from what was built and checked today. It claims only what Cassini, Titan or Saturn
confirmed. Aaron reads it by 16:05 on the laptop clock; Rhea redoes any number the final save changes.
The form is one shot (Aaron, 14:52): nothing is pasted until this is approved.

## The paragraph

**Find the Right Talk is built for the press.** When a conference plan falls apart, it shows a media
outlet its next story in seconds. An outlet's profile (what it covers, its audience, and what it came
to find) is matched against the whole program, and the talks, speakers and sponsors that fit come
back, each with the passage that made it match. Turned round, a company finds the outlets that would
want its story, and a "Start-ups only" switch surfaces small companies beside the big names. This
build uses the KubeCon + CloudNativeCon North America 2026 program as its example (601 sessions, 715
speakers, 226 sponsors and 14 outlet profiles), and the idea works for any conference.

It runs on Elastic Cloud serverless. Elasticsearch searches by words and by meaning, and in the cloud
adds Elastic's own ELSER model, Jina's embeddings and a Jina re-ranker, blended in code written for
this project. An Elastic Agent Builder agent answers in plain words and quotes the program's own
passage for every pick. A fit check, labeled as AI-written, gives one sentence on why each of the top
three results (talks, speakers or sponsors) may suit the outlet; the search, not the AI, decides the order. Gitar reviewed all the
code and approved it, Dash0 traces each search without the typed words, and a hosted copy runs live on
Radar's Kubernetes cluster at https://caiv.cnh.radarhq.io until 13 November. All of the code was
written on the day, from an empty folder, by Claude Code under my direction. It does not always get it
right, and `notes/evidence.md` says where.

## A shorter version, if the form has a small box

Find the Right Talk is built for the press: when a conference plan falls apart, it shows a media outlet
the talks, speakers and sponsors that fit what it covers, each with the passage that made it match, and
turns round to show a company the outlets that would want its story. Built on Elastic Cloud serverless
with keyword and semantic search, Elastic's ELSER and Jina models, an Agent Builder agent and an
AI-written, labeled fit check. KubeCon 2026 is the example. Live at https://caiv.cnh.radarhq.io.

## Facts, with who measured them today

- 601 sessions (501 talks and 100 events), 715 speakers, 226 sponsors, 14 outlets (6 with a KubeCon
  assignment; 8 real media partners and 6 labeled samples, recounted by Neptune at 15:02); 2,250
  passages in all, 2,225 for the program and 25 for the outlets; 0 email addresses in the loaded text
  (Titan, re-measured 11:38; Cassini's fresh copy, 11:52).
- 32 of the 226 sponsors are Start-ups; the switch takes the picker from 226 to 32 and back to 226
  (Titan, 12:24 to 12:25; Cassini, in a real browser, 12:31).
- Elastic Cloud load takes 66 seconds (ELSER and Jina read every passage); 12 seconds on the laptop
  engine (Titan, 13:35 and 12:01 to 12:09).
- The fit check: in three runs in a real browser (Cassini, 15:46) its three names were the list's top
  three every time (mirrord by MetalBear, JetBrains, Momentic); all 18 checkable claims were found in the
  passage the model read; it appeared 1.6 to 3.3 seconds after the results.
- Gitar: "Approved", its one finding closed (seen by Saturn on GitHub, 15:13).
- Dash0: the dashboard shows one service, three operations, no errors (Aaron's dashboard, about 14:20).
- Radar: live and checked from the public address by Dione and in a browser by Saturn.

## What the repository holds, in two sentences (for the form)

Before 11:00 on 9 November: the idea, the notes, the public KubeCon program copied with credit, and
the sponsor and outlet profiles in `data/`, including six labeled sample outlets. After 11:00: every
line of code, written by Claude Code under Aaron's direction, and the commit history that starts at
11:00.

## Not claimed

- Elastic Workflows is not used (final).
- Geo queries: not used. The data has no coordinates.
- Creating your own outlet profile and saving a plan are not built: you pick a loaded profile or type
  what an outlet came to find, and nothing typed is saved.
- "Nothing is sent anywhere" is not said. Words, meaning and ELSER stay inside Aaron's own Elastic
  project; Jina's embeddings, the re-ranker, the agent and the fit check use Elastic's hosted service,
  and the agent and fit check send text to OpenAI's gpt-4.1 through Elastic, billed to Aaron.
- Speed is claimed only where measured: a Gazette Go about 2 to 2.5 seconds; the agent is shown as a
  recording.

## Where it falls short (in `notes/evidence.md`; the README points to it)

- The Hello World Gazette finds its hidden gem (mirrord) and two of its three must-finds in the top
  ten; Faros, a tool a manager uses to see what coding agents cost, is 13th.
- The Breach Chronicle misses: its wording is about attacks while its companies talk about
  vulnerabilities and sandboxes. It stays in the data as a reported miss.
- Places 9 and 10 of the Gazette's list can swap between runs; the top eight never changed in 13 runs.
- The flip's outlet order is a weak signal and moves between versions; its talks are strong.
- The fit check and the agent are AI-written and can be wrong; each has the passage it read, to check.

## The checklist

- [ ] Public repository link: https://github.com/aaronallsop/find-the-right-talk
- [ ] README setup: the fresh-copy test of 11:53 stands (Aaron, 12:40); the README was shortened after.
- [ ] AI use disclosed in the README's "AI disclosure" section (done; Gemini and Jules are not used)
- [ ] What existed before 11:00 and what was built after, in two sentences (above)
- [ ] Data credit: KubeCon + CloudNativeCon North America 2026 program as of 4 November 2026, The
      Linux Foundation, CC BY 3.0
- [ ] The paragraph above, and the screen recording (Aaron's)
- [ ] Screenshot of the confirmation (Aaron's)
