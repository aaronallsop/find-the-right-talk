# Review instructions for this repository

This is a hackathon entry, "Find the Right Talk": a Python package (`ftrt/`) that loads the KubeCon programme
into two Elasticsearch catalogues and searches them by words, by meaning, by Elastic's ELSER, blended, and
re-ranked, with a small Flask page. This pull request is for review only and will not be merged. Please
comment; do not push fixes or suggest auto-applied changes.

Please look hardest at:

1. **Correctness bugs**: wrong results, crashes, results that change depending on how many are asked for,
   ties broken differently between runs, an ELSER or re-ranker failure that blanks a whole search instead of
   being left out.
2. **Secrets**: anything that could print, log, return to the browser or commit a password, API key, or the
   contents of a settings file (`~/elastic-cloud/.env`, `~/elastic-start-local/.env`).
3. **Touching anything not ours**: the code may create, change or delete only the catalogues `ftrt-programme`
   and `ftrt-outlets` and only Agent Builder objects whose id starts with `ftrt`. Flag any path that could reach
   another index or object.
4. **Privacy on the page**: it must listen on 127.0.0.1 only, never port 5000, 5060 or 5061, with Flask's
   debugger off; typed text must never be stored, logged or put in a URL.
5. **The blend**: reciprocal rank fusion with k = 60, the outlet's KubeCon assignment (and a sponsor's
   "showing at KubeCon") counting double; every list ranked to a fixed depth so the order does not depend on
   how many results are shown.

Less important: style, naming, and comments; the notes and README are plain-words documents for a
non-programmer and are out of scope.
