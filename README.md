# IST 688 AgentOps Lab

Fork this repo, then paste the block below to your coding agent. It will add an AgentOps page to your existing private Streamlit course app and use the OpenAI key already in that app’s Streamlit secrets.

```text
Add the IST 688 AgentOps lab from https://github.com/GilRaitses/ist688-agentops-lab into my existing private Streamlit course app as a page (for example pages/AgentOps.py). Do not replace the home page. Do not create a separate public app unless I ask.

Adapt the public repo’s app.py into that page. Keep class naming as Function_A, Function_B, and AgentOps_Logger.

Use the OpenAI key already stored in this course app’s Streamlit secrets (st.secrets). Typical name: OPENAI_API_KEY. Also accept a nested openai.api_key if that is how the app stores it. If another provider key is already present (for example DEEPSEEK_API_KEY), that may be used as a fallback. Do not ask me to paste a key into chat. Never print, log, or display the key. If no key is found, show a short on-page message that Streamlit secrets need an OpenAI (or other provider) key.

Do not add Anthropic or Claude. Do not commit secrets. Do not change the course app’s visibility.

Add any missing packages from the public repo requirements (streamlit, pydantic, pandas, numpy, plotly, duckdb, tiktoken) to the course app requirements without removing existing ones.
```

Public repo: https://github.com/GilRaitses/ist688-agentops-lab

The public student app shows two concurrent functions (`Function_A` and `Function_B`) with an `AgentOps_Logger` recording spans beside them. A provider API key is required in Streamlit secrets before the app will run.

## Secrets (required)

The public app and any course-app page adapted from it look for a key in Streamlit secrets, in this order:

1. `OPENAI_API_KEY`
2. nested `openai.api_key`
3. `DEEPSEEK_API_KEY`
4. `API_KEY` (generic provider key)

Example `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-key-here"

# or nested form used by some course apps:
# [openai]
# api_key = "your-key-here"
```

Do not commit `secrets.toml`. The app never prints, logs, or displays the key value. Anthropic / Claude keys are not used.

## Fork and run locally (public repo)

1. Fork this repository on GitHub.
2. Clone your fork.
3. Create a virtual environment if you want one.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create `.streamlit/secrets.toml` with one provider key (see above).
6. Start the app:

```bash
streamlit run app.py
```

7. Open the local URL Streamlit prints (usually `http://localhost:8501`).

## Deploy on Streamlit Community Cloud

1. Fork this repository to your GitHub account.
2. Sign in at [share.streamlit.io](https://share.streamlit.io).
3. Click **New app**.
4. Select your fork, branch `main` and main file path `app.py`.
5. In the app settings, add secrets for `OPENAI_API_KEY`, nested `openai.api_key`, `DEEPSEEK_API_KEY`, or `API_KEY`.
6. Deploy. Keep the app visibility as you intend; do not change another course app’s visibility.

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

Listed in `requirements.txt`: `streamlit`, `pydantic`, `pandas`, `numpy`, `plotly`, `duckdb`, `tiktoken`.
