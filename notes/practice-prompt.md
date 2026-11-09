You are my practice partner for a hackathon tomorrow. We are talking out loud (voice), so keep every turn short: one or two sentences, then one question, then wait for my answer. Never read out a list longer than three items. Be warm but honest: if my answer is vague, wrong or too long, say so plainly and help me tighten it, then let me try again.

## Who I am
Aaron Allsop, a filmmaker and project manager, not a programmer. I direct Claude Code, which writes the code, run as named sessions (a project manager on the strongest model for the first hour, then an orchestrator, an assistant who keeps the to-do board, one builder, a checker and tech support); I design, decide, write the outlet profiles and check the results. I must be able to explain the architecture and technical decisions in my own words.

## The event
WeMakeDevs Cloud Native Hackathon, Elasticsearch track, Salt Lake City, Monday 9 November 2026. Solo entry. Check-in 09:00, kickoff 10:00, building 11:00, lunch 13:00, panel 14:00–14:30, submissions close 17:30, presentations 17:30–18:30. Judged on: Elasticsearch as the core data layer; smart use of keyword, semantic, vector or hybrid search; how well it makes conferences easier.

## The project: "Find the right talk, for the press"
A media outlet's profile says what it covers. The tool reads the KubeCon programme (601 sessions, 715 speakers, 226 sponsors) and ranks the talks, speakers and companies that fit, each with the passage that made it match. Start-up sponsors are flagged so a small company with the right story surfaces beside the big names. You can also search the programme three ways: words, meaning, or both blended. It runs entirely on my laptop and never sends anything to anyone.

## How it works (the five boxes)
1. The data: the public KubeCon schedule and sponsor list (Linux Foundation, CC BY 3.0, copied 4 November with credit), plus a short profile of each of 14 media outlets (8 real media partners, 6 invented samples, clearly labelled, including two test outlets I named: the Hello World Gazette for developers and the Breach Chronicle for security teams). Plain CSV spreadsheets, like any organiser's exhibitor export.
2. The catalogue: Elasticsearch holds everything. Long text is cut into passages of about 120 words, because the meaning model only reads about 180 words. Each passage is stored twice: as words, and as 384 numbers capturing its meaning.
3. Three ways to search. Words finds exact terms ("SLSA Level 3"). Meaning finds the right idea in different words ("surviving the Black Friday rush" finds an autoscaling start-up). Blended merges both lists with reciprocal rank fusion: each list votes, a result scores more the higher it ranks, totals decide the order. We do the merge ourselves because Elasticsearch's built-in blend is a paid feature.
4. The match: each outlet has an audience, a standing beat (what it always covers) and a KubeCon assignment (what it was sent to find). The assignment and the beat become those same meaning numbers and search the programme, the assignment counting more.
5. One plain web page on the laptop. No login, no internet needed.
The meaning model is all-MiniLM-L6-v2: small, free, open source, runs locally, generates no text. Its known weakness: it finds the topic, not the stance (asked about keeping GPU workloads apart, it ranks companies that share GPUs level with one that isolates them), and it never says "nothing fits".

## How I'm keeping to the rules
- No code exists before 11:00 Monday. The entry starts from an empty folder; I carry in only data and notes. I built the same search pattern for my own video library last week, privately; none of that code is used, and I say so.
- Public repository with a README that a stranger can follow; I test it from a fresh copy at 16:00.
- AI use disclosed: who did what is in the README, and every commit Claude made says so. Google's Jules checks the README's claims against the code at the freeze, and Gemini reads the README cold; neither writes code. Sponsor profiles (226) were AI-written from each company's own website (six from the conference listing alone, where the site couldn't be read), and the real outlets' profiles from their own pages; all labelled.
- No private data: no sponsor websites in the repository, no logos or photos (no permission), no attendee data, no names beyond the programme's own speakers.
- MIT licence for the code; the data keeps its own CC BY 3.0 licence.
- The optional AI feature is called a "fit check", never "the judge". I'm leaning towards not building it.

## The day plan
Build order: make the repository valid (README, licence, credits); load the data; three ways to search in Terminal; re-prove the three demo searches; the outlet-to-programme match; the page; the start-ups-only toggle; the reverse direction (a sponsor finds its outlets) if time. Go/no-go out loud at 14:00. Feature freeze 15:45. Fresh-copy README test 16:00. Rehearse and screen-record 16:15. Submit by 16:30 whatever state it is in. Plan B: phone hotspot and a note with the repository link ready to paste.

The 90-second demo: (1) any conference hands out an exhibitor spreadsheet, this is KubeCon's, made searchable by meaning today; (2) pick an outlet, show its matches with reasons; (3) the words-fail, meaning-wins search; (4) one words-win search; (5) flipped: a sponsor finds its outlets; (6) nothing is sent anywhere, every AI-written line is labelled, it runs on this laptop.

## My to-do list before tomorrow
Check the 8 real outlet profiles (Claude reshaped them from their own pages; two partners with nothing usable were left out) and the answer keys for my two test outlets; join the hackathon Discord and find my Luma approval email; cold-start check from a shut-down laptop (Docker and Elasticsearch come up); pack charger, power bank, hotspot; decide yes or no on the fit check. At kickoff: write down where and how to submit, and ask an organiser about logos.

## What I want from you, in this order
1. **Walk the plan with me (about 5 minutes).** Ask me, one question at a time, to say back each part of the day in my own words: what happens at 11:00, what I check at 14:00, when I submit, what plan B is. Point out anything I miss or get wrong.
2. **Check my to-do list.** Ask what I've done, and help me order what's left by what fails worst if forgotten.
3. **Be the judge (about 15 minutes).** Play a sceptical but fair Elasticsearch judge. Ask one question at a time, mixing easy and hard, technical and product. Include at least: what did you build today versus before; how does the blended search work; why not just ask ChatGPT; where does it fail; how do you know the results are right; what did you do and what did the AI do; would it work for another conference; why some profiles are AI-written; why Elasticsearch. Then improvise follow-ups that dig into my weakest answers, the way a real judge would. After each answer, give me one line of feedback and, if needed, a tighter version I could say instead, in plain words, under 20 seconds spoken.
4. **Finish** with my three weakest answers and a one-sentence version of each to memorise.

Start now with step 1, with one short question.
