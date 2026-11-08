# AgentOps Class Deck — Canva Presentation Brief

**Course:** IST 688 · Multi-Agent Systems teach-in  
**Working title:** AgentOps: seeing what multi-agent systems actually did  
**Format:** Canva Presentation · Widescreen 16:9  
**Timing:** about 10 minutes talk + about 10 minutes lab (classmates may already be using the app during the talk)  
**Audience:** students  
**Build note:** Designed class presentation — diagrams, hierarchy, readable type. Do **not** use a sparse outline-only dark template.

## Global design system (apply to every slide)

| Token | Direction |
|-------|-----------|
| Background | Soft cool off-white / mist (`#EEF3F4` to white). Subtle atmosphere with a faint nodes-and-edges motif in the far background — not flat purple gradients, not warm cream + terracotta broadsheet. |
| Primary | Deep navy (`#0F2C3A`) for titles |
| Accent | Teal (`#0E7C7B`) for section kickers, connectors, positive callouts |
| Emphasis | Warm clay (`#C45C26`) for contrast panels / warnings only |
| Body text | Near-black ink (`#1B242C`), 24–32 pt for body; titles 40–56 pt |
| Type | Expressive but readable: a clean geometric sans for UI/diagrams + a slightly tighter display sans for titles (avoid Inter/Roboto/Arial defaults if Canva offers better pairings like “Montserrat + Source Sans” or “Poppins + Lato”) |
| Layout | Generous margins; one job per slide; real diagram anchors; no card clutter in the hero; avoid pill clusters and stat strips |
| Footer | Small: `IST 688 · AgentOps` left · slide number right |
| Motion (optional in Canva) | 2–3 intentional motions only: (1) title node motif fade-in, (2) arrow draw on the single-agent loop, (3) Function_A / Function_B panels slide in together |

**Hard stops for all on-slide copy and notes:** never use the banned print-stem phrasing (or close variants that open with that stem); no proprietary orchestration names; no cast/casting wording; no Anthropic model names; no coordinator-plus-two-workers framing; no columnar storage-engine lecture; no invented percentages, dollars, compression ratios, or latency targets; no authorship lines; no hidden lab-solution slide.

---

## Slide 1 — Title

### Slide title
AgentOps: seeing what multi-agent systems actually did

### On-slide copy
**Kicker:** IST 688 · Multi-Agent Systems teach-in

**Title:** AgentOps: seeing what multi-agent systems actually did

**Support:** From the functions lecture to named spans, a non-blocking logger, and a compact readable log.

**Left panel:** Talk · about 10 minutes  
Why prints go dark · traces as spans · AgentOps_Logger · what to record · TOON as a readable form

**Right panel:** Lab · about 10 minutes  
Start the app now from the next slide so you can try it during the talk.

### Visual direction
Full-bleed navy hero band across the top ~55% of the slide (not an inset card). Faint teal nodes-and-edges constellation in the upper-right of the navy field. Brand/title is the dominant type. Two clean white timing panels sit on the soft ground below the hero — no stacked stats, no badges over the hero image. One composition, not a dashboard.

### Speaker notes
Welcome the class. This teach-in connects today’s functions lecture to watching several agents work at once. Timing is about ten minutes of talk and about ten minutes of lab. Tell them the next slide has the repo and README paste block so they can start the app while Gil and Scott present.

---

## Slide 2 — Start the app now

### Slide title
Start the app now

### On-slide copy
**Kicker:** DO THIS NOW · WHILE WE TALK

**Title:** Start the app now

**Subtitle:** Open the repo, copy the README paste block, and give it to your coding agent.

**Step 1:** Open the repo  
https://github.com/GilRaitses/ist688-agentops-lab

**Step 2:** Copy the paste block  
At the top of README.md — easy to select and copy

**Step 3:** Give it to your coding agent  
Adds a page to your existing private Streamlit course app

**Bottom callout — What the paste block asks your agent to do:**  
Add `pages/AgentOps.py` (or similar) to your existing course app · adapt public `app.py` · use `OPENAI_API_KEY` or nested `openai.api_key` already in Streamlit secrets · never paste a key into chat · no Anthropic/Claude · do not change app visibility

### Visual direction
Three equal horizontal step panels with large teal numbered discs (1–2–3). Repo URL set in bold monospace-friendly type so it is readable from the back of the room. Bottom teal-tinted callout bar with the agent instructions in one dense but readable paragraph — hierarchy is steps first, details second. No QR clutter unless Gil adds one later.

### Speaker notes
Pause here. Ask everyone to open the GitHub link, copy the fenced paste block at the top of the README, and hand it to their coding agent. The agent should add the lab as a page inside their existing private course Streamlit app and reuse the OpenAI key already in that app’s secrets. They can keep configuring while the conceptual talk continues.

---

## Slide 3 — Where class left off

### Slide title
Where class left off: one model and a tool

### On-slide copy
**Kicker:** FROM THE FUNCTIONS LECTURE

**Title:** Where class left off: one model and a tool

**Subtitle:** Still one agent, one context, and one visible sequence.

**Flow (four stages):**  
1 · User asks — A question enters the loop  
2 · Model requests — May ask for a function  
3 · App runs it — Function executes  
4 · Result returns — Model can answer

**Callout:** Familiar case: looking up weather  
You can still follow the whole path. One agent. One context. One sequence you can read top to bottom.

### Visual direction
Horizontal process: four rounded stages connected by short teal chevrons/arrows (Gemini-style linear API path). Soft teal footer callout for the weather example. Calm, linear, “you can see everything” mood — this slide is the clean baseline before concurrency.

### Speaker notes
Walk the functions-lecture loop. Emphasize that with one agent, students can still see the whole path. Weather lookup is a familiar case. Hold this clarity for one beat before the next slide breaks it.

---

## Slide 4 — What changes with more agents

### Slide title
What changes when more than one agent is involved

### On-slide copy
**Kicker:** THE CORE CHALLENGE

**Title:** What changes when more than one agent is involved

**Subtitle:** Non-deterministic paths branch. Visibility is no longer free.

**Left column — Single-agent loop:**  
Ask → Think → Call tool → Answer

**Right column — Concurrent functions:**  
Shared user turn  
Function_A · runs now  
Function_B · runs at the same time

**Bullets under the right diagram:**  
• Path is no longer one visible sequence  
• A mistake can hide in more than one place  
• Ordinary console output loses the story

### Visual direction
Split composition (Gemini “linear vs branching” visual). Left: tidy vertical stack. Right: one parent node splitting into Function_A and Function_B panels that appear side-by-side. Warm clay accent only on the concurrent side to signal friction. This is the “black box of concurrent execution” idea without proprietary orchestration language.

### Speaker notes
Contrast the single-agent loop with two functions running at once. Keep the focus on visibility: the run path is no longer one readable sequence, and a mistake can hide in more than one place.

---

## Slide 5 — Why print statements go dark

### Slide title
Why ordinary print statements go dark

### On-slide copy
**Kicker:** WHY PRINTS FAIL

**Title:** Why ordinary print statements go dark

**Subtitle:** Print statements leave out who called whom, how long a step took, and how many tokens it used.

**Three panels:**  
Who called whom? — Concurrent lines interleave. Caller and target are missing.  
How long did it take? — A print has no `latency_ms` attached to the span.  
What did it cost? — Input and output tokens are not in the scrap of console text.

**Takeaway bar:** A multi-agent run needs a trace — a sequence of named spans — not a scrap of console output.

### Visual direction
Three equal problem panels with a thin clay accent stripe on the left edge of each. Strong takeaway bar across the bottom in warm tint. Keep the subtitle as written above; do not revert to the banned print-stem phrasing.

### Speaker notes
Make the takeaway concrete: when agents run together, print statements leave out caller, target, latency, and tokens. Silent execution failures get missed. The class needs a trace of named spans.

---

## Slide 6 — Reasoning traces as named spans

### Slide title
A reasoning trace is a sequence of named spans

### On-slide copy
**Kicker:** REASONING TRACES

**Title:** A reasoning trace is a sequence of named spans

**Subtitle:** Thought → tool call → result. Parent and child make caller and target visible.

**Left vertical stack:**  
Thought — Planning before action · What the step intends to do  
Tool call — Named call with arguments · The action that leaves the model  
Result — What came back · Observation the next step can use

**Right hierarchy panel — Parent / child:**  
parent span · user turn  
  child · thought  
  child · tool call  
  child · result

### Visual direction
Gemini-style vertical deconstruction on the left (Thought → Action/Tool → Observation/Result) with connecting stems. Right side shows a parent/child tree so “caller” and “target” become spatial, not abstract. Teal for thought/tool, clay for result is fine if contrast stays readable.

### Speaker notes
A reasoning trace is not a scrap of console text. It is a live history of thought, action, and result. Draw the parent and child so students can see who called whom.

---

## Slide 7 — AgentOps as a non-blocking logger

### Slide title
AgentOps as a non-blocking logger

### On-slide copy
**Kicker:** AGENTOPS LOGGER

**Title:** AgentOps as a non-blocking logger

**Subtitle:** The logger sits beside the work — not inside the answers.

**Three columns:**  
Function_A — Runs its work · Keeps going  
Function_B — Runs at the same time · Keeps going  
AgentOps_Logger — Records each span · Beside them

**Pipeline strip:**  
Span happens → Push to async queue → Functions do not wait → Flush after both finish

### Visual direction
Three peer columns (not a boss-and-workers hierarchy). Function_A and Function_B share teal headers; AgentOps_Logger gets navy to mark the side-channel. Bottom pipeline is a Canva “process” row with arrows — the non-blocking idea from Gemini’s early AgentOps pipeline slide, renamed for class (no proprietary systems).

### Speaker notes
Stress that AgentOps_Logger sits beside the work. Function_A and Function_B keep running while records enter an async queue. Logging must not make the functions wait.

---

## Slide 8 — What to record

### Slide title
What to record

### On-slide copy
**Kicker:** SCHEMA

**Title:** What to record

**Subtitle:** Lab fields checked with a Pydantic model before a record enters the log.

**Field list:**  
`caller` — Who started the span  
`target` — What was called  
`latency_ms` — How long the step took  
`input_tokens` — Tokens into the step  
`output_tokens` — Tokens out of the step

**Side panel — Pydantic check:**  
A malformed record is rejected before it enters the log.  
Stay with these lab fields.

### Visual direction
Left: stacked field rows with monospace field names in teal-tinted chips. Right: solid navy panel for the Pydantic message. Clean schema poster — no fake dashboards, gauges, or invented metric graphs.

### Speaker notes
These are the fields students implement. Pydantic rejects malformed records before they enter the log. Stay with the lab fields.

---

## Slide 9 — Compact TOON log form

### Slide title
Writing the log in a compact, readable form

### On-slide copy
**Kicker:** COMPACT LOG FORM

**Title:** Writing the log in a compact, readable form

**Subtitle:** TOON: field names once at the top, then one row per span.

**Left — What TOON is for:**  
1. Header declares field names once  
2. Each span is one row under that header  
3. Easier to scan than verbose nested JSON  
4. A readable log form for class — not a measured production saving

**Right — Example shape:**  
```
trace_stream[2]{caller,target,latency_ms,
               input_tokens,output_tokens}:
  Function_A,search_tool,480,320,185
  Function_B,search_tool,510,350,190
```

**Caption under example:** No compression ratios. No token-savings percents. Just a compact readable form.

### Visual direction
Two-column layout: explanatory list left, code panel right on a light code background. The example numbers are shape demos for the format, not production claims. Keep TOON framed as readable compaction for class.

### Speaker notes
Show the header-plus-rows shape. TOON is how we keep the log readable. Do not present it as a measured production saving.

---

## Slide 10 — What a trace helps you notice

### Slide title
What a trace helps you notice

### On-slide copy
**Kicker:** WHY IT HELPS

**Title:** What a trace helps you notice

**Subtitle:** Silent execution failures become visible when spans are named and linked.

**Four notices:**  
1 · Who called whom — Caller and target on every span  
2 · How long a step took — `latency_ms` on the record  
3 · How many tokens it used — `input_tokens` and `output_tokens`  
4 · Where a step went wrong — Malformed records rejected by schema

### Visual direction
2×2 grid of clear notice panels with large teal numbers. One idea per panel. Calm “usefulness” slide — debugging and cost visibility — without enterprise retention or storage-engine claims.

### Speaker notes
A complete trace lets you see who called whom, how long a step took, and how many tokens it used. That is how silent failures become visible.

---

## Slide 11 — Lab brief

### Slide title
Lab brief: build a small AgentOps logger

### On-slide copy
**Kicker:** IN-CLASS LAB · ABOUT 10 MINUTES

**Title:** Lab brief: build a small AgentOps logger

**Subtitle:** Not a database product. Repo + README paste block were shared at the start of the talk.

**Four tasks:**  
1. Define a Pydantic record with caller, target, latency, and token counts.  
2. Run Function_A and Function_B at the same time; push valid records to an async queue.  
3. Serialize the collected records into a compact TOON string.  
4. Print the trace after both functions finish.

**Rubric panel (10 pts):**  
3 concurrency  
4 schema  
3 TOON  
Four lab tasks total.

**Bottom bar:**  
Same repo from the opening setup slide  
https://github.com/GilRaitses/ist688-agentops-lab  
Uses Streamlit secrets already in your course app (`OPENAI_API_KEY` or `openai.api_key`)

### Visual direction
Tasks as a numbered stack on the left; navy rubric panel on the right. Bottom teal bar repeats the repo URL (already introduced on slide 2) without pretending this is the first time students see it. No solution code on this student deck.

### Speaker notes
Keep this short. Setup already happened. Students should be on the four tasks and the 3 / 4 / 3 rubric. Remind them the page lives in their private course app and uses existing Streamlit secrets.

---

## Slide 12 — Questions

### Slide title
Questions

### On-slide copy
**Title:** Questions

**Support:** Open floor after the talk or after the lab — whichever the session needs.

**Footer mark:** IST 688 · AgentOps

### Visual direction
Full navy field, teal left rail, centered large title. Minimal text. Breathing room after dense content. Optional faint node motif matching slide 1 for bookend continuity.

### Speaker notes
Open floor for questions after the talk or after the lab, whichever the session needs. No hidden solution slide in the student deck.

---

## Canva build checklist

1. Create a widescreen Presentation (16:9).  
2. Apply the global palette and type pairing once; duplicate a master layout.  
3. Build slides 1→12 in order; do not skip the setup slide.  
4. Paste on-slide copy exactly as written above (student-facing).  
5. Add speaker notes from each slide section into Canva’s notes panel.  
6. Self-check: search the finished Canva doc for banned stems and proprietary names before presenting.  
7. Do not add a lab-solution slide to the student file.
