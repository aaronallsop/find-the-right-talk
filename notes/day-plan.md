# Day plan — Monday 9 November 2026, from an empty folder

WeMakeDevs Cloud Native Hackathon, Elasticsearch track, Salt Lake City. Building 11:00 to
17:30. Solo: Claude Code builds, Aaron directs, checks and decides. Written Sunday 8 November;
replaces the earlier plan, which assumed the code would be carried in (it is not: decided 8
November, so nothing is coded before the start).

## The product, in one paragraph

**Find the right talk, for the press.** A media outlet's profile says what it covers. The tool
reads the KubeCon programme (601 sessions, 715 speakers, 226 sponsors) and ranks the talks,
speakers and companies that fit, each with the passage that made it match. Start-up sponsors
are flagged, so a small company with the right story surfaces beside the big names. Search
the programme three ways: words, meaning, blended. Nothing is ever sent to anyone.

## Rules for the day

- **Command line first, page second.** If the page breaks, the demo runs from Terminal.
- **Fix the data before the code.** Poor results usually mean the outlet's beat text.
- **Save and push after every piece that works** (as `CLAUDE.md` defines saving: files named,
  `data/` committed, never `git add -A` mid-work).
- **Valid early.** The README, licence and credits go in in the first hour, so the repository
  is a valid entry from then on.
- **Two go/no-go points, 14:00 and 15:45.** Missing one means cutting a tier, not working faster.
- **Freeze at 15:45.** Then: test the README, rehearse, record, submit.
- **One run is not proof.** Every demo search three times.

## Other AI tools: checkers, never builders

Claude Code is the only thing that writes or edits code in this folder or the repository, and
within it only Neptune before 12:00 and Titan after (the sessions are in `notes/sessions.md`).
Aaron's Google tools have two jobs, both as outside readers that have not seen the work:

- **Jules: the fact checker.** At the 15:45 freeze, once the code is pushed, Aaron gives Jules
  one task on the public repository: *"Review only. Do not change any file and do not open a
  pull request. Check every claim and number in the README against the code and the data in
  this repository: the counts, the setup commands, and the statements that nothing is sent
  anywhere and that no password or key is committed. List each claim as confirmed, wrong, or
  can't tell, with the reason."* It runs while the fresh-copy test does. Anything it opens as a
  change or pull request is closed unmerged. Its findings go to Claude Code; only small fixes,
  each re-tested, and only before 16:30. Connecting Jules to the new repository is Aaron's to
  do, in any quiet moment after B0 and before 15:00 (two minutes, his GitHub permission).
- **Gemini (Argon, in Antigravity or the Gemini app): the cold reader and the backup.** At
  16:00 it reads the README as a stranger would and says where it would get stuck. If Claude
  Code is down or out of usage, Aaron uses Gemini for questions and explanations only; it
  edits nothing. Argon's allowance is small and weekly, so it is not spent on anything else.
- Both go in the README's AI section if used.

## Build order

| # | What | Done means, on screen |
|---|---|---|
| B0 | The folder becomes a repository: **`.gitignore` first** (before any `git add`), then the README draft, MIT licence, credits, the CSVs and notes. Aaron's go-ahead before the first push to the public repository | The public repository exists and its README says what was pre-built |
| B1 | **Load:** read the CSVs, cut long text into passages, turn passages into numbers, load two new, empty catalogues (programme, outlets) | Counts on screen: 601 sessions, 715 speakers, 226 sponsors, 14 outlets |
| B2 | **Three ways to search** the programme in Terminal, with a compare mode | One search shows words and meaning disagreeing |
| B3 | **Re-prove the demo searches** (recipe, last section). Replace any that no longer land | Three searches, each three times, same top result |
| M2 | **The match:** an outlet's assignment and standing beat search the programme, the assignment counting more; ranked talks, speakers, sponsors, each with the passage that matched | One outlet's list reads sensibly; then the two test outlets scored against `notes/answer-keys.md` |
| M3 | **The page:** search box with the three-way switch, and an outlet picker that shows its matches | Every one of the 14 outlets works in the browser |
| M4 | **Hidden gems:** Start-up tier marked; a "start-ups only" toggle | Count drops, and comes back |
| M5 | **The flip:** a sponsor finds its outlets | One sponsor's outlet list matches common sense |
| S1 | *Only if well ahead:* the AI **fit check** (needs Aaron's key). Not called "the judge" anywhere | GPU case: it separates sharing from isolating |

## Timeline

Aaron's own quarter-hour version, with milestones to tell whether he is ahead or behind, is
`notes/schedule.md`. Where the two differ by a quarter hour (they do, in two or three rows),
the schedule's milestones are the ones Saturn checks against; the fixed times 14:00, 15:45
and 16:30 are the same in both.

| Time | Do | State at the end |
|---|---|---|
| 09:00 | Check-in; arrive on time (late arrivals may be turned away). Power, hotspot, Docker, Elasticsearch started and healthy | Engine green |
| 10:00 | Kickoff. **Write down where and how to submit, and whether a submission can be edited.** Ask an organiser about logos and photos | Submission route written down |
| 11:00 | Building opens. Open a Claude Code session in the new folder named **Neptune** (Fable 5.1, ultracode) and paste its prompt from `notes/sessions.md`; the folder's `CLAUDE.md` is the brief. Neptune runs the first hour alone: the lock test below, B0, B1, and B2 if time, then a handoff on the board by 11:50. **At 12:00** Saturn (Opus 5.5) takes over, starts Rhea, Titan, Cassini and Dione, and runs the relay test (about ten minutes). Why 12:00: Aaron's usage windows (`notes/sessions.md`). **First, the lock test (2 min):** ask it to read the README in the media-connect folder next door and say which rulebook it follows. It must be refused, and name this folder's brief. If it reads the file, stop and fix the lock before anything else. (The lock covers Claude's file tools, not the shell; the brief's rule covers the rest.) Then B0 | Public repository pushed, README valid |
| 11:30 | B1 load, first half | Programme loaded, counts right |
| 12:00 | B1 outlets; B2 three ways in Terminal. Checkpoint | Three ways work |
| 12:30 | B3 re-prove the demo searches | Written down which land |
| 13:00 | Lunch at the desk. M2 the match | One outlet's list reads sensibly |
| 13:30 | M2: score the Hello World Gazette and the Breach Chronicle against the answer keys, three ways. Fix wording first if they fail. Checkpoint | Both scored and written down |
| **14:00** | **Go/no-go 1**, out loud. B0–B3 and M2 done? Yes: watch the panel (14:00–14:30), then M3. No: stay at the desk | A decision said out loud |
| 14:30 | M3 the page. Checkpoint | Search and outlet picker work in the browser |
| 15:00 | M4 start-ups toggle; M5 the flip if time. **If the form allows edits, submit now** | Submitted, or the reason it is not yet |
| 15:30 | Demo searches on the page, three times each. README setup steps written | Same top results every time |
| **15:45** | **Freeze.** Checkpoint "freeze". Aaron gives Jules the fact-check task (above) | Nothing new from here; Jules running |
| 16:00 | **Fresh-copy test:** Cassini clones the public repository into `~/ftrt-freshcopy`, follows the README word for word (skipping only the Elasticsearch install, which is already running), and sees the search come up. Gemini reads the README cold. Read Jules's findings | It works from the README alone, or the README is fixed; every Jules "wrong" fixed or answered |
| 16:15 | Rehearse twice with a timer; screen-record (copy to phone) | Under three minutes; a recording that plays |
| **16:30** | **Submit, whatever state the product is in.** Read the form twice; screenshot the confirmation | Submitted |
| 16:45 | Buffer. Only if submitted: small fixes, each re-tested | Still submitted |
| 17:15 | Pre-demo screen check (below). Pitch ready | Ready |
| 17:30 | Submissions close; presentations to 18:30; winners 18:30 | Presented |

**Plan B for submitting:** phone hotspot on; a note on the phone with the repository link and the
submission paragraph, ready to paste.

## The demo, in ninety seconds

1. "Any conference hands out an exhibitor spreadsheet. This is KubeCon's, with credit, made
   searchable by meaning today."
2. Pick an outlet with a niche beat: its matches, with the passage that matched each.
3. The words-fail, meaning-wins search: a Start-up nobody would find by hand.
4. One words-win search, to show the trade-off is understood.
5. "Same thing, flipped": a sponsor finds its outlets.
6. "Nothing is sent anywhere, every AI-written line is labelled, and it runs on this laptop."

## Pre-demo screen check (17:15)

- Do Not Disturb on; notifications off.
- Only the demo windows open: the page, one Terminal, the README.
- Kibana, if shown, only on today's two catalogues (it also lists Aaron's private ones).
- Never show the settings file that holds the Elasticsearch password.
- Hotspot ready; charger plugged in.

## Submission checklist

- [ ] Public repository link; README with setup steps that passed the fresh-copy test
- [ ] AI use disclosed: who did what (README section)
- [ ] What existed before 11:00 and what was built after, in two sentences
- [ ] Data credit: KubeCon + CloudNativeCon North America 2026 programme as of 4 November
      2026, The Linux Foundation, CC BY 3.0
- [ ] The paragraph above; the screen recording
- [ ] Screenshot of the confirmation
