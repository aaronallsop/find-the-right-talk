# Checks — Cassini's results, with the time of each

Cassini looks and never fixes. Everything below was measured on 9 November 2026 against the
program as loaded at that time (commit f712a6d plus whatever was on disk; no code was changed
by Cassini). Command, run from the folder:
`.venv/bin/python -m ftrt.search --mode compare --kind sponsor -n 5 "<search>"`
Default engine is Elastic Cloud serverless (named on screen as "Engine: Elastic Cloud serverless");
`FTRT_ENGINE=local` in front gives the laptop engine ("local engine at http://localhost:9200").

---

## B3 — the three demo searches re-proved (11:30 to 11:33). This is the "before" baseline for Titan's reload.

Each search was run three times in a row on the cloud (about 5 seconds apart). **In every case
all three runs gave identical top-5 lists in words, meaning and blended.** Sponsors only unless
said otherwise. Tier in brackets.

### 1. "SLSA Level 3" — **lands: words win** (runs at 11:30:41, 11:30:47, 11:30:52)

| Way | Top results (same in all 3 runs) |
|---|---|
| Words | 1 Docker (Platinum), 2 ActiveState (Silver); only two results |
| Meaning | 1 Open Source Security Foundation (OpenSSF) (Silver), 2 Nebius (Platinum), 3 Arpio (Silver), 4 HeroDevs (Silver), 5 Akeyless Security (Silver) |
| Blended | 1 Docker, 2 OpenSSF, 3 ActiveState, 4 Nebius, 5 Arpio |

Words and meaning disagree on the top result. Words finds the two sponsors whose own text names
the standard; meaning drifts to general open-source-security companies. Nebius and Arpio (meaning
ranks 2 and 3) have nothing to do with SLSA: meaning is just returning the nearest things.

### 2. Black Friday sentence, exactly as Neptune worded it — **lands only partly** (11:30:57, 11:31:02, 11:31:08)

"How do you survive a Black Friday traffic spike without paying for idle servers the rest of the year?"

| Way | Top results (same in all 3 runs) |
|---|---|
| Words | (nothing) |
| Meaning | 1 North (Silver), 2 Pump (Silver), 3 Fastly (Silver), 4 pgEdge (**Start-Up**), 5 Kedify (**Start-Up**) |
| Blended | identical to meaning (words is empty) |

Words fails and meaning answers, as the demo needs, but **no Start-Up is in the top three**, and
the top result is a Silver sponsor, not the autoscaling start-up. Stable, but not the hoped-for
story. (My reading, not measured: "idle servers ... rest of the year" pulls toward cost and
hosting companies.)

### 2b. Black Friday rewordings, three runs each, sponsors only

| # | Wording | Words | Meaning top 5 (same in all 3 runs) | Start-Up in top 3? |
|---|---|---|---|---|
| a | "scale up for a traffic spike and back down afterwards" (11:32:13, :18, :23) | (nothing) | 1 **Kedify (Start-Up)**, 2 ScaleOps (Diamond), 3 DataAgent (Silver), 4 pgEdge (Start-Up), 5 Better Stack (Silver) | **Yes: Kedify is first** |
| b | "autoscale our servers up when traffic surges and back down to nothing when it passes" (11:32:27, :32, :37) | (nothing) | 1 pgEdge (Start-Up), 2 DataAgent (Silver), 3 Better Stack (Silver), 4 Arpio (Silver), 5 Kedify (Start-Up) | Yes: pgEdge first. Kedify (the actual autoscaler) only fifth |
| c | "how do we handle a sudden surge of visitors, adding capacity at the peak and removing it afterwards?" (11:32:42, :47, :51) | (nothing) | 1 Ascendra Networks (Start-Up), 2 Kedify (Start-Up), 3 Pump (Silver), 4 Better Stack (Silver), 5 Cloudchipr (Start-Up) | Yes: Ascendra and Kedify |

Blended equalled meaning in every case (words empty). Every run of every wording agreed with the
other two runs.

**Chosen: wording (a), "scale up for a traffic spike and back down afterwards".** Words finds
nothing; meaning's first result is **Kedify (Start-Up tier)**, whose own text in `data/sponsors.csv`
says "a Kubernetes autoscaling platform ... scale-to-zero" — the right company for the story, and a
Start-Up. It is also the plainest wording, with no cost words. (b) and (c) also put a Start-Up in
the top three, but (b) puts the real autoscaler fifth and (c) leads with Ascendra Networks, which
I did not check.

### 3. The GPU sentence — **lands** (runs at 11:31:13, 11:31:18, 11:31:22; all kinds at 11:31:58, 11:32:03, 11:32:08)

"keeping different tenants' GPU workloads isolated from each other on shared hardware"

Sponsors only, identical in all 3 runs:

| Way | Top results |
|---|---|
| Words | 1 Edera (Silver); one result only |
| Meaning | 1 vCluster (Gold), 2 Edera (Silver), 3 Cast AI (Platinum), 4 Runpod (Silver), 5 Aranya (Start-Up) |
| Blended | 1 Edera, 2 vCluster, 3 Cast AI, 4 Runpod, 5 Aranya |

All kinds (program-wide; the command does allow it), identical in all 3 runs:

| Way | Top results |
|---|---|
| Words | 1 Edera (sponsor) |
| Meaning | 1 vCluster (sponsor), then four talks: "Extending NetworkPolicy to RDMA: Hardware-Enforced Tenant Isolation for AI Clusters", "Beyond the Cluster Boundary: Sharing GPUs at Scale", "Feeding the GPU: Streaming Data into Training, Lakehouse, and Serving without the Serialization Tax", "Why Are You Still Wasting Whole GPUs? Hardware-Level Sharing, Scheduled with DRA" |
| Blended | 1 Edera, 2 vCluster, 3 to 5 the first three talks above |

Words and meaning disagree on the top result (Edera, which isolates, against vCluster). The
person still has to read the passage; this is the "why a person has to read" demo.

### Scores for the three meaning lists above (for the "within 0.027" claim in the recipe)

Not measured in this check; the compare output prints scores but I recorded only order. Say
nothing about the gap until it is measured.

---

## Laptop engine against the cloud, once each (11:33:01 to 11:33:13, `FTRT_ENGINE=local`)

| Search | Laptop top-5 lists (words, meaning, blended) vs cloud |
|---|---|
| "SLSA Level 3" | identical to the cloud |
| Black Friday, Neptune's wording | identical to the cloud |
| Black Friday, chosen wording (a) | identical to the cloud (Kedify first) |
| GPU sentence (sponsors only) | identical to the cloud |

Same top result and the same top five, in all three ways, on the laptop and in the cloud. The
all-kinds GPU search was not run on the laptop.

---

## Summary for Saturn (11:35)

- **Land:** SLSA yes; GPU yes; Black Friday as worded by Neptune partly (words empty, but no Start-Up in top three).
- **Chosen Black Friday wording:** "scale up for a traffic spike and back down afterwards": words nothing, meaning gives Kedify (Start-Up) first, same in 3 of 3 runs.
- **Cloud against laptop:** same top five, all three ways, on all four searches checked once.

---

## B3 "after" — the same three searches after Titan's reload (commit 174effd), cloud, sponsors only, three runs each (11:48:09 to 11:48:47)

Code on disk at the time: commit 174effd, plus uncommitted edits to `ftrt/config.py` and a new
`ftrt/match.py` that were Titan's work in progress (the search command did not use them, as far as I
can tell; I did not read them). All 3 runs of each search gave identical top-5 lists, scores
included. Scores are printed after each name.

**SLSA Level 3: the tie keeps the same order in all 3 runs, it does not flip.**

| Way | After (same in all 3 runs) | Before (11:30, same in all 3 runs) |
|---|---|---|
| Words | 1 ActiveState (Silver) 12.9189, 2 Docker (Platinum) 10.0805 | 1 Docker, 2 ActiveState |
| Meaning | 1 OpenSSF 0.6728, 2 HeroDevs 0.6330, 3 Akeyless Security 0.6301, 4 AEnix 0.6264, 5 Nebius 0.6234 | 1 OpenSSF, 2 Nebius, 3 Arpio, 4 HeroDevs, 5 Akeyless |
| Blended | 1 ActiveState 0.0164, 2 OpenSSF 0.0164, 3 Docker 0.0161, 4 HeroDevs 0.0161, 5 Akeyless 0.0159 | 1 Docker, 2 OpenSSF, 3 ActiveState, 4 Nebius, 5 Arpio |

The top of the blend is a true tie: ActiveState is first in words and OpenSSF is first in meaning, so
each gets 1 ÷ 61 and the printed scores are equal. The order between them (ActiveState first) came out
the same in all 3 runs, but nothing in the scores decides it, so it rests on how ties are broken. Words
still win in the sense that matters (words names the two sponsors whose text says it; meaning names
OpenSSF, HeroDevs, Akeyless, AEnix, Nebius, none of them clearly about SLSA from what I read). Words'
order changed: ActiveState now ahead of Docker. Meaning no longer shows Arpio.

**"scale up for a traffic spike and back down afterwards": holds.** Words nothing in all 3 runs.
Meaning and blended: 1 Kedify (Start-Up) 0.6342, 2 ScaleOps (Diamond) 0.6169, 3 DataAgent (Silver),
4 Better Stack (Silver), 5 Ascendra Networks (Start-Up). Before: Kedify, ScaleOps, DataAgent, pgEdge,
Better Stack. Same top three; pgEdge dropped out, Ascendra came in at 5.

**GPU sentence: holds on the top result; the rest changed.** Words: Edera alone (18.6225). Meaning:
1 vCluster (Gold) 0.7479, 2 Edera (Silver) 0.7460, 3 Rafay Systems 0.7011, 4 AEnix 0.6933, 5 Cast AI
0.6921. Blended: 1 Edera 0.0325 (both lists voted for it), 2 vCluster, 3 Rafay, 4 AEnix, 5 Cast AI.
Before: meaning vCluster, Edera, Cast AI, Runpod, Aranya (Start-Up). Runpod and Aranya are no longer in
the top five. The recipe's "five companies within 0.027" now reads: meaning scores 0.7479 to 0.6921
across the top five, a spread of 0.0558 (arithmetic on the printed scores).

---

# M2 scoring sheet — laid out 11:41, nothing scored yet (the match is not built)

Source of every row: `notes/answer-keys.md`, which is never edited. Run for each outlet:
sponsors only, top 10, three ways (words, meaning, blended). Fill in **rank** (1 to 10, or "–" if
not in the top 10; "empty" if the way returned nothing) in each way's column. "In blended top 10"
is the pass test. Record the time and the engine of each scoring run, and score three runs, not one.

**The pass, as the answer keys state it:** all must-finds in the blended top 10, the hidden gem in
the top 10, nothing from the lower groups above the gem.

## Hello World Gazette

Assignment: AI agents built for developers, agents that help you write code.
Scoring run: time ______ engine ______ (run 1 / 2 / 3)

| Group | Company | Found (Y/N) | Words rank | Meaning rank | Blended rank | In blended top 10 |
|---|---|---|---|---|---|---|
| Must find (assignment) | Coder (Silver) | | | | | |
| Must find (assignment) | Momentic (Silver) | | | | | |
| Must find (assignment) | Faros (Silver) | | | | | |
| **Hidden gem** | **mirrord by MetalBear (Start-Up)** | | | | | |
| Should also do well | Docker (Platinum) | | | | | |
| Should also do well | JetBrains (Silver) | | | | | |
| Standing beat only: should rank lower | KodeKloud (Silver) | | | | | |
| Trap | Endor Labs (Silver) | | | | | |

Summary per way (fill in):

| | Words | Meaning | Blended |
|---|---|---|---|
| Assignment companies (the 3 must-finds + the gem) in the top 10 (of 4) | | | |
| Hidden gem's rank | | | |
| Any standing-beat-only company or trap ranked above any assignment company? Which | | | |
| Pass / fail | | | |

Came up in the top 10, not expected (company, tier, rank, which way, and the passage that made it match):

| Company | Tier | Rank | Way | Why it matched (passage) | Fair or wrong? |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

## The Breach Chronicle (the demo outlet)

Assignment, two halves: AI agents built to help people working in cybersecurity, or to keep AI
agents themselves safe inside the companies using them. The test is whether **both** halves are found.
Scoring run: time ______ engine ______ (run 1 / 2 / 3)

| Group | Company | Found (Y/N) | Words rank | Meaning rank | Blended rank | In blended top 10 |
|---|---|---|---|---|---|---|
| Must find: agents that help security teams | Maze (Start-Up) | | | | | |
| Must find: agents that help security teams | Emphere (Start-Up) | | | | | |
| Must find: agents that help security teams | Endor Labs (Silver) | | | | | |
| Must find: keeping agents safe | Edera (Silver) | | | | | |
| Must find: keeping agents safe | Cosmonic (Silver) | | | | | |
| Must find: keeping agents safe | Teleport (Platinum) | | | | | |
| Must find: keeping agents safe | Archestra AI (Start-Up) | | | | | |
| **Hidden gem** | **Vijil (Start-Up)** | | | | | |
| Standing beat only: should rank lower | Akamai | | | | | |
| Standing beat only: should rank lower | RapidFort | | | | | |
| Standing beat only: should rank lower | Echo | | | | | |
| Partial word trap (a fair middle result, not a must-not) | Orca Security (Silver) | | | | | |

Summary per way (fill in):

| | Words | Meaning | Blended |
|---|---|---|---|
| Assignment companies in the top 10 (of 8: the 7 must-finds + the gem) | | | |
| "Helps security teams" half found (of 3) | | | |
| "Keeping agents safe" half found (of 4) | | | |
| Hidden gem's rank | | | |
| Any standing-beat-only company above any assignment company? Which | | | |
| Where Orca Security landed | | | |
| Pass / fail | | | |

Came up in the top 10, not expected (company, tier, rank, which way, and the passage that made it match):

| Company | Tier | Rank | Way | Why it matched (passage) | Fair or wrong? |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

If a sheet fails, the answer keys say: fix the outlet's wording first, re-run; code comes last. If
standing-beat companies crowd out the assignment, the beat is weighing too much: lighten it before
touching anything else. Cassini records; Titan and Saturn decide.

---

# M2 scoring sheet — FILLED IN (the blank sheet above is the template; this is the result)

Scored 11:50 against commit 552c262 (the match), Elastic Cloud serverless, sponsors only, command
`.venv/bin/python -m ftrt.match --mode compare --kind sponsor -n 10 "<outlet>"`. **Three runs
(11:50:01 to :03 Gazette; 11:50:19 to :22 Breach): identical names, ranks and scores in all three.**
Rank is the position in that way's top 10; **"(n50: r)" is the rank when the same command is run
with `-n 50`**, to show where a company sits outside the top ten. "–" is not in the top 10.

## Hello World Gazette — FAIL on the answer key's pass test

| Group | Company | Found in top 10 (any way) | Words | Meaning | Blended | In blended top 10 |
|---|---|---|---|---|---|---|
| Must find | Coder | Y (blended) | – (n50: 29) | – (n50: 11) | 6 (n50: 9) | Y |
| Must find | Momentic | Y (words) | 7 (n50: 8) | – (n50: 21) | – (n50: 8) | **N** (but 8th at n=50) |
| Must find | Faros | Y (meaning) | – (n50: 38) | 3 (n50: 7) | – (n50: 11) | **N** (11th at n=50) |
| **Hidden gem** | **mirrord by MetalBear (Start-Up)** | Y (blended) | – (n50: 26) | – (n50: 4) | 5 (n50: 4) | **Y** |
| Should also do well | Docker | Y | 3 | – (n50: 14) | 4 (n50: 3) | Y |
| Should also do well | JetBrains | Y | 1 | 2 (n50: 3) | 1 | Y |
| Standing beat only | KodeKloud | N | not in top 50 | – (n50: 27) | not in top 50 | N (good) |
| Trap | Endor Labs | N | – (n50: 17) | – (n50: 45) | – (n50: 20) | N (good) |

| Summary (n=10) | Words | Meaning | Blended |
|---|---|---|---|
| Assignment companies in the top 10 (3 must-finds + gem, of 4) | 1 (Momentic) | 1 (Faros) | 2 (Coder, mirrord) |
| Hidden gem's rank | not in top 10 (26) | not in top 10 (n50: 4) | 5 |
| Standing-beat-only or trap above an assignment company? | no (KodeKloud, Endor Labs absent) | no | no |
| Pass: all 3 must-finds in blended top 10, gem in top 10, nothing lower above the gem | – | – | **Fail**: gem yes; Coder yes; Momentic and Faros no (at n=50, Momentic 8th, Faros 11th) |

Came up in the top 10, not expected (n=10): words: Temporal (Gold) 2, Stacklet 4, ControlTheory (Gold) 5,
Dash0 (Platinum) 6, Sentry 8, Xata 9, empirik 10. Meaning: Paper Compute Company (Start-Up) 1,
ControlTheory 4, Vijil (Start-Up) 5, Komodor 6, Resolve AI 7, PatapscoAI (Start-Up) 8, Nirmata 9,
Klique 10. Blended: ControlTheory (Gold) 2, Cosmonic (Silver) 3, Syntasso 7, Maze (Start-Up) 8,
Spotify 9, Dash0 10. From the passages printed: Paper Compute (its text: "records your agents' work and
surfaces the sessions worth learning"), Cosmonic ("Sandbox Agents, Tools, and Apps") and PatapscoAI
("runs long-lived AI agents in sandboxed workspaces") are about agents but not clearly about
helping developers write code; I have not judged them fair or wrong beyond that. Maze (blended 8) is
the Breach Chronicle's security-agent company, ranked in the Gazette's list.

## The Breach Chronicle — FAIL: no must-find in the blended top 10, not even at n=50 except three

| Group | Company | Words | Meaning | Blended | In blended top 10 |
|---|---|---|---|---|---|
| Must find: helps security teams | Maze (Start-Up) | – (not in top 50) | 4 | – (n50: 26) | N |
| Must find: helps security teams | Emphere (Start-Up) | – (not in top 50) | – (not in top 50) | – (not in top 50) | N |
| Must find: helps security teams | Endor Labs (Silver) | – (not in top 50) | – (n50: 43) | – (n50: 27) | N |
| Must find: keeping agents safe | Edera (Silver) | – (not in top 50) | – (not in top 50) | – (not in top 50) | N |
| Must find: keeping agents safe | Cosmonic (Silver) | – (not in top 50) | – (n50: 36) | – (not in top 50) | N |
| Must find: keeping agents safe | Teleport (Platinum) | – (not in top 50) | – (not in top 50) | – (not in top 50) | N |
| Must find: keeping agents safe | Archestra AI (Start-Up) | – (not in top 50) | – (not in top 50) | – (n50: 49) | N |
| **Hidden gem** | **Vijil (Start-Up)** | – (not in top 50) | – (n50: 23) | – (not in top 50) | **N** |
| Standing beat only | Akamai | – (not in top 50) | – (n50: 40) | – (not in top 50) | N (good) |
| Standing beat only | RapidFort | not in top 50 | not in top 50 | not in top 50 | N (good) |
| Standing beat only | Echo | not in top 50 | not in top 50 | not in top 50 | N (good) |
| Partial word trap | Orca Security | not in top 50 | not in top 50 | not in top 50 | N |

| Summary (n=10) | Words | Meaning | Blended |
|---|---|---|---|
| Assignment companies in the top 10 (7 must-finds + gem, of 8) | 0 | 1 (Maze, rank 4) | 0 |
| "Helps security teams" half found in top 10 (of 3) | 0 | 1 | 0 |
| "Keeping agents safe" half found in top 10 (of 4) | 0 | 0 | 0 |
| Hidden gem's rank | not in top 50 | n50: 23 | not in top 50 |
| Standing-beat-only above an assignment company? | no (none in the lists) | no in the top 10; at n=50 Akamai (40) is ahead of Endor Labs (43) | no |
| Orca Security | not in top 50 | not in top 50 | not in top 50 |
| Pass | – | – | **Fail**: no must-find, no gem in the blended top 10 |

Came up in the top 10, not expected (n=10): words: PagerDuty 1, Northflank 2, Uber 3, Linux
Foundation Education 4, Jozu 5, Tigris Data 6, VAST Data 7, Docker 8, Aiven 9, Diagrid 10. Meaning:
Resolve AI (Gold) 1, Twingate 2, Sysdig (Gold) 3, Datadog (Platinum) 5, Infisical (Platinum) 6, Plural 7,
Tigera 8, Solo.io (Diamond) 9, Klique 10. Blended: Sysdig 1, Plural 2, Northflank 3, Jozu 4, Radar
(Start-Up) 5, Kubex 6, Edge Delta 7, PatapscoAI (Start-Up) 8, Resolve AI 9, Twingate 10. Most are ordinary
security, observability or platform companies, the group the key says should rank lower; I read only the
first lines of their passages and have not judged each.

## Finding: the match's ranking changes with how many results are asked for

The same command at `-n 10` and `-n 50` does not give the same first ten. Measured (3 identical runs
at n=10; one at n=50): Gazette meaning top five is Paper Compute, JetBrains, Faros, ControlTheory, Vijil
at n=10 but Komodor, Paper Compute, JetBrains, mirrord, Resolve AI at n=50; Gazette blended is
JetBrains, ControlTheory, Cosmonic, Docker, mirrord at n=10 but JetBrains, ControlTheory, Docker,
mirrord, Paper Compute at n=50. Breach blended top five is Sysdig, Plural, Northflank, Jozu, Radar at
n=10 but Resolve AI, Jozu, PagerDuty, Plural, Sysdig at n=50. Only Breach words was the same. Neptune's
fix in 42c36e0 made plain search steady across result counts; the match does not have that. Cause not
investigated (I do not edit or diagnose code). Because of it, the sheet's "(n50)" ranks are not exactly
the ranks a user would see at n=10.

## All kinds (sponsors, talks, speakers), one run each at n=10 (Gazette 11:50:31, Breach 11:50:33)

Sponsors were identical to the sponsors-only runs above. Talks and speakers, blended top 5:
- **Gazette talks:** MCP Was the Easy Half, The Rest Was a Skill Issue; Agentic + Cloud Native: Getting
  Started Contributing to Kagent; What monday.com's 500+ Engineers and AI Agents Have in Common; Demo
  Theater: Do you trust your AI agent? Pod Sandboxing on OKE; What's New with Kubectl and Kustomize …
- **Gazette speakers:** Drew Brown, Valentina Rodriguez Sosa, Michael Rishi Forrester, Aman Singh, Casey West.
- **Breach talks (reads well):** How Kubernetes Handles AI Generated Security Reports; Following the Evidence
  with HolmesGPT; Agentic Ops: Building Guardrails for Autonomous AI with Policy-as-Code; Pods Are Not
  Enough for AI Agents, Meet Agent-substrate; From Platform Catalog to Conversational Agent … Meaning's top
  ten for Breach also holds "The Agent Has Entered the Cluster: AI Auth 101 for Kubernetes", "Untrusted Code
  on Secure Runtimes: Agent Sandboxes on Kubernetes", "Platform-First AI Agent Security: Zero-Trust Patterns for
  Kubernetes" and "The Identity Crisis: Who is the AI Agent in Your Cluster?": titles that read as both halves
  of the assignment. The talks side lands far better than the sponsors side.
- **Breach speakers:** Vicente Herrera, Ant(on) Weiss, Ashwin Sarimin, Valentina Rodriguez Sosa, Drew Bowman.
- Words for Breach talks returns "Project Lightning Talk - Project Overview" twice (ranks 5 and 6): two
  talks with the same title, so either two real sessions or a duplicate; not checked.

---

# Fresh-copy test, early (11:49 to 11:54), README as at commit 552c262

Clone of https://github.com/aaronallsop/find-the-right-talk.git into `~/ftrt-freshcopy` (did not
exist beforehand, so nothing to empty), HEAD 552c262 = origin/main. README followed step by step.
Engine used: Elastic Cloud serverless (the demo's project) with Aaron's **second** key through
`FTRT_CLOUD_ENV=~/elastic-cloud/.env.freshcopy` in front of every command. I never opened, printed or
copied either settings file (only listed their names and sizes). No docker command; no installer.

| README step | What I did | Result |
|---|---|---|
| 1. Create your own Elastic Cloud serverless project | Skipped on purpose: the demo's existing project is used, Aaron's second key | not tested (a judge makes their own project) |
| Alternative: install Elasticsearch locally (Docker, start-local) | Skipped: already installed, not re-run | not re-run |
| 2. Make `~/elastic-cloud/.env` with `ES_CLOUD_URL=` and `ES_CLOUD_API_KEY=` | **Deliberate deviation:** used the README's own option, `FTRT_CLOUD_ENV=/path/to/.env` in front of each command, pointing at `~/elastic-cloud/.env.freshcopy` | works: every command printed "Engine: Elastic Cloud serverless" |
| 3. `python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt` | Ran exactly that (python3.11 is 3.11.16) | **passes**: exit 0, no errors or warnings; `.venv` is 1.1 GB; only a "new pip release available" notice. About 1 to 2 minutes here (not timed exactly) |
| 4. `.venv/bin/python -m ftrt.load` | Ran with the key switch, 11:51:46 to 11:52:54 | **passes**, with two README claims wrong (below). Exit 0 |
| 5. "Start the page: [command], and open [address]." | Not runnable: the README still has the placeholder | **fails / unclear**: the step has no command and no address |
| "Until the page exists" search command | `.venv/bin/python -m ftrt.search --mode compare "SLSA Level 3"`, then `--kind sponsor --startups` with the traffic-spike wording | passes; see below |

Load counts printed by the fresh copy (these rebuilt the demo's two catalogs in the cloud project):
501 talks in 816 passages; 100 events in 126 passages; 715 speakers in 717 passages; 226 sponsors in
566 passages; 14 outlets (6 with a KubeCon assignment) in 25 passages. 2,225 passages turned into 384
numbers each for `ftrt-programme` (7 s) and 25 for `ftrt-outlets`. In the engine afterwards:
`ftrt-programme` 2,225 passages, `ftrt-outlets` 25 passages; 0 email addresses in each; 33 passages
with an @ sign (social handles). "Done in 68s".

**Steps that fail or are unclear, and README statements that are wrong:**
1. **Step 5 is a placeholder** ("[command]" and "[address]"): a judge cannot start the page. (Expected
   at this stage, since the page was not built when I cloned.)
2. **README step 4 says "cuts the text into 2,250 passages"; the load printed 2,225** program passages
   (2,250 would be 2,225 + 25 outlet passages, if that is the intended total; the README reads as the
   program's count). Wrong or ambiguous.
3. **README step 4 says "about 30 seconds to Elastic Cloud"; this run took 68 s** (the 25 s Neptune
   measured earlier was before the passage rework). One run only; the claim is not supported by this run.
4. **A machine without the meaning model already cached cannot run it.** `ftrt/quiet.py` sets
   `HF_HUB_OFFLINE=1` unless the environment says otherwise, and the README says nothing about downloading
   the model. Test: with an empty Hugging Face cache (`HF_HOME` pointed at an empty folder, search only,
   no write to the engine) the search stops with "We couldn't connect to 'https://huggingface.co' to load
   the files, and couldn't find them in the cached files." This laptop has the model cached from before the
   day, so the load worked here only for that reason. I did not download the model, so I do not know
   whether the load would then pass; the offline setting is the blocker I saw.
5. The README describes only `ftrt.search`; the match (`python -m ftrt.match`, in the clone) is not
   mentioned yet.
6. README step 2 says the file is `~/elastic-cloud/.env`; a judge on another machine has no such folder
   (they would create it). Clear enough as written; recorded because it is where the README tells a
   judge to put their settings. **Where I deviated: only here**, via the README's own `FTRT_CLOUD_ENV`
   option.

**Searches from the fresh copy (11:53):** "SLSA Level 3" (all kinds): words ActiveState, Docker; meaning
OpenSSF first; blended ActiveState first, OpenSSF second: the same as the "after" check in the main
folder. The traffic-spike wording with `--kind sponsor --startups`: words nothing, meaning and blended
Kedify first, then Ascendra Networks, pgEdge, Radar, FluidCloud. Cloud engine named on screen both times.
`ftrt.match --list` lists the 14 outlets, including Hello World Gazette and The Breach Chronicle.

**Not tested:** the page; the match from the fresh copy (the main folder's match was scored above);
creating an Elastic Cloud project and its settings file from nothing; installing the model on a
machine with no cache. The second key was accepted for loading: no refusal.

---

# M3 the page (commit fba8720), http://127.0.0.1:5060, checked 11:55 to 11:56

**How:** the browser pane was tried first and **refused**: `navigate` to http://127.0.0.1:5060 returned
"navigation ... was denied or failed" and the pane stayed on a blank page. So this is **a check through
the page's own web requests (curl and a small Python script), not through a browser**: the screen was
never rendered, buttons and tabs were not clicked, and the page's JavaScript was not run. What it proves
is that every request the page's JavaScript makes (`/api/lists`, `/api/match`, `/api/flip`, `/api/search`)
answers correctly; it does not prove the buttons, tabs, layout or how the results look on screen. The
page served (HTTP 200). Engine named by `/api/lists`: "cloud". I did not start or stop the page.

## The 14 outlets (`/api/match` with each outlet's id, as the picker sends it)

All 14 answered HTTP 200 in 0.5 to 1.4 s, no error. Each returns 10 sponsors, 10 talks and 10 speakers
in blended and in meaning. Words came back with fewer in some cases (words can legitimately find
less; this is the one thing to know when looking at the Words switch):

| Outlet | Parts used | Blended and meaning (sponsors / talks / speakers) | Words (sponsors / talks / speakers) |
|---|---|---|---|
| Futurum Group | beat | 10 / 10 / 10 | 2 / 0 / 2 |
| Greenstack | beat + assignment | 10 / 10 / 10 | 10 / 10 / 10 |
| Hello World Gazette | beat + assignment | 10 / 10 / 10 | 10 / 10 / 10 |
| LearnKube | beat | 10 / 10 / 10 | 10 / 8 / 1 |
| Open Source Sustainability Weekly | beat + assignment | 10 / 10 / 10 | 10 / 10 / 10 |
| OpsMatters | beat | 10 / 10 / 10 | 3 / 0 / 0 |
| SDxCentral | beat | 10 / 10 / 10 | 5 / 1 / 0 |
| TechRevolt News | beat | 10 / 10 / 10 | **0 / 0 / 0** (the Words switch would show nothing for all three tabs) |
| Techstrong | beat | 10 / 10 / 10 | 10 / 5 / 10 |
| TFIR | beat | 10 / 10 / 10 | 10 / 10 / 10 |
| The Breach Chronicle | beat + assignment | 10 / 10 / 10 | 10 / 10 / 10 |
| The New Stack | beat | 10 / 10 / 10 | 10 / 5 / 10 |
| The Regulated Cloud | beat + assignment | 10 / 10 / 10 | 10 / 10 / 9 |
| Women in Infrastructure | beat + assignment | 10 / 10 / 10 | 10 / 10 / 10 |

Blended top three sponsors for the outlets, as the page returns them: Gazette JetBrains, ControlTheory,
Cosmonic; Breach Chronicle Sysdig, Plural, Northflank (the same top three as the Terminal run at `-n 10`
before; I did not re-score the match: Titan has a fix coming); TFIR Stacklok, IBM, Komodor; The New Stack
Red Hat, Better Stack, New Relic; Women in Infrastructure Tigera, Radar, KodeKloud. (All 14 lists are in
the run output; I judged none of them for sense.) The pickers: 14 outlets and 226 sponsors load.

## Press door, typed

- **Both boxes** (the Breach Chronicle's beat and assignment wording, typed in my own words from the answer
  key, not the stored text): HTTP 200, "Your outlet", parts beat + assignment. 10 each; blended sponsors
  Sysdig, Jozu, Radar (Start-Up), Plural, Northflank; meaning Twingate, Maze (Start-Up), Jozu, Sysdig, Palo
  Alto Networks; blended talks Pods Are Not Enough for AI Agents, Meet Agent-substrate; Agentic Ops: Building
  Guardrails for Autonomous AI with Policy-as-Code; …
- **First box only:** HTTP 200, parts beat only; 10 each; blended sponsors Crash Override, Wiz, Maze (Start-Up),
  Black Duck, Sysdig; talks Five Stages of Kubernetes Security Grief; AI-DDoS: …
- **Second box only, or both empty:** HTTP 400 "Pick an outlet, or say what you always cover."
  (readable, not a crash). Unknown outlet id: HTTP 404 "No outlet 'nope' in ftrt-outlets. Run the loader first."

## Vendor door

`/api/flip` answers HTTP 200 with `pending: true` and the message "The flip, outlets that fit your company,
is the next piece to be built." (the page's JavaScript shows it in a note under the vendor form; I did not
see it on screen). That is correct for now: M5 is not built.

## The plain search for "SLSA Level 3", page against Terminal

Page (`/api/search`, three modes) against `.venv/bin/python -m ftrt.search --mode compare "SLSA Level 3"`
in the main folder: **identical in all three ways**: the same names, order and scores (blended: ActiveState,
OpenSSF, Docker, Priyanka Saggu, Baruch Sadogursky, …; words: ActiveState 12.9189, Docker 10.0805, Baruch
Sadogursky 6.8636; meaning: OpenSSF first). Empty search: HTTP 400 "Type something to search for."; unknown
mode: HTTP 400 "Unknown search."

**To note:** the plain search (unlike the match) includes **events** in its results: "Distributed SQL
Summit Hosted by YugabyteDB | SEPARATE REGISTRATION REQUIRED" and "Project Pavilion Kiosks | Tuesday Morning"
are in the top 10 for "SLSA Level 3". They are not talks, speakers or sponsors; this is the same as the
Terminal, not a page bug.

**Not checked (needs a browser):** how the page looks, that the door buttons, switches and tabs work, that
the page's JavaScript handles every answer above, narrow or phone widths, and the Start-Up marking on screen.

---

# M2 scoring sheet, SECOND column set: after 321b069 ("the match no longer changes with how many results are shown"), before Elastic's model

Scored 11:57 (Gazette runs 11:57:34, :36, :38; Breach runs 11:57:41, :42, :43; n=50 once at 11:57:39 and
11:57:45), commit 321b069, Elastic Cloud serverless, sponsors only, `-n 10`, three runs: **identical names,
ranks and scores in all three runs, for both outlets**. This is the baseline before Titan's reload for
Elastic's model. The first column set above is kept unchanged. "Rank" is at `-n 10`; "(n50)" is the same
company's rank at `-n 50`, shown only where it is outside the top 10.

**The fix holds:** for both outlets and all three ways, the `-n 10` list is exactly the first ten of the
`-n 50` list, names and scores (compared programmatically). The first set's "n=10 differs from n=50" fault
is gone. The new n=10 ranks equal the old "n50" ranks, so the first set's "(n50)" numbers were the right
ones.

## Hello World Gazette — still FAIL on the answer key's test, by one place

| Group | Company | Words | Meaning | Blended | In blended top 10 | First set (n=10) for comparison: W / M / B |
|---|---|---|---|---|---|---|
| Must find | Coder | – (n50: 29) | – (n50: 11) | 9 | **Y** | – / – / 6 |
| Must find | Momentic | 8 | – (n50: 21) | 8 | **Y** | 7 / – / – |
| Must find | Faros | – (n50: 38) | 7 | – (n50: 11) | **N** (11th) | – / 3 / – |
| **Hidden gem** | **mirrord by MetalBear** | – (n50: 26) | 4 | 4 | **Y** | – / – / 5 |
| Should also do well | Docker | 3 | – (n50: 14) | 3 | Y | 3 / – / 4 |
| Should also do well | JetBrains | 1 | 3 | 1 | Y | 1 / 2 / 1 |
| Standing beat only | KodeKloud | not in top 50 | – (n50: 27) | not in top 50 | N (good) | – / – / – |
| Trap | Endor Labs | – (n50: 17) | – (n50: 45) | – (n50: 20) | N (good) | – / – / – |

| Summary (n=10) | Words | Meaning | Blended |
|---|---|---|---|
| Assignment companies in the top 10 (3 must-finds + gem, of 4) | 1 (Momentic) | 2 (mirrord, Faros) | **3 (Coder, Momentic, mirrord)** (first set: 2) |
| Hidden gem's rank | – (26) | 4 | 4 |
| Standing-beat-only or trap above an assignment company? | no | no | no |
| Pass: all 3 must-finds in blended top 10, gem in top 10, nothing lower above the gem | – | – | **Fail by one: Faros is 11th** (gem 4th, KodeKloud and Endor Labs well below) |

Came up in the top 10, not expected: words: Temporal (Gold) 2, Stacklet 4, ControlTheory (Gold) 5, Dash0
(Platinum) 6, Black Duck 7, Sentry 9, Xata 10. Meaning: Komodor (Gold) 1, Paper Compute Company (Start-Up) 2,
Resolve AI (Gold) 5, PatapscoAI (Start-Up) 6, ControlTheory 8, Vijil (Start-Up) 9, Coralogix 10. Blended:
ControlTheory 2, Paper Compute Company 5, Sentry 6, Resolve AI 7, Temporal 10.

## The Breach Chronicle — still FAIL: no must-find and no gem in the blended top 10

| Group | Company | Words | Meaning | Blended | In blended top 10 | First set (n=10): W / M / B |
|---|---|---|---|---|---|---|
| Must find: helps security teams | Maze (Start-Up) | – (not in top 50) | 4 | – (n50: 26) | N | – / 4 / – |
| Must find: helps security teams | Emphere (Start-Up) | not in top 50 | not in top 50 | not in top 50 | N | same |
| Must find: helps security teams | Endor Labs | not in top 50 | – (n50: 43) | – (n50: 27) | N | same |
| Must find: keeping agents safe | Edera | not in top 50 | not in top 50 | not in top 50 | N | same |
| Must find: keeping agents safe | Cosmonic | not in top 50 | – (n50: 36) | not in top 50 | N | same |
| Must find: keeping agents safe | Teleport | not in top 50 | not in top 50 | not in top 50 | N | same |
| Must find: keeping agents safe | Archestra AI (Start-Up) | not in top 50 | not in top 50 | – (n50: 49) | N | same |
| **Hidden gem** | **Vijil (Start-Up)** | not in top 50 | – (n50: 23) | not in top 50 | **N** | same |
| Standing beat only | Akamai | not in top 50 | – (n50: 40) | not in top 50 | N (good) | same |
| Standing beat only | RapidFort, Echo | not in top 50 | not in top 50 | not in top 50 | N (good) | same |
| Partial word trap | Orca Security | not in top 50 | not in top 50 | not in top 50 | N | same |

| Summary (n=10) | Words | Meaning | Blended |
|---|---|---|---|
| Assignment companies in the top 10 (7 must-finds + gem, of 8) | 0 | 1 (Maze, 4th) | 0 |
| "Helps security teams" half found in top 10 (of 3) | 0 | 1 | 0 |
| "Keeping agents safe" half found in top 10 (of 4) | 0 | 0 | 0 |
| Hidden gem's rank | not in top 50 | 23 | not in top 50 |
| Standing-beat-only above an assignment company? | none present | Akamai (40) above Endor Labs (43) | none present |
| Pass | – | – | **Fail** |

Ranks of each must-find at n=50 (the Breach must-finds you asked for): Maze: meaning 4, blended 26, words not
in top 50. Endor Labs: meaning 43, blended 27. Cosmonic: meaning 36, blended and words not in top 50.
Archestra AI: blended 49, meaning and words not in top 50. Emphere, Edera, Teleport: not in the top 50 in any
way. Vijil (gem): meaning 23, blended and words not in top 50. These are the same as in the first set's "(n50)".

Came up in the top 10, not expected: words (unchanged): PagerDuty 1, Northflank 2, Uber 3, Linux Foundation
Education 4, Jozu 5, Tigris Data 6, VAST Data 7, Docker 8, Aiven 9, Diagrid 10. Meaning: Resolve AI (Gold) 1,
Twingate 2, Sysdig (Gold) 3, Plural 5, Tigera 6, Komodor 7, Datadog (Platinum) 8, Jozu 9, groundcover 10.
Blended: Resolve AI 1, Jozu 2, PagerDuty 3, Plural 4, Sysdig 5, Edge Delta 6, Radar (Start-Up) 7, Northflank 8,
Nirmata 9, Docker 10. As before, mostly ordinary security, observability and platform companies.

---

# M2 scoring sheet, THIRD column set: with Elastic's own model, ELSER (commit 2e26f1b, cloud reloaded 12:01 to 12:10)

Scored 12:13 (Gazette runs 12:13:18, :20, :22; Breach runs 12:13:28, :30, :32; `-n 50` once at 12:13:25 and
12:13:34), Elastic Cloud serverless, sponsors only, `-n 10`. Four ways: words, meaning, **elser** (Elastic's
own model, `--mode elser`), blended (now six lists: words, meaning and ELSER for each of the beat and the
assignment). **Three runs: identical names, ranks and scores in all three, for both outlets.** The first
and second column sets above are kept. "(n50)" is the rank at `-n 50` where it is outside the top 10.
"2nd" is the second set (321b069, before ELSER).

**Words against the previous set:** Hello World Gazette's words list is **identical** to the second set
(same names, ranks and scores). The Breach Chronicle's words list **changed with the reload** (as Titan said;
the engine re-counts word rarity): top ten is now Sysdig, PagerDuty, Wiz, Northflank, Uber, Linux Foundation
Education, Jozu, Tigris Data, VAST Data, Docker; it was PagerDuty, Northflank, Uber, Linux Foundation
Education, Jozu, Tigris Data, VAST Data, Docker, Aiven, Diagrid. Still no must-find in it. Meaning is
identical to the second set for both outlets (names and scores), as it should be.

## Hello World Gazette — still FAIL by Faros, now 13th (was 11th)

| Group | Company | Words | Meaning | ELSER | Blended | In blended top 10 | 2nd set blended |
|---|---|---|---|---|---|---|---|
| Must find | Coder | – (n50: 29) | – (n50: 11) | – (n50: 13) | 8 | **Y** | 9 |
| Must find | Momentic | 8 | – (n50: 21) | 3 | 4 | **Y** | 8 |
| Must find | Faros | – (n50: 38) | 7 | – (n50: 37) | – (n50: 13) | **N** | – (11) |
| **Hidden gem** | **mirrord by MetalBear** | – (n50: 26) | 4 | 2 | 3 | **Y** | 4 |
| Should also do well | Docker | 3 | – (n50: 14) | 1 | 1 | Y | 3 |
| Should also do well | JetBrains | 1 | 3 | – (not in top 50) | 5 | Y | 1 |
| Standing beat only | KodeKloud | not in top 50 | – (n50: 27) | not in top 50 | not in top 50 | N (good) | not in top 50 |
| Trap | Endor Labs | – (n50: 17) | – (n50: 45) | – (n50: 30) | – (n50: 17) | N (good) | – (20) |

| Summary (n=10) | Words | Meaning | ELSER | Blended |
|---|---|---|---|---|
| Assignment companies in the top 10 (3 must-finds + gem, of 4) | 1 (Momentic) | 2 (Faros, mirrord) | 2 (Momentic, mirrord) | **3 (Coder, Momentic, mirrord)** |
| Hidden gem's rank | – (26) | 4 | 2 | 3 |
| Standing-beat-only or trap above an assignment company? | no | no | no | no |
| Pass | – | – | – | **Fail: Faros 13th** (gem 3rd, KodeKloud and Endor Labs well below) |

Came up in the top 10, not expected: **ELSER:** Syntasso (Silver) 4, Chainguard (Platinum) 5, ControlTheory (Gold)
6, Temporal (Gold) 7, Traversal (Platinum) 8, ActiveState (Silver) 9, Testkube (Start-Up) 10. **Blended:**
ControlTheory 2, Syntasso 6, Temporal 7, Sentry 9, Resolve AI 10. (Words and meaning unexpected lists are
unchanged from the second set.) The blended top ten is now: Docker, ControlTheory, mirrord, Momentic, JetBrains,
Syntasso, Temporal, Coder, Sentry, Resolve AI. Paper Compute Company (Start-Up), 5th in the second set's
blended, has left the top ten.

## The Breach Chronicle — still FAIL: no must-find, no gem in the blended top 10; ELSER adds Akamai at 9th

| Group | Company | Words | Meaning | ELSER | Blended | In blended top 10 | 2nd set blended |
|---|---|---|---|---|---|---|---|
| Must find: helps security teams | Maze (Start-Up) | not in top 50 | 4 | – (n50: 30) | – (n50: 23) | N | – (26) |
| Must find: helps security teams | Emphere (Start-Up) | not in top 50 | not in top 50 | not in top 50 | not in top 50 | N | not in top 50 |
| Must find: helps security teams | Endor Labs | not in top 50 | – (n50: 43) | not in top 50 | **not in top 50** | N | – (27) |
| Must find: keeping agents safe | Edera | not in top 50 | not in top 50 | – (n50: 40) | not in top 50 | N | not in top 50 |
| Must find: keeping agents safe | Cosmonic | not in top 50 | – (n50: 36) | not in top 50 | not in top 50 | N | not in top 50 |
| Must find: keeping agents safe | Teleport | not in top 50 | not in top 50 | not in top 50 | not in top 50 | N | not in top 50 |
| Must find: keeping agents safe | Archestra AI (Start-Up) | not in top 50 | not in top 50 | not in top 50 | **not in top 50** | N | – (49) |
| **Hidden gem** | **Vijil (Start-Up)** | not in top 50 | – (n50: 23) | not in top 50 | not in top 50 | **N** | not in top 50 |
| Standing beat only | Akamai | not in top 50 | – (n50: 40) | **9** | – (n50: 31) | N | not in top 50 |
| Standing beat only | RapidFort, Echo | not in top 50 | not in top 50 | not in top 50 | not in top 50 | N (good) | not in top 50 |
| Partial word trap | Orca Security | not in top 50 | not in top 50 | not in top 50 | not in top 50 | N | not in top 50 |

| Summary (n=10) | Words | Meaning | ELSER | Blended |
|---|---|---|---|---|
| Assignment companies in the top 10 (7 must-finds + gem, of 8) | 0 | 1 (Maze 4th) | **0** | 0 |
| "Helps security teams" half found in top 10 (of 3) | 0 | 1 | 0 | 0 |
| "Keeping agents safe" half found in top 10 (of 4) | 0 | 0 | 0 | 0 |
| Hidden gem's rank | not in top 50 | 23 | not in top 50 | not in top 50 |
| Standing-beat-only above an assignment company? | none present | Akamai (40) above Endor Labs (43) | **Akamai 9th, with no assignment company in ELSER's top 10; above every must-find** | Akamai (31) is below Maze (23), above every other must-find (none in the top 50) |
| Pass | – | – | – | **Fail** |

**Where each Breach Chronicle must-find lands by ELSER at n=50:** Maze 30th; Edera 40th; Emphere, Endor Labs,
Cosmonic, Teleport, Archestra AI: not in ELSER's top 50. Vijil (gem): not in ELSER's top 50. (Meaning, for
comparison: Maze 4, Cosmonic 36, Endor Labs 43, Vijil 23. Blended at n=50: Maze 23rd, and **Endor Labs and
Archestra AI have fallen out of the top 50**, where the second set had them at 27th and 49th.)

Came up in the top 10, not expected: **ELSER:** Sysdig (Gold) 1, Palo Alto Networks (Gold) 2, Plural (Silver) 3,
Kubex (Silver) 4, Twingate (Silver) 5, Resolve AI (Gold) 6, Tigera (Gold) 7, Chainguard (Platinum) 8,
Temporal (Gold) 10 (and Akamai 9, a beat-only company). **Blended:** Sysdig 1, Plural 2, Resolve AI 3, Jozu 4,
Kubex 5, Radar (Start-Up) 6, Docker 7, Nirmata 8, Twingate 9, Edge Delta 10. Words: Sysdig (Gold) 1, PagerDuty
2, Wiz (Gold) 3, Northflank 4, Uber 5, Linux Foundation Education 6, Jozu 7, Tigris Data 8, VAST Data 9, Docker
10. All ordinary security, observability or platform companies; I read the passages' first lines only.

## What the third set shows, in one place

- **Gazette:** ELSER helps. Momentic goes from 8th to 4th in blended, mirrord from 4th to 3rd, Docker to 1st;
  Coder 9th to 8th. Faros slipped from 11th to 13th, so the Gazette still misses the pass by the one company.
- **Breach Chronicle:** ELSER does not find the assignment: no must-find in its top ten, Maze only 30th, and it
  puts Akamai (a company the key says should rank lower) 9th. In blended, Maze improves (26th to 23rd) but
  Endor Labs and Archestra AI drop out of the top 50, so on the key's own test (all must-finds in the top 10,
  the gem in the top 10) the Breach Chronicle is no nearer than before.

---

# Read-only look (12:20): the Breach Chronicle's wording against its must-finds' own text

Read from `data/outlets.csv` (The Breach Chronicle row) and `data/sponsors.csv` (the eight must-finds as the
answer key names them). No searches run, nothing changed, and nothing suggested for the answer key. Word
counts below are my own counts over every text column of the sponsor's row (so "agent" includes "agents"),
done once; they show which words are present, not how a search weighs them.

**What the outlet says.** Beat: "Security breaches as they happen; How attackers got in; What companies and
security teams did in response; The threats security teams are dealing with right now." What they cover:
"News about security breaches as they happen: who was hit, how it happened, and what is being done about it."
Audience: "People who work in cybersecurity". Assignment: "how AI agents are being built, either to help
people working in cybersecurity, or to keep AI agents themselves safe inside the companies using them."
Its own words are about attacks and response: breach, attackers, threats, response, cybersecurity, security
teams; and, in the assignment, AI agents, help, safe, inside the companies using them.

**What each must-find's own text is about**
- **Maze (Start-Up), helps security teams:** AI agents that investigate vulnerabilities, work out which are
  really exploitable (it says 90% are not), and send a fix to the developer. Words: vulnerabilit- (11),
  exploit- (6), CVE (3), security (5), agent (7).
- **Emphere (Start-Up), helps security teams:** AI agents that patch every known vulnerability in container
  images, with signed, tested images and proof. Words: vulnerabilit- (4), CVE (2), container, SLSA, compliance.
- **Endor Labs, helps security teams:** an application-security platform; AI agents find, prioritize and fix
  vulnerabilities in code and packages, and it also checks coding agents' actions against policy. Words:
  security (5), agent (7), vulnerabilit- (5), policy, SLSA, FedRAMP.
- **Edera, keeps agents safe:** a hypervisor that runs each container or AI agent in its own isolated zone so
  one compromised workload cannot reach the others. Topic "Platform Engineering". Words: isolat- (4),
  agent (2), attacker (1), safe (1), security (1).
- **Cosmonic, keeps agents safe:** a WebAssembly sandbox for each AI agent or tool, with no access except
  what is granted; limits what a prompt injection can do. Topic "Artificial Intelligence". Words: sandbox (8),
  agent (8), safe (1); **"security" does not appear in its text.**
- **Teleport, keeps agents safe:** identity and access: cryptographic identities and short-lived access for
  people, machines and AI agents, instead of passwords and standing access. Topics "Platform Engineering;
  Security". Words: identity (12), access (11), attack (3), security (3), agent (3).
- **Archestra AI (Start-Up), keeps agents safe:** open-source gateway that controls which data, tools and
  actions a company's AI agents can reach, with audit and spending budgets. No conference topic. Words: agent
  (6), MCP, access, policy, identity, audit; **"security" does not appear in its text.**
- **Vijil (Start-Up, the gem), keeps agents safe in the wider sense:** finds, tests, guards and monitors a
  company's agents and gives a trust score and audit evidence. Topic "Artificial Intelligence". Words: agent
  (23), trust (2), audit, govern, prompt injection (2), security (3).

**Where the outlet's wording points somewhere else**
1. **The outlet's own news-and-attack words are in none of the eight.** "Breach", "cybersecurity", "threat",
   "incident" and "response/respond" appear in none of the eight texts (all zero). "Attacker" is in one
   (Edera) and "attack" in two more (Teleport, three times; Edera once). The beat, which is the part that is
   all about breaches and response, therefore has almost nothing to hold on to in these companies.
2. **What the eight share is vocabulary the outlet never uses.** The three that help security teams talk in
   vulnerabilities, CVEs, exploitability, patches and fixes (the outlet never says "vulnerability", "fix" or
   "patch"). The five that keep agents safe talk in isolation, sandboxes, identity, access, policy, audit,
   trust and governance (the outlet says only "safe" and "inside the companies using them").
3. **The word "agents" is the main thing in common**, and the outlet says it once. Counts of "agent" in the
   eight: Vijil 23, Cosmonic 8, Maze 7, Endor Labs 7, Archestra 6, Teleport 3, Edera 2, Emphere 2.
4. **Two of the eight never use "security" at all** (Cosmonic and Archestra AI), and two more are filed under
   "Artificial Intelligence" (Cosmonic, Vijil) or "Platform Engineering" (Edera) rather than "Security". An
   outlet worded around cybersecurity does not meet them on that word.
5. **Companies that do use the outlet's words are the ones ranking above them.** For comparison, counts in
   those companies' own text: Sysdig ("detect and respond to attacks": attack 5, threat 2, respond 3,
   security 11, agent 10), PagerDuty (incident 7), Resolve AI (incident 6), Palo Alto Networks
   ("cybersecurity company", incident 3), Akamai ("cybersecurity", 2). Those are detection, response and
   incident companies; their text matches the beat's breach-and-response language more directly than the
   eight's matches the assignment's "agents" language.
6. **The outlet's two halves are worded at different levels.** "Help people working in cybersecurity" reads
   as the job of the security team, and the three that fit it describe it in vulnerability terms; "keep AI
   agents themselves safe inside the companies" reads as a trust or security idea, and the five that fit it
   describe mechanisms (isolation, sandbox, identity, gateway, testing). The outlet states neither the
   problems nor the mechanisms.

---

# Read-only look (12:25): the Hello World Gazette's wording against Faros, KodeKloud and Endor Labs

Asked in place of the Breach Chronicle look above (which stays). Read from `data/outlets.csv` (the Gazette row)
and `data/sponsors.csv`. No searches run now; the ranks are from the third column set (12:13, n=50, cloud, with
ELSER). Nothing suggested for the answer key. Word counts are mine, over every text column of the sponsor's
row, done once.

**A note on the three companies.** Only **Faros** is a must-find that misses. In the answer key KodeKloud is
"standing beat only: should rank lower" and Endor Labs is "trap", so for those two a low rank is the outcome
the key expects, not a miss.

**What the outlet says.** Covers: "a newsletter for developers about the new tools coming out for programming:
what has just been released, what is worth trying, and how it changes the way software gets written, tested and
shipped." Beat: "New developer tools and releases; Programming languages and frameworks; How developers write,
test and ship code; Open-source tools developers rely on". Audience: developers who want to stay up to date with
new tools. Assignment: "AI agents built for developers: agents that help you write code."

| Company | Words | Meaning | ELSER | Blended | Landed |
|---|---|---|---|---|---|
| Faros (must-find) | 38 | 7 | 37 | 13 | misses the blended top 10 |
| Endor Labs (trap) | 17 | 45 | 30 | 17 | low, as the key expects |
| KodeKloud (beat only) | not in top 50 | 27 | not in top 50 | not in top 50 | low, as the key expects |

**Faros** (Silver, topic "Artificial Intelligence"): "tracks what an organisation spends on AI coding agents,
links that spend to the work actually shipped, routes tasks to the best-value model, and enforces budgets and
model policies." Its customers are "engineering leaders", "developer enablement teams" and "enterprises", not
individual developers. Its words: token (10), model (6), spend (4), budget (3), productivity (3), coding agent
(3), ship- (3), code (3), agent (6). It has none of the outlet's "write", "test", "release", "language",
"framework", "programming" or "open source", and says "developer" once and "tool" once. **Why it lands low:** it
is about what AI coding agents *cost*, not about helping a developer write code, and its vocabulary is money,
models and governance. **Does the wording point away?** Partly. It shares "AI coding agents", "code" and
"shipped" with the outlet, which is how meaning finds it (7th, from the passage "Wasted spend on retry loops and
agent work that never ships"); it does not share the words, so words (38th) and ELSER (37th) put it low, and
blending averages that into 13th. The outlet's "agents that help you write code" reads as a tool a developer
uses; Faros is a tool a manager uses about those agents.

**KodeKloud** (Silver, topics "Kubernetes Certified Service Providers + Kubernetes Training Partners"): "an
online training platform that teaches DevOps, cloud and AI skills through video courses and hands-on labs",
with certification preparation and an AI playground for comparing models. Its words: learn (5), course (3),
video (2), train (5), lab/certification terms, "language" (1, as in large language models), agent (0), "AI" (4).
**Why it lands low:** it teaches people; it neither releases a tool nor builds an agent. **Does the wording point
away?** Yes on both parts: the outlet never says learning, courses, training or certification, and the
assignment is about agents, which KodeKloud's text never mentions. Its only meeting point is the audience
(developers, DevOps engineers) and the general territory of developer tooling, which is why meaning has it 27th
and the other ways drop it out of the top 50.

**Endor Labs** (Silver, topic "Security"): "an application security platform that uses AI agents to find,
prioritize and fix vulnerabilities in human-written and AI-generated code, open-source dependencies and
container images", and it checks coding agents' actions against policy. Its words: code (13), agent (7),
secur- (6), vulnerab- (5), coding agent (4), open-source (2/1). **Why it lands low:** its subject is security
and compliance; the outlet never says security, vulnerability, risk or compliance. **Does the wording point
away?** Yes on the subject, but not on the vocabulary: it shares "AI coding agents", "code", "agents" and
"open source" with the outlet, so it does not fall far: it is 17th in words and in blended, 30th in ELSER, and
only meaning (45th) puts it near the bottom. In blended it is 17th, four places below Faros (13th) and
seven below the top 10; it is the one of the two trap-like companies that sits closest to the must-finds.

---

# M5 the flip (commit 68c98c7), checked 12:18 to 12:19, cloud

Command: `.venv/bin/python -m ftrt.flip "<sponsor>"` (blended), three runs each at 12:18:15 to :27 (Kedify),
12:18:38 to :49 (Edera) and 12:19:01 to :13 (Docker), then `--mode compare` once each (12:18:33, 12:18:54,
12:19:19). **All three runs agreed exactly for all three sponsors** (same outlets, order and scores, same talks).
Common sense is Aaron's call; this only reports what came out. "Score" is the flip's own blended score. Kedify
and Docker have a "what it is showing at KubeCon" part (counted double); **Edera has none** and is matched
on what it does alone, so its scores sit on a smaller scale (three lists instead of six): compare spreads as a
percentage of the top score, not in raw numbers.

## Kedify (Start-Up)

Outlets, in order: 1 Greenstack 0.1422; 2 LearnKube 0.1398; 3 TFIR 0.1390; 4 Women in Infrastructure 0.1385;
5 The Regulated Cloud 0.1378; 6 SDxCentral 0.1355; 7 The Breach Chronicle 0.1353; 8 Open Source Sustainability
Weekly 0.1350; 9 Hello World Gazette 0.1310; 10 Techstrong 0.1295; 11 Futurum Group 0.1293; 12 The New Stack
0.1276; 13 OpsMatters 0.1274; 14 TechRevolt News 0.1253.
Top three talks (blended): 1 Battle-tested Autoscaling Paradigms with KEDA; 2 SIG Autoscaling Project Updates;
3 Beyond Model Serving: Running Production LLMs on Kubernetes with KServe.
**Spread:** top 0.1422, bottom 0.1253, range 0.0169 (12% of the top); first to second 0.0024; the top five are
within 0.0044.
Compare, top outlets by way: words Greenstack, Women in Infrastructure, SDxCentral, TFIR, Breach Chronicle;
meaning LearnKube, The Regulated Cloud, Greenstack, Open Source Sustainability Weekly, TFIR; ELSER LearnKube,
The Regulated Cloud, TFIR, Women in Infrastructure, Greenstack. Talks top three: words KEDA talk, Beyond the
Cluster Boundary: Sharing GPUs at Scale, KServe; meaning SIG Autoscaling Project Updates, The New Scaling
Matrix: Balancing In-Place Resizing, VPA, HPA and Automation Solutions, Saturated by Design; ELSER KEDA talk,
Demo Theater: Why Your Kubernetes Autoscalers Keep Fighting (and How to End the Thrash), SIG Autoscaling.

## Edera (Silver; no KubeCon part)

Outlets, in order: 1 TFIR 0.0492; 2 Greenstack 0.0471; 3 SDxCentral 0.0464; 4 Techstrong 0.0459; 5 The Regulated
Cloud 0.0457; 6 The Breach Chronicle 0.0457; 7 LearnKube 0.0452; 8 Futurum Group 0.0439; 9 Women in
Infrastructure 0.0437; 10 Hello World Gazette 0.0431; 11 The New Stack 0.0429; 12 OpsMatters 0.0421; 13
TechRevolt News 0.0421; 14 Open Source Sustainability Weekly 0.0413.
Top three talks: 1 Untrusted Code on Secure Runtimes: Agent Sandboxes on Kubernetes; 2 Extending NetworkPolicy to
RDMA: Hardware-Enforced Tenant Isolation for AI Clusters; 3 Securing the Agentic Future: Distributing LLM Weights
and Sandboxed AI Agents via Harbor.
**Spread:** top 0.0492, bottom 0.0413, range 0.0079 (16% of the top); first to second 0.0021; the top five are
within 0.0035; places 5 and 6 are tied at the printed precision (0.0457), as are 12 and 13 (0.0421).
Compare, top outlets by way: words TFIR, Greenstack, Women in Infrastructure, Techstrong, SDxCentral; meaning
TFIR, SDxCentral, The Breach Chronicle, The Regulated Cloud, LearnKube; ELSER TFIR, LearnKube, Greenstack, The
Regulated Cloud, Techstrong. Talks top three: words Demo Theater: Agent Sandbox on EKS: Hardware-Isolated microVM
Pods for AI Agents, the RDMA tenant-isolation talk, Untrusted Code on Secure Runtimes; meaning Demo Theater: Agent
Substrate: Secure, High-Density Sandboxing for AI Agents, Platform-First AI Agent Security: Zero-Trust Patterns
for Kubernetes, the RDMA talk; ELSER Securing the Agentic Future (Harbor), Platform-First AI Agent Security,
Untrusted Code on Secure Runtimes.

## Docker (Platinum)

Outlets, in order: 1 Hello World Gazette 0.1438; 2 The Breach Chronicle 0.1422; 3 TFIR 0.1419; 4 Techstrong
0.1368; 5 Women in Infrastructure 0.1351; 6 The New Stack 0.1344; 7 Greenstack 0.1330; 8 Open Source
Sustainability Weekly 0.1329; 9 LearnKube 0.1318; 10 OpsMatters 0.1280; 11 The Regulated Cloud 0.1076;
12 SDxCentral 0.0997; 13 Futurum Group 0.0997; 14 TechRevolt News 0.0961.
Top three talks: 1 Demo Theater: From YOLO to Golden Paths: Building Trusted Environments for AI Agents; 2 Untrusted
Code on Secure Runtimes: Agent Sandboxes on Kubernetes; 3 Securing the Agentic Future: Distributing LLM Weights and
Sandboxed AI Agents via Harbor.
**Spread:** top 0.1438, bottom 0.0961, range 0.0477 (33% of the top). Docker is the one with a real gap: places 1
to 10 are within 0.0158 (0.1438 to 0.1280) and then it falls to 0.1076 at 11th; first to second only 0.0016.
Compare, top outlets by way: words Women in Infrastructure, The New Stack, Hello World Gazette, TFIR, Breach
Chronicle; meaning TFIR, Hello World Gazette, The Breach Chronicle, Techstrong, The Regulated Cloud; ELSER Hello
World Gazette, The Regulated Cloud, The Breach Chronicle, TFIR, Women in Infrastructure. Talks top three: words
the YOLO to Golden Paths talk, Supply Chain Security at Home: From Source to Service Without the Hassle, Demo
Theater: Agent Sandbox on EKS; meaning and blended the YOLO talk, Untrusted Code on Secure Runtimes, Securing the
Agentic Future; ELSER the YOLO talk, Demo Theater: Agent Sandbox on EKS, Demo Theater: The Spin Sandbox.

## Reading the spread

For Kedify and Edera the 14 outlets' scores bunch: the whole list spans 12% (Kedify) and 16% (Edera) of the top
score and the leader's lead over second is 0.0024 and 0.0021, so the order inside the list is decided by very
small differences (Edera has two printed ties). Docker's list has more shape: ten outlets within 0.0158 and then
a drop to the last four. Where the flip is most useful as a ranking, then, is the grouping (which outlets are in
the top handful and which are at the bottom), not the order of neighbors. The outlets each sponsor puts in the
top two or three differ by way (words, meaning and ELSER each lead with different outlets for Kedify and
Docker), and the blended order is a compromise of the three.

---

# M4 the start-ups toggle (commit 9ab6782), checked 12:25 to 12:30 at http://127.0.0.1:8765

**How:** this time the browser pane opened the page (the earlier refusal was for port 5060), so the match,
the plain search and the vendor picker were driven in the real page (clicks on the checkbox, "Go" and
"Search"; the answers read back from what the page itself displayed), with the page's own web requests
(Python) for the extra combinations. The page shows "Start-ups only" as a checkbox under the two door
buttons, with a line "Sponsors: all 226 (32 of them start-ups)".

**Does the count drop and come back exactly?** Yes, with one thing to know about what "count" means.
- **The pool:** the line under the checkbox goes "Sponsors: all 226 (32 of them start-ups)" → "Sponsors: the 32
  start-ups of 226" → back to "all 226 (32 of them start-ups)". The vendor picker goes 226 sponsors → 32
  → 226 (its first line also changes to "Choose one of the start-up sponsors…"). The 226-name list after
  switching off is **identical, name for name and in order,** to the list before. The 32 names with the switch
  on are exactly the 32 rows whose tier is Start-Up in `data/sponsors.csv` (compared as sets: none missing, none extra).
- **The match (Hello World Gazette, picked from the outlet picker, Go):** with the switch off the Sponsors tab
  shows 10 sponsors per way (blended Docker, ControlTheory, mirrord, Momentic, JetBrains, Syntasso, Temporal,
  Coder, Sentry, Resolve AI). Switching it on re-runs the match by itself (no second Go): the tab is renamed
  "Start-up sponsors" and shows 10 per way, all start-ups (blended mirrord by MetalBear, Paper Compute Company,
  pgEdge, Radar, Vijil, CodeVisionary, Testkube, Maze, StackGuardian, PatapscoAI). **Each shown start-up carries
  a "Start-Up" tag. Talks and speakers are identical to the switch-off lists in all four ways.** Switching off
  again: all four ways' lists (sponsors, talks, speakers) are **identical to the first switch-off lists**
  (compared programmatically across Blended, Meaning, Words, Elastic ELSER). Because each list is capped at 10, the
  sponsor *count* stays 10 before and after; what changes is who is in it, plus the pool line and the picker above.
- **The plain search, "scale up for a traffic spike and back down afterwards" (Everything, Blended):** off: 10
  results, nine talks and one sponsor (Kedify); on: 10 results, **all sponsors, all start-ups** (Kedify,
  Ascendra Networks, Cloudchipr, pgEdge, KubeDB, Causal Dynamics Lab, mirrord, Actualyze AI, Radar,
  CodeVisionary); off again: **identical to the first off list**.
- **Every sponsor shown with start-ups on is Start-Up tier in `sponsors.csv`:** checked for the four match
  ways (40 sponsor rows), the plain search (10), and the picker (32): zero non-start-ups. By request, for the plain
  search in blended, meaning and ELSER, with Everything, Sponsors or Talks chosen, on and off: every on-list was all
  Start-Up (none outside it), and off-on-off gave the same off list each time.

**Things to know (not failures of the check):**
1. **With the switch on, "Talks" in the plain search returns start-up sponsors, not talks.** `kind=talk` plus the
   switch on gave 10 sponsors (blended, meaning and ELSER), because only sponsors have a tier (the code says
   so). A viewer who picks "Talks" and turns the switch on sees sponsors under that choice.
2. **Words search for that sentence finds nothing** (0 results, switch on or off, any kind), as before.
3. **Speed:** a match, and each re-run when the switch is flipped, took roughly 8 to 10 seconds in the page
   (the button shows "Matching…"), where the match took about 1 second in the page check at 11:55 (before ELSER). A
   curl of `/api/match` took 7.6 seconds at 12:27. Not investigated; Titan may have load running at the same time.
4. The page's way-buttons include a fifth, "Re-ranked", in its markup. Clicking it by script gave no result list
   (one empty row per tab), and the screenshot afterwards showed only Blended, Meaning, Words and Elastic ELSER, so
   it appears to be hidden until used. I did not test it.

---

# Titan's speed and Talks-tab fixes (commit c4a8ae8), checked 12:34 to 12:39 (machine clock) in the real browser at http://127.0.0.1:8765

Driven in the in-app browser pane. Times are taken in the page itself (from the click until the page's
button is back to "Go" or "Search"; the request's own time is in brackets), cloud engine, three runs each.
The page times a whole request including the server's work for the match; other sessions may have been using
the engine at the same moment.

| Action | Run 1 | Run 2 | Run 3 | Before (12:25) |
|---|---|---|---|---|
| Gazette, pick it and press Go | 2.71 s (request 2.69) | 2.48 s (2.46) | 2.69 s (2.67) | about 8 to 10 s |
| Start-ups toggle ON, match re-runs by itself | 2.09 s (2.08) | 1.93 s (1.92) | 2.26 s (2.25) | about 8 to 10 s |
| Start-ups toggle off, match re-runs | 2.46 s (2.45) | 2.35 s (2.33) | 2.74 s (2.71) | about 8 to 10 s |
| Flip, Kedify, vendor door, Go | 1.87 s (1.84) | 1.66 s (1.64) | 1.52 s (1.50) | not timed in the page |
| Plain search, Re-ranked way, "scale up for a traffic spike and back down afterwards" | 1.21 s (1.21) | 1.33 s (1.31) | 1.13 s (1.11) | not timed |

**Speed: fixed.** All of them are between 1.1 and 2.8 seconds, and the three runs of each are within half a
second of each other. Page-load to ready was not timed.

**The Gazette's blended top ten (sponsors) is unchanged from the third column set.** On the page after each of
the three Go runs: Docker, ControlTheory, mirrord by MetalBear, Momentic, JetBrains, Syntasso, Temporal,
Coder, Sentry, Resolve AI: the same ten, in the same order, as the third set (12:13, 2e26f1b). Switching
start-ups off gave that same list again after each of the three ON/off pairs; with it ON the list was the same
ten start-ups all three times (mirrord, Paper Compute Company, pgEdge, Radar, Vijil, CodeVisionary, Testkube,
Maze, StackGuardian, PatapscoAI), the tab named "Start-up sponsors".

**Flip (Kedify), on the page:** title "Outlets and talks for Kedify, on what it does and what it is showing at
KubeCon (counting double)"; two tabs, "Outlets" (14) and "Talks"; first five outlets Greenstack, LearnKube,
TFIR, Women in Infrastructure, The Regulated Cloud, identical in the three runs and equal to the Terminal
flip's first five (12:18). No error shown.

**Re-ranked plain search** (way button "Re-ranked" pressed, then Search): 10 results, same in the three runs:
Kedify, Green Dashboards Broken Clusters: Taming Stale Watches in Kubernetes Operators, ScaleOps, In-Place Pod
Resizing Like I'm 5: Scaling Without Restarts, Autoscaling Reality Check: The Hands-On HTTP Optimization
Challenge, Battle-tested Autoscaling Paradigms with KEDA, and four more. No "re-ranker did not answer" note.

**With start-ups on, the plain search can no longer show sponsors under "Talks": confirmed in the page.**
Choosing Talks, then switching the toggle on, sets the "Among" box to "Sponsors", grays it out (tooltip
"Start-ups only: sponsors"), so "Talks" cannot be chosen while the toggle is on; switching off un-grays it
and puts "Talks" back (the page remembers the previous choice). **The server itself has not changed:** a
direct request with the toggle flagged on and `kind` talk, speaker or event still returns 10 sponsors (in blended,
meaning, ELSER and re-ranked; words returns none), so the fix is in the page, not in the engine's answer.
Anyone using the page cannot reach it; a direct web request still can.

Note: an earlier measuring script of mine kept running in the page after the tool timed out and made
the first attempt's states confusing; I reloaded the page and re-ran everything cleanly. The numbers above are
from the clean run.

---

# On-screen engine line and "Compare all" (commit acdd654), checked 12:36 to 12:41 (machine clock), real browser at http://127.0.0.1:8765

**The page says on screen that it uses Elastic Cloud: yes.** A small label at the top right of the page, beside
the title, reads "Elastic Cloud serverless, with Elastic's ELSER" (seen in a screenshot, visible and not hidden;
it first reads "connecting…" for a moment while the page loads its lists). When the engine is the laptop it
would read "Elasticsearch on this laptop" (from the page's code).

**Compare all** is a sixth button after the way buttons (Blended, Meaning, Words, Elastic ELSER, Re-ranked,
Compare all) in both the match panel and the plain search. It shows five columns side by side: Words, Meaning,
Elastic ELSER, Blended, Re-ranked. Each name that appears in more than one column carries an "in N" badge (N =
how many of the five columns it is in); sponsors that are Start-Up carry a "Start-Up" tag; hovering shows the
passage. Everything below was read back from what the page itself drew, three runs each unless noted.

## Plain search, the GPU sentence, "Among: Sponsors", Compare all (runs at 12:36, three)

Time from click to Search button back: **1.54 s, 1.73 s, 1.17 s** (one request each, 1.53 / 1.83 / 1.26 s).
Identical columns and badges in all three runs. Counts: Words 1, Meaning 10, Elastic ELSER 10, Blended 10,
Re-ranked 10. Top three of each column (with the badge the page showed):
- Words: Edera (in 5)
- Meaning: vCluster (in 4), Edera (in 5), Rafay Systems (in 4)
- Elastic ELSER: Edera (in 5), vCluster (in 4), Cast AI (in 4)
- Blended: Edera (in 5), vCluster (in 4), Cast AI (in 4)
- Re-ranked: vCluster (in 4), Edera (in 5), AEnix (in 4)

## Match, Hello World Gazette (the demo outlet), Compare all (three runs); and the Breach Chronicle (once)

Time for the match request to come back (Go): Gazette **3.15 s, 2.45 s, 2.46 s** (the match itself; the page
then draws Compare all by itself in about 50 to 57 ms since it uses the answer already fetched); Breach
Chronicle **2.64 s**. Identical columns and badges in all three Gazette runs. Each column has 10 sponsors, 10
talks and 10 speakers.

**Gazette, sponsors, top three of each column:**
- Words: JetBrains (in 3), Temporal (in 4), Docker (in 4)
- Meaning: Komodor, Paper Compute Company [Start-Up], JetBrains (in 3)
- Elastic ELSER: Docker (in 4), mirrord by MetalBear [Start-Up] (in 4), Momentic (in 4)
- Blended: Docker (in 4), ControlTheory (in 4), mirrord by MetalBear [Start-Up] (in 4)
- Re-ranked: mirrord by MetalBear [Start-Up] (in 4), Docker (in 4), Diagrid

**Gazette, talks, top one of each (the page shows more; first only here):** Words MCP Was the Easy Half, The Rest
Was a Skill Issue (in 2); Meaning, ELSER and Blended all From Platform Catalog to Conversational Agent: Wiring AI
Into Your Internal Developer Platform (in 4); Re-ranked Demo Theater: From YOLO to Golden Paths: Building Trusted
Environments for AI Agents (in 2). **Speakers:** Words Stefan Prodan (in 3); Meaning Mike Swift; ELSER, Blended
and Re-ranked all Mofi Rahman (in 4).

**Breach Chronicle, sponsors, top three of each column (one run):**
- Words: Sysdig (in 5), PagerDuty (in 2), Wiz
- Meaning: Resolve AI (in 4), Twingate (in 4), Sysdig (in 5)
- Elastic ELSER: Sysdig (in 5), Palo Alto Networks, Plural (in 4)
- Blended: Sysdig (in 5), Plural (in 4), Resolve AI (in 4)
- Re-ranked: Plural (in 4), Sysdig (in 5), Resolve AI (in 4)
Maze is the only gem-tagged start-up outside the beat companies shown (with Radar); no must-find is in a top three.

**Are the "in N" badges and Start-Up tags right? Yes.**
- **Badges:** I recomputed N for every name in every column from the page's own columns (how many of the five
  columns it is in) and compared with the badge shown: **zero mismatches** across the three GPU runs, the three
  Gazette runs (sponsors, talks and speakers tabs) and the Breach run. A name in one column only has no badge.
- **Against the separate views:** for each way, the Compare all column is **name-for-name and in order the same
  list** as the separate view of that way (GPU search: Words 1, the other four 10; Gazette sponsors: all five
  ways 10; Breach sponsors: all five ways 10). No tag differs between a column and its separate view.
- **Start-Up tags against `data/sponsors.csv`:** every sponsor shown in the compare columns was checked
  (GPU 15 different sponsors, Gazette 28, Breach 26): the tag appears on exactly the Start-Up tier ones and on
  no others (GPU: Aranya; Gazette: Paper Compute Company, mirrord by MetalBear, PatapscoAI, Vijil, Testkube;
  Breach: Maze, Radar). None missing, none wrongly tagged.

**Not checked:** how the columns look at phone width or with the longest names (the grid is code-defined to wrap);
the hover passages; Compare all with start-ups only switched on; talks and speakers tabs beyond the badge
check and each column's first entry.

---

# The Agent Builder agent (commit 44b827a): one question, 12:53 (machine clock) — REFUSED, nothing checked

Asked exactly one question, at 12:53:23, after waiting until 12:53 as told:
`.venv/bin/python -m ftrt.agent ask "Which sponsors and talks at KubeCon fit the Hello World Gazette?"`
(the question in the commit message of 44b827a). **The agent did not answer: HTTP 429, "Too Many Requests",
from Elastic's hosted language model: "You have reached your trial limit for this model ... or wait 8m44s for
your trial quota to be refilled."** The refusal came back after 30 seconds. As instructed I did not retry, so:
no answer, no list of companies, no quotations, no closing line to check, and no time for an answer to
report. The quota should refill at about 13:02 (12:53:53 plus 8m44s, machine clock), if the earlier use was the cause.
The checker for the answer (every company named is a sponsor in `data/sponsors.csv`, every quotation found
word for word in the program text, the closing line exactly as the agent's instructions require) is ready and
unused. What I have of the agent's earlier answer (12:42 to 12:45, 41 s, in the commit message of 44b827a)
is the other session's report, not my measurement, and I did not repeat it.

## The Agent Builder agent, second try at 13:06 (machine clock): REFUSED again

Waited until 13:06 (13 minutes after the first refusal), then asked the same one question at 13:06:08.
**Refused after 32 seconds with the same HTTP 429 from Elastic's hosted model, this time: "wait 6m7s for your
trial quota to be refilled."** (First refusal, 12:53:53: wait 8m44s.) Not retried, as instructed: nothing to
check, no answer time. What the two refusals show: the quota had not refilled after 13 minutes, and each
refused request ran for about 30 seconds before the refusal came back, which suggests the agent had already
used the model (reading the outlet, searching) before the limit stopped it; I cannot see inside to confirm.
The wait it quoted shortened from 8m44s to 6m7s over 13 minutes, so the trial quota behaves as a longer
rolling allowance, not one question every 7 minutes. Next possible time on its own figure: about 13:12:45 on
this clock (13:06:40 plus 6m7s), with no guarantee.

---

# The Agent Builder agent, read back from its saved conversation (13:08, machine clock). No model call made.

Read only: listed the project's saved agent conversations (`GET /api/agent_builder/conversations`: six, of which
five are the project's agent; the other belongs to Elastic's built-in agent and I did not open it) and read the one
titled "KubeCon Sponsors and Talks for Hello World Gazette", created 12:42:46 local (19:42:46 UTC), the one
asked 12:42. My own two refused questions (12:53, 13:06) are listed as conversations too; I read none of them.
Nothing created, changed or deleted. (An 'ask' by me at 12:53:23 and 13:06:08 created those two empty records.)

**What was asked:** "Which sponsors and talks at KubeCon fit the Hello World Gazette?" Status completed.
**Time and cost, as the record states:** started 12:42:49.659; first words after 11.6 s; finished after 33.7 s
(the 41 s Titan reported includes starting and printing); 4 calls to the language model (Anthropic Claude
Sonnet 4.5 on Elastic's hosted service), 41,917 input tokens, 1,282 output tokens.
**Tool calls it made (3, in order):** `ftrt.outlet_profile` with "Hello World Gazette"; `ftrt.search_program`
with "AI agents built for developers that help you write code" (kind any, start-ups only false);
`ftrt.search_program` with "new developer tools programming languages frameworks how developers write test
and ship code" (kind any, start-ups only false). No other tool, and none outside the project's three.

**Companies named, against `data/sponsors.csv`:** five sponsors, all in the file, with the tier the answer gave:
Coder (Silver), Dash0 (Platinum), Momentic (Silver), mirrord by MetalBear (Start-Up), Docker (Platinum). (My
checker also counted "Elastic" as a sponsor name: that is the closing line's "Elastic Agent Builder", not a pick.)
**Talks named, against `data/sessions.csv`:** five, all exist, and the day and time the answer gave match the file
for the three it dated: "What monday.com's 500+ Engineers and AI Agents Have in Common" (Thursday 12 November,
11:00–11:30), "Demo Theater: From YOLO to Golden Paths..." (Thursday 12 November, 11:00–11:20), "Demo Theater:
Agent Sandbox on EKS..." (Wednesday 11 November, 11:25–11:45); the other two ("Agents Fail. Workflows Recover.",
"From Platform Catalog to Conversational Agent") carry no date in the answer. No speaker named.
**Quotations:** 19 quoted pieces (sponsor passages, talk descriptions and talk titles): **all 19 found word
for word, character for character (whitespace aside), in the program's own CSV text.** None failed even the
looser punctuation-free test. The agent used "…" nowhere inside a quotation.
**The closing line:** the answer's last line is exactly "AI-written by the Find the Right Talk agent (Elastic
Agent Builder). Check each quoted passage before you rely on it." (checked against the instruction text).

**Against the project's own answer key for this outlet (`notes/answer-keys.md`):** of the five sponsors the agent
named, four are on the key (Coder and Momentic, two of the three must-finds; mirrord by MetalBear, the hidden gem;
Docker, a "should also do well"); Dash0 is not on the key. It did not name Faros (the third must-find) or JetBrains.
It did not name KodeKloud or Endor Labs.

**Flaws to know about (not failures of the checks):**
1. The answer opens with narration before the answer: "Perfect! I now have comprehensive results. Let me provide
   the Hello World Gazette with the top sponsors and talks ...". On screen or in a recording that line shows.
2. The instructions say "up to five picks"; it gave five sponsors and five talks (ten picks in two lists).
3. Its one-line reasons are the model's own words (for example "Perfect match for the assignment", "Novel
   approach to letting AI agents test against real environments") and are not checked against anything: only the
   quotations were.

---

# "Before Breach/Jina reload" set: baseline on 44b75dc, cloud, 13:28 to 13:30 (machine clock)

Three runs of each, all identical (names, order and scores). Agent not asked anything. Sponsors only. Five ways now:
words, meaning, ELSER, blended, re-ranked (Elastic's hosted re-ranker over the blended top 20). At n=10 and n=50 the
first ten are identical in every way for both outlets (compared by program), re-ranked included.
**Compared with the third set (2e26f1b, 12:13): words, meaning, ELSER and blended are identical for both outlets;
only re-ranked is new.**

## The three demo searches (compare, sponsors, three runs: 13:28:48 to :59, 13:29:06 to :17, 13:29:23 to :34)

| Search | Words | Meaning | ELSER | Blended | Re-ranked |
|---|---|---|---|---|---|
| "SLSA Level 3" | ActiveState 12.92, Docker 10.08 | OpenSSF, HeroDevs, Akeyless Security, AEnix, Nebius | ActiveState, OpenSSF, Emphere (Start-Up), Docker, Chainguard | ActiveState 0.0442, Docker 0.0400, OpenSSF, HeroDevs, Nebius | ActiveState, Docker, OpenSSF (three only) |
| "scale up for a traffic spike and back down afterwards" | nothing | Kedify (Start-Up), ScaleOps, DataAgent, Better Stack, Ascendra Networks | Kedify, PlanetScale, DevZero, ScaleOps, Zesty | Kedify, ScaleOps, Ascendra Networks, Zesty, DevZero | Kedify, Zesty (two only) |
| GPU sentence | Edera | vCluster, Edera, Rafay Systems, AEnix, Cast AI | Edera, vCluster, Cast AI, AEnix, Runpod | Edera 0.0489, vCluster, Cast AI, AEnix, Rafay Systems | vCluster 0.4794, Edera, AEnix (three only) |

Changes since the "after" check (11:48, 174effd): the SLSA tie is gone in blended (ActiveState 0.0442, Docker
0.0400, OpenSSF 0.0325: ActiveState first on a clear margin); in the traffic-spike search Kedify is still first
everywhere it appears (pgEdge and Better Stack no longer both in the blended top five); GPU blended still Edera first.
The re-ranked column lists only the sponsors among the blended top 20 it re-ordered, which is why it has two or three.

## Hello World Gazette (n=10 and n=50; runs at 13:29:44, :47, :50; n=50 at 13:29:52)

| Company | Words | Meaning | ELSER | Blended | Re-ranked |
|---|---|---|---|---|---|
| Coder (must) | – (n50: 29) | – (11) | – (13) | **8** | – (12) |
| Momentic (must) | 8 | – (21) | 3 | **4** | 6 |
| Faros (must) | – (38) | 7 | – (37) | – (13) | – (not in the 48 shown) |
| mirrord by MetalBear (gem) | – (26) | 4 | 2 | **3** | 1 |
| Docker (also) | 3 | – (14) | 1 | 1 | 2 |
| JetBrains (also) | 1 | 3 | not in top 50 | 5 | – (13) |
| KodeKloud (beat only) | not in top 50 | – (27) | not in top 50 | not in top 50 | not in top 50 |
| Endor Labs (trap) | – (17) | – (45) | – (30) | – (17) | not in top 50 |

Assignment companies (3 must + gem) in the top 10: words 1, meaning 2, ELSER 2, **blended 3**, re-ranked 2 (mirrord, Momentic).
Blended top ten: Docker, ControlTheory, mirrord by MetalBear, Momentic, JetBrains, Syntasso, Temporal, Coder,
Sentry, Resolve AI (as in the third set). Key's pass test (all three must-finds in the blended top 10): **fails,
Faros 13th**. Re-ranked top ten: mirrord, Docker, Diagrid, Temporal, Tigera, Momentic, Cosmonic, Resolve AI, Sentry,
Depot: the gem and Docker rise to 1 and 2, Coder and Faros leave the top 10.

## The Breach Chronicle (n=10 and n=50; runs at 13:29:54, :57, :59; n=50 at 13:30:01)

No must-find and no gem in the top 10 of any way except Maze 4th by meaning. Ranks at n=50 of each must-find:

| Company | Words | Meaning | ELSER | Blended | Re-ranked |
|---|---|---|---|---|---|
| Maze (Start-Up, must) | not in top 50 | 4 | 30 | 23 | 23 |
| Emphere (must) | not in top 50 | not in top 50 | not in top 50 | not in top 50 | not in top 50 |
| Endor Labs (must) | not in top 50 | 43 | not in top 50 | not in top 50 | not in top 50 |
| Edera (must) | not in top 50 | not in top 50 | 40 | not in top 50 | not in top 50 |
| Cosmonic (must) | not in top 50 | 36 | not in top 50 | not in top 50 | not in top 50 |
| Teleport (must) | not in top 50 | not in top 50 | not in top 50 | not in top 50 | not in top 50 |
| Archestra AI (must) | not in top 50 | not in top 50 | not in top 50 | not in top 50 | not in top 50 |
| Vijil (gem, Start-Up) | not in top 50 | 23 | not in top 50 | not in top 50 | not in top 50 |
| Akamai (beat only) | not in top 50 | 40 | **9** | 31 | 31 |
| RapidFort, Echo, Orca Security | not in top 50 | not in top 50 | not in top 50 | not in top 50 | not in top 50 |

Top ten, blended: Sysdig, Plural, Resolve AI, Jozu, Kubex, Radar (Start-Up), Docker, Nirmata, Twingate, Edge Delta;
re-ranked: Plural, Sysdig, Resolve AI, Twingate, Tigera, Jozu, PagerDuty, Docker, Edge Delta, Radar; ELSER: Sysdig, Palo Alto
Networks, Plural, Kubex, Twingate, Resolve AI, Tigera, Chainguard, Akamai, Temporal. (The re-ranked list at n=50 holds
40 sponsors, Maze and Akamai at the same places and scores as in blended.) Pass test: **fails, none of the 7 must-finds
or the gem in any way's top 10 except Maze 4th by meaning.**

---

# The Agent Builder agent, third try at 13:38 (machine clock), after the default model was reported switched: REFUSED, still the Anthropic model

Asked the same one question at 13:38:46: `ftrt.agent ask "Which sponsors and talks at KubeCon fit the Hello World Gazette?"`.
**Refused after 43 seconds. Exact message: "The agent did not answer: 429 ... Received a rate limit status code for
request from inference entity id [.anthropic-claude-4.5-sonnet-chat_completion] status [429]. Error message: [You
have reached your trial limit for this model. Upgrade to continue building and enable full production capacity or
wait 3m36s for your trial quota to be refilled. Visit ela.st/upgrade-now to learn more on how to upgrade.]"** Not retried.

**Which model answered: the Anthropic one, not gpt-4.1.** The refusal names the inference entity
`.anthropic-claude-4.5-sonnet-chat_completion`, and the saved conversation record of this attempt (read back, no
model call) says the same: connector `.anthropic-claude-4.5-sonnet-chat_completion`, model anthropic-claude-4.5-sonnet,
3 model calls, 23,792 input tokens and 517 output tokens, round "completed" but with an empty response
message; its steps: the outlet's profile, then two searches whose parameters the record shows as empty. The agent's
own saved definition has no model field (only instructions, tools, capabilities), so it uses whatever the project's
default connector is when it runs; at 13:38:46 that was still the Anthropic one. The earlier refusals: 12:53:53 (wait
8m44s), 13:06:40 (wait 6m7s); this one at 13:39:29 (wait 3m36s).
Nothing to check: no answer, no companies, quotations or closing line. The checked answer remains the 12:42 one.

---

# "After Breach/Jina reload" set: 809ca91, cloud reloaded 13:35 to 13:37, measured 13:45 to 13:48 (machine clock)

Six ways now: words, meaning, ELSER, **Jina** (a further embedding model, one more voice), blended, re-ranked. Sponsors only.
The commit message says the Breach Chronicle split was "tried and dropped", so the Breach outlet is still matched on its beat and
its one assignment. Agent not asked anything.

**A new fact: the match is no longer exactly repeatable run to run.** Words, meaning and ELSER were identical in every
run. The Jina list is not: its *names and order* were identical in all runs but its scores shifted in the fourth decimal
in some runs (for example Endor Labs 0.0393 in two runs and 0.0390 in the third). Because blending adds scores, that
moves companies that are almost tied. Measured: Gazette, n=10, 13 runs in all (3 at 13:46:36 to :41, 10 more at 13:47):
- **Jina top ten names and order: identical in all 13** (scores in two variants).
- **Blended top five: identical in all 13.** Places 1 to 8 identical in all 13; places 9 and 10 flip between two
  versions: "Cosmonic, Syntasso" (about 6 of 10 runs, and runs 1 and 2) and "Syntasso, Dash0" (about 4 of 10 and run 3).
- **Re-ranked:** places 1 to 9 identical in all 13; place 10 flips between ControlTheory and Dash0 the same way
  (6 and 4 of the 10 extra runs), and in run 3 places 3 to 9 had slightly different scores.
Cause not investigated (I do not read or change code).
**n=10 against n=50:** the Gazette's top ten at n=10 equals the first ten of the n=50 run exactly in words, meaning and ELSER in
all three runs, in Jina, blended and re-ranked in runs 1 and 2, but **not in run 3** (blended places 9 and 10, re-ranked
places 3 to 10 differ). So the difference Titan saw is this run-to-run wobble in the Jina voice, not a depth fault: the same
command run twice at the same n=10 gives the two versions. I have not seen it differ for a reason that depends on n.

## The three demo searches (compare, sponsors, three runs each: 13:45:20 to :35, 13:45:42 to :57, 13:46:05 to :21)

All three runs agreed on names and order in every way, every search. Jina scores in the GPU search moved by 0.0001 to
0.0002 between runs (Edera 0.7480, 0.7478, 0.7478) without changing any order.

| Search | Words | Meaning | ELSER | Jina | Blended | Re-ranked |
|---|---|---|---|---|---|---|
| "SLSA Level 3" | ActiveState, Docker | OpenSSF, HeroDevs, Akeyless Security, AEnix, Nebius | ActiveState, Emphere (Start-Up), OpenSSF, Docker, Chainguard | OpenSSF, Sonrai Security, Akeyless Security, Sonatype, Maze (Start-Up) | ActiveState 0.0593, OpenSSF 0.0487, Docker 0.0469, StackGen, Akeyless Security | ActiveState, Docker, OpenSSF, Emphere |
| "scale up for a traffic spike and back down afterwards" | nothing | Kedify (Start-Up), ScaleOps, DataAgent, Better Stack, Ascendra Networks | Kedify, DevZero, PlanetScale, ScaleOps, Zesty | ScaleOps, Tailscale, Kedify, PlanetScale, PerfectScale by DoiT | Kedify 0.0487, ScaleOps 0.0481, Ascendra Networks, DevZero, PlanetScale | Kedify, ScaleOps, Zesty |
| GPU sentence | Edera | vCluster, Edera, Rafay Systems, AEnix, Cast AI | Edera, vCluster, Cast AI, AEnix, Lablup | Edera, vCluster, CoreWeave, Lablup, Cast AI | Edera 0.0653, vCluster, Cast AI, Rafay Systems, Lablup | vCluster, Edera |

Against the 13:29 "before": words and meaning unchanged; ELSER slightly changed (SLSA: Emphere now 2nd, ahead of OpenSSF);
blended: SLSA is now ActiveState, OpenSSF, Docker, StackGen, Akeyless (before: ActiveState, Docker, OpenSSF, HeroDevs, Nebius: Docker
and OpenSSF swapped); traffic spike blended: Kedify, ScaleOps, Ascendra Networks, DevZero, PlanetScale (before ...Zesty, DevZero); GPU
blended: Edera, vCluster, Cast AI, Rafay Systems, Lablup (before ...AEnix, Rafay). The top result of all three is unchanged in blended.
Jina on its own finds ScaleOps (not Kedify) first for the traffic-spike sentence, and OpenSSF first for SLSA.

## Hello World Gazette, sponsors (n=10; runs 13:46:36, :38, :41; n=50 at 13:46:43)

| Company | Words | Meaning | ELSER | Jina | Blended | Re-ranked |
|---|---|---|---|---|---|---|
| Coder (must) | – (29) | – (11) | – (19) | **1** | **5** | – (17) |
| Momentic (must) | 8 | – (21) | **2** | 4 | **3** | 4 |
| Faros (must) | – (38) | 7 | – (39) | – (27) | – (**18**) | not in the 47 shown |
| mirrord by MetalBear (gem) | – (26) | 4 | 3 | 8 | **4** | 2 |
| Docker (also) | 3 | – (14) | 1 | 3 | 1 | 1 |
| JetBrains (also) | 1 | 3 | – (35) | 9 | 2 | 8 |
| KodeKloud (beat only) | not in top 50 | – (27) | not in top 50 | not in top 50 | not in top 50 | not in top 50 |
| Endor Labs (trap) | – (17) | – (45) | – (31) | **6** | – (13) | not in top 50 |

Assignment companies (3 must + gem) in the top 10: words 1, meaning 2, ELSER 2, **Jina 3 (Coder, Momentic, mirrord)**,
**blended 3 (Coder, Momentic, mirrord)**, re-ranked 2. Blended top ten (run 1): Docker, JetBrains, Momentic, mirrord by MetalBear, Coder,
Resolve AI, Sentry, Stacklet, Cosmonic, Syntasso; re-ranked: Docker, mirrord, Temporal, Momentic, Cosmonic, Resolve AI, Sentry, JetBrains,
Syntasso, ControlTheory. Key's pass test (all three must-finds in the blended top 10): **still fails, Faros 18th (was 13th)**; gem 4th
(was 3rd); KodeKloud and Endor Labs not in the top 10 blended (Endor Labs 13th, was 17th), but **Endor Labs, the trap, is 6th in Jina's own list,
above mirrord and JetBrains**. Docker and JetBrains now 1st and 2nd blended; Coder rose from 8th to 5th, Momentic from 4th to 3rd.

## The Breach Chronicle (once: n=10 at 13:47:34, n=50 at 13:47:36)

Still no must-find and no gem in the blended top 10; **Maze is 11th in blended** (was 23rd), the first time any must-find is that close in blended.
Ranks at n=50 of each must-find:

| Company | Words | Meaning | ELSER | Jina | Blended | Re-ranked |
|---|---|---|---|---|---|---|
| Maze (must) | not in top 50 | 4 | 27 | **7** | **11** | not in the 41 shown |
| Emphere (must) | not in top 50 | not in top 50 | not in top 50 | 25 | not in top 50 | not in top 50 |
| Endor Labs (must) | not in top 50 | 43 | not in top 50 | **11** | 28 | 28 |
| Edera (must) | not in top 50 | not in top 50 | 42 | not in top 50 | not in top 50 | not in top 50 |
| Cosmonic (must) | not in top 50 | 36 | not in top 50 | 42 | not in top 50 | not in top 50 |
| Teleport, Archestra AI (must) | not in top 50 | not in top 50 | not in top 50 | not in top 50 | not in top 50 | not in top 50 |
| Vijil (gem) | not in top 50 | 23 | not in top 50 | 32 | 41 | 41 |
| Akamai (beat only) | not in top 50 | 40 | 10 | 18 | 19 | 10 |
| Orca Security (partial) | not in top 50 | not in top 50 | not in top 50 | 36 | not in top 50 | not in top 50 |
| RapidFort, Echo | not in top 50 | not in top 50 | not in top 50 | not in top 50 | not in top 50 | not in top 50 |

Blended top ten: Sysdig, Resolve AI, Jozu, Plural, Edge Delta, Docker, Kubex, Chainguard, Tigera, Wiz. Jina's top ten: Digital.ai, Chainguard,
Jozu, Edge Delta, Docker, Resolve AI, Maze (7th), Sysdig, ActiveState, Tigera. Pass test: **still fails**: 0 of 7 must-finds and not Vijil in the
blended top 10 (Maze 11th, Endor Labs 28th, Vijil 41st). Jina is the first way to put two must-finds (Maze 7th, Endor Labs 11th) near the top.

---

# Page checks refreshed on 904a577 (Dash0 tracing on), real browser at http://127.0.0.1:8765, 14:03 to 14:07 (machine clock)

Agent not asked, catalogs not touched (read-only requests only). Times are click to button-back, cloud.
**Engine label on screen:** "Elastic Cloud serverless, with Elastic's ELSER, Jina embeddings and a re-ranker". Way buttons: Blended, Meaning, Words,
Elastic ELSER, Jina, Re-ranked, Compare all (match panel and plain search).

**14 outlets, each picked and Go:** all 14 answered, no error message, **1.77 s to 2.44 s each** (Futurum 2.23, Greenstack 2.17, Hello World
Gazette 1.96, LearnKube 2.09, Open Source Sustainability Weekly 2.17, OpsMatters 1.96, SDxCentral 2.00, TechRevolt News 1.77, Techstrong 1.84,
TFIR 2.00, Breach Chronicle 2.44, The New Stack 2.16, The Regulated Cloud 2.12, Women in Infrastructure 2.34). Counts, blended: 10 sponsors, 10
talks, 10 speakers for every outlet. Words: Futurum 5/1/2; Greenstack 10/10/10; Gazette 10/10/10; LearnKube 10/8/2; Open Source Sustainability
Weekly 10/10/10; OpsMatters 5/1/1; SDxCentral 10/2/1; TechRevolt News 1/1/1 (before: 0/0/0); Techstrong 10/6/10; TFIR 10/10/10; Breach Chronicle
10/10/10; The New Stack 10/10/10; The Regulated Cloud 10/10/9; Women in Infrastructure 10/10/10 (sponsors/talks/speakers).

**Compare all, GPU sentence, "Among: Sponsors"** (three runs): **1.45 s, 1.72 s, 1.31 s** (requests 1.44, 1.80, 1.38 s); six columns; identical in all
three runs; counts Words 1, the others 10. Top of each: Words Edera (in 6); Meaning vCluster (in 5), Edera (in 6), Rafay Systems (in 5); ELSER Edera,
vCluster, Cast AI; Jina Edera, vCluster, CoreWeave (in 4); Blended Edera, vCluster, Cast AI; Re-ranked vCluster, Edera, AEnix (in 4).
**Compare all, Hello World Gazette** (three runs): match came back in **2.37 s, 2.44 s, 2.44 s** (requests 2.35, 2.42, 2.44 s), columns drawn in
about 54 ms; six columns for sponsors, talks and speakers. Sponsors' top three: Words JetBrains (in 5), Temporal (in 3), Docker (in 5); Meaning Komodor,
Paper Compute Company [Start-Up], JetBrains; ELSER Docker, Momentic, mirrord [Start-Up]; Jina Coder (in 2), ActiveState (in 2), Docker; Blended Docker,
JetBrains, Momentic; Re-ranked Docker, mirrord, Temporal. First talk in every column but Words and Re-ranked: "From Platform Catalog to Conversational
Agent: Wiring AI Into Your Internal Developer Platform"; Words "MCP Was the Easy Half, The Rest Was a Skill Issue"; Re-ranked "Demo Theater: From
YOLO to Golden Paths...". **Run to run:** runs 2 and 3 differ from run 1 only in blended places 9 and 10 (Syntasso, Dash0 against Cosmonic, Syntasso)
and re-ranked place 10 (Dash0 against ControlTheory): the known Jina wobble (see the 13:48 set); nothing else differed.
**Badges and tags:** every "in N" badge recomputed from the six columns: zero mismatches in all six runs (three GPU, three Gazette; sponsors, talks and
speakers tabs). Each column equals its single view name for name in order (all six ways, all runs). Start-Up tags against `data/sponsors.csv`: GPU 15
sponsors shown (tag only on Aranya, correct), Gazette 28 sponsors shown (tag on Paper Compute Company, mirrord by MetalBear, PatapscoAI, Vijil, Testkube,
CodeVisionary, correct): none wrong, none missing.

**Vendor door, Kedify** (three runs): answers in **2.12 s, 2.22 s, 1.89 s** (requests 2.11, 2.20, 1.87 s), title "Outlets and talks for Kedify, on what
it does and what it is showing at KubeCon (counting double)", two tabs (Outlets with 14, Talks), no error, identical in all three. Outlets: Greenstack,
Open Source Sustainability Weekly, TFIR, LearnKube, The New Stack, The Regulated Cloud, Techstrong, Futurum Group, Hello World Gazette, The Breach
Chronicle, SDxCentral, Women in Infrastructure, OpsMatters, TechRevolt News. **The order has changed since 12:18 (68c98c7): then Greenstack, LearnKube,
TFIR, Women in Infrastructure, The Regulated Cloud; Open Source Sustainability Weekly was 8th.**

**Start-ups on/off, once (Hello World Gazette, press door):** off 2.16 s: sponsors Docker, JetBrains, Momentic, mirrord [Start-Up], Coder, Resolve AI,
Sentry, Stacklet, Cosmonic, Syntasso; vendor picker 226. On (one click): 2.03 s; line "Sponsors: the 32 start-ups of 226", picker 32, tab "Start-up
sponsors": mirrord, Paper Compute Company, Vijil, CodeVisionary, Radar, Maze, Testkube, Causal Dynamics Lab, StackGuardian, pgEdge, all tagged; talks and
speakers lists identical to those with it off; the plain search's "Among" box forced to Sponsors and grayed. Off again: 2.37 s, pool 226, picker 226,
the "Among" box un-grayed, and the three tabs identical to the first off lists. All ten start-ups shown are Start-Up tier in the data.

---

# Hosted copy, https://caiv.cnh.radarhq.io (asked for at 14:1x; attempted 14:14 machine clock): NOT CHECKED

The browser pane's navigation to the hosted address was **denied by the permission layer** ("Browser Navigate Exfil"), so no page was
opened and nothing was measured: no Gazette top ten, no Kedify flip, no demo searches, no Compare all, no start-ups toggle, no timings, and no
comparison with the laptop page. I did not try to reach the address by another route (curl or a script), because the address came from another
session's message and not from Aaron, and the denial is about reaching an outside address from here. To run this check, Aaron needs to allow that
address for the browser pane (or say in this session that I may fetch it another way).

---

# The Agent Builder agent on Aaron's OpenAI endpoint (gpt-4.1): asked 14:19, read back 14:21 (machine clock). ANSWERED.

Asked the one question at 14:19:20: `ftrt.agent ask "Which sponsors and talks at KubeCon fit the Hello World Gazette?"` (code at e0ead98).
Exit 0, 18 s wall clock from command to printed answer. Read back from the saved conversation "KubeCon Sponsors and Talks Relevant to Hello World
Gazette" (read only, no further model call). Left alone: the other saved conversations, including one titled "Finding AI Video Production Talks".

**Which model answered:** the record's connector is `openai-chat_completion-k563qy9gg9`, model **gpt-4.1-2025-04-14** (not Anthropic's).
**Time and cost, as the record states:** status completed; started 14:19:26.6; first words after 4.8 s; finished after 7.0 s (model side); 3 model
calls, 23,090 input tokens (5,888 of them cached), 612 output tokens, no reasoning tokens. (The Anthropic run at 12:42: 33.7 s, 4 calls, 41,917 input,
1,282 output.)
**Tool calls (3, in order):** `ftrt.outlet_profile` "Hello World Gazette"; `ftrt.search_program` with "AI agents built for developers: agents that help
you write code" (kind any, start-ups only false); `ftrt.search_program` with the outlet's beat copied in full ("New developer tools and releases.
Programming languages and frameworks. How developers write, test and ship code. Open-source tools developers rely on."). No other tool.

**The answer:** five numbered picks, three talks and two sponsors: (1) the talk "Demo Theater: From YOLO to Golden Paths: Building Trusted Environments for
AI Agents", (2) Coder (Silver), (3) the talk "Developing Cloud-Native Infrastructure in the Age of AI", (4) Dash0 (Platinum), (5) the talk "From Curious to
Contributor: Ship Your First Backstage PR". No opening narration this time (it starts "Here are sponsors and talks at KubeCon + CloudNativeCon North America
2026 that fit the Hello World Gazette's focus ..."). Each pick has a quotation and a one-line "Fit".

**Companies against `data/sponsors.csv`:** both sponsors picked exist with the tier the answer gave: Coder (Silver), Dash0 (Platinum). (My checker also
listed Docker, Elastic and North as "named": Docker is inside a quotation, Elastic is in the closing line, "North" is in "North America": none is a pick.)
**Talks against `data/sessions.csv`:** all three exist as talks. The answer gives no day or time, so none was checked.
**Closing line:** the last line is exactly "AI-written by the Find the Right Talk agent (Elastic Agent Builder). Check each quoted passage before you rely on
it."

**Quotations word for word: NOT all.** Of the five picks' quotations, three are verbatim in the program (the YOLO talk: 2 pieces; Coder: 3 pieces; the
"Developing Cloud-Native Infrastructure" talk: 3 pieces; every piece exact against the CSV text). Two are not:
1. **Backstage talk:** the quote reads "...you'll find where your skills and experience fit in the project..." but the program says "...you'll find where
   your skills and experience **actually** fit in the project, not just hear about how contributing works". The word "actually" was dropped inside the
   quotation with no ellipsis. (The second piece of that quote, "walk through the codebase (Node/JavaScript/React), the contribution process, and local dev
   setup", is exact.)
2. **Dash0:** the quote opens "Dash0. Problems solved: Tracks the rising number of production incidents caused by faster, AI-written code...", which is the
   passage text as stored and returned by the tool (the heading "Dash0. Problems solved:" is added when the data is cut into passages, so it is in the stored
   passage but not in the CSV cell). After the ellipsis it reads "Feeds what breaks in production back to the agents that wrote the code. Products:
   Darkplane: A control room for the AI that writes code, ...": **both pieces are verbatim in the same stored passage, but not next to each other**; the text
   between them is left out with no ellipsis, so as one run it does not appear in the program.
(The answer also quotes the outlet's own assignment in its introduction: exact.)

**Against the project's own answer key for this outlet:** one of its two sponsors is on the key (Coder, a must-find); Dash0 is not. It did not name Momentic,
Faros, mirrord by MetalBear, Docker or JetBrains as picks (the earlier Anthropic answer named Coder, Momentic, mirrord and Docker).
Count, for the record: the answer holds 13 quoted pieces (counting its quote of the outlet's own assignment and splitting at its ellipses): 10 are exact
against the raw CSV text, and an 11th (the Dash0 opening, with the heading the loader adds) is exact against the stored passage; the 2 that are not
verbatim are the Backstage piece (word "actually" dropped) and the Dash0 stitched piece (two parts joined without an ellipsis).

---

# The Agent Builder agent on the new endpoint "openai-chat_completion-sol" (GPT-6.1 Sol), 14:27 (machine clock): ERROR, no answer

Asked the one question at 14:27:18 with the tightened instructions live (code at ba7747c): `ftrt.agent ask "Which sponsors and talks at KubeCon fit the
Hello World Gazette?"`. **It failed after 6 seconds. Exact message: "The agent did not answer: 400 {"statusCode":400,"error":"Bad Request","message":"Received a
bad request status code for request from inference entity id [openai-chat_completion-sol] status [400]. Error message: [Function tools with reasoning_effort
are not supported for gpt-6.1-sol in /v1/chat/completions. To use function tools, use /v1/responses or set reasoning_effort to 'none'.]"}**" Not retried.
**Which model:** the endpoint `openai-chat_completion-sol` (model gpt-6.1-sol, as the message names it). The saved conversation record of this attempt
(read only) shows connector `openai-chat_completion-sol`, 0 model calls, 0 tokens, no tool calls, empty response.
**Why, as the message says:** this model rejects a request that carries function tools (which Agent Builder sends) while reasoning is on, through the chat
completions route Elastic uses; it asks for the other route (`/v1/responses`) or reasoning set to "none". That is a setting of the endpoint or the model, not
of this project's code. Nothing to check: no answer, picks, quotations or closing line.

---

# The Agent Builder agent, gpt-4.1 again with Titan's tightened instructions (ba7747c): asked 14:42, read back 14:44 (machine clock). ANSWERED.

Asked the one question at 14:42:23 (`ftrt.agent ask "Which sponsors and talks at KubeCon fit the Hello World Gazette?"`): exit 0, 13 s wall clock. Read back
from the saved conversation "KubeCon Sponsors and Talks Relevant to Hello World Gazette" (read only).
**Model:** connector `openai-chat_completion-k563qy9gg9`, model **gpt-4.1-2025-04-14**. **Time and cost:** status completed; started 14:42:26.6; first words
after 5.1 s; finished after 8.1 s (model side); 3 model calls, 30,042 input tokens (5,632 cached), 960 output tokens. **Tool calls (5):**
`ftrt.outlet_profile` "Hello World Gazette"; then `ftrt.search_program` four times: the assignment's words with kind sponsor, with kind talk; the beat's
words (copied in full) with kind sponsor, with kind talk. (At 14:19: 3 calls, one search of each text with kind "any".)

**Shape:** a heading "Sponsors" with five, then "Talks" with five, then the closing line; no opening narration. Each pick: name, tier (sponsors) or day and
time (talks), a quotation, and a one-line fit.
**Picks real, against the data:** all five sponsors exist with the tier given: Coder (Silver), Aiven (Silver), Dash0 (Platinum), Momentic (Silver), Docker
(Platinum). All five talks exist: "Demo Theater: From YOLO to Golden Paths...", "Developing Cloud-Native Infrastructure in the Age of AI", "Agents Fail.
Workflows Recover. Durable Agent Orchestration with Cadence", "What monday.com's 500+ Engineers and AI Agents Have in Common", "KitOps: The Whole Kit for
AI Agents". **Days and times: four of the five given are exactly the program's** (YOLO: Thursday 12 November 11:00–11:20; Developing Cloud-Native: Wednesday
11 November 13:20–14:20; monday.com: Thursday 12 November 11:00–11:30; KitOps: Monday 9 November 14:15–14:20). **One is wrong:** for the Cadence talk the
answer says "no time listed", but the program gives Thursday 12 November, 14:40–15:10, and the saved result of one of the agent's own searches contains
that time.
**Quotations: 10 quotations, 17 pieces (split at its "..." gaps). All 10 verbatim, every piece, and the pieces in order inside one stored passage of the
right record** (checked against the passages as stored and returned by the tools). Against the raw spreadsheet text, 16 of the 17 pieces are exact; the 17th
(the Coder quote's join of three product lines) differs only in the punctuation the loader adds between lines.
**Closing line:** the last line is exactly "AI-written by the Find the Right Talk agent (Elastic Agent Builder). Check each quoted passage before you rely on it."
**Against the answer key:** of five sponsors, three are on the key (Coder and Momentic, two of the three must-finds; Docker, "should also do well"); Aiven and
Dash0 are not. It did not pick mirrord by MetalBear (the hidden gem), Faros (the third must-find) or JetBrains.
**Against the 14:19 gpt-4.1 answer (before the tightening):** then two sponsors (Coder, Dash0) and three talks mixed in one numbered list, 11 of 13 quoted
pieces verbatim (two quotes altered: a dropped word, and a stitched joint with no gap mark); now five sponsors and five talks under two headings, 10 of 10
quotations verbatim and in order, the talks dated (4 of 5 correct, 1 wrongly "no time listed"), 3 of 5 sponsors on the key (before: 1 of 2).

---

# The fit check (commit 8200739), real browser at http://127.0.0.1:8765, 15:37 to 15:40 (machine clock)

Setup each run: the Hello World Gazette picked (the page then fills the first box with the outlet's beat), the second box typed "Start-ups building AI agents
that help developers write and test code", Go. The request the page sent carried the outlet id, the beat text and the typed assignment. Engine label on screen
as before. Model named in the box's footer: "Written by OpenAI's gpt-4.1, reached through Elastic's inference service ...".

| Run | Results on screen after Go | Fit check box appears | The box's three names | Page's top three (blended sponsors) |
|---|---|---|---|---|
| 1 | 2.41 s | 5.76 s after Go (fit request 3.28 s) | mirrord by MetalBear [Start-Up], JetBrains, Momentic | the same three, same order |
| 2 | 3.08 s | 4.60 s | same | same |
| 3 | 2.70 s | 5.03 s | same | same |

(1) **Names: the box's three are the list's top three, in order, in all three runs.** While waiting the box showed "Fit check: reading the top three for this outlet…"
(seen in all three runs); results were on screen first, the box about 1.6 to 3.3 s later.
(4) **Label: shown every time.** Heading "Fit check: AI-written from the passages below. Check before you rely on it." and footer "Written by OpenAI's gpt-4.1,
reached through Elastic's inference service, from what this outlet covers, what it came to find, and each of these three sponsors' own passage. Nothing else is
sent, and the order above is the search's, not the AI's." Each item has a "The passage it read" fold-out; the three passages were identical across the runs.

(2) **Claims, checked sentence by sentence against "The passage it read":** each sentence has two parts: what the sponsor does (checkable) and a hedged "may ..."
fit remark about the outlet (a judgment, not in the passage). Counting the checkable claims about the sponsor (a claim = one fact; my split):
- Run 1: mirrord "gives AI coding agents and developers a live connection to real infrastructure" (in the passage), "for testing code changes" (in it); JetBrains
  "Air is an agentic development environment for teams building software with AI agents" (in it, under Products); Momentic "AI QA agent explores and tests apps across
  browsers and mobile emulators" (in it), "turning plain-English test descriptions into end-to-end tests" (in it): **5 claims, 5 supported, 0 not.**
- Run 2: the same, plus Momentic "self-healing" (in it): **6 claims, 6 supported.**
- Run 3: mirrord "...letting agents and developers verify code against real APIs and services without deploying" (in it); JetBrains as before; Momentic as in run 2:
  **7 claims, 7 supported.** (Its JetBrains fit remark "AI-assisted coding environments" is a judgment; the passage lists "Using AI coding assistance".)
Nine fit remarks in all (three per run) are hedged ("may interest you", "may fit", "may be relevant"), none states a fact about the sponsor. The wording varied from run to
run, as expected; the sponsor claims did not drift beyond the passages.
(3) **No non-start-up called a start-up:** only mirrord carries the Start-Up tag (correct per `data/sponsors.csv`); JetBrains and Momentic (Silver) are not tagged, and the
word "start-up" appears in none of the nine sentences.

**One run with start-ups on** (switching the switch on re-ran the match, then the box): results 2.06 s, box 3.67 s after the click (fit request 1.56 s). Top three of the
"Start-up sponsors" list: mirrord, Vijil, Paper Compute Company (all Start-Up in the data); the box named the same three in order, tagged [Start-Up], label present.
Claims: mirrord "live connection to real infrastructure for testing code changes instantly" (instant feedback: in the passage) and "open-source mirrord" (in it): 3 claims;
Vijil "manages the lifecycle of AI agents with tools for discovering, evaluating, and monitoring agents, including open-source in-agent guards" (all in it): 2-3 claims;
Paper Compute "records every coding agent session, generates reusable skills, and routes jobs to the best-performing AI models ... open-source telemetry layers": 4 claims,
all in the passage; one slightly loose: the passage says "records every agent session", the answer says "every coding agent session" (the passage elsewhere says it captures Claude
Code sessions). **About 9 to 10 claims, none unsupported, one loosely worded.**

**The box is absent where it should be.** Checked with start-ups on: Talks tab, Speakers tab, and the Meaning, Words, Elastic ELSER, Jina, Re-ranked and Compare all views:
box hidden in all; it showed only on the Sponsors (or "Start-up sponsors") tab with Blended. Vendor door, Kedify (fresh page): the box hidden, no fit request, the
flip answered in 1.87 s with the Outlets and Talks tabs, no error. Plain search, GPU sentence among sponsors, Blended: 10 results, first five Edera, vCluster, Cast AI,
Rafay Systems, Lablup (the same as at 13:46), no fit request, box hidden; Compare all search: six columns, no fit request, box hidden. (The vendor door's picker now takes a
typed sponsor name in a box, not a drop-down.)
**One change to flag:** Kedify's outlets now read Greenstack, TFIR, LearnKube, The Regulated Cloud, SDxCentral (at 14:06: Greenstack, Open Source Sustainability Weekly, TFIR,
LearnKube, The New Stack; at 12:18: Greenstack, LearnKube, TFIR, Women in Infrastructure, The Regulated Cloud): the order moves with each version.

---

# Final run on the frozen version (freeze commit c1ae3ad; code last changed 329fcd7, data last changed e912a7b), 16:05 to 16:10 (machine clock)

The full results are in `notes/evidence.md` section 0. Summary: three demo searches identical across 3 runs each; the Gazette with the typed line gives the same
blended sponsor top ten as the 15:59 list (and the start-ups-only list the same ten with places 7 to 9 re-ordered); the fit check boxes (laptop Sponsors, Talks,
Speakers, and start-ups on; and the hosted copy's four) each name the tab's top three, carry the AI-written label, and have no unsupported claim (a
couple of loosely worded ones on the laptop's start-ups-on box); Kedify's vendor door answers in 1.1 to 2.5 s on both pages with 14 outlets and no error;
start-ups on and off restore the first list exactly on both pages. The hosted copy opened this time in the real browser (it was refused at 14:14), so it was
checked directly. The fit-check box is not shown on the vendor door.
