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

## Now

- Neptune: finished at 11:25.
- Titan: adding Elastic's own meaning model and reloading the cloud, then M5 the flip.
- Rhea: the cloud wording in the README, cheat sheet and a first draft of the submission paragraph.
- Cassini: re-scores after Titan's reload. Checked the page through its own web requests at 11:57 (it could not open it in a browser pane).
- Aaron: looks at the page. M3, the two-door page, is saved and pushed (fba8720, 11:55) and runs on this laptop at http://127.0.0.1:5060; the press door works, the vendor door says "the flip comes next". Cassini's 11:57 check: all 14 outlets answer in under 1.5 seconds with ten sponsors, talks and speakers each (blended and meaning), and the typed boxes and plain search match the Terminal. Not yet seen rendered in a browser (Cassini's and Saturn's browser panes refused the address), so it stays here until Aaron has looked.
- Dione: standing by.

Watch for the demo: Elastic's in-project model sleeps when idle and took 81 seconds to wake. Run one search a minute or two before presenting; the same goes in the 17:15 screen check (the day plan, not Rhea's file, so Saturn to add it).

Watch: by words alone some outlets find little or nothing (TechRevolt News nothing at all).

Watch: both test outlets still FAIL their answer keys (re-scored 11:59, after the order fix). The
Hello World Gazette misses by one place. The Breach Chronicle, the demo outlet, has none of its
must-finds in the top ten. Aaron decides what to do about it.

## Next

Aaron's build order as of 11:55 (Elastic's meaning model moved forward, before the page). Cut from
the bottom if behind. The 15:45 freeze and the 16:30 submission do not move.

1. Titan fixes the match order.
2. Elastic's own meaning model as a fourth voice in the blend (cloud only).
3. Cassini re-scores the two test outlets.
4. The page (M3), the two-door demo.
5. The flip (M5), as the vendor door's engine.
6. Cloud wording in the README and the pitch.
7. Elastic's re-ranker (cloud only).
8. The start-ups toggle (M4).
9. The fit check (S1), only if ahead at 15:00.

## Done

- 11:00 B0 the public repository (a497b1d)
- 11:04 B1 the loader (6096f75)
- 11:07 B2 the three searches (50019ed)
- 11:09 passage-cutting fix (0560c9b)
- 11:20 search fixes from review (42c36e0)
- 11:21 Elastic Cloud connection (c346c70); 11:24 cloud catalogues loaded and demo searches proven there
- 11:57 Saved and pushed (321b069): the match's order no longer shifts with how many results are shown, and the first run on a new machine downloads the meaning model. Passage count explained: 2,225 programme passages plus 25 outlet passages is 2,250.
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

- Elastic's own meaning model is built and tested on the laptop. The cloud reload waits for Aaron's approval, which he gives himself in Titan's session (it rebuilds the cloud catalogues).
- The page could not open in any browser: port 5060 is on the browsers' blocked list (found by Dione). Titan is moving it to port 8765 and will send the README line. Until then the README's page address is wrong.
- The fresh-copy test waits on Aaron's second key for the same cloud project (Aaron to create it himself and keep it outside the folder).

## Decided today

The decisions up to 11:25 are listed in the handoff above. Added since, per Neptune's report:

- 11:12, Aaron: geo queries are out; the data has no coordinates, and we say so plainly.
- 11:12, Aaron: Elastic's own model or re-ranker only after M3, in M5's slot, if time.
- 11:17, Aaron: helpers sparingly until 13:20.
- About 11:30, Aaron: start the team early, before 12:00, now that Neptune has finished.
- Aaron (relayed by Neptune, 12:05 by Neptune's clock): approved a rewritten 90-second demo script and three new judge answers (why Elastic Cloud, why no geo, why Elastic's own models). Rhea put them in the cheat sheet; the day plan's demo is superseded.
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
