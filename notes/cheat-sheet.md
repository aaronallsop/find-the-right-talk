# Cheat sheet — explaining it to a judge (rule 6)

In Aaron's words, to be practised out loud. Sunday's version; Monday adds one line per piece as
it is built.

## The five boxes

1. **The data.** The public KubeCon programme and sponsor list, copied once with credit, plus a
   short profile of each media outlet. Plain spreadsheets, the kind any organiser hands over.
2. **The catalogue.** Elasticsearch holds every talk, speaker, sponsor and outlet. Long text is
   cut into short passages, and each passage is stored twice: as words, and as a list of 384
   numbers that capture its meaning.
3. **Three ways to search.** Words finds exact terms. Meaning finds the right idea in different
   words. Blended runs both and merges the two ranked lists.
4. **The match.** An outlet's KubeCon assignment and its standing beat become those same
   meaning numbers and search the programme, the assignment counting more: the talks and
   sponsors it would want to cover, with the passage that made each one match.
5. **The page.** One simple web page on this laptop. No login, no internet needed.

## Why each choice

- **Words and meaning together:** each fails where the other succeeds. Words can't see that
  "survive a traffic spike" means autoscaling; meaning blurs exact names like "SLSA Level 3".
- **How they are merged:** each list votes; a result gets more points the higher it ranks in
  each, and the totals decide the order. A standard method, reciprocal rank fusion.
- **Short passages:** the meaning model only reads about 180 words, and a sponsor's material
  is far longer. Cutting it up also lets the page show *which* passage matched.
- **A small model on the laptop:** free, private, fast, works offline. It finds meaning; it
  doesn't write anything.
- **Elasticsearch:** it does words, meaning and filters in one place, and it is the track.
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

## Built on the day, one line per piece

- **Loading (B1, 11:03):** One command reads the spreadsheets, cuts every talk, speaker,
  sponsor and outlet into passages of about 120 words (2,209 in all), turns each passage into 384
  numbers with the small meaning model on the laptop, and loads them into two brand-new catalogues
  in about 12 seconds; a search of the loaded text for email addresses finds none.
- **Three ways to search (B2, 11:07):** From Terminal, one command searches the programme by words
  (exact terms; it can come back empty, which is information), by meaning (the nearest idea in any
  wording; it always returns something), or blended (each list votes, a result gets more points the
  higher it ranks in each, and the totals decide), and shows the passage that made each result match;
  a compare mode runs all three at once so you can watch them disagree. Measured 9 November: "SLSA
  Level 3" is won by words (Docker and ActiveState, the two sponsors whose own text says it); the Black Friday sentence gets nothing from
  words and cloud-cost and autoscaling companies from meaning (North first, the Start-Up Kedify fifth); the GPU-isolation sentence gets Edera from words and vCluster from
  meaning, with the next four close behind.
- **Elastic Cloud (11:24):** The same two catalogues now live in an Elastic Cloud serverless
  project; the code uses the cloud when its settings file is filled in and the laptop engine
  otherwise, so the demo has a fallback if the wifi fails. Loading to the cloud took 25 seconds
  and the three demo searches give the same top results there as on the laptop.
