# Cheat sheet — explaining it to a judge (rule 6)

In Aaron's words, to be practised out loud. Sunday's version; Monday adds one line per piece as
it is built.

## The five boxes

1. **The data.** The public KubeCon programme and sponsor list, copied once with credit, plus a
   short profile of each media outlet. Plain spreadsheets, the kind any organiser hands over.
2. **The catalogue.** Elasticsearch, running in Elastic Cloud serverless, holds every talk,
   speaker, sponsor and outlet. Long text is
   cut into short passages, and each passage is stored twice: as words, and as a list of 384
   numbers that capture its meaning.
3. **Three ways to search.** Words finds exact terms. Meaning finds the right idea in different
   words. Blended runs both and merges the two ranked lists.
4. **The match.** An outlet's KubeCon assignment and its standing beat become those same
   meaning numbers and search the programme, the assignment counting more: the talks and
   sponsors it would want to cover, with the passage that made each one match.
5. **The page.** One simple web page on this laptop. It talks to the search engine: your own
   Elastic Cloud project, or the copy on the laptop, which needs no internet.

## Why each choice

- **Words and meaning together:** each fails where the other succeeds. Words can't see that
  "survive a traffic spike" means autoscaling; meaning blurs exact names like "SLSA Level 3".
- **How they are merged:** each list votes; a result gets more points the higher it ranks in
  each, and the totals decide the order. A standard method, reciprocal rank fusion.
- **Short passages:** the meaning model only reads about 250 word-pieces, roughly 170 words, and a sponsor's material
  is far longer. Cutting it up also lets the page show *which* passage matched.
- **A small model on the laptop:** free, private, fast, works offline. It finds meaning; it
  doesn't write anything.
- **Elasticsearch:** it does words, meaning and filters in one place, and it is the track.
- **Elastic Cloud serverless:** the programme lives in a cloud project, so anyone can run this
  from the public repository with their own project. A copy on the laptop is the fallback if the
  wifi fails.
- **An outlet has a standing beat and an assignment:** what it always covers, and what it was
  sent to find at this event. The match uses both, and the assignment counts more, because
  that is how an editor actually briefs a reporter.

## Questions a judge might ask

1. *What did you build today?* — Everything in the code: loading, the three searches, the match,
   the page. Before today: the idea, the data, the profiles. The history shows it.
2. *Why not just ask ChatGPT?* — It can't rank the whole programme against an outlet in a second,
   doesn't know this year's programme, and can't show its working. This shows the passage.
3. *How do you know the results are right?* — I read them. [Monday's checks.] And the demo
   shows where each method is wrong.
4. *Where does it fail?* — Meaning finds the topic, not the stance (the GPU search). And it never
   says "nothing fits"; it just returns the nearest thing.
5. *What's the hidden-gem idea?* — Start-ups rarely get press. The match surfaces them by what
   they do, not by how big their booth is.
6. *Would it work for another conference?* — Yes: any exhibitor spreadsheet and any list of
   outlets. Nothing is KubeCon-specific except the data.
7. *Why are some profiles AI-written?* — Two hundred and twenty-six sponsors in the time
   available; each is labelled, and drawn from the company's own website, or from its conference listing
   alone where the website could not be read (six of them).
8. *What did you do, and what did Claude do?* — I designed it, named and briefed the two test outlets, made
   every decision and checked the results. Claude wrote the code, and every commit says so.
9. *Why Elastic Cloud?* — Judges and anyone else run it from the public repository on their own
   laptop against their own free serverless project; my laptop engine is only the fallback if the
   wifi dies. The data is public, so nothing private goes to the cloud.
10. *Why no geo?* — My data has no coordinates: rooms in one building and a region word per outlet.
    A map would be decoration, so I spent the time on your models and your cloud instead.
11. *Why Elastic's own models?* — The blend is my own code and takes any number of voices, so
    Elastic's meaning model is a fourth list beside words and my small local model, and the
    compare mode shows where they disagree. The re-ranker then re-orders the top results.
    [Say this only once the fourth voice and the re-ranker are built; until then: "that is the
    next step on the board."]

## The demo, in ninety seconds (Aaron's script, approved 12:05; replaces the day plan's version)

Words are Aaron's, kept as written. Square brackets are what is on screen, not words to say.

1. [The page, press door, nothing picked yet]
   "I'm a video producer. I've covered a lot of conferences as media, and the plan never survives
   the morning. An interview cancels, another one moves, and suddenly you've got ninety free
   minutes, six hundred talks, two hundred booths, and no idea where to start. You don't want to
   sit in the press room, but you also can't read the whole schedule. So I built the thing I
   wanted in that moment: KubeCon's own programme, public data with credit, made searchable by
   meaning in Elastic Cloud, today."
2. [Pick The Hello World Gazette, press Go]
   [AARON'S WORDS FOR THE GAZETTE TO BE WRITTEN: the lines here were about the Breach Chronicle's
   beat and assignment, and the Chronicle is set aside as the demo outlet (12:16).]
   "...The match reads that brief and ranks the whole programme against it, in a second. Every
   result shows the passage that made it fit, so you can check my working. And start-ups are
   flagged: this one you'd never find by booth size." [Point at a flagged start-up.]
3. [Vendor door, pick a start-up sponsor, Go]
   "Same engine, turned round. I'm a vendor whose press meeting just cancelled: which outlets
   should I be talking to instead, and which talks are near my story?"
4. [Compare mode, "scale up for a traffic spike and back down afterwards"]
   "Three searches underneath. Words finds nothing, because no sponsor uses those words. Meaning
   finds the autoscaling start-up, Kedify. Blended lets each list vote."
5. [Compare mode, "SLSA Level 3"]
   "The other way round: an exact standard name. Words wins, meaning blurs. That's why there are
   three, and why the page shows which one found what."
6. [Back to the page]
   "Elastic Cloud serverless, Elastic's own model as one voice, every AI-written line labelled,
   all the code written today from an empty folder. Next time an interview cancels, I've got my
   next three stories before I've finished my coffee."

**Before presenting:** Elastic's own model sleeps when idle and took 81 seconds to wake once. Run one
search a minute or two before the demo so it is awake. Warm the Elastic models before the
16:15 recording, again before the 16:30 submission, and again in the 17:15 screen check (Titan sends the command).

**Two conditions.** Beat 4 uses whatever sentence Cassini's three runs agree on (so far: that
sentence, Kedify first). "Elastic's own model as one voice" in beat 6 is said only once the fourth
voice is built (it is, since 12:12, in the cloud only; the laptop leaves it out, so demo from the
cloud); if it does not answer, say "searched three ways" and stop.

**Not true yet, as of 12:22 (do not rehearse as if it were):** the Hello World Gazette, the demo outlet since 12:16,
still fails its answer key by one place (Faros 13th) after the last re-score; "in a second" has not
been timed; the flip (beat 3) is built (12:17) but nobody has checked that its outlet list makes sense for a sponsor. The Breach Chronicle is set aside: it stays in the data
and is reported honestly as a miss.

## Built on the day, one line per piece

- **Loading (B1, 11:03):** One command reads the spreadsheets, cuts every talk, speaker,
  sponsor and outlet into passages of about 120 words (2,225 for the programme and 25 for the outlets), turns each passage into 384
  numbers with the small meaning model on the laptop, and loads them into two brand-new catalogues
  in about 12 seconds; a search of the loaded text for email addresses finds none.
- **Three ways to search (B2, 11:07):** From Terminal, one command searches the programme by words
  (exact terms; it can come back empty, which is information), by meaning (the nearest idea in any
  wording; it always returns something), or blended (each list votes, a result gets more points the
  higher it ranks in each, and the totals decide), and shows the passage that made each result match;
  a compare mode runs all three at once so you can watch them disagree. Measured 9 November, three runs
  each, identical every time (Cassini, after the reload): "SLSA Level 3" is won by words (ActiveState
  then Docker, the two sponsors whose own text says it), while meaning puts OpenSSF first; the
  traffic-spike sentence "scale up for a traffic spike and back down afterwards" gets nothing from
  words and the Start-Up Kedify first from meaning; the GPU-isolation sentence gets Edera from
  words and vCluster then Edera from meaning.
- **Elastic Cloud (11:24):** The same two catalogues now live in an Elastic Cloud serverless
  project; the code uses the cloud when its settings file is filled in and the laptop engine
  otherwise, so the demo has a fallback if the wifi fails. Loading to the cloud now takes 470 seconds, because Elastic's ELSER reads every passage
  and the three demo searches give the same top results there as on the laptop.
- **Cleaner loading and searching (11:39):** The loader now cuts every passage to fit what the
  meaning model actually reads, drops placeholder bios like "TODO", puts the day and time into
  every session so the seven coffee breaks are told apart, and the searches no longer print
  library noise before their results.
- **The match (M2, 11:48):** The match takes an outlet's two parts, what it always covers and what
  it came to KubeCon to find, searches the programme with each part by meaning and by its most
  telling words, and merges the rankings with the KubeCon part's votes counting double, so each
  talk, speaker or sponsor it lists comes with the passage that matched and the part that found it.
- **The page (M3, 11:55):** The page has two doors: press pick an outlet, or type what they always cover and what they came to KubeCon to find, and get the talks, speakers and sponsors that fit, each with the passage that matched; vendors pick their company or describe it (the flip, which finds the outlets that fit them, comes next); and the plain three-way search sits underneath.
- **Steadier results (11:57):** Results no longer reshuffle when you ask for more of them: every list is ranked to the same depth before they are blended.
- **Elastic's own model (12:12):** In Elastic Cloud a second, larger meaning model, Elastic's own ELSER, reads every passage too and gets one vote in the blend, beside the words search and the small model on the laptop; on the laptop it is simply left out.
- **The flip (M5, 12:17):** The flip turns the match round: a sponsor, picked or typed in, finds the outlets whose beat and KubeCon assignment fit it, each with the outlet's own passage that matched, and the talks nearest to what it does, with what it is showing at KubeCon counting double.
- **Start-ups toggle (M4, 12:27):** One 'Start-ups only' switch narrows every sponsor list on the page, the press door's matches, the vendor door's picker and the plain search, to the 32 start-ups among the 226 sponsors, and switching it off brings the full lists back unchanged; for the Breach Chronicle it brings up Maze and Archestra AI, small companies doing exactly what the outlet came to find.
