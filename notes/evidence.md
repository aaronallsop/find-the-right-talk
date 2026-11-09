# Evidence: what was measured, and what it showed

Everything here was run and read back on 9 November 2026 by a checker that only runs the tool and writes
down what it sees (it changes no code). Times are the laptop's own clock. Every search was run against
the project's Elastic Cloud serverless engine unless a line says otherwise. A search is "stable" only if
repeated runs gave the identical list, scores included. Each result names the version of the code (the commit
hash from the repository history) it was measured on; a result is a statement about that version only.

**Draft stamp: first written 12:44 on 9 November. To be re-run and re-stamped after the 15:45 freeze;
until then each line stands for the version named on it.**

## 1. The data, loaded from a fresh copy of the public repository

Measured 11:51 to 11:53 on version 552c262, from a new clone, following the README: installing the packages
worked (exit 0, no errors); the load finished in 68 seconds (exit 0). What it printed:

| What | Count | Passages |
|---|---|---|
| Talks | 501 | 816 |
| Events | 100 | 126 |
| Speakers | 715 | 717 |
| Sponsors | 226 | 566 |
| Outlets (6 with a KubeCon assignment) | 14 | 25 |

2,225 programme passages and 25 outlet passages in all, each turned into 384 numbers. Email addresses found
in the loaded text: 0 in the programme, 0 in the outlets. The same two searches that follow, run from this
clone, gave the same top results as in the working folder ("SLSA Level 3": ActiveState first in words,
OpenSSF first in meaning; the traffic-spike sentence below: Kedify first). The meaning model was already in
this machine's cache; a clone on a machine without it was not tested to the end.

**The setup was tested once from a fresh copy, at 11:51 to 11:53 on 9 November, before Elastic's own model
(ELSER) and the re-ranker were added, and has not been re-tested from a fresh copy since.** Everything later in
this file was measured in the working folder, not in a fresh clone.

## 2. The three demo searches (sponsors only, three runs each, all three runs identical every time)

Measured 11:30 to 11:33 (version f712a6d) and again 11:48 (version 174effd, after the passages were re-cut).
"Words" finds records that contain the typed words; "meaning" finds the nearest by meaning; "blended" merges
the two lists.

| Search | Words (11:48) | Meaning (11:48) | Blended (11:48) |
|---|---|---|---|
| "SLSA Level 3" | ActiveState, Docker | OpenSSF, HeroDevs, Akeyless Security, AEnix, Nebius | ActiveState, OpenSSF, Docker, HeroDevs, Akeyless Security |
| "scale up for a traffic spike and back down afterwards" | nothing | Kedify (Start-Up), ScaleOps, DataAgent, Better Stack, Ascendra Networks | same as meaning |
| "keeping different tenants' GPU workloads isolated from each other on shared hardware" | Edera | vCluster, Edera, Rafay Systems, AEnix, Cast AI | Edera, vCluster, Rafay Systems, AEnix, Cast AI |

- "SLSA Level 3": words finds the two sponsors whose own text names the standard; meaning drifts to
  general open-source-security companies. In blended, ActiveState and OpenSSF are exactly tied on score; the
  order between them was the same in all three runs.
- The traffic-spike sentence: words finds nothing, meaning finds a Start-Up autoscaler first. The wording
  used for it was chosen at 11:32 from three alternatives run three times each; the sentence
  first tried ("How do you survive a Black Friday traffic spike without paying for idle servers the rest of
  the year?") put no Start-Up in meaning's top three, so it was not used.
- The GPU sentence: words and meaning disagree on the top result (Edera against vCluster); blended puts Edera
  first because both lists name it.
- The laptop's own engine (same data, same code) gave the identical top five in every way for "SLSA Level 3",
  both traffic-spike wordings and the GPU sentence, run once each at 11:33.
- The three sentences after later changes: in the page's "Compare all" (version acdd654, 12:36), the GPU
  sentence among sponsors gave Edera first in words, ELSER and blended and vCluster first in meaning and
  re-ranked, identical in three runs. In the page's "Re-ranked" search (version c4a8ae8, 12:34 to 12:39) the
  traffic-spike sentence gave Kedify first, identical in three runs. The SLSA sentence was not re-run on these.

## 3. The match, scored against answer keys written before the build

The two answer keys (`notes/answer-keys.md`) were written on 8 November from the sponsors' own descriptions,
before any code. A company counts as "found" if it appears in the top 10 sponsors the outlet's own profile
brings up, run three ways (words, meaning, blended) and, from 12:13, a fourth (Elastic's own model, "ELSER").
All runs were repeated three times and were identical each time. Sponsors only, top 10.

### Hello World Gazette (assignment: AI agents that help you write code)

Key: three must-finds (Coder, Momentic, Faros), one hidden gem (mirrord by MetalBear, a Start-Up), two that
should also do well (Docker, JetBrains), one beat-only company that should rank lower (KodeKloud), one trap (Endor Labs).

| Version, time | Must-finds in blended top 10 | Hidden gem's rank in blended | KodeKloud, Endor Labs |
|---|---|---|---|
| 552c262, 11:50 (as first built) | 1 of 3 (Coder 6th) | 5th | not in top 10 |
| 321b069, 11:57 | 2 of 3 (Momentic 8th, Coder 9th; Faros 11th) | 4th | not in top 10 |
| 2e26f1b, 12:13 (with ELSER) | 2 of 3 (Momentic 4th, Coder 8th; Faros 13th) | 3rd | not in top 10 |

At 12:13: the gem is 2nd in the ELSER list; all three ways together put 3 of the 4 assignment companies in
the blended top 10; the one missing, Faros, is 13th. The key's own pass test (all three must-finds in the
top 10) is therefore not met, by one company. At 12:13 the blended top ten was Docker, ControlTheory, mirrord
by MetalBear, Momentic, JetBrains, Syntasso, Temporal, Coder, Sentry, Resolve AI; the page showed the same ten in
the same order in each of three runs at 12:35 (version c4a8ae8).

### The Breach Chronicle (assignment: AI agents that help security teams, or keep agents safe)

Key: seven must-finds (Maze, Emphere, Endor Labs; Edera, Cosmonic, Teleport, Archestra AI), one hidden gem
(Vijil), and companies that should rank lower (Akamai, RapidFort, Echo).

| Version, time | Must-finds or the gem in the blended top 10 |
|---|---|
| 552c262, 11:50 | none |
| 321b069, 11:57 | none |
| 2e26f1b, 12:13 (with ELSER) | none |

At 12:13, in the top 50: Maze 4th by meaning, 30th by ELSER, 23rd blended; Vijil 23rd by meaning; Edera 40th by
ELSER; Cosmonic 36th and Endor Labs 43rd by meaning; Emphere and Teleport in no list's top 50. The match does
not find this outlet's assignment: the companies it ranks top (Sysdig, Plural, Resolve AI) are ordinary
security, observability and platform companies. The outlet's own wording is about breaches, attackers and
incident response; the words "breach", "cybersecurity", "threat", "incident" and "respond" appear in the text of
none of the eight key companies (counted once in the sponsor data, 12:20). On the talks side the same match is more convincing (for example "How Kubernetes Handles AI Generated
Security Reports", "The Agent Has Entered the Cluster: AI Auth 101 for Kubernetes").

### A fault found and fixed

At 11:50 the match gave different top tens when asked for 10 results and when asked for 50. After the fix
(version 321b069) the top 10 at `-n 10` was exactly the first ten of the top 50, for both outlets and all ways,
checked by program.

## 4. The flip: a sponsor finds the outlets that fit it

Measured 12:18 to 12:19 on version 68c98c7: three runs of each sponsor's blended result, all three identical
for each; plus one comparison run each. All 14 outlets are ranked every time.

| Sponsor | Top three outlets | Top three talks | Score spread across 14 outlets |
|---|---|---|---|
| Kedify (Start-Up) | Greenstack, LearnKube, TFIR | Battle-tested Autoscaling Paradigms with KEDA; SIG Autoscaling Project Updates; Beyond Model Serving (KServe) | 12% of the top score; first to second gap 0.0024 |
| Edera | TFIR, Greenstack, SDxCentral | Untrusted Code on Secure Runtimes: Agent Sandboxes on Kubernetes; Extending NetworkPolicy to RDMA; Securing the Agentic Future | 16%; gap 0.0021 |
| Docker | Hello World Gazette, The Breach Chronicle, TFIR | From YOLO to Golden Paths: Building Trusted Environments for AI Agents; Untrusted Code on Secure Runtimes; Securing the Agentic Future | 33%; ten outlets within 0.0158, then a drop |

The scores bunch: the flip shows the right group of outlets better than it orders neighbours.

## 5. The page

### 5.1 It answers (version fba8720, 11:55)
All 14 outlets answered through the page's own requests in 0.5 to 1.4 seconds with no error. Typing both boxes
or only the first gave an answer; typing only the second, or nothing, gave a readable message (HTTP 400); the plain
"SLSA Level 3" search matched the Terminal's result exactly in all three ways.

### 5.2 Speed, in the real browser (version c4a8ae8, 12:34 to 12:39, three runs each)

Time from the click until the page's button is back:

| Action | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Hello World Gazette, press Go | 2.71 s | 2.48 s | 2.69 s |
| Start-ups only switched on (match re-runs by itself) | 2.09 s | 1.93 s | 2.26 s |
| Start-ups only switched off | 2.46 s | 2.35 s | 2.74 s |
| Flip, Kedify | 1.87 s | 1.66 s | 1.52 s |
| Plain search, "Re-ranked" way, traffic-spike sentence | 1.21 s | 1.33 s | 1.13 s |

### 5.3 Compare all (version acdd654, 12:36 to 12:41, in the real browser)
One click shows the same search or match every way at once, as five columns (words, meaning, ELSER, blended,
re-ranked). GPU sentence among sponsors: 1.54 s, 1.73 s, 1.17 s (three runs, identical). Hello World Gazette
match: 3.15 s, 2.45 s, 2.46 s for the match to come back; the columns are then drawn in about 55 ms. The
Breach Chronicle once: 2.64 s. A name in several columns carries "in N": every badge was recomputed from the
columns (zero mismatches in all runs); every column equals its single view name for name and in order; Start-Up
tags were compared to the data for all 69 sponsors shown (GPU 15, Gazette 28, Breach 26): none missing, none wrong.

### 5.4 Start-ups only (version 9ab6782, 12:29, in the real browser)
Switching it on takes the sponsor pool from 226 to 32, and back to 226 on switching off; the sponsor list after
switching off was identical, name for name, to the one before. The 32 are exactly the 32 Start-Up rows in the data.
With it on, every sponsor shown (40 match rows, 10 search rows, 32 picker rows) is a Start-Up and carries the tag;
talks and speakers lists do not change; the lists after switching off are identical to the lists before. In
version c4a8ae8 the page no longer lets "Talks" be chosen while it is on (the box is set to sponsors and greyed).

### 5.5 The engine is named on screen
The page shows "Elastic Cloud serverless, with Elastic's ELSER" beside the title (screenshot, 12:36).

## 6. What was not measured
The setup steps in the README were run from a fresh copy only once (section 1), before ELSER was added; no
fresh-copy run was made after that. Nothing here says how the page looks on a phone, how long it takes on a slow connection, or how the tool
behaves for anyone but the person who built it. The word counts quoted for the Breach Chronicle's wording are a
single count over the sponsors' text. The Gazette misses its own key's pass test by one company; the Breach
Chronicle misses it entirely. No geographic search is offered: the data has no coordinates.
