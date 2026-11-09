# Where this data comes from

**Programme, speakers, sponsors, media partners:** KubeCon + CloudNativeCon North America 2026
programme, The Linux Foundation, CC BY 3.0. Copied once on 4 November 2026 from the event's
public schedule and sponsor directory; the live pages have changed slightly since. Email
addresses on those pages were dropped. Logos and speaker photos are not included: the licence
does not cover logos, and no permission has been asked for photos.

**Files**
- `sessions.csv` — 601 rows: 501 talks and 100 events (`kind` says which).
- `speakers.csv` — 715 rows, as listed on the public schedule.
- `sponsors.csv` — 226 of the 229 listed sponsors. Three are left out because nothing usable
  was found for them (Loophole Labs, MyDecisive, VATES).
- `media-partners.csv` — the 10 media partners the conference lists.
- `outlets.csv` — one profile per media outlet, see below.

**Written by AI, and labelled so:**
- Every `sponsors.csv` column starting `ai_` was drafted by Claude (Anthropic) on 4 November
  2026 from that company's own public homepage and About page, label "From their website,
  summarised by AI". The other columns are the conference's own listing. Six were drafted from
  the conference listing alone, because the website could not be read (`ai_source_quality`
  says "conference only").
- `outlets.csv`: eight of the ten real partners, drafted by Claude on 5 November 2026 from
  each outlet's own public pages and reshaped on 8 November from the same pages (SD Times and
  theCUBE are left out: nothing usable could be read from their sites). Real outlets have no
  KubeCon assignment, because none of their pages states one and it is not ours to invent; `edited_by_aaron` says which Aaron has since rewritten. The six
  rows marked SAMPLE are invented examples, not real outlets; two of them, the Hello World
  Gazette and the Breach Chronicle, were named by Aaron on 8 November as test cases, with
  answer keys written beforehand.

The sponsors' and outlets' websites themselves are not included: they belong to those
companies, and the outlets' pages name journalists.
