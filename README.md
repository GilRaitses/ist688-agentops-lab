# IST 688 AgentOps Lab

Standalone Streamlit lab for **AgentOps: seeing what multi-agent systems actually did**.

The app shows two concurrent functions (`Function_A` and `Function_B`) with an `AgentOps_Logger` recording spans beside them. It needs **no paid API keys**. Model labels in the UI are local simulation labels only.

Public repo for class forks: https://github.com/GilRaitses/ist688-agentops-lab

## Fork and run locally

1. Fork this repository on GitHub (or copy the files into your own class repo).
2. Clone your fork.
3. Create a virtual environment if you want one.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Start the app:

```bash
streamlit run app.py
```

6. Open the local URL Streamlit prints (usually `http://localhost:8501`).

## Deploy on Streamlit Community Cloud

1. Fork this repository to your GitHub account.
2. Sign in at [share.streamlit.io](https://share.streamlit.io).
3. Click **New app**.
4. Select your fork, branch `main` and main file path `app.py`.
5. Deploy. No secrets or API keys are required.

## What you will do in the lab

Build a small AgentOps logger (not a database product):

1. Define a Pydantic record with `caller`, `target`, `latency_ms`, `input_tokens` and `output_tokens`.
2. Run two functions at the same time and push valid records to an async queue.
3. Serialize the collected records into a compact TOON string.
4. Print the trace after both functions finish.

**Rubric (10 points):** 3 for non-blocking concurrency, 4 for the schema and 3 for the TOON output.

## App modes

- **Interactive In-Class Lab Sandbox:** run two concurrent functions and inspect traces (this is the lab)
- **Talk recap:** optional recap of the class slides if someone wants to reread them during the lab
- **Local Trace Query (DuckDB):** query session spans with in-process DuckDB

## Requirements

Listed in `requirements.txt`: `streamlit`, `pydantic`, `pandas`, `numpy`, `plotly`, `duckdb`.
