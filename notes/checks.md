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
