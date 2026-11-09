# Checks — Cassini's results, with the time of each

Cassini looks and never fixes. Everything below was measured on 9 November 2026 against the
programme as loaded at that time (commit f712a6d plus whatever was on disk; no code was changed
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
story. (My reading, not measured: "idle servers ... rest of the year" pulls towards cost and
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

All kinds (programme-wide; the command does allow it), identical in all 3 runs:

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

Load counts printed by the fresh copy (these rebuilt the demo's two catalogues in the cloud project):
501 talks in 816 passages; 100 events in 126 passages; 715 speakers in 717 passages; 226 sponsors in
566 passages; 14 outlets (6 with a KubeCon assignment) in 25 passages. 2,225 passages turned into 384
numbers each for `ftrt-programme` (7 s) and 25 for `ftrt-outlets`. In the engine afterwards:
`ftrt-programme` 2,225 passages, `ftrt-outlets` 25 passages; 0 email addresses in each; 33 passages
with an @ sign (social handles). "Done in 68s".

**Steps that fail or are unclear, and README statements that are wrong:**
1. **Step 5 is a placeholder** ("[command]" and "[address]"): a judge cannot start the page. (Expected
   at this stage, since the page was not built when I cloned.)
2. **README step 4 says "cuts the text into 2,250 passages"; the load printed 2,225** programme passages
   (2,250 would be 2,225 + 25 outlet passages, if that is the intended total; the README reads as the
   programme's count). Wrong or ambiguous.
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
