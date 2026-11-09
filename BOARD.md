# Today's board — Monday 9 November 2026

Plain words, kept by Neptune until 12:00 and by Rhea after. The record of the day is the commit
history; this is the to-do list.

## Handoff from Neptune (written 11:25; Neptune finished early to save usage)

**Done, all saved and pushed to https://github.com/aaronallsop/find-the-right-talk**

| Piece | Commit | What it does |
|---|---|---|
| B0 the repository | a497b1d, 11:00 | Public from 11:00. Data, notes, rulebook, MIT licence, README. No code. |
| B1 the loader | 6096f75, 11:04 | One command rebuilds the two catalogues `ftrt-programme` and `ftrt-outlets` from the spreadsheets in about 12 seconds. |
| B2 the three searches | 50019ed, 11:07 | Words, meaning, blended, and a compare mode, from Terminal. |
| Fix to passage cutting | 0560c9b, 11:09 | List cells cut at their items; no passage starts mid-sentence. |
| Search fixes from review | 42c36e0, 11:20 | Results no longer shift with how many are shown; honest empty messages; README setup wording. |
| Elastic Cloud connection | c346c70, 11:21 | Uses the serverless project when `~/elastic-cloud/.env` is filled in, the laptop engine otherwise. Proven against the cloud at 11:24. |

**Measured today** (re-measure before quoting): 501 talks, 100 events, 715 speakers, 226 sponsors
in 2,184 passages; 14 outlets (6 with a KubeCon assignment) in 25 passages. No passage over 180
words. 0 email addresses in the loaded text (33 passages hold speakers' social handles).
Meaning depth check: same top answer at 1 and at 48 results, on five searches.

**The move to Elastic Cloud is done (11:24).** Aaron put the endpoint and key of his serverless
project in `~/elastic-cloud/.env` himself; the loader filled the cloud catalogues first time, in
25 seconds, with the same counts; the three demo searches give the same top results in the cloud
as on the laptop; `FTRT_ENGINE=local` in front of a command still uses the laptop engine, which
stays loaded as the demo's fallback. Every command now uses the cloud by default.

**Half done:** nothing. No uncommitted work in the folder.

**Next step: B3**, Cassini re-proves the demo searches three times each (recipe, last section),
sponsors only, with the command in the README (`--mode compare --kind sponsor`). What they gave
at 11:08, once each:
- "SLSA Level 3": words finds Docker then ActiveState, the two sponsors whose own text says it;
  meaning puts OpenSSF first. Words win. Holds.
- The Black Friday sentence ("How do you survive a Black Friday traffic spike without paying for
  idle servers the rest of the year?"): words finds nothing; meaning gives North, Pump, Fastly,
  pgEdge, Kedify (Start-Up, autoscaling), Northflank. The recipe warned this one leaned on
  website text last week. It still shows words failing and meaning answering, but the top result
  is a cloud-cost company, not the autoscaling start-up. Cassini should try two or three
  rewordings that lean on scaling rather than cost (for example "scale up for a traffic spike
  and back down afterwards") and keep the one where a Start-Up lands in the top three.
- The GPU sentence ("keeping different tenants' GPU workloads isolated from each other on shared
  hardware"): words gives Edera alone; meaning gives vCluster, Edera, Cast AI, Runpod, Aranya,
  Rafay; blended puts Edera first because both lists voted for it. Holds.

**Then M2, the match.** The pieces it needs are in place: each outlet is stored as a "beat" part
and, for the six sample outlets, an "assignment" part, each with its 384 numbers; the search
code has a function that searches by numbers already in hand, and the blending function takes a
weight per list (the assignment's vote counts double, per Aaron's 8 November decision). An
outlet with no assignment is matched on its beat alone.

**Judges' criteria, from the Elastic team's talk (Aaron, 11:12):** depth and creativity; use of
Elastic's own generative models; use of Elastic Cloud; geo queries. Aaron's decisions: move to
Elastic Cloud serverless (first); Elastic's own meaning model or re-ranker as a fourth voice in
the blend or a re-rank of the top results, after M3, in M5's slot, if time; geo: no, the data has
no coordinates, and say so plainly to the judges.

**Left for Titan from the adversarial review (confirmed, not fixed; do them in one reload, running
the demo searches before and after):**
- 32 passages are longer than the meaning model actually reads (256 word-pieces, not 180 words;
  technical text runs about 1.5 pieces per word), so their tails are never seen. Lower the
  passage size to about 100 words, or cut by the model's own tokeniser.
- Doubled punctuation where a title ends in "?" or "!" ("Now What?. Track:") and ":." after labels;
  cosmetic, harmless to search.
- Placeholder bios ("TODO", "none", ".") and two speakers whose job cell holds their own name are
  loaded as text. A data fix in speakers.csv, or drop values under three characters.
- Recurring events (seven "Coffee Break", six "CNCF Project Demos") have identical text and no
  date in it; fold the day into the passage or hide events from the match.
- Each search prints two or three lines of library noise first (a torch note, "Could not reach
  the Hub"); silence them before the demo.

**Decided today**
- 10:52, Aaron: the usage window resets at 13:20, not 12:00 (he started it at 08:30 on purpose
  so the credits are not front-loaded). The 12:00 hand-over stays; usage checks move to 13:20.
- 10:58, Aaron: the repository is named find-the-right-talk, as the README says; the local
  folder has a different name, which appears in no public file.
- 10:59, Aaron: Rhea keeps a live status page for Aaron as an Artifact (time, where we are
  against the schedule, now, next, blocked, decisions waiting), besides BOARD.md.
- 11:12, Aaron: pivot from "runs on this laptop" to Elastic Cloud serverless, laptop as fallback
  (see the judges' criteria above). Not geo.
- 11:17, Aaron: stop the adversarial-review helpers to save usage (56% of the window at 11:17,
  resets 13:20); no more helpers before 12:00.
- 11:04, Neptune: one document per passage carrying the record's details; every passage begins
  with the record's name; words and meaning read the same text; blending is our own code.

**Watch out for**
- Serverless accepted everything the laptop engine did, apart from the shard settings the
  loader already skips. The engine in use is named on screen at the start of every command.
- The engine's trial licence runs to 3 December; nothing here depends on it (blending is ours).
- Port 5000 is macOS's; the page (M3) should use another port and say so in the README.
- Only Titan commits from 12:00. Save by naming files; never `git add -A`.

## For Saturn

(messages Aaron left with Rhea, each with the time, until Saturn has them)

(none)

## For Aaron

(what Saturn or Rhea needs from you, each with the time; taken off when you have answered)

- 12:45 Still open: does "run on the cloud" mean the searches (already so) or hosting the page itself online?
- 12:23 At 13:20 read the usage page (Claude app, Settings, Usage) and tell Saturn the five-hour and weekly figures.
- 15:30 Read the submission paragraph (Rhea's draft is in the notes) and say what to change.
- 12:22 Demo beat 2: you wrote the opening words (12:45, in the cheat sheet). Still to decide: words for the passage and the start-up flag, or leave those silent.
- 16:10 Warm the Elastic models before recording: run `.venv/bin/python -m ftrt.warm` ("awake (0 s)" means already awake). Again at 16:25, before submitting. Also goes in the 17:15 screen check.

## Now

- Neptune: finished at 11:25.
- Titan: working on Agent Builder (Saturn is confirming with Titan what Aaron said).
- Rhea: README rewritten at 12:36 as the product's face, for a judge who reads and watches (setup moved lower); the words are drafted; waiting for the page-speed and Talks-tab fixes, then redoes the numbers after the freeze.
- Cassini: checking the start-ups toggle. Checked the page through its own web requests at 11:57 (it could not open it in a browser pane).
- Dione: standing by.

Watch for the demo: Elastic's in-project model sleeps when idle and took 81 seconds to wake. Run one search a minute or two before presenting; the same goes in the 17:15 screen check (the day plan, not Rhea's file, so Saturn adds it there) and before the 16:15 recording and 16:30 submission.

Watch (demo note): with start-ups only, the Breach Chronicle shows Maze and Archestra AI, two of its must-finds.

Watch: by words alone some outlets find little or nothing (TechRevolt News nothing at all).

Watch: both test outlets still FAIL their answer keys (re-scored 12:15, with Elastic's model). The
Hello World Gazette, the demo outlet since 12:16, is one short (Faros 13th). The Breach Chronicle is
set aside: it has none of its must-finds in the top ten, stays in the data, and is reported honestly
as a miss.

## Next

Aaron's plan as of 12:40 (after the organiser and the info message): no live presentation. Judging is
the GitHub repository plus a 3-minute video on the WeMakeDevs platform by 17:30, and judges are
unlikely to run it. The freeze at 15:45 holds.

1. Titan's page-speed and Talks-tab fixes.
2. A side-by-side compare view on the page.
3. An Agent Builder agent, scoped first, only if we get there.
4. From 15:45: the README as the product's face (Rhea), the evidence page of measured results
   (Cassini), screenshots, Aaron's recording.
5. Aaron submits at 16:30 with take one; 16:30 to 17:30 a better take, if the platform allows edits.
   Warming the Elastic models before recording is Aaron's job.

## Done

- 11:00 B0 the public repository (a497b1d)
- 11:04 B1 the loader (6096f75)
- 11:07 B2 the three searches (50019ed)
- 11:09 passage-cutting fix (0560c9b)
- 11:20 search fixes from review (42c36e0)
- 11:21 Elastic Cloud connection (c346c70); 11:24 cloud catalogues loaded and demo searches proven there
- 11:57 Saved and pushed (321b069): the match's order no longer shifts with how many results are shown, and the first run on a new machine downloads the meaning model. Passage count explained: 2,225 programme passages plus 25 outlet passages is 2,250.
- 12:12 Elastic's own meaning model, ELSER, saved and pushed (2e26f1b): in the cloud it reads every passage and gets one vote in the blend; the laptop leaves it out. Cloud load now takes 470 seconds (Titan, measured 12:01 to 12:09). The cloud was reloaded on Aaron's go-ahead. Demo searches unchanged at the top; Elastic's model alone also gets all three right. A four-helper review found and fixed 7 faults before saving. Not yet re-scored.
- 12:33 Rhea finished the submission draft, added "Where it falls short" to the README and "Honest limits" to the cheat sheet, and wrote the fit check as not built. Aaron reads the paragraph by 15:30.
- 12:43 Aaron tried the flip at the vendor door and it works; Cassini checked three sponsors. M5 is done.
- 12:37 "Compare all" on the page (acdd654): five columns side by side (words, meaning, Elastic's ELSER, blended, re-ranked), so the video can show Elastic's voice. Checked by Cassini in a real browser (12:42), three runs each, identical: the GPU sentence takes 1.2 to 1.7 seconds, every column matches its own view, and the Start-Up tags are all correct. The page shows "Elastic Cloud serverless, with Elastic's ELSER" on screen, for the video.
- 12:35 Page fixes (c4a8ae8): checked by Cassini in a real browser (12:42), three runs each, identical: a Gazette Go takes about 2.5 seconds and a re-ranked search about 1.2 seconds; Talks cannot be chosen with start-ups on.
- 12:32 Elastic's hosted re-ranker (Jina) added as its own "Re-ranked" view (0c57178), on Aaron's yes in Titan's session. It adds about half a second to a search. For that view only, the search text and the top results' passages go to Elastic's hosted inference service, billed per use; every other view stays inside the project. Kept (Saturn, 12:37).
- 12:31 Cassini checked the start-ups toggle in a real browser: counts drop from 226 to 32 and come back exactly; every sponsor shown is a start-up.
- 12:30 The README's setup commands, as Titan ran them, are in, with the list of what was built and when.
- 12:29 Warm-up command and the fallback saved and pushed (6ff0e6b): `.venv/bin/python -m ftrt.warm` wakes Elastic's models. A search waits at most 4 seconds for ELSER; if it is still waking, results come without it and the page says so.
- 12:27 M4, the start-ups toggle, saved and pushed (9ab6782): one switch narrows every sponsor list on the page to the 32 start-ups among the 226 sponsors, and back. Measured by Titan, 12:24 to 12:25: the picker went 226, 32, 226. Cassini is checking it. Also: a sleeping Elastic model is now left out of a search instead of making it fail.
- 12:20 The flip checked by Cassini on three sponsors, identical in three runs: the talks it finds are on target; the outlet scores bunch close together.
- 12:20 M3, the two-door page, done: Aaron opened http://127.0.0.1:8765 in his own browser and it works. Cassini checked all 14 outlets at 11:57; Titan and Aaron saw it on screen. (Saved in fba8720; moved to port 8765 in d5e84b1.)
- 12:17 M5, the flip, saved and pushed (68c98c7): a sponsor, picked or typed in, finds the outlets that fit it, and the talks nearest to what it does. It is the vendor door on the page. Not yet checked that its outlet list matches common sense.
- 12:15 Cassini re-scored with Elastic's model: the Hello World Gazette is still one short (Faros 13th); the Breach Chronicle still has none of its must-finds.
- 11:59 Cassini re-scored the match after the fix: the Hello World Gazette fails its key by one place (Faros 11th; Coder, Momentic and the gem mirrord in the top ten); the Breach Chronicle still has none of its must-finds in the top ten.
- 11:53 Fresh-copy test (Cassini): a clean clone, set up from the README's own steps with a second key, loads and searches the cloud. PASS, with fixes needed (details in the checks file, "fresh-copy"). Rhea fixed the passage count and the load time in the README; the page step, the model download step and the match command wait for Titan.
- 11:49 Cassini's "after" check: all three demo searches hold after the reload, three runs each, identical.
- 11:48 The match (M2) built, saved and pushed (552c262). Not yet scored against the answer keys; the Breach Chronicle's first look is below.
- 11:47 Review fixes saved and pushed (174effd): passages fit what the meaning model reads, placeholder text dropped, quieter searches, and a switch to point at a second cloud settings file. Re-measured by Titan: 501 talks, 100 events, 715 speakers, 226 sponsors, 14 outlets, 2,250 passages, 0 email addresses. The README, board, cheat sheet, submission draft and Cassini's checks went in the same save.
- 11:42 Cassini laid out the scoring sheet for the match (Gazette 8 items, Chronicle 12); nothing scored yet.
- 11:41 Dione confirmed, read-only, that the cloud project offers Elastic's own meaning model (ELSER) and Elastic's re-ranker as ready-made services; nothing was called or changed.
- 11:36 Relay test passed (Aaron to Rhea to Saturn): Saturn confirmed it had the message.
- 11:33 B3, the three demo searches re-proved in the cloud by Cassini: three runs each, all
  identical, and the laptop agrees. Not yet saved to the repository; Titan saves it next.

## Blocked

Nothing.

## Decided today

The decisions up to 11:25 are listed in the handoff above. Added since, per Neptune's report:

- 11:12, Aaron: geo queries are out; the data has no coordinates, and we say so plainly.
- 11:12, Aaron: Elastic's own model or re-ranker only after M3, in M5's slot, if time.
- 11:17, Aaron: helpers sparingly until 13:20.
- About 11:30, Aaron: start the team early, before 12:00, now that Neptune has finished.
- Aaron (relayed by Neptune, 12:05 by Neptune's clock): approved a rewritten 90-second demo script and three new judge answers (why Elastic Cloud, why no geo, why Elastic's own models). Rhea put them in the cheat sheet; the day plan's demo is superseded.
- 12:32, Aaron (said in Titan's session): yes to the hosted Jina re-ranker; it is kept.
- 12:43, Aaron: Cassini's evidence goes in notes/evidence.md, a clean file for judges. He also says the Agent Builder question is "already answered" (typed in Titan's session); Saturn and Titan to confirm what the answer was.
- 12:40, Aaron (after the organiser and the info message): no live presentation. Judging is the GitHub repository plus a 3-minute video on the WeMakeDevs platform by 17:30; judges are unlikely to run it. Build to work and be shown; no more effort on hosting, packaging, cold starts or edge cases; the own-project setup stays in the README with the one fresh-copy test already done (11:53). What is on screen is real and measured by Cassini; nothing staged. Aaron submits at 16:30 with take one; a better take 16:30 to 17:30 if the platform allows edits.
- 12:35, Aaron: the submission form is one shot, so no early submission. Submit once, after the freeze, the fresh-copy test and a rehearsal, by 16:30 at the latest. Rhea has the submission paragraph ready for Aaron to read by 15:30.
- 12:31, Titan and Saturn: the Hello World Gazette's wording stays as it was. No true short phrase would lift Faros; it would mean adding an idea the outlet never had.
- 12:27, Aaron: try Elastic's hosted Jina re-ranker once, ten minutes; keep it if it answers fast, else skip; no raising capacity. A slow Elastic model must never blank the page (fallback). Warm the Elastic models before the 16:15 recording and the 16:30 submission. Fix the Gazette's wording (Faros 13th) only if cheap, otherwise leave it.
- 12:20, Aaron: in the flip, what a sponsor is showing at KubeCon counts double, like an outlet's assignment.
- 12:16, Aaron: the Hello World Gazette is the demo outlet; the Breach Chronicle is set aside (it stays in the data and is reported honestly as a miss).
- 11:55, Aaron: Elastic's own meaning model moves forward, before the page.
- 11:47, Aaron: the 12:00 hand-over rule is phased out; Titan is the only builder and the only one
  who saves, from now.
- 11:45, Aaron: the fresh-copy test uses a second key on the same cloud project, kept outside the
  folder.
- About 11:41, Aaron (confirmed to Saturn; Neptune stays on as architect, plan advice comes through
  Aaron): the page is the two-door demo, the flip moves up to right after the page, Elastic's
  meaning model and re-ranker come after both and are cloud only.
- 11:30 to 11:42, Aaron (confirmed to Saturn): cloud by default, laptop as demo fallback only;
  geo no, the data has no locations; the build order above; the page is a two-door demo ("I'm
  press" / "I'm a vendor"); text typed into it is used once and never stored.
- 11:33, Cassini and Saturn: the Black Friday demo search is now "scale up for a traffic spike and
  back down afterwards". Words find nothing; meaning puts Kedify, a Start-Up, first.
- 11:30, Aaron (relayed by Neptune at 11:36): the product runs on Elastic Cloud by default; the
  laptop engine is the demo fallback only. Judges will run it from the public repository with
  their own Elastic Cloud project, so the README setup is written that way (Rhea, 11:40).
- 11:36, Aaron: approved the new wording for the "nothing is sent anywhere" line: "Your programme
  data and searches live in your own Elastic Cloud project and nowhere else, every AI-written line
  is labelled, and a copy on this laptop runs offline as the fallback." Rhea has changed the cheat
  sheet and will use it in the submission paragraph. The same line in the day plan, the Jules
  task and Neptune's prompt is not Rhea's to change; Saturn to decide. Still to confirm by Titan
  or Cassini: that nothing but Elastic Cloud is contacted.

Rhea adds new ones from 12:00.
