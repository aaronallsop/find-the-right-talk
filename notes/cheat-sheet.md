# Cheat sheet — explaining it to a judge (rule 6)

In Aaron's words, to be practiced out loud. Sunday's version; Monday adds one line per piece as
it is built.

## The five boxes

1. **The data.** The public KubeCon program and sponsor list, copied once with credit, plus a
   short profile of each media outlet. Plain spreadsheets, the kind any organizer hands over.
2. **The catalog.** Elasticsearch, running in Elastic Cloud serverless, holds every talk,
   speaker, sponsor and outlet. Long text is
   cut into short passages, and each passage is stored twice: as words, and as a list of 384
   numbers that capture its meaning.
3. **Three ways to search.** Words finds exact terms. Meaning finds the right idea in different
   words. Blended runs both and merges the two ranked lists.
4. **The match.** An outlet's KubeCon assignment and its standing beat become those same
   meaning numbers and search the program, the assignment counting more: the talks and
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
- **Elastic Cloud serverless:** the program lives in a cloud project, so anyone can run this
  from the public repository with their own project. A copy on the laptop is the fallback if the
  wifi fails.
- **An outlet has a standing beat and an assignment:** what it always covers, and what it was
  sent to find at this event. The match uses both, and the assignment counts more, because
  that is how an editor actually briefs a reporter.

## Questions a judge might ask

1. *What did you build today?* — Everything in the code: loading, the three searches, the match,
   the page. Before today: the idea, the data, the profiles. The history shows it.
2. *Why not just ask ChatGPT?* — It can't rank the whole program against an outlet in a second,
   doesn't know this year's program, and can't show its working. This shows the passage.
3. *How do you know the results are right?* — I read them. [Monday's checks.] And the demo
   shows where each method is wrong.
4. *Where does it fail?* — Meaning finds the topic, not the stance (the GPU search). And it never
   says "nothing fits"; it just returns the nearest thing. The honest limits are in "Honest limits" below.
5. *What's the hidden-gem idea?* — Start-ups rarely get press. The match surfaces them by what
   they do, not by how big their booth is.
6. *Would it work for another conference?* — Yes: any exhibitor spreadsheet and any list of
   outlets. Nothing is KubeCon-specific except the data.
7. *Why are some profiles AI-written?* — Two hundred and twenty-six sponsors in the time
   available; each is labeled, and drawn from the company's own website, or from its conference listing
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

## The old 90-second demo (Aaron's script, approved 12:05; superseded by the 3-minute video below, now that there is no live presentation)

Words are Aaron's, kept as written. Square brackets are what is on screen, not words to say.

1. [The page, press door, nothing picked yet]
   "I'm a video producer. I've covered a lot of conferences as media, and the plan never survives
   the morning. An interview cancels, another one moves, and suddenly you've got ninety free
   minutes, six hundred talks, two hundred booths, and no idea where to start. You don't want to
   sit in the press room, but you also can't read the whole schedule. So I built the thing I
   wanted in that moment: KubeCon's own program, public data with credit, made searchable by
   meaning in Elastic Cloud, today."
2. [Pick The Hello World Gazette, press Go]
   Aaron's words (12:45, verbatim): "Hello World Gazette is a newsletter for developers about new
   tools being created. They are at KubeCon to focus specifically on ai agents that are built to
   help developers work day to day."
   [On screen, no words yet: the matches come up; point at the passage that made one match; point at
   mirrord, flagged as a Start-Up. Aaron to add the words for these, or leave them silent.]
3. [Vendor door, pick a start-up sponsor, Go]
   "Same engine, turned round. I'm a vendor whose press meeting just canceled: which outlets
   should I be talking to instead, and which talks are near my story?"
4. [Compare mode, "scale up for a traffic spike and back down afterwards"]
   "Three searches underneath. Words finds nothing, because no sponsor uses those words. Meaning
   finds the autoscaling start-up, Kedify. Blended lets each list vote."
5. [Compare mode, "SLSA Level 3"]
   "The other way round: an exact standard name. Words wins, meaning blurs. That's why there are
   three, and why the page shows which one found what."
6. [Back to the page]
   "Elastic Cloud serverless, Elastic's own model as one voice, every AI-written line labeled,
   all the code written today from an empty folder. Next time an interview cancels, I've got my
   next three stories before I've finished my coffee."

**Before presenting:** Elastic's own model sleeps when idle and took 81 seconds to wake once. Run
`.venv/bin/python -m ftrt.warm` a few minutes before the demo (it says how long each model took;
"awake (0 s)" means it was already awake). Starting the page does it too, in the background. Do it
before the 16:15 recording, again before the 16:30 submission, and again in the 17:15 screen check.

**Two conditions.** Beat 4 uses whatever sentence Cassini's three runs agree on (so far: that
sentence, Kedify first). "Elastic's own model as one voice" in beat 6 is said only once the fourth
voice is built (it is, since 12:12, in the cloud only; the laptop leaves it out, so demo from the
cloud); if it does not answer, say "searched three ways" and stop.

**Still not perfect, as of 12:50 (say so, do not hide it):** the Hello World Gazette misses its answer
key by one place (Faros 13th); the flip's outlet order is a weak signal while its talks are strong;
re-ranked, the GPU search puts vCluster above Edera. The Breach Chronicle is set aside: it stays in
the data and is reported honestly as a miss.

## The 3-minute video (Aaron's final script, approved 14:58, sent by Neptune; supersedes the 12:05 and 12:50 versions)

Aaron's words, kept as written. Square brackets are what is on screen, not words to say.

1. [The page, press door, nothing picked. 0:00]
   "I'm a video producer. I've covered a lot of conferences as media, and the plan never survives the
   morning. An interview cancels, another one moves, and suddenly you've got ninety free minutes, six
   hundred talks, two hundred booths, and no idea where to start. You don't want to sit in the press
   room, but you can't read the whole schedule either. So I built the thing I wanted in that moment.
   This is KubeCon's own program, public data with credit, searchable by meaning in Elastic Cloud
   serverless, built today from an empty folder."
2. [Pick Hello World Gazette; its beat fills in. TYPE this exact line into "What we came to KubeCon to
   find", then Go. 0:30]
   **Type exactly (do not rephrase; the measured order belongs to these words):**
   `Start-ups building AI agents that help developers write and test code`
   Measured on the laptop page at 15:18, the same in four runs out of four (Neptune/Cassini): mirrord by
   MetalBear first, then JetBrains, Momentic, Docker, Vijil, Testkube. Do NOT say Docker is first: it
   came first only with the Gazette's stored KubeCon line, and everyone already knows Docker.
   Aaron's words, with the two changed lines marked (approved by Aaron at about 15:25 laptop clock;
   they were written because the old line named Docker first):
   "I'm press. This outlet covers developer tools. I tell it what I'm after: start-ups
   building AI agents that help developers write and test code. The match ranks the whole program
   against that in about two seconds. And first comes mirrord, a start-up I would have walked
   straight past. Every result shows the passage that made it fit, so you can check my working."
   [The Fit check box appears above the list (checked by Cassini); read ONE sentence of it aloud, then
   open "The passage it read" under it. The box is labeled "Fit check: AI-written from the passages
   below. Check before you rely on it."]
   [Scroll to mirrord.] "Nobody finds it by booth size. The passage says exactly why it fits."
   (The measured results for the Gazette's stored line, Docker, JetBrains, Momentic, mirrord, Coder,
   remain true and are in `notes/evidence.md`; the line typed in the video is Aaron's own, not the stored one.)
3. [Start-ups toggle. 0:55]
   "Start-ups only: two hundred and twenty-six sponsors become thirty-two. That's the hidden-gem list,
   and it's the list a reporter never has time to make." (With Start-ups only on, the list opens with
   mirrord, Paper Compute Company, Vijil and CodeVisionary, measured 15:18 with the stored line; mirrord
   was first either way.)
4. [Vendor door, pick Kedify, Go. 1:10]
   "Same engine turned round. I'm a vendor whose press meeting just canceled. Which outlets should I
   be talking to instead?" [Point at the list.] "Greenstack comes first, each outlet with the line
   from its own profile that matched. And below, the talks nearest my story." (CHANGED at 15:47 on
   Saturn's word: Kedify's order moved again, now Greenstack, TFIR, LearnKube, The Regulated Cloud,
   SDxCentral, and it moves between versions, so name only "Greenstack first" and read the screen.
   Aaron to approve this edit of his line.)
5. [Click "How these were found" once, then Compare all, and type "scale up for a traffic spike and back down afterwards". 1:35]
   "Under the hood, six columns. Keyword search finds nothing: no sponsor uses those words. My small
   local model, Elastic's ELSER and Jina's embeddings all find Kedify, the autoscaling start-up. The
   blend lets every list vote, and Jina's re-ranker reads the top twenty again."
6. [Compare all (already open), "SLSA Level 3". 1:55]
   "The other way round: an exact standard name. Keyword wins, ActiveState and Docker, because their
   text says it. Meaning blurs. That's why there are six columns and why the page shows which one
   found what."
7. [Agent clip, pre-recorded. 2:10]
   "And an agent, built in Elastic's Agent Builder with three read-only tools on these catalogs.
   Ask it what the Gazette should cover, and it answers with real companies, real talks, and quotes
   it can point to."
8. [Radar page in the browser, then the Dash0 trace. 2:30]
   "The hosted version runs on Radar's Kubernetes cluster, searching with Elastic's models alone.
   Every press of Go is traced in Dash0, so you can see the searches running in parallel. And Gitar
   reviewed every line of today's code." (CHANGED: "Sonar's Gitar" is now "Gitar"; Titan knows of no link
   to Sonar, gitar.ai is the reviewer, so "Gitar" is the safe wording. Aaron to approve.)
9. [GitHub: the commit history scrolling from the 11:00 commit. 2:45]
   "All of it written today. The first commit, at eleven, has no code in it; the history shows the
   rest. Where does it fail? Meaning finds the topic, not the stance, and my hardest test outlet, the
   Breach Chronicle, is a miss that I report rather than hide. Next time an interview cancels, I've
   got my next three stories before I've finished my coffee."

**Checks before recording (Neptune's, kept under the script):** the Gazette's top five and Kedify's outlet
list are Cassini's afternoon measurements; if the final save changes either, read what is on screen.
Beat 7 only if the agent clip exists; cut it otherwise. Beat 8's Gitar line: the review pull
request (aaronallsop/find-the-right-talk#1) is closed unmerged as of 16:10; show it as closed, not deleted.

**Things to confirm before recording (Rhea's flags; the words are Aaron's, these are checks):**
- **Beat 5, Jina finds Kedify:** the measured result is that meaning, and Elastic's ELSER alone, put
  Kedify first. I have not seen Jina's own column for that sentence. Read the Compare all screen; if
  Jina does not show Kedify, drop "and Jina's embeddings" from the sentence.
- **Beat 8, Dash0 and Radar are different pages:** the Dash0 dashboard shows traces from the laptop
  page only; the hosted Radar copy is not traced. "Every press of Go is traced" is true of the
  laptop page, so show the Dash0 trace from a Go on the laptop page, not from the Radar page.
  "Searches running in parallel" is not something anyone has measured; check the trace view shows it
  before saying it.
- **Beat 8, "Sonar's Gitar":** nobody has confirmed the link to Sonar. Say "Gitar" unless Aaron has
  checked.
- **Beat 8, "Elastic's models alone":** the hosted copy also uses the words search, so say "without
  the laptop's own meaning model" if you want it exact.
- **Beat 7, the agent:** Cassini found 2 of 13 quotations in the agent's answer on the OpenAI model
  were not word for word. "Quotes it can point to" is only safe if the clip you record has exact
  quotations; check the saved answer against the program first.
- **Length:** the spoken words come to about 460, which is about 3 minutes 15 seconds at a steady 140
  words a minute, or about 3 minutes at 150 to 155. The timings in the script put beat 9 at 2:45, but
  beat 9 alone is about 80 words, roughly 35 seconds. It is tight against the 3-minute limit; rehearse
  with a timer, and if it runs over, cut the optional Dash0 and Radar sentence in beat 8 or the last
  sentence of beat 9 first.
- **Beat 2, "about two seconds":** measured about 2.4 to 2.5 seconds for a Gazette Go.

**Before recording (Aaron):** at 16:10 run `.venv/bin/python -m ftrt.warm` (and again at 16:25 before
submitting). **The agent is its own clip, recorded once (Aaron, 13:10), at about 14:05 after the
go/no-go,** in the cloud Kibana (Agents, "Find the Right Talk"), using the screen check below. Ask:
"Which sponsors and talks at KubeCon fit the Hello World Gazette?" Nobody asks the agent anything
before that (refused questions use the trial allowance too). If Elastic refuses, stop and tell Saturn;
do not retry on camera.

**Screen check before recording (Dione's list; the full version is in "For Aaron" on `BOARD.md`):**
record a browser, not the Claude app; one new private window with the bookmarks bar hidden; tabs
in this order: the laptop page, the GitHub README (signed out), the Radar page, Dash0 traces, the
cloud Kibana's Agent Builder; Do Not Disturb on; quit apps that can pop up. Film only the cloud Kibana,
never the local one. Never show a key, a token, a settings file, the kubeconfig, the Elastic console,
Radar Cloud (app.radarhq.io), Dash0 settings, your real email, or anything from your private project.
Clear typed boxes first. In the Terminal, only run `.venv/bin/python -m ftrt.warm`.

## Built on the day, one line per piece

- **Loading (B1, 11:03):** One command reads the spreadsheets, cuts every talk, speaker,
  sponsor and outlet into passages of about 120 words (2,225 for the program and 25 for the outlets), turns each passage into 384
  numbers with the small meaning model on the laptop, and loads them into two brand-new catalogs
  in about 12 seconds; a search of the loaded text for email addresses finds none.
- **Three ways to search (B2, 11:07):** From Terminal, one command searches the program by words
  (exact terms; it can come back empty, which is information), by meaning (the nearest idea in any
  wording; it always returns something), or blended (each list votes, a result gets more points the
  higher it ranks in each, and the totals decide), and shows the passage that made each result match;
  a compare mode runs all three at once so you can watch them disagree. Measured 9 November, three runs
  each, identical every time (Cassini, after the reload): "SLSA Level 3" is won by words (ActiveState
  then Docker, the two sponsors whose own text says it), while meaning puts OpenSSF first; the
  traffic-spike sentence "scale up for a traffic spike and back down afterwards" gets nothing from
  words and the Start-Up Kedify first from meaning; the GPU-isolation sentence gets Edera from
  words and vCluster then Edera from meaning.
- **Elastic Cloud (11:24):** The same two catalogs now live in an Elastic Cloud serverless
  project; the code uses the cloud when its settings file is filled in and the laptop engine
  otherwise, so the demo has a fallback if the wifi fails. Loading to the cloud now takes 66 seconds (measured 13:35; ELSER and Jina read every passage)
  and the three demo searches give the same top results there as on the laptop.
- **Cleaner loading and searching (11:39):** The loader now cuts every passage to fit what the
  meaning model actually reads, drops placeholder bios like "TODO", puts the day and time into
  every session so the seven coffee breaks are told apart, and the searches no longer print
  library noise before their results.
- **The match (M2, 11:48):** The match takes an outlet's two parts, what it always covers and what
  it came to KubeCon to find, searches the program with each part by meaning and by its most
  telling words, and merges the rankings with the KubeCon part's votes counting double, so each
  talk, speaker or sponsor it lists comes with the passage that matched and the part that found it.
- **The page (M3, 11:55):** The page has two doors: press pick an outlet, or type what they always cover and what they came to KubeCon to find, and get the talks, speakers and sponsors that fit, each with the passage that matched; vendors pick their company or describe it (the flip, which finds the outlets that fit them, comes next); and the plain three-way search sits underneath.
- **Steadier results (11:57):** Results no longer reshuffle when you ask for more of them: every list is ranked to the same depth before they are blended.
- **Elastic's own model (12:12):** In Elastic Cloud a second, larger meaning model, Elastic's own ELSER, reads every passage too and gets one vote in the blend, beside the words search and the small model on the laptop; on the laptop it is simply left out.
- **The flip (M5, 12:17):** The flip turns the match round: a sponsor, picked or typed in, finds the outlets whose beat and KubeCon assignment fit it, each with the outlet's own passage that matched, and the talks nearest to what it does, with what it is showing at KubeCon counting double.
- **Start-ups toggle (M4, 12:27):** One 'Start-ups only' switch narrows every sponsor list on the page, the press door's matches, the vendor door's picker and the plain search, to the 32 start-ups among the 226 sponsors, and switching it off brings the full lists back unchanged; for the Breach Chronicle it brings up Maze and Archestra AI, small companies doing exactly what the outlet came to find.
- **Warming Elastic's models (12:29):** Elastic's models sleep when nobody uses them, so one command wakes them before a demo, and if one is still slow a search answers without it in a few seconds and says so, rather than leaving the page blank.
- **Re-ranking (12:32):** A 'Re-ranked' switch hands the top twenty blended results to Elastic's own re-ranking model, which reads the question and each passage together and puts them in a new order, so the demo can show the list before and after. For that view only, the text goes to Elastic's hosted service outside the project.
  Demo note: re-ranked, the GPU search puts vCluster (shares GPUs) above Edera (isolates them): the re-ranker cannot tell the stance either, so say so rather than hope nobody asks.
- **The agent (12:46):** An Elastic Agent Builder agent, 'Find the Right Talk', answers in plain words using three read-only tools over our two catalogs, quotes the program's own passage for every company or talk it suggests, and labels its answer AI-written; on Elastic's trial it can answer about one long question every few minutes (a second question at 12:45 was refused with 'wait 6m53s'), so the video shows one recorded answer.
- **Jina's embeddings (13:44):** In Elastic Cloud a third meaning model, Jina's, reads every passage through Elastic's hosted service and gets one vote in the blend, so each result now combines four voices: the words, the small meaning model, Jina's model and Elastic's own ELSER, and Compare all shows each of them side by side.
- **Dash0 tracing (13:49):** Every search on the page can be traced in Dash0: each step, words, the meaning models, Elastic's ELSER, Jina and the re-ranker, shows how long it took and whether it answered, without the search's own words ever leaving the laptop in the trace. It sends traces only when a Dash0 settings file is filled in.
- **The fit check (built 15:3x):** After the search has picked its top three sponsors, an AI model (OpenAI's gpt-4.1, reached through Elastic) reads only what the outlet said and those three sponsors' own text and writes a sentence on why each may suit; the search still decides the order, and if the model is slow nothing is shown.
