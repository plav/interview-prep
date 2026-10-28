# Interview and job prep

Everything I use to prepare for software engineering interviews: tailored CVs and cover letters, a job tracker, practice tools, cheat sheets, and an AI coding skill.

## What's here

| Folder | What it holds |
| --- | --- |
| [`cv/`](cv/) | Tailored CVs and cover letters, in Word (editable) and PDF (ready to send), plus a guide to which one fits which job |
| [`job-search/`](job-search/) | `job-listings.html`: software jobs in Northern Ireland, Ireland and UK remote (October 2026), with the CV and letter to send for each |
| [`practice/`](practice/) | Two practice tools that open in any browser (see below), plus the source used to build the cheat-sheet practice site |
| [`cheat-sheets/`](cheat-sheets/) | Engineering cheat sheets across 13 topics, from foundations to AI-assisted engineering |
| [`skills/`](skills/) | `library-docs`: a Claude skill that checks current library documentation before writing code |

## Practice tools

Download an HTML file and open it in a browser. No install, no account. Progress is saved in that browser only.

- **`practice/interview-gym.html`**: one system design question a day (350 in the backlog, Devmaxx-style), streak and levels, role prep questions, the cheat-sheet question bank, design drills, and a "Say it well" section with answer shapes, a phrase bank and before-and-after examples.
- **`practice/interview-practice.html`**: 536 questions from the cheat sheets, with timed answers, model answers, weak-versus-strong examples and progress by topic.

The AI buttons ("Get feedback", "Say it better") only work when the pages are opened inside Claude; everything else works anywhere.

## Rebuilding the practice site

The cheat-sheet practice site is generated from plain-text question files:

```bash
cd practice/interview-practice-source
python3 build.py          # writes interview-practice.html
```

Question files live in `data/`, one per topic, in this format:

```
#DOC <doc name>
#SHEET <sheet name>
Q <main question>
A <30-second answer>
F <follow-up question> || <answer>
W <weak answer>
S <strong answer>
I <interview question> || <answer>
```

## Using the library-docs skill

- **Claude (web or app):** upload `skills/library-docs.skill` under Settings → Capabilities → Skills.
- **Claude Code:** copy `skills/library-docs/` to `~/.claude/skills/library-docs/`.

Then ask for code that uses a library, or say "use library-docs". It checks the docs for the exact version (via the Context7 MCP server if installed, otherwise official docs on the web) and says what it checked.

## Notes

- Contact details are deliberately left off the CVs and letters; add them before sending (see [`cv/README.md`](cv/README.md)).
- No licence is granted: all rights reserved.
