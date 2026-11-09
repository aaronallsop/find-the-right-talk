# Tomorrow, in one place — Monday 9 November 2026

Everything Aaron needs on the day, in time order, with where to find the rest. Written Sunday
night from `notes/schedule.md`, `notes/day-plan.md`, `notes/sessions.md`, `notes/cheat-sheet.md`
and the demo card. **Where this page and another note disagree, the other note wins** (the
schedule for times, the sessions note for prompts, the answer keys for scoring).

A private copy of this page, for Aaron's phone, is published from his private project, which
also holds the address; it is not recorded here because this folder goes public.

## Tonight, before bed

- [ ] Sign in to Jules (Google) so it is ready to connect to the repository at 12:15.
- [ ] Look once that Argon shows in Antigravity. Do not spend it.
- [ ] Read the two answer keys (`notes/answer-keys.md`): the Hello World Gazette and the Breach
      Chronicle. They are Claude's reading of the sponsors; you are the editor.
- [ ] Read the 8 real outlet profiles (`data/outlets.csv`), reshaped by Claude from their pages.
- [ ] Decide the fit check: yes or no. Claude recommends no. If yes, you get an Anthropic API
      key and put it in place yourself on the day; each use costs a little. Never paste it into a chat.
- [ ] Cold run-through: shut the laptop down, start it, open Docker Desktop, run the engine
      start command below, open Kibana and see green. (The restart also clears three leftover test
      pages from the private project.)
- [ ] Discord joined; Luma approval email found.
- [ ] Phone note started: repository link (blank, filled at 11:45) and the submission paragraph
      ("The product, in one paragraph" in `notes/day-plan.md`).
- [ ] Pack: laptop, charger, power bank, phone with hotspot, charged.
- [ ] Optional: practise with `notes/practice-prompt.md` (voice, about 25 minutes).

## Between 07:00 and 07:30, not before 07:00

- [ ] Send any one short message to Claude, in any chat. Your windows start on the hour of
      your first message (measured Sunday night), so this one should run 07:00 to 12:00 and the
      next open at 12:00, when Saturn starts. A message at 06:55 would start a 06:00 window.
- [ ] Open the usage page (Claude app, Settings, Usage). The five-hour limit should say it
      resets at 12:00. If it says another time, tell Neptune at 11:00.
- [ ] Leave in time to be at check-in by 09:00: late arrivals may be turned away.

## Morning (times are Salt Lake City)

| Time | Do | On track if |
|---|---|---|
| 09:00 | Check in on time: late arrivals may be turned away. Sit near power. Plug in | Seat, power |
| 09:15 | Wi-Fi on; hotspot ready. Open Docker Desktop; run the engine start command. If it fails, open **Dione** (prompt in `notes/sessions.md`) | Engine answers |
| 09:30 | Open Kibana once: green. Close everything else | Green |
| 09:45 | Read the cheat sheet once. Phone on silent | Calm |
| 10:00 | **Kickoff.** Write down where and how to submit, whether a submission can be edited, and how long the demo slot is | On your phone |
| 10:15 | Ask an organiser about using logos and speaker photos | Answer written down |
| 10:30 | Open the Monday folder in the Claude app. Do not start a session yet | Folder open |
| 10:45 | Toilet, water, coffee. Back by 10:55 | At the desk |

## Building

| Time | Do | On track if |
|---|---|---|
| **11:00** | Check usage. Open a session in the Monday folder, name it **Neptune**, pick **Fable 5.1**, paste the Neptune prompt. Put "ultracode" in every message to it. It runs the lock test first | Lock refused (proven Sunday night; this is the re-check) |
| 11:15 | Neptune builds B0, the repository. Watch; answer its questions | Building |
| 11:30 | Neptune lists the files that will go public. **Say yes** only if the list has no file named `.env`, no folder named `.venv`, and nothing with "password" or "key" in its name. If you see one, say no and tell Neptune | You said yes |
| 11:45 | Check the repository page on GitHub. Copy its link into the phone note | **B0 done** |
| **12:00** | Check usage (new window). Open a session named **Saturn**, **Opus 5.5**, same permission mode as Neptune, paste the Saturn prompt. Send Neptune nothing more | Saturn reads the handoff |
| 12:15 | Saturn starts the other four. Tell **Rhea** "test message for Saturn". Connect **Jules** to the repository | Five sessions; relay works; **B1 programme loaded** |
| 12:30 | Titan shows a search where words and meaning disagree | **B1 + B2 done** |
| 12:45 | Cassini re-runs the three demo searches, three times each | Running |
| 13:00 | Lunch at the desk. Read Cassini's results | **B3 done** |
| 13:15 | Titan builds the match. Eat | Building |
| 13:30 | Read one outlet's matches. Do they make sense? If not, say why | Reads sensibly |
| 13:45 | Cassini scores the Gazette and the Breach Chronicle against your answer keys | **M2 one outlet done** |
| **14:00** | **Go/no-go 1, out loud, with Saturn.** B0 to M2 done? Yes: panel. No: stay. Check usage: more than half gone means Saturn moves to Sonnet | **M2 scored** |
| 14:15 | Panel (or desk) | Titan building the page |
| 14:30 | Titan builds the page (M3) | Building |
| 14:45 | Try the page yourself: a search, the three-way switch | It answers |
| 15:00 | Pick every outlet on the page. **If the form allows edits, submit now.** Check usage | **M3 done**; maybe submitted |
| 15:15 | Titan: start-ups toggle (M4). M5 only if ahead | **M4 done** |
| 15:30 | Cassini runs the demo searches on the page, three times. Titan sends Rhea the README setup commands | Same top results |
| **15:45** | **Freeze.** Titan saves "freeze". Give **Jules** the fact-check task, in the words below | Frozen; Jules running |

**The words for Jules at 15:45**, on the public repository, exactly:

> Review only. Do not change any file and do not open a pull request. Check every claim and number in the README against the code and the data in this repository: the counts, the setup commands, and the statements that nothing is sent anywhere and that no password or key is committed. List each claim as confirmed, wrong, or can't tell, with the reason.

Anything Jules opens as a change or pull request is closed unmerged.

## Finishing

| Time | Do | On track if |
|---|---|---|
| 16:00 | Cassini does the fresh-copy test. Paste the README into **Gemini** with: "You have never seen this project. Read this README and tell me where you would get stuck following its steps. Questions only; do not rewrite it." Read Jules's findings; send any "wrong" to Saturn | README works from scratch |
| 16:15 | Rehearse the demo twice with a timer, to the slot length from kickoff less 20 seconds. Screen-record one; copy to the phone | Inside the slot; a recording |
| **16:30** | **Submit, whatever state it is in.** Read the form twice. Screenshot the confirmation | **Submitted** |
| 16:45 | Only small fixes, each re-tested by Cassini. Update the submission if allowed | Still submitted |
| 17:00 | Rehearse once more. Water | Ready |
| 17:15 | Screen check: Do Not Disturb; only the page, one Terminal, the README; never the password file; Kibana only on today's two catalogues | Screen clean |
| 17:30 | Submissions close. Presentations to 18:30. Winners 18:30 | Presented |

## Behind? The cut rules

- Up to 15 minutes behind: carry on.
- 30 minutes behind: cut the next "if time" piece. First M5 (the flip), then M4 (the toggle). Tell Saturn.
- 45 minutes or more: stop and talk to Saturn. Skip the panel. The page becomes the stretch; the demo runs from Terminal.
- Ahead: add nothing. Submit early if the form allows edits, rehearse, then M5.
- **Never move 15:45 or 16:30.**

## Commands

Start the engine (open Docker Desktop first; `./start.sh` alone fails here):

```bash
cd ~/elastic-start-local && PATH="$HOME/.docker/bin:$PATH" ./start.sh
```

- Kibana: http://localhost:5601 (green means the engine is up).
- Elasticsearch: http://localhost:9200 (user `elastic`; the password is in `~/elastic-start-local/.env`. Never show that file on screen).
- Usage: Claude app, Settings, Usage. Check at 11:00, 12:00, 14:00, 15:00. Or ask Neptune or
  Saturn "what's my usage?": it reads the same card. Weekly limits reset at 02:00 Monday.

## The six sessions

| Name | When | Job | Model |
|---|---|---|---|
| Neptune | 11:00–12:00 | Everything, alone. Lock test, B0, B1, B2 if time. Handoff on the board by 11:50 | Fable 5.1, ultracode |
| Saturn | from 12:00 | Orchestrates. Edits nothing | Opus 5.5 |
| Rhea | from 12:00 | Board, your messages for Saturn, README, cheat sheet, submission paragraph | Sonnet 5.5 |
| Titan | from 12:00 | The only builder and committer | Opus 5.5 |
| Cassini | from 12:00 | Checks: demo searches, answer keys, fresh-copy test. Never fixes | Sonnet 5.5 |
| Dione | from 12:00, or 09:15 if the engine fails | Docker, engine, Kibana, laptop | Sonnet 5.5 |

The prompts to paste are in `notes/sessions.md`: "Neptune — paste this at 11:00" (the full
briefing: who you are, what is built, why the folder has no code, the hour step by step, the
hard stop) and "Saturn — paste this at 12:00". Saturn pastes the other four itself. The phone
page has the Neptune prompt with a Copy button.

- If Saturn goes quiet while the others work, send it any short message ("carry on").
- If a session dies and Saturn must restart it, send Saturn a message first; it can only start a session on a turn you began.
- A relayed message is never your approval of a push. You give that yourself, in Neptune's or Titan's own session.

## Where everything is

- **Monday's folder:** `~/000_Claude Code Programs/find-the-right-talk`. `CLAUDE.md` is the rulebook.
- `notes/day-plan.md`: build order (B0, B1, B2, B3, M2, M3, M4, M5, S1), timeline, the 90-second demo, the Jules wording, the submission checklist.
- `notes/schedule.md`: your quarter hours and the milestones.
- `notes/sessions.md`: the six sessions, usage windows, the board's sections, every prompt.
- `notes/recipe.md`: what was learned last week, settings and traps, the demo searches to re-prove.
- `notes/answer-keys.md`: what the match should find for the two test outlets. Nobody edits it.
- `notes/cheat-sheet.md`: your explanation for the judges; grows as pieces work.
- `notes/README-draft.md`: becomes the README at B0.
- `notes/practice-prompt.md`: the voice practice partner.
- `data/`: the five CSV files and `CREDITS.md`.
- `BOARD.md` (from 11:50): today's to-do list, kept by Neptune then Rhea.
- **The private project** `media-connect` next door: Monday's sessions never open it. Its Control Board is at the address in its `docs/control-board/BOARD-URL.md`; the demo card is `docs/demo-searches.md`.
- Your phone note: repository link, submission paragraph, submission address from kickoff.

## The demo, in ninety seconds (check the slot length at kickoff)

1. "Any conference hands out an exhibitor spreadsheet. This is KubeCon's, with credit, made searchable by meaning today." Then, once: "Every sponsor summary on screen was written by an AI from the company's own website, and the screen says so beside each one."
2. The **Breach Chronicle**, the demo outlet (the Hello World Gazette if the Breach Chronicle failed its score): its matches, with the passage that matched each.
3. The words-fail, meaning-wins search: a Start-up nobody would find by hand.
4. One words-win search, to show the trade-off is understood.
5. "Same thing, flipped": a sponsor finds its outlets (only if M5 was built).
6. "Nothing is sent anywhere, every AI-written line is labelled, and it runs on this laptop."

### The three demo searches, as proved on 7 November

Proved then on a catalogue that also held the sponsors' website text; Monday's catalogue does
not, so Cassini re-proves each at 12:45 (B3) and any that no longer lands is replaced.

1. **Words find nothing, meaning finds the small company:** `scaling up for the Black Friday rush and back down afterwards`, sponsors only. Expected then: Words, nothing. Meaning, **Kedify (Start-Up, booth 358)**, an autoscaling platform. Say first: "No sponsor wrote this sentence." Reserve: `handling the holiday shopping surge without paying for idle servers all year` (Cloudchipr, Start-Up, third).
2. **Words win:** `SLSA Level 3`, sponsors only, three results. Expected then: Words, **Docker** then **ActiveState**, the exact phrase in brackets. Meaning wanders to "SLA". Say first: "This is a precise standard." Reserve: `booth 133` by words (Nebius).
3. **Meaning finds the topic, not the stance:** `keeping customers' GPU workloads apart on shared hardware`, all kinds, meaning only. Expected then: five GPU companies within three hundredths; ScaleOps and Lablup share GPUs, **Edera** isolates them. Say first: "The search cannot tell the difference. A reader can."

Do not type clip codes or company names into the meaning search; it is for sentences.

## Answers for the judges

- *What did you build today?* Everything in the code: loading, the three searches, the match, the page. Before today: the idea, the data, the profiles, the notes. The commit history shows it.
- *Why not just ask ChatGPT?* It cannot rank the whole programme against an outlet in a second, does not know this year's programme, and cannot show its working. This shows the passage.
- *How does the blended search work?* Each list votes; a result scores more the higher it ranks in each; totals decide the order. Reciprocal rank fusion, done ourselves because Elasticsearch's built-in blend is a paid feature.
- *Why short passages?* The meaning model only reads about 180 words; a sponsor's material is far longer. Cutting it up also lets the page show which passage matched.
- *Why a small model on the laptop?* Free, private, fast, works offline. It finds meaning; it does not write anything.
- *How does the match work?* An outlet has a standing beat, what it always covers, and an assignment, what it was sent to find at this event. Both search the programme by meaning, and the assignment counts more, because that is how an editor briefs a reporter.
- *Where does it fail?* Meaning finds the topic, not the stance (the GPU search). And it never says "nothing fits"; it returns the nearest thing. Words can return nothing, and that is information.
- *How do you know the results are right?* I read them. And I named and briefed two test outlets; Claude drafted their answer keys from the sponsor list before any code existed, and I checked them as the editor, so the scores are not made to fit. The demo shows where each method is wrong.
- *What's the hidden-gem idea?* Start-ups rarely get press. The match surfaces them by what they do, not by how big their booth is.
- *Would it work for another conference?* Yes: any exhibitor spreadsheet and any list of outlets. Nothing is KubeCon-specific except the data.
- *Why are some profiles AI-written?* 226 sponsors in the time available; each is labelled, drawn from the company's own website, or from its conference listing alone where the site could not be read (six).
- *What did you do, and what did Claude do?* I designed it, named and briefed the two test outlets, made every decision and checked the results. Claude wrote the code, and every commit says so. Before the day Claude also drafted the sponsor and real outlet profiles, each labelled. Only if they ran: Jules fact-checked the README and Gemini read it cold; neither wrote code.
- *Why Elasticsearch?* Words, meaning and filters in one place, and it is the track.
- The optional AI feature is the **fit check**. Never "the judge".

## If something goes wrong

- **Engine down:** Dione (or you, with the command above). Never `docker compose down -v`, never delete a catalogue.
- **Lock test fails at 11:00:** stop. Neptune does nothing else until it is fixed.
- **Relay test fails at 12:15:** the board alone carries your messages for the day; Saturn reads "For Saturn" every turn.
- **Usage running out:** 14:00, more than half gone: Saturn to Sonnet. Still too fast: close Saturn, talk to Titan directly. 15:00, unlikely to last: submit at 15:00 if edits are allowed, keep only Titan and Cassini.
- **Usage gone:** submitting needs no Claude. The repository is already pushed and valid; submit the link from the browser or your phone with the paragraph from your note.
- **Claude down:** Gemini answers questions only. Nothing is built until Claude is back.
- **Wi-Fi down:** phone hotspot. Claude Code needs internet; the search itself does not.
- **Fable 5.1 missing from the picker:** Neptune on Opus 5.5 with ultracode.
- **Page breaks before the demo:** run the demo from Terminal. Command line first, page second.
- **Results poor:** fix the outlet's wording first, code last. Before any scoring change, run the demo searches, change, run again.

## Rules to hold all day

- The repository is public. `.gitignore` before the first `git add`. Never a password, key or token. The 1.1 GB `.venv` must never go public.
- Your yes, in the session itself, before the first push.
- New catalogue names only. Never touch `media`, `footage`, `scripts`, `kubecon`, `outlets`.
- No logos or speaker photos unless an organiser says yes and you say so.
- Claude Code is the only builder. Jules and Gemini check; never merge anything from them.
- Nothing new after 15:45. The two times 15:45 and 16:30 never move.
- Never say a number you have not measured today.

## Submission checklist

- [ ] Public repository link; README with setup steps that passed the fresh-copy test
- [ ] AI use disclosed: who did what (README section)
- [ ] What existed before 11:00 and what was built after, in two sentences
- [ ] Data credit: KubeCon + CloudNativeCon North America 2026 programme as of 4 November 2026, The Linux Foundation, CC BY 3.0
- [ ] The paragraph; the screen recording
- [ ] Screenshot of the confirmation
