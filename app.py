import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
import time
import uuid
import json
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Dict, Any

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AgentOps: Multi-Agent Observability",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #1E222D;
        border: 1px solid #2E3440;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .badge-pass {
        background-color: #10B981;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-fail {
        background-color: #EF4444;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .stCodeBlock {
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "telemetry_logs" not in st.session_state:
    st.session_state.telemetry_logs = []
if "rejected_records" not in st.session_state:
    st.session_state.rejected_records = []
if "lab_graded" not in st.session_state:
    st.session_state.lab_graded = False

# ==========================================
# PYDANTIC TELEMETRY SCHEMAS
# ==========================================
class ToolArgumentsSchema(BaseModel):
    query: str
    max_results: int = Field(default=5, ge=1, le=20)
    filter_tag: Optional[str] = None

class AgentSpanTelemetry(BaseModel):
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    session_id: str
    timestamp: str
    agent_name: str
    model_name: str
    prompt_version_hash: str
    caller: str
    target: str
    internal_thought: str
    tool_call_name: Optional[str] = None
    raw_tool_arguments: Optional[Dict[str, Any]] = None
    completion_output: str
    latency_ms: int
    input_tokens: int
    thought_tokens: int
    output_tokens: int
    schema_ok: bool = True

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def span_to_dict(span: AgentSpanTelemetry) -> Dict[str, Any]:
    if hasattr(span, "model_dump"):
        return span_to_dict(span)
    return span.dict()

def convert_to_toon(spans: List[Dict[str, Any]]) -> str:
    """TOON compaction: field names once at the top then one row per span."""
    if not spans:
        return "trace_stream[0]{}: empty"
    header = (
        f"trace_stream[{len(spans)}]"
        "{span_id,caller,target,latency_ms,input_tokens,output_tokens}:"
    )
    rows = []
    for s in spans:
        row = (
            f"  {s['span_id'][:8]},{s['caller']},{s['target']},"
            f"{s['latency_ms']},{s['input_tokens']},{s['output_tokens']}"
        )
        rows.append(row)
    return header + "\n" + "\n".join(rows)

def init_duckdb_storage(spans: List[Dict[str, Any]]) -> duckdb.DuckDBPyConnection:
    """Local in-process DuckDB populated with active telemetry."""
    con = duckdb.connect(database=":memory:")
    if not spans:
        con.execute("""
            CREATE TABLE trace_spans (
                trace_id VARCHAR, span_id VARCHAR, parent_span_id VARCHAR,
                agent_name VARCHAR, model_name VARCHAR, prompt_version_hash VARCHAR,
                caller VARCHAR, target VARCHAR,
                latency_ms BIGINT, input_tokens INTEGER, thought_tokens INTEGER,
                output_tokens INTEGER, schema_ok BOOLEAN
            )
        """)
        return con
    df = pd.DataFrame(spans)
    if "raw_tool_arguments" in df.columns:
        df["raw_tool_arguments"] = df["raw_tool_arguments"].apply(
            lambda x: json.dumps(x) if x else None
        )
    con.register("df_spans", df)
    con.execute("CREATE TABLE trace_spans AS SELECT * FROM df_spans")
    return con

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://img.icons8.com/fluency/96/network-intelligence.png", width=64)
st.sidebar.title("AgentOps Lab")
app_mode = st.sidebar.radio(
    "Choose Mode:",
    [
        "Interactive In-Class Lab Sandbox",
        "Talk recap",
        "Local Trace Query (DuckDB)",
    ],
)

st.sidebar.divider()
st.sidebar.markdown("""
**Course:** IST 688  
**Topic:** Multi-Agent Observability  
**Local query engine:** DuckDB  
**Lab focus:** traces not console scrap  
""")

# ==========================================
# MODE 1: CLASS SLIDE DECK (locked outline)
# ==========================================
if app_mode == "Talk recap":
    st.title("AgentOps: seeing what multi-agent systems actually did")
    st.caption("Optional recap of the class talk. Present from the slide deck, then use this app for the lab.")

    slides = [
        "Slide 1: Title",
        "Slide 2: Where class left off",
        "Slide 3: What changes with more agents",
        "Slide 4: Why print statements go dark",
        "Slide 5: A reasoning trace is spans",
        "Slide 6: AgentOps as a non-blocking logger",
        "Slide 7: What to record",
        "Slide 8: Compact TOON log form",
        "Slide 9: What a trace helps you notice",
        "Slide 10: In-class lab brief",
        "Slide 11: Questions",
    ]

    current_slide = st.select_slider("Presentation Flow Navigator:", options=slides)

    if current_slide == slides[0]:
        st.subheader("AgentOps: seeing what multi-agent systems actually did")
        st.markdown("""
        * Multi-Agent Systems teach-in
        * Connects the functions lecture to watching several agents work at once
        * About 30 minutes talk then a 30-minute lab
        """)
        with st.expander("Speaker notes"):
            st.write(
                "Say that the group is teaching Multi-Agent Systems and that "
                "the talk connects today's functions lecture to the problem of "
                "watching several agents work at once."
            )

    elif current_slide == slides[1]:
        st.subheader("Where class left off: one model and a tool")
        st.markdown("""
        * User asks a question
        * Model may request a function
        * Application runs that function
        * Result returns so the model can answer
        * Familiar case: looking up weather
        """)
        st.code(
            "user question\n"
            "model may request a function\n"
            "application runs the function\n"
            "result returns so the model can answer",
            language="text",
        )
        st.info("This is still one agent, one context and one visible sequence.")
        with st.expander("Speaker notes"):
            st.write(
                "Walk the functions lecture loop. Emphasize that the student "
                "can still see the whole path when only one agent is involved."
            )

    elif current_slide == slides[2]:
        st.subheader("What changes when more than one agent is involved")
        st.markdown("""
        * More than one agent can run at the same time
        * The path is no longer one visible sequence
        * A mistake can hide in more than one place
        """)
        with st.expander("Speaker notes"):
            st.write(
                "Contrast the single-agent loop with concurrent agents. "
                "Keep the focus on visibility of the run path."
            )

    elif current_slide == slides[3]:
        st.subheader("Why ordinary print statements go dark")
        st.markdown("""
        * A printed line rarely names who called whom, how long a step took or how many tokens it used
        * Silent execution failures get missed
        """)
        st.warning("A multi-agent run needs a trace not a scrap of console output.")
        with st.expander("Speaker notes"):
            st.write(
                "Make the takeaway concrete: print statements are not enough "
                "when agents run together."
            )

    elif current_slide == slides[4]:
        st.subheader("A reasoning trace is a sequence of spans")
        c1, c2, c3 = st.columns(3)
        c1.info("**Thought**\n\nPlanning before action")
        c2.warning("**Tool call**\n\nNamed call with arguments")
        c3.success("**Result**\n\nWhat came back")
        st.code(
            "parent span: user turn\n"
            "  child span: thought\n"
            "  child span: tool call\n"
            "  child span: result",
            language="text",
        )
        with st.expander("Speaker notes"):
            st.write(
                "Draw a parent and child so students can see the caller and the target."
            )

    elif current_slide == slides[5]:
        st.subheader("AgentOps as a non-blocking logger")
        st.markdown("""
        * The logger sits beside the agents not inside their answers
        * It records each span while the agents keep running
        * Records are pushed to a queue
        * Logging does not make the agents wait
        """)
        st.code(
            "Function_A  (runs)\n"
            "Function_B  (runs at the same time)\n"
            "AgentOps_Logger  (records spans beside them)",
            language="text",
        )
        with st.expander("Speaker notes"):
            st.write(
                "Stress that the logger is beside the work. Two concurrent "
                "functions keep running while records enter a queue."
            )

    elif current_slide == slides[6]:
        st.subheader("What to record")
        st.markdown("""
        Lab fields checked with a Pydantic model:

        1. `caller`
        2. `target`
        3. `latency_ms`
        4. `input_tokens`
        5. `output_tokens`
        """)
        st.info("A malformed record is rejected before it enters the log.")
        with st.expander("Speaker notes"):
            st.write(
                "Stay with the lab fields. Do not add scoring gateways or "
                "database columns the lab does not use."
            )

    elif current_slide == slides[7]:
        st.subheader("Writing the log in a compact form")
        st.markdown("""
        * Field names declared once at the top
        * One row per span under that header
        * Keeps the log readable and smaller than verbose JSON
        """)
        st.code(
            "trace_stream[2]{caller,target,latency_ms,input_tokens,output_tokens}:\n"
            "  Function_A,search_tool,480,320,185\n"
            "  Function_B,search_tool,510,350,190",
            language="text",
        )
        st.caption(
            "Present TOON as a compact log form. Do not treat it as a measured production saving."
        )
        with st.expander("Speaker notes"):
            st.write(
                "Show the header-plus-rows shape. Avoid inventing compression ratios "
                "or token-savings percents."
            )

    elif current_slide == slides[8]:
        st.subheader("What a trace helps you notice")
        st.markdown("""
        * Who called whom
        * How long a step took
        * How many tokens a step used
        * Silent execution failures become visible
        """)
        st.info("Usefulness: debugging and cost visibility in a multi-agent run.")
        with st.expander("Speaker notes"):
            st.write(
                "Do not claim enterprise predictability or storage-engine performance "
                "you have not measured."
            )

    elif current_slide == slides[9]:
        st.subheader("In-class lab brief")
        st.markdown("""
        Students build a small AgentOps logger not a database product.

        1. Define a Pydantic record with caller, target, latency and token counts.
        2. Run two functions at the same time and push valid records to an async queue.
        3. Serialize the collected records into a compact TOON string.
        4. Print the trace after both functions finish.

        **Rubric (10 points):** 3 for non-blocking concurrency, 4 for the schema and 3 for the TOON output.
        """)
        st.success(
            "Starter app: fork the public repo listed on the class lab brief slide "
            "then run `streamlit run app.py`."
        )
        with st.expander("Speaker notes"):
            st.write(
                "Keep this slide short so the lab can start on time. Point students "
                "to the public GitHub repo URL on the class deck."
            )

    else:
        st.subheader("Questions")
        st.markdown("Open floor for class questions after the talk or after the lab.")
        with st.expander("Speaker notes"):
            st.write(
                "Use whichever timing the session needs. Solution review is instructor-only."
            )

# ==========================================
# MODE 2: INTERACTIVE LAB SANDBOX
# ==========================================
elif app_mode == "Interactive In-Class Lab Sandbox":
    st.title("IST 688 Lab: AgentOps logger beside concurrent functions")
    st.write(
        "Run two concurrent functions, validate telemetry with Pydantic, "
        "inspect TOON serialization and check the rubric."
    )

    tabs = st.tabs([
        "1. Run concurrent functions",
        "2. Schema check",
        "3. TOON output",
        "4. Lab grading rubric",
    ])

    with tabs[0]:
        st.subheader("Step 1: Run two functions at the same time")
        st.write(
            "Function_A and Function_B run together. AgentOps_Logger records "
            "spans beside them without blocking their work."
        )

        colA, colB = st.columns(2)
        with colA:
            user_prompt = st.text_input(
                "User prompt:",
                value="Analyze quarterly earnings report for risk factors and revenue trends",
            )
            simulate_drift = st.checkbox(
                "Inject schema drift on Function_B (malformed tool arguments)",
                value=True,
            )
        with colB:
            model_selection = st.selectbox(
                "Simulated local model label (no paid API calls):",
                ["gpt-4o-mini", "deepseek-r1-distill"],
            )
            prompt_hash = st.text_input("Prompt version hash:", value="a9f4c3b1e802")

        if st.button("🚀 Run concurrent functions", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            trace_id = str(uuid.uuid4())
            session_id = f"sess_{int(time.time())}"
            new_spans = []
            rejected = []

            # Logger note: no decomposer agent. Two functions start together.
            status_text.text("AgentOps_Logger ready. Starting Function_A and Function_B...")
            time.sleep(0.25)
            progress_bar.progress(15)

            # Function_A (valid)
            status_text.text("Function_A running (risk scan)...")
            time.sleep(0.3)
            function_a_id = str(uuid.uuid4())
            function_a_span = AgentSpanTelemetry(
                trace_id=trace_id,
                span_id=function_a_id,
                parent_span_id=None,
                session_id=session_id,
                timestamp=datetime.utcnow().isoformat(),
                agent_name="Function_A",
                model_name=model_selection,
                prompt_version_hash=prompt_hash,
                caller="user_prompt",
                target="Function_A",
                internal_thought="Scanning risk language in the prompt text.",
                tool_call_name="execute_vector_search",
                raw_tool_arguments={"query": "supply chain disruption risk", "max_results": 5},
                completion_output="Risk items listed for the prompt.",
                latency_ms=480,
                input_tokens=320,
                thought_tokens=140,
                output_tokens=185,
                schema_ok=True,
            )
            new_spans.append(span_to_dict(function_a_span))
            progress_bar.progress(55)

            # Function_B (clean or drifted)
            status_text.text("Function_B running (revenue scan)...")
            time.sleep(0.35)
            function_b_id = str(uuid.uuid4())

            if simulate_drift:
                try:
                    ToolArgumentsSchema(query="revenue figures", max_results=999)
                    args_ok = True
                except ValidationError:
                    args_ok = False

                function_b_span = AgentSpanTelemetry(
                    trace_id=trace_id,
                    span_id=function_b_id,
                    parent_span_id=None,
                    session_id=session_id,
                    timestamp=datetime.utcnow().isoformat(),
                    agent_name="Function_B",
                    model_name=model_selection,
                    prompt_version_hash=prompt_hash,
                    caller="user_prompt",
                    target="Function_B",
                    internal_thought="Tool arguments failed the local schema check.",
                    tool_call_name="execute_vector_search",
                    raw_tool_arguments={"query": "revenue figures", "max_results": 999},
                    completion_output="Raw text block returned without clean fields.",
                    latency_ms=1250,
                    input_tokens=420,
                    thought_tokens=310,
                    output_tokens=520,
                    schema_ok=args_ok,
                )
                payload = span_to_dict(function_b_span)
                new_spans.append(payload)
                if not args_ok:
                    rejected.append(payload)
            else:
                function_b_span = AgentSpanTelemetry(
                    trace_id=trace_id,
                    span_id=function_b_id,
                    parent_span_id=None,
                    session_id=session_id,
                    timestamp=datetime.utcnow().isoformat(),
                    agent_name="Function_B",
                    model_name=model_selection,
                    prompt_version_hash=prompt_hash,
                    caller="user_prompt",
                    target="Function_B",
                    internal_thought="Revenue tables extracted cleanly.",
                    tool_call_name="execute_vector_search",
                    raw_tool_arguments={"query": "revenue figures", "max_results": 5},
                    completion_output="Quarterly revenue metrics listed.",
                    latency_ms=510,
                    input_tokens=350,
                    thought_tokens=110,
                    output_tokens=190,
                    schema_ok=True,
                )
                new_spans.append(span_to_dict(function_b_span))

            progress_bar.progress(100)
            status_text.text(
                "Both functions finished. AgentOps_Logger flushed the queue."
            )

            for s in new_spans:
                st.session_state.telemetry_logs.append(s)
            for r in rejected:
                st.session_state.rejected_records.append(r)

            st.success(
                f"Logger captured {len(new_spans)} spans. Trace ID: `{trace_id}`"
            )
            st.caption(f"Prompt used: {user_prompt}")

        st.subheader("Captured spans in buffer")
        if st.session_state.telemetry_logs:
            df = pd.DataFrame(st.session_state.telemetry_logs)
            display_cols = [
                "span_id",
                "agent_name",
                "caller",
                "target",
                "latency_ms",
                "input_tokens",
                "output_tokens",
                "schema_ok",
            ]
            st.dataframe(df[display_cols].tail(10), use_container_width=True)
        else:
            st.info("No spans recorded yet. Click the run button above.")

    with tabs[1]:
        st.subheader("Step 2: Schema check on recorded spans")
        st.write(
            "Valid records stay in the log. Records that fail the local argument "
            "schema are listed separately."
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Accepted (`schema_ok = true`)")
            clean_spans = [s for s in st.session_state.telemetry_logs if s.get("schema_ok")]
            st.metric("Accepted spans", len(clean_spans))
            if clean_spans:
                st.json(clean_spans[-1].get("raw_tool_arguments"))
        with c2:
            st.markdown("#### Rejected (`schema_ok = false`)")
            st.metric("Rejected spans", len(st.session_state.rejected_records))
            if st.session_state.rejected_records:
                latest = st.session_state.rejected_records[-1]
                st.error("Latest rejected payload:")
                st.write(f"**Function:** `{latest['agent_name']}`")
                st.json({
                    "raw_arguments": latest["raw_tool_arguments"],
                    "internal_thought": latest["internal_thought"],
                    "output": latest["completion_output"],
                })

    with tabs[2]:
        st.subheader("Step 3: TOON string vs verbose JSON")
        st.markdown("""
        TOON declares field names once at the top then stacks one row per span.
        Use it as a compact readable log form not as a measured production claim.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Verbose JSON")
            raw_json_str = (
                json.dumps(st.session_state.telemetry_logs[-3:], indent=2)
                if st.session_state.telemetry_logs
                else "{}"
            )
            st.text_area("JSON view:", value=raw_json_str, height=260)
        with col2:
            st.markdown("#### Compact TOON")
            toon_str = convert_to_toon(st.session_state.telemetry_logs[-3:])
            st.text_area("TOON view:", value=toon_str, height=260)

    with tabs[3]:
        st.subheader("Step 4: Lab rubric (10 points)")
        st.write("Rubric: 3 concurrency, 4 schema, 3 TOON.")

        score = 0
        has_concurrent = len(st.session_state.telemetry_logs) >= 2
        has_metrics = all(
            k in (st.session_state.telemetry_logs[0] if st.session_state.telemetry_logs else {})
            for k in ["caller", "target", "latency_ms", "input_tokens", "output_tokens"]
        )
        has_toon = len(st.session_state.telemetry_logs) > 0

        st.markdown("---")
        if has_concurrent:
            st.markdown(
                "✅ **Criteria 1 (3/3 Pts):** Two concurrent function spans were recorded."
            )
            score += 3
        else:
            st.markdown(
                "❌ **Criteria 1 (0/3 Pts):** Concurrent function spans have not been recorded."
            )

        if has_metrics:
            st.markdown(
                "✅ **Criteria 2 (4/4 Pts):** Pydantic fields caller, target, latency_ms, "
                "input_tokens and output_tokens are present."
            )
            score += 4
        else:
            st.markdown(
                "❌ **Criteria 2 (0/4 Pts):** Required telemetry fields are missing."
            )

        if has_toon:
            st.markdown(
                "✅ **Criteria 3 (3/3 Pts):** Spans are available for TOON serialization."
            )
            score += 3
        else:
            st.markdown("❌ **Criteria 3 (0/3 Pts):** TOON serialization unverified.")

        st.markdown("---")
        st.metric(label="Student lab score", value=f"{score} / 10 Points")
        if score == 10:
            st.balloons()
            st.success("All criteria met for this sandbox check.")

# ==========================================
# MODE 3: LOCAL DUCKDB QUERY
# ==========================================
elif app_mode == "Local Trace Query (DuckDB)":
    st.title("Local trace query with DuckDB")
    st.caption("In-process DuckDB over spans captured in this session")

    if not st.session_state.telemetry_logs:
        st.warning(
            "No telemetry spans in this session. Run the lab sandbox or generate sample spans."
        )
        if st.button("Generate sample spans"):
            agents = ["Function_A", "Function_B"]
            models = ["gpt-4o-mini", "deepseek-r1-distill"]
            hashes = ["a9f4c3b1e802", "e5b871c42fa1", "f001b98ac433"]

            synthetic_spans = []
            for _ in range(20):
                agent = str(np.random.choice(agents))
                dur = max(int(np.random.normal(500, 150)), 60)
                out_tok = int(np.random.normal(250, 80))
                schema_ok = bool(np.random.random() >= 0.25)
                span = AgentSpanTelemetry(
                    trace_id=str(uuid.uuid4()),
                    span_id=str(uuid.uuid4()),
                    parent_span_id=None,
                    session_id=f"sess_{np.random.randint(100, 999)}",
                    timestamp=datetime.utcnow().isoformat(),
                    agent_name=agent,
                    model_name=str(np.random.choice(models)),
                    prompt_version_hash=str(np.random.choice(hashes)),
                    caller="user_prompt",
                    target=agent,
                    internal_thought="Sample reasoning step.",
                    tool_call_name="execute_query",
                    raw_tool_arguments={"param": "sample_val"},
                    completion_output="Processed output block.",
                    latency_ms=dur,
                    input_tokens=int(np.random.randint(100, 400)),
                    thought_tokens=int(np.random.randint(50, 200)),
                    output_tokens=out_tok,
                    schema_ok=schema_ok,
                )
                synthetic_spans.append(span_to_dict(span))
            st.session_state.telemetry_logs.extend(synthetic_spans)
            st.rerun()

    if st.session_state.telemetry_logs:
        con = init_duckdb_storage(st.session_state.telemetry_logs)

        total_spans = con.execute("SELECT count(*) FROM trace_spans").fetchone()[0]
        rejected_count = con.execute(
            "SELECT count(*) FROM trace_spans WHERE schema_ok = false"
        ).fetchone()[0]

        c1, c2 = st.columns(2)
        c1.metric("Total spans", total_spans)
        c2.metric("Rejected schema spans", rejected_count)

        st.divider()

        st.subheader("Latency and tokens by function")
        query_a = """
        SELECT
            agent_name,
            count(*) AS span_count,
            round(avg(latency_ms), 1) AS avg_latency_ms,
            sum(input_tokens) AS sum_input_tokens,
            sum(output_tokens) AS sum_output_tokens
        FROM trace_spans
        GROUP BY agent_name
        ORDER BY agent_name
        """
        df_a = con.execute(query_a).fetchdf()
        st.dataframe(df_a, use_container_width=True)

        st.subheader("Latency by function")
        query_b = """
        SELECT
            agent_name,
            round(avg(latency_ms), 1) AS avg_latency_ms
        FROM trace_spans
        GROUP BY agent_name
        ORDER BY avg_latency_ms DESC
        """
        df_b = con.execute(query_b).fetchdf()
        fig = px.bar(
            df_b,
            x="agent_name",
            y="avg_latency_ms",
            title="Average latency by function",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Custom SQL over `trace_spans`")
        custom_sql = st.text_area(
            "SQL:",
            value=(
                "SELECT agent_name, avg(latency_ms) AS avg_latency, "
                "sum(output_tokens) AS total_tokens "
                "FROM trace_spans GROUP BY agent_name;"
            ),
        )
        if st.button("Run SQL query"):
            try:
                res_df = con.execute(custom_sql).fetchdf()
                st.dataframe(res_df, use_container_width=True)
            except Exception as e:
                st.error(f"SQL error: {e}")
