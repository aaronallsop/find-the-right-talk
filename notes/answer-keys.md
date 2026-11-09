# Answer keys — what the match should find, written before anything was built

Written Sunday 8 November, before the day (corrected the same evening by an independent review: JetBrains, Splunk, Orca and the agents count), by reading the sponsor spreadsheet, not by running
any search engine. An answer key a search engine wrote would only grade it against itself. The
two outlets are invented samples (rows in `data/outlets.csv`). **Their name, audience, standing
beat and KubeCon assignment are Aaron's**; the companies below are Claude's first reading of the
sponsors' own descriptions, for Aaron to check as the editor.

## The shape of an outlet (Aaron, 8 November)

Every outlet has three parts, as a real publication does:
- **Audience:** who reads it.
- **Standing beat:** what it always covers (`what_they_cover`, `beat`).
- **This event's assignment:** what it is specifically hunting for at KubeCon
  (`kubecon_assignment`). A company can fit the standing beat and still not be the assignment.

The beat and assignment lines are in the editor's own words, not lifted from any company's copy,
so the words search cannot pass by echo. And a profile says only what the outlet *does* cover: a
line like "we never cover security" would put "security" into its meaning and pull security
companies towards it.

## How to score it on Monday (after M2 works, about 13:30)

The match uses the assignment plus the standing beat, the assignment counting more (Aaron,
8 November). Run it for each outlet, sponsors only, top 10, three ways (words, meaning,
blended). If standing-beat-only companies crowd out the assignment, the beat is weighing too
much: lighten it before touching anything else.
Write down for each way:
- how many **assignment** companies are in the top 10;
- where the **hidden gem** lands;
- whether any **standing beat only** company or **trap** is above any assignment company.

A pass: all must-finds in the blended top 10, the hidden gem in the top 10, nothing from the
lower groups above the gem. If it fails, fix the outlet's wording first, re-run; code comes last.
Never edit this file to fit the results.

## Hello World Gazette (the warm-up: should simply work)

- **Audience:** developers who want to stay up to date with the new tools coming out for
  programming and building software.
- **Standing beat:** new developer tools and releases; languages and frameworks; how developers
  write, test and ship code; open-source tools developers rely on.
- **KubeCon assignment:** AI agents built for developers, agents that help you write code.

| Group | Company | Why, from its own description |
|---|---|---|
| Must find (assignment) | Coder (Silver) | Managed workspaces where developers and coding agents work |
| Must find (assignment) | Momentic (Silver) | An AI agent that tests apps and finds bugs |
| Must find (assignment) | Faros (Silver) | Tracks what coding agents cost against the work shipped |
| **Hidden gem** | **mirrord by MetalBear (Start-Up)** | Lets a coding agent try changes against a live test environment without deploying |
| Should also do well | Docker (Platinum) | Sandboxes for coding agents, at its booth |
| Should also do well (corrected at review) | JetBrains (Silver) | Programming tools, and also Air, "an agentic development environment for teams building software with AI agents": it does fit the assignment |
| Standing beat only: should rank lower | KodeKloud (Silver) | Teaches developers, through video courses, not agents |
| Trap | Endor Labs (Silver) | AI-written code, but its story is security holes |

## The Breach Chronicle (the hard test, and the demo outlet)

- **Audience:** people who work in cybersecurity, and people interested in it who want to know
  what is happening right now.
- **Standing beat:** news about security breaches as they happen: who was hit, how, and what
  was done about it.
- **KubeCon assignment:** how AI agents are being built, *either* to help people working in
  cybersecurity, *or* to keep AI agents themselves safe inside the companies using them.

The assignment has two halves. The test is whether the match finds **both**, not just one, and
keeps ordinary security companies (breaches, yes; agents, no) below them.

| Group | Company | Why, from its own description |
|---|---|---|
| Must find: agents that help security teams | Maze (Start-Up) | Its agents investigate vulnerabilities and work out which are really exploitable |
| Must find: agents that help security teams | Emphere (Start-Up) | Its agents patch known vulnerabilities in container images |
| Must find: agents that help security teams | Endor Labs (Silver) | Uses AI agents to find and fix vulnerabilities in code |
| Must find: keeping agents safe | Edera (Silver) | Runs every agent in its own hardware-isolated zone |
| Must find: keeping agents safe | Cosmonic (Silver) | Each agent in its own sandbox, no access unless granted |
| Must find: keeping agents safe | Teleport (Platinum) | Gives agents identities and short-lived access |
| Must find: keeping agents safe | Archestra AI (Start-Up) | Controls which data, tools and actions agents can reach |
| **Hidden gem** | **Vijil (Start-Up)** | Finds, tests, guards and monitors agents so a company can show they are trustworthy |
| Standing beat only: should rank lower | Akamai, RapidFort, Echo | Security companies whose descriptions say nothing about agents (Splunk removed at review: it mentions "the agentic era") |
| **Partial word trap** | Orca Security (Silver) | Calls itself "agentless", but also finds the AI agents running in a cloud: a fair middle result, not a must-not |

**The line for the judges, if it works:** "113 of the 226 sponsors mention AI agents. My breach-news outlet
came to KubeCon with one assignment, and the match found both halves of it, including Vijil, a
start-up, while keeping the ordinary security companies out of the way." **If it doesn't work, that is also a demo:** it shows exactly where a person
still needs to read.
