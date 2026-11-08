# IST 688 AgentOps slide copy matrix

Purpose: fill each class slide with a required claim, vendor evidence from public docs and synthesized Canva-ready class text. Claim matrix at the store path `internal/sources/SLIDE_CLAIM_MATRIX.md` wins. Quotes below were retrieved from the linked pages. No invented quotes.

Visual tokens for Canva (Syracuse design system):
- Orange `#F76900`
- Blue `#000E54`
- White `#FFFFFF`
- Secondary text gray `#404040` when needed
- Do not use teal or cyan

Writing rules applied to synthesized class text:
- No filler use of "actually" or "actual"
- No em dashes, no en dashes used as pauses, no dramatic ellipses, no stacked hedges
- No arrows in prose, no semicolons, no Oxford comma
- Class names stay Function_A, Function_B and AgentOps_Logger
- Lab fields stay caller, target, latency_ms, input_tokens and output_tokens
- TOON is a class log form only
- No coordinator that splits work into workers on any class slide

Research coverage retrieved for this matrix:
- OpenTelemetry traces concepts and GenAI observability blog
- OpenAI Agents SDK tracing
- LangSmith observability concepts
- Langfuse data model, observation types, queuing and token tracking
- Arize Phoenix traces concepts and span dataframe export
- Datadog Agent Observability terms
- AgentOps product docs (spans and core concepts)
- W&B Weave ops, calls and traces

---

## Slide 1. Title

### Required claim
- This is an IST 688 Multi-Agent Systems teach-in about AgentOps.
- The topic is making a multi-agent run visible as named work, not as leftover console text.
- Timing is about 10 minutes of talk and about 10 minutes of lab.
- Classmates should start the app now and use it during the talk.

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| OpenTelemetry | traces / path | "Traces give us the big picture of what happens when a request is made to an application." | https://opentelemetry.io/docs/concepts/signals/traces/ |
| Langfuse | application tracing | "The core of this is application tracing — structured logs of every request that capture the exact prompt sent, the model's response, token usage, latency, and any tools or retrieval steps in between." | https://langfuse.com/docs/observability/overview |
| Phoenix | traces | "A trace records the paths taken by requests (made by an application or end-user) as they propagate through multiple steps." | https://arize.com/docs/phoenix/tracing/concepts-tracing/what-are-traces |
| Datadog | Agent Observability traces | "Each request fulfilled by your application is represented as a trace on the Agent Observability page in Datadog." | https://docs.datadoghq.com/llm_observability/ |
| OpenAI Agents SDK | tracing | "The Agents SDK includes built-in tracing, collecting a comprehensive record of events during an agent run: LLM generations, tool calls, handoffs, guardrails, and even custom events that occur." | https://openai.github.io/openai-agents-python/tracing/ |
| LangSmith | traces | "Traces are the record of what your agents did in production." | https://docs.langchain.com/langsmith/observability |

### Synthesized class text
**Headline:** AgentOps: named work you can see

**Body:**
- IST 688 Multi-Agent Systems teach-in
- Make a multi-agent run visible as named work not leftover console text
- Talk about 10 minutes · Lab about 10 minutes
- Start the app now and use it during the talk

**Visual note:** Blue `#000E54` title field. Orange `#F76900` accent on timing labels. White `#FFFFFF` ground.

---

## Slide 2. Start the app now

### Required claim
- Open https://github.com/GilRaitses/ist688-agentops-lab
- Copy the paste block at the top of the README
- Give that block to a coding agent
- The agent adds the lab as a page in the student's private Streamlit course app not as the home page
- The page uses the OpenAI key already stored in that app's Streamlit secrets
- Do not paste a key into chat

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| Class setup | n/a | This slide is class setup only. Do not replace it with vendor marketing. | Claim matrix research ask |

### Synthesized class text
**Headline:** Start the app now

**Body:**
1. Open https://github.com/GilRaitses/ist688-agentops-lab
2. Copy the paste block at the top of the README
3. Give that block to your coding agent
4. The agent adds the lab as a page in your private Streamlit course app not as the home page
5. The page uses the OpenAI key already stored in Streamlit secrets
6. Do not paste a key into chat

**Visual note:** Number steps in orange `#F76900` on blue `#000E54` headers. Repo URL in large readable type.

---

## Slide 3. Where class left off

### Required claim
- The functions lecture still has one agent one context and one visible sequence
- The familiar path: a question enters the model may request a function the app runs it the result returns so the model can answer
- A weather lookup is a fine example of that single path

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| Datadog | LLM inference / single LLM span | "A trace can contain a single LLM span, in which case the trace represents an LLM inference operation." | https://docs.datadoghq.com/llm_observability/quickstart/terms/ |
| OpenAI Agents SDK | default tracing of one run | "The entire Runner.{run, run_sync, run_streamed}() is wrapped in a trace()." | https://openai.github.io/openai-agents-python/tracing/ |
| Langfuse | tool observation | "tool represents a single action that does something, such as a function or API call (for example a weather API)." | https://langfuse.com/docs/observability/features/observation-types |
| LangSmith | trace as one operation | "A trace is a collection of runs for a single operation." | https://docs.langchain.com/langsmith/observability-concepts |

### Synthesized class text
**Headline:** Where class left off: one model and one tool

**Body:**
- Still one agent one context and one visible sequence
- Question enters · Model may request a function · App runs it · Result returns so the model can answer
- Weather lookup is a fine example of that single path

**Visual note:** One linear sequence in blue `#000E54`. Keep Function names off this slide.

---

## Slide 4. What changes with more than one function

### Required claim
- Function_A and Function_B can run at the same time
- The path is no longer one visible sequence
- A mistake can hide in more than one place
- Ordinary console output loses the story of who ran in what order and with what result

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| OpenTelemetry | sibling child spans | "That also makes it a sibling of the hello-greetings span." | https://opentelemetry.io/docs/concepts/signals/traces/ |
| OpenTelemetry GenAI | span tree with tool children | "Selecting a trace reveals the span tree: the top-level invoke_agent span with child chat spans for each LLM call and execute_tool spans for each tool invocation." | https://opentelemetry.io/blog/2026/genai-observability/ |
| Datadog | agent / nested spans | "Each trace contains spans representing each choice made by an agent or each step of a given workflow." | https://docs.datadoghq.com/llm_observability/ |
| Phoenix | nested spans | "Spans can be nested, as is implied by the presence of a parent span ID: child spans represent sub-operations." | https://arize.com/docs/phoenix/tracing/concepts-tracing/what-are-traces |
| OpenAI Agents SDK | concurrent context | "The current trace is tracked via a Python contextvar. This means that it works with concurrency automatically." | https://openai.github.io/openai-agents-python/tracing/ |

### Synthesized class text
**Headline:** What changes with Function_A and Function_B

**Body:**
- Function_A and Function_B can run at the same time
- The path is no longer one visible sequence
- A mistake can hide in more than one place
- Ordinary console output loses who ran in what order and with what result

**Visual note:** Split layout. Left stays linear. Right shows Function_A and Function_B side by side with orange `#F76900` stress.

---

## Slide 5. Why ordinary print statements go dark

### Required claim
- Exact required sentence: Print statements leave out who called whom, how long a step took and how many tokens it used.
- Concurrent lines interleave so caller and target are missing
- A print has no latency attached to the step
- Input and output tokens are not in the console text
- A multi-agent run needs a trace which is a sequence of named spans not a scrap of console output

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| OpenTelemetry | traces vs unstructured path | "One way to think of Traces is that they're a collection of structured logs with context, correlation, hierarchy, and more baked in." | https://opentelemetry.io/docs/concepts/signals/traces/ |
| Langfuse | tracing vs guesswork | "Therefore, debugging your application without any observability tool is more like guesswork." | https://langfuse.com/docs/observability/overview |
| Langfuse | structured request record | "structured logs of every request that capture the exact prompt sent, the model's response, token usage, latency, and any tools or retrieval steps in between." | https://langfuse.com/docs/observability/overview |
| Datadog | span metrics | "Metrics, such as input_tokens and output_tokens" | https://docs.datadoghq.com/llm_observability/quickstart/terms/ |
| OpenTelemetry GenAI | guessing without observability | "and without observability, you are guessing." | https://opentelemetry.io/blog/2026/genai-observability/ |

### Synthesized class text
**Headline:** Why ordinary print statements go dark

**Body:**
- Print statements leave out who called whom, how long a step took and how many tokens it used.
- Concurrent lines interleave so caller and target are missing
- A print has no latency attached to the step
- Input and output tokens are not in the console text
- A multi-agent run needs a trace: a sequence of named spans not a scrap of console output

**Visual note:** Three problem panels with orange `#F76900` left edge. Takeaway bar in blue `#000E54` on white.

---

## Slide 6. A reasoning trace is a sequence of named spans

### Required claim
- A trace is a sequence of named spans
- A useful span shape for class is thought then tool call then result
- A parent span and a child span make caller and target visible

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| OpenTelemetry | span | "A span represents a unit of work or operation. Spans are the building blocks of Traces." | https://opentelemetry.io/docs/concepts/signals/traces/ |
| OpenTelemetry | parent / child | "Spans can be nested, as is implied by the presence of a parent span ID: child spans represent sub-operations." | https://opentelemetry.io/docs/concepts/signals/traces/ |
| OpenAI Agents SDK | traces and spans | "Traces represent a single end-to-end operation of a \"workflow\". They're composed of Spans." | https://openai.github.io/openai-agents-python/tracing/ |
| OpenAI Agents SDK | parent_id | "parent_id, which points to the parent Span of this Span (if any)" | https://openai.github.io/openai-agents-python/tracing/ |
| Langfuse | observations / generations / tools | "Observations are the individual steps of your application: LLM calls, tool calls, retrieval steps, and so on. They can be nested to reflect the structure of your application" | https://langfuse.com/docs/observability/data-model |
| Langfuse | generation / tool | "generation logs generations of AI models incl. prompts, token usage and costs." / "tool represents a single action that does something, such as a function or API call" | https://langfuse.com/docs/observability/features/observation-types |
| Phoenix | TOOL / AGENT | "TOOL A Tool is a span that represents a call to an external tool such as a calculator or a weather API." / "AGENT A span that encompasses calls to LLMs and Tools." | https://arize.com/docs/phoenix/tracing/concepts-tracing/what-are-traces |
| LangSmith | run ≈ span | "If you are familiar with OpenTelemetry, you can think of a run as a span." | https://docs.langchain.com/langsmith/observability-concepts |
| AgentOps | hierarchy | "Every span exists within the context of a session, and most spans (other than the session itself) have a parent span that provides context." | https://docs.agentops.ai/v2/concepts/spans |
| Weave | Call ≈ span | "Calls are similar to spans in the OpenTelemetry data model." | https://docs.coreweave.com/products/wandb/weave/guides/tracking/tracing |

### Synthesized class text
**Headline:** A reasoning trace is a sequence of named spans

**Body:**
- A trace is a sequence of named spans
- Useful class shape: thought then tool call then result
- Parent span and child span make caller and target visible
- Vendor words you will hear later: span observation generation tool run Call

**Visual note:** Left stack thought / tool call / result. Right parent with nested children. Keep Function_A and Function_B out of vendor product names.

---

## Slide 7. AgentOps as a non-blocking logger

### Required claim
- AgentOps_Logger sits beside the work not inside the answers
- Function_A and Function_B keep running
- The logger records each span beside them
- Records go to an async queue so the functions do not wait
- The log is flushed after both functions finish

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| Langfuse | background processing | "In order to avoid slowing down your application, Langfuse doesn't send traces synchronously the moment they're created. Instead, Langfuse batches traces locally and sends them in the background, keeping your application fast and responsive." | https://langfuse.com/docs/observability/data-model |
| Langfuse | queue / flush | "Langfuse's client SDKs and integrations are all designed to queue and batch requests in the background to optimize API calls and network time." / "short-lived applications must explicitly call flush() before exiting." | https://langfuse.com/docs/observability/features/queuing-batching |
| Langfuse FAQ | non-blocking | "No. Langfuse SDKs send tracing data asynchronously in the background. Trace events are queued locally and flushed in batches, so your application's response time is not affected." | https://langfuse.com/docs/observability/overview |
| OpenAI Agents SDK | BatchTraceProcessor / flush | "The default BatchTraceProcessor exports traces in the background every few seconds, or sooner when the in-memory queue reaches its size trigger, and also performs a final flush when the process exits." | https://openai.github.io/openai-agents-python/tracing/ |
| OpenTelemetry | BatchSpanProcessor | "The OpenTelemetry SDK provides a set of default span and log record processors, that allow you to either emit spans one-by-on (\"simple\") or batched. Using batching is recommended" | https://opentelemetry.io/docs/languages/python/exporters/ |
| LangSmith JS note | background callbacks | "we also recommend setting the following explicitly to reduce latency: export LANGCHAIN_CALLBACKS_BACKGROUND=true" | https://docs.langchain.com/langsmith/observability/how_to_guides/trace_with_langchain |

### Synthesized class text
**Headline:** AgentOps_Logger sits beside the work

**Body:**
- AgentOps_Logger sits beside the work not inside the answers
- Function_A and Function_B keep running
- The logger records each span beside them
- Records go to an async queue so the functions do not wait
- Flush the log after both functions finish

**Visual note:** Three peer columns. Function_A Function_B in blue. AgentOps_Logger in orange accent. Keep the three columns as peers.

---

## Slide 8. What to record

### Required claim
Lab fields checked with a Pydantic model before a record enters the log:
- caller: who started the span
- target: what was called
- latency_ms: how long the step took
- input_tokens: tokens into the step
- output_tokens: tokens out of the step
- A malformed record is rejected before it is written

### Vendor evidence
| Lab field | Vendor mapping | Short quote | URL |
| --- | --- | --- | --- |
| caller | OTel parent / AgentOps parent | "parent_id, which points to the parent Span of this Span (if any)" / "most spans (other than the session itself) have a parent span that provides context." | https://openai.github.io/openai-agents-python/tracing/ · https://docs.agentops.ai/v2/concepts/spans |
| target | span name / tool name | "Name" on every span · "Tool Name: The name of the tool used" | https://opentelemetry.io/docs/concepts/signals/traces/ · https://docs.agentops.ai/v2/concepts/spans |
| latency_ms | start/end · duration | "Start and End Timestamps" · "Start time and duration" · "Timing and latency" | https://opentelemetry.io/docs/concepts/signals/traces/ · https://docs.datadoghq.com/llm_observability/quickstart/terms/ · https://docs.coreweave.com/products/wandb/weave/guides/tracking/tracing |
| input_tokens | gen_ai.usage.input_tokens / usage input | "gen_ai.usage.input_tokens and gen_ai.usage.output_tokens — token counts for each LLM call." · "Prompt Tokens: Number of tokens in the input" · Datadog metrics "input_tokens and output_tokens" | https://opentelemetry.io/blog/2026/genai-observability/ · https://docs.agentops.ai/v2/concepts/spans · https://docs.datadoghq.com/llm_observability/quickstart/terms/ |
| output_tokens | gen_ai.usage.output_tokens / completion tokens | Same sources as input_tokens · Langfuse usage_details keys `"input"` and `"output"` | https://langfuse.com/docs/observability/features/token-and-cost-tracking |
| schema reject | class Pydantic check | Vendor docs validate attributes at ingest. Class lab uses Pydantic before write. | Class claim |

### Synthesized class text
**Headline:** What to record

**Body:**
- caller: who started the span
- target: what was called
- latency_ms: how long the step took
- input_tokens: tokens into the step
- output_tokens: tokens out of the step
- Checked with a Pydantic model before a record enters the log
- A malformed record is rejected before it is written

**Mapping note (speaker only):** Keep lab field names on the slide. Map vendor parent to caller, name or tool to target, duration to latency_ms and usage tokens to input_tokens or output_tokens. Do not put span_id or parent_id on the student slide.

**Visual note:** Field list in monospace. Blue `#000E54` panel for the Pydantic reject line.

---

## Slide 9. Writing the log in a compact form

### Required claim
- TOON declares field names once at the top then writes one row per span
- That is easier to scan than verbose nested JSON
- It is a readable log form for class not a measured production saving
- No compression ratio. No token-savings percent.

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| Langfuse | observations table | Observations table rows with columns such as type name latency and shared trace fields: "Langfuse stores one observations table, and each row holds the observation-level data plus a copy of the trace-level attributes." | https://langfuse.com/docs/observability/data-model |
| Phoenix | spans as dataframe | "Download all spans as a dataframe" / "Exports all spans in a project as a dataframe" | https://arize.com/docs/phoenix/tracing/how-to-tracing/importing-and-exporting-traces/extract-data-from-spans |
| OpenTelemetry GenAI | nested JSON hard to read | "many observability platforms render them as raw JSON, making them difficult to read." | https://opentelemetry.io/blog/2026/genai-observability/ |
| TOON vendor use | none found | No retrieved vendor doc claimed TOON as a product log format. Keep TOON as the class form only. | Research note |

### Synthesized class text
**Headline:** Write the log in a compact readable form

**Body:**
- TOON declares field names once at the top then writes one row per span
- Easier to scan than verbose nested JSON
- A readable log form for class not a measured production saving
- No compression ratio. No token-savings percent.

**Example shape only:**
```
trace_stream[2]{caller,target,latency_ms,input_tokens,output_tokens}:
  Function_A,search_tool,480,320,185
  Function_B,search_tool,510,350,190
```

**Visual note:** Example on a light code panel. Caption under it restates "shape only."

---

## Slide 10. What a trace helps you notice

### Required claim
- Who called whom because caller and target are on every span
- How long a step took because latency_ms is on the record
- How many tokens a step used because input_tokens and output_tokens are on the record
- Where a malformed record was rejected

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| Datadog | end-to-end tracing | "View every step of your LLM application chains and calls to pinpoint problematic requests and identify the root cause of errors." | https://docs.datadoghq.com/llm_observability/ |
| Datadog | tokens latency | "Track token usage, error rates, and latencies for your LLM calls." | https://docs.datadoghq.com/llm_observability/quickstart/terms/ |
| LangSmith | debug with traces | "Use them to debug failures, monitor quality, and build the datasets you evaluate against." | https://docs.langchain.com/langsmith/observability |
| LangSmith | when to use a trace | "You are debugging why one operation failed or ran slow" | https://docs.langchain.com/langsmith/observability-concepts |
| Phoenix | latency and cost inspection | "Inspect the traces and spans of your application to identify sources of latency and cost" | https://github.com/Arize-ai/phoenix/blob/main/tutorials/tracing/langchain_tracing_tutorial.ipynb |
| OpenTelemetry GenAI | token and duration attributes | "Only metadata like model names, token counts, and durations are included." | https://opentelemetry.io/blog/2026/genai-observability/ |
| AgentOps | timeline / tree | "Timeline View: Shows the sequence and duration of spans" / "Tree View: Displays the hierarchical relationship between spans" | https://docs.agentops.ai/v2/concepts/core-concepts |

### Synthesized class text
**Headline:** What a trace helps you notice

**Body:**
1. Who called whom: caller and target on every span
2. How long a step took: latency_ms on the record
3. How many tokens a step used: input_tokens and output_tokens on the record
4. Where a malformed record was rejected

**Visual note:** 2×2 notice panels. Orange numbers on blue titles. No dollar figure.

---

## Slide 11. Lab tasks classmates can already be doing

### Required claim
Four tasks:
1. Define a Pydantic record with caller target latency and token counts
2. Run Function_A and Function_B at the same time and push valid records to an async queue
3. Serialize the collected records into a compact TOON string
4. Print the trace after both functions finish

Rubric: 10 points total 3 for concurrency 4 for the schema and 3 for TOON

Repeat: https://github.com/GilRaitses/ist688-agentops-lab

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| Class lab brief | n/a | Do not replace the four tasks or the rubric with vendor tutorials. | Claim matrix research ask |

### Synthesized class text
**Headline:** Lab brief: build a small AgentOps logger

**Body:**
1. Define a Pydantic record with caller target latency and token counts
2. Run Function_A and Function_B at the same time and push valid records to an async queue
3. Serialize the collected records into a compact TOON string
4. Print the trace after both functions finish

**Rubric (10 pts):**
- 3 concurrency
- 4 schema
- 3 TOON

**Repo:** https://github.com/GilRaitses/ist688-agentops-lab

**Visual note:** Tasks left. Rubric panel right in blue `#000E54`. Repo bar at bottom.

---

## Slide 12. Questions

### Required claim
- Open floor after the talk or while people are still working in the lab

### Vendor evidence
| Vendor | Term | Short quote | URL |
| --- | --- | --- | --- |
| none | n/a | No vendor research ask for this slide. | Claim matrix |

### Synthesized class text
**Headline:** Questions

**Body:**
- Open floor after the talk or while people are still working in the lab

**Visual note:** Full blue `#000E54` field. White title. Orange left rail. Footer `IST 688 · AgentOps`.

---

## Field mapping summary (for parent Canva pass)

| Lab field | Clean vendor terms retrieved |
| --- | --- |
| caller | parent span / parent_id (OpenAI Agents SDK, OpenTelemetry, AgentOps, Phoenix) |
| target | span name / tool name / observation name (OpenTelemetry, AgentOps Tool Name, Langfuse observation name) |
| latency_ms | start/end timestamps, duration, latency (OpenTelemetry, Datadog, Weave Call timing) |
| input_tokens | gen_ai.usage.input_tokens, Prompt Tokens, Datadog input_tokens, Langfuse usage_details input |
| output_tokens | gen_ai.usage.output_tokens, Completion Tokens, Datadog output_tokens, Langfuse usage_details output |

## Quote integrity
All quoted strings above were taken from pages fetched during this research pass. Where a slide is class setup or lab brief only, vendor evidence is marked n/a by the claim matrix research ask.
