# The recipe — what a week of building this taught us, in plain words

This is research, not code. It is what was learned building a search engine for Aaron's video
library (media-connect, 3–7 November 2026), written down so that Monday's build, which starts
from an empty folder, does not have to rediscover it. Nothing here is to be copied as code; it
says what to build and which traps to avoid, and Monday writes it fresh.

## The shape

1. **Read the CSVs** in `data/`. One row is one thing: a sponsor, a session, a speaker, an
   outlet. Lists inside a cell are separated by "; ". The files start with a byte-order mark
   (so Excel opens them properly); read them as "UTF-8 with BOM" or the first column's name
   comes out with an invisible character in front of it.
2. **One catalogue for the programme** (sessions, speakers, sponsors together, told apart by a
   `kind` field) and **one for the outlets**. Give them new names (not `kubecon` or
   `outlets`: those already exist on this laptop from the earlier project and must not be
   reused or overwritten). Load into empty catalogues, so the entry visibly starts from zero.
3. **Each record's text is cut into short passages** before it is turned into numbers.
4. **Three ways to search:** words, meaning, and both blended.
5. **The match:** an outlet's own numbers are used to search the programme. That is the
   product. Decided by Aaron (8 November): an outlet has a **standing beat** (what it always
   covers) and a **KubeCon assignment** (what it was sent to find, the `kubecon_assignment`
   column), and the match uses **both, the assignment counting more**. Turn the assignment and
   the beat into numbers separately, search the programme by meaning with each, and merge the
   two rankings by the same reciprocal rank fusion as the blended search, with the assignment's
   votes counting double. **An outlet with no assignment** (the eight real ones: none of their
   pages says what they want at KubeCon, and we do not invent it) **is matched on its beat
   alone.** Score it against `notes/answer-keys.md`. The reverse (a sponsor finds
   its outlets) is the same thing turned round.
6. **One plain web page** on this laptop: a text box, the three-way switch, results; then an
   outlet picker that shows its matches.

## Settings that were found the hard way

- **The meaning model:** `sentence-transformers/all-MiniLM-L6-v2`. Free, open source, runs on
  the laptop, no key, nothing leaves the machine. It produces **384 numbers** per passage, and
  the catalogue has to be told 384 before anything is loaded; it cannot be changed later
  without rebuilding.
- **The model reads only about the first 180 words** of anything and ignores the rest. So long
  text is cut into **passages of about 120 words**. A typical sponsor's material is several
  passages. Search the passages for meaning and report the parent record, with the passage that
  matched as the reason ("found because…").
- **Blending: do the merge ourselves, not with Elasticsearch's own blending.** Elasticsearch's
  built-in blend is a paid feature that works today only because the free trial is running; it
  stops on about 3 December. The method is called **reciprocal rank fusion**: each list votes,
  a result gets 1 ÷ (60 + its position) from each list it appears in, and the totals decide the
  order. 60 is the standard value from the original paper.
- **Words search must not match on one stray word.** Require about half the typed words to be
  present for a whole record. For a single short passage, half is too loose: require all of
  them when two or fewer words are typed, three quarters when more (Elasticsearch writes this
  as `2<75%`). Found when a four-word passage containing "booth" beat the sponsor whose text
  said "booth 133".
- **Meaning search must look deep enough.** Elasticsearch stores the numbers compressed and,
  by default, re-checks too few candidates at full detail; asking for 12 results once gave a
  first result that was not the best. Ask it to consider a few hundred candidates (200 worked)
  and check: the same question at 1 result and at 48 should give the same top answer.
- **Reading a record back does not return its numbers** unless asked for them by name. The
  match (an outlet's numbers searching the programme) needs this.
- **Words and meaning must read exactly the same text**, or the blend compares two different
  things.

## Traps

- **Meaning finds the topic, not the stance.** Asked about keeping customers' GPU workloads
  apart, it ranked companies that share GPUs level with the one that isolates them. Show the
  passage so a person can tell; this is what an AI "fit check" would be for.
- **Meaning never says "nothing fits"**; it always returns the nearest thing. Words search can
  return nothing, and that is information.
- **Before changing how results are scored, write down the top result of every demo search,
  change it, then compare.** A scoring change that fixed one search broke the best demo for an
  hour on 7 November.
- **One-word profile lines** ("Industries: Telecoms.") become passages of their own and attract
  the meaning search; fold short lines into their neighbours.
- **Check by searching the output**, not by reading the rule: if something must be absent
  (a person's name, an email), search the loaded catalogue for it.
- **Flask reads the page file once, at start.** After editing the page, restart it. Keep the
  debugger off (it would put a console on a page with no login). Bind to this machine only.
- **Do not use port 5000.** On this Mac it is already taken by macOS itself (AirPlay Receiver),
  so a page started on Flask's default port answers with someone else's error. Ports 5055 to
  5057 may also be held by the private project's test pages until the laptop restarts. Pick
  another port (5060 was free Sunday night) and put it in the README's "open" step.
- **The meaning model is already on this laptop**, in the Hugging Face cache. On first use the
  library still asks the internet whether there is a newer copy, and on flaky venue wifi that
  can hang. If loading is slow, set `HF_HUB_OFFLINE=1` in the environment before running
  (or in the code, before the model is loaded) and it reads the cache only.
- **zsh, not bash:** brace variables; never build a list of arguments as one string.

## The demo searches, to re-prove on Monday

These were proved on 7 November against a catalogue that also held the sponsors' own website
text. Monday's catalogue does not (decided 8 November), so each must be re-run and may change.

1. **"Black Friday" sentence** — an outlet-voiced sentence about surviving a traffic spike.
   Words found nothing; meaning found a Start-Up autoscaling company. *Most at risk*: the
   meaning hit leaned on website text.
2. **"SLSA Level 3"** — words win: exact standard names are where meaning blurs.
3. **The GPU sentence** — keeping tenants' GPU workloads isolated on shared hardware. Five
   companies within 0.027 of each other; shows why a person (or a fit check) has to read.

If one fails, pick a replacement on the day by running candidates in all three modes and keeping
one where words and meaning clearly disagree.
