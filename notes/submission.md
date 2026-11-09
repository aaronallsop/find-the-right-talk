# Submission paragraph — draft for Aaron to read, Monday 9 November 2026

Written by Rhea from "The product, in one paragraph" in `notes/day-plan.md`, and from what was
built and checked today. It claims only what is built. Aaron reads it by 15:30; Rhea redoes the
numbers after the freeze. The submission form is one shot (Aaron, 12:35): nothing is pasted until
the freeze, the fresh-copy test and the rehearsal are done.

## The paragraph

**Find the Right Talk, for the press.** A media outlet's profile says what it covers. This tool
reads the KubeCon programme (601 sessions, 715 speakers, 226 sponsors) and ranks the talks,
speakers and sponsors that fit an outlet, each with the passage that made it match. A press door
takes an outlet's standing beat and its KubeCon assignment; a vendor door turns the same engine
round, so a sponsor finds the outlets and talks that fit it. A "Start-ups only" switch narrows the
sponsors to the 32 start-ups among the 226, so a small company with the right story can surface
beside the big names. The programme is searched by words and by meaning, and in Elastic Cloud
serverless four voices are blended: words, a small meaning model, Elastic's own ELSER and Jina's
embeddings, with Elastic's hosted Jina re-ranker as a further view. An Elastic Agent Builder agent
answers in plain words and quotes the programme's own passage for every pick. Sonar's Gitar
reviewed all the code, and Dash0 traces each search without the typed words. [A hosted copy runs on
Radar: add this only once Saturn confirms it is live.] It does not always get it right, and the
README says where.

## A shorter version, if the form has a small box

Find the Right Talk, for the press: pick a media outlet and it ranks the KubeCon programme (601
sessions, 715 speakers, 226 sponsors) by fit, each result with the passage that made it match. A
vendor door runs it in reverse, and a start-ups switch surfaces small companies. Words, meaning,
Elastic's ELSER and Jina's embeddings are blended in Elastic Cloud serverless, with a re-ranker and
an Agent Builder agent; Gitar reviewed the code and Dash0 traces the searches. All the code was
written on the day.

## Facts, with who measured them today

- 601 sessions (501 talks and 100 events), 715 speakers, 226 sponsors, 14 outlets (6 with a KubeCon
  assignment); 2,250 passages in all, 2,225 for the programme and 25 for the outlets; 0 email
  addresses in the loaded text (Titan, re-measured 11:38; Cassini's fresh copy, 11:52).
- 32 of the 226 sponsors are Start-ups; the switch takes the picker from 226 to 32 and back to 226
  (Titan, 12:24 to 12:25; Cassini, in a real browser, 12:31).
- Elastic Cloud load takes 66 seconds (ELSER and Jina read every passage); 12 seconds on the laptop
  engine (Titan, 12:01 to 12:09).
- The demo searches gave the same top results in three runs each (Cassini, 11:49).
- Demo outlet: the Hello World Gazette (Aaron, 12:16). The Breach Chronicle, the other test outlet,
  is set aside, stays in the data, and is reported honestly as a miss.

## What the repository holds, in two sentences (for the form)

Before 11:00 on 9 November: the idea, the notes, the public KubeCon programme copied with credit,
and the sponsor and outlet profiles in `data/`, including six labelled sample outlets. After 11:00:
every line of code, written by Claude Code under Aaron's direction, and the commit history that
starts at 11:00.

## Not built, so not claimed

- The fit check (an AI judgement of the top results) is not built. Nothing here says it is. It
  stays called the "fit check", never "the judge".
- Elastic Workflows is not used (the plan was to try it only if everything else was done by 15:00).
- Geo queries: not used. The data has no coordinates (Aaron, 11:12).
- The Radar hosted copy is not claimed as live until Saturn confirms it works.
- "Nothing is sent anywhere" is not said. In Elastic Cloud the programme and every search's text are
  read by Elastic's ELSER model inside Aaron's own project; Jina's embeddings, the re-ranker and the
  agent use Elastic's hosted service, billed per use (the README says so).
- Speed is not claimed beyond what was measured (a Gazette Go about 2.5 seconds; the agent answer
  took 41 seconds, so the video shows a recording).

## Where it falls short (also in the cheat sheet)

- The Hello World Gazette finds its hidden gem (mirrord) and two of its three must-finds in the top
  ten; Faros, a tool a manager uses to see what coding agents cost, is 13th.
- The Breach Chronicle misses: its wording is about attacks while its companies talk about
  vulnerabilities and sandboxes. It has no must-find in its top ten.
- Places 9 and 10 of the Gazette's list can swap between runs (Jina's scores differ in the fourth
  decimal); the top eight never changed in 13 runs.
- The flip's outlet order is a weak signal (the scores bunch together); its talks are strong.

## The checklist (from the day plan)

- [ ] Public repository link: https://github.com/aaronallsop/find-the-right-talk
- [ ] README setup passed the fresh-copy test (Cassini's early test at 11:53 passed with fixes; it
      is redone after the freeze)
- [ ] AI use disclosed in the README (written; the Gemini line stays bracketed until Aaron says whether he uses it; Jules is skipped)
- [ ] What existed before 11:00 and what was built after, in two sentences (above)
- [ ] Data credit: KubeCon + CloudNativeCon North America 2026 programme as of 4 November 2026, The
      Linux Foundation, CC BY 3.0
- [ ] The paragraph above, and the screen recording (Aaron's)
- [ ] Screenshot of the confirmation (Aaron's)
