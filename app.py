import time

import streamlit as st
from analyzer import analyze_visual, chat_followup
from parser import parse_response, to_dataframe
from charts import draw_chart
from report import generate_report

# ── page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Visual Analyst Agent",
    page_icon="📊",
    layout="wide"
)

# ── custom CSS — full dark theme ──────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', system-ui, sans-serif !important; }

/* main background */
.stApp { background: #08080f !important; }
section[data-testid="stSidebar"] { background: #0c0c18 !important; border-right: 1px solid #16162a !important; }
.stMainBlockContainer { background: #08080f !important; padding: 2rem 2rem !important; }

/* hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }

/* top header */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 24px 0;
    border-bottom: 1px solid #16162a;
    margin-bottom: 24px;
}
.app-title {
    font-size: 20px;
    font-weight: 600;
    color: #c8c0f0;
    letter-spacing: .3px;
}
.app-powered {
    font-size: 11px;
    color: #3a3a5a;
    background: #12121e;
    padding: 4px 12px;
    border-radius: 20px;
    border: 0.5px solid #2a2a3e;
}

/* sidebar labels */
.sidebar-label {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    color: #3a3a5a;
    margin-bottom: 10px;
    margin-top: 20px;
}

/* upload zone */
.upload-zone {
    border: 1.5px dashed #252540;
    border-radius: 12px;
    padding: 24px 12px;
    text-align: center;
    cursor: pointer;
    transition: border-color .2s;
    margin-bottom: 12px;
}
.upload-zone:hover { border-color: #6c63ff; }

/* file uploader override */
[data-testid="stFileUploader"] {
    background: #0c0c18 !important;
    border: 1.5px dashed #252540 !important;
    border-radius: 12px !important;
    padding: 8px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6c63ff !important;
}
[data-testid="stFileUploader"] label {
    color: #4a4a6a !important;
    font-size: 12px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #4a4a6a !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: #6c63ff !important;
}

/* analyze button */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #5a52e8, #9333ea) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 0 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: .3px !important;
    box-shadow: 0 4px 15px rgba(108,99,255,.25) !important;
    transition: all .2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 20px rgba(108,99,255,.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:disabled {
    background: #1a1a2e !important;
    color: #3a3a5a !important;
    box-shadow: none !important;
    transform: none !important;
}

/* tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0c0c18 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #4a4a6a !important;
    border-radius: 7px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #16162a !important;
    color: #a89fcc !important;
}

/* cards */
.stat-card {
    background: #0c0c18;
    border: 0.5px solid #1a1a2e;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.stat-val { font-size: 22px; font-weight: 700; margin-bottom: 4px; }
.stat-label {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: .8px;
    color: #3a3a5a;
}

.content-card {
    background: #0c0c18;
    border: 0.5px solid #1a1a2e;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
}
.card-label {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: .8px;
    color: #6a6a9a;
    margin-bottom: 12px;
}
.analysis-text {
    font-size: 13px;
    color: #c8c4e0;
    line-height: 1.8;
}

/* badge */
.visual-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #16162a;
    border: 0.5px solid #2a2a4a;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #a89fcc;
    margin-bottom: 16px;
}
.badge-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #6c63ff;
    display: inline-block;
}

/* chart type chips */
.chip-row { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px; }
.chip {
    font-size: 9px;
    padding: 3px 9px;
    border-radius: 20px;
    font-weight: 500;
}

/* dataframe */
[data-testid="stDataFrame"] {
    background: #0c0c18 !important;
    border: 0.5px solid #1a1a2e !important;
    border-radius: 10px !important;
}

/* chat messages */
.chat-user {
    background: #1e1440;
    border: 0.5px solid #3a2a70;
    border-radius: 12px 12px 2px 12px;
    padding: 10px 14px;
    font-size: 13px;
    color: #c8b8f8;
    max-width: 80%;
    margin-left: auto;
    margin-bottom: 10px;
    line-height: 1.6;
}
.chat-ai {
    background: #0c0c18;
    border: 0.5px solid #1a1a2e;
    border-radius: 12px 12px 12px 2px;
    padding: 10px 14px;
    font-size: 13px;
    color: #7a789a;
    max-width: 85%;
    margin-bottom: 10px;
    line-height: 1.6;
}
.chat-label {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: .6px;
    color: #3a3a5a;
    margin-bottom: 4px;
}

/* chat input */
[data-testid="stChatInput"] {
    background: #0c0c18 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6c63ff44 !important;
}
[data-testid="stChatInputTextArea"] {
    color: #8a88a0 !important;
    background: transparent !important;
}

/* idle state */
.idle-container {
    text-align: center;
    padding: 80px 20px;
}
.idle-icon {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: #1a1a2e;
    margin: 0 auto 16px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.idle-title {
    font-size: 16px;
    font-weight: 500;
    color: #a89fcc;
    margin-bottom: 6px;
}
.idle-sub { font-size: 12px; color: #4a4a6a; }

/* step indicator */
.step-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 20px;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
}
.step-circle {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 600;
    flex-shrink: 0;
}
.step-done { background: #6c63ff; color: white; }
.step-active { background: #16162a; border: 1.5px solid #6c63ff; color: #6c63ff; }
.step-idle { background: #16162a; color: #3a3a5a; }
.step-line { flex: 1; height: 1px; background: #1a1a2e; }

/* download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1a3a28, #0f2a1e) !important;
    color: #34d399 !important;
    border: 0.5px solid #1a4a2a !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #34d399, #059669) !important;
    color: white !important;
}

/* metric */
[data-testid="stMetric"] {
    background: #0c0c18 !important;
    border: 0.5px solid #1a1a2e !important;
    border-radius: 12px !important;
    padding: 14px !important;
}
[data-testid="stMetricValue"] { color: #c8c0f0 !important; }
[data-testid="stMetricLabel"] { color: #3a3a5a !important; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #08080f; }
::-webkit-scrollbar-thumb { background: #2a2a4a; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── session state ─────────────────────────────────────────────────
for key in ["result", "parsed", "image_bytes"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 8px'>
        <div style='font-size:16px;font-weight:600;color:#c8c0f0;margin-bottom:4px'>
            📊 Visual Analyst
        </div>
        <div style='font-size:10px;color:#3a3a5a'>powered by Gemini</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-label'>Upload</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop chart or table",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed"
    )

    analyze_btn = st.button(
        "Analyze visual",
        disabled=uploaded is None,
        use_container_width=True
    )

    st.markdown("<div class='sidebar-label'>Supports</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='chip-row'>
        <span class='chip' style='background:#1a1040;color:#6c63ff;border:0.5px solid #2a2060'>Bar</span>
        <span class='chip' style='background:#0a1a30;color:#38bdf8;border:0.5px solid #1a3a50'>Line</span>
        <span class='chip' style='background:#0a2010;color:#34d399;border:0.5px solid #1a4020'>Pie</span>
        <span class='chip' style='background:#20180a;color:#fbbf24;border:0.5px solid #3a2a10'>Table</span>
        <span class='chip' style='background:#200a10;color:#f87171;border:0.5px solid #3a1a20'>Dashboard</span>
        <span class='chip' style='background:#0a1a20;color:#a78bfa;border:0.5px solid #2a1a50'>Scatter</span>
    </div>
    """, unsafe_allow_html=True)

# ── header ────────────────────────────────────────────────────────
st.markdown("""
<div class='app-header'>
    <div class='app-title'>Visual Analyst Agent</div>
    <div class='app-powered'>powered by Gemini</div>
</div>
""", unsafe_allow_html=True)


def render_steps(active_idx, steps):
    html = "<div class='step-row'>"
    for i, step in enumerate(steps):
        if i < active_idx:
            circle = f"<div class='step-circle step-done'>✓</div>"
            color = "#a89fcc"
        elif i == active_idx:
            circle = f"<div class='step-circle step-active'>{i+1}</div>"
            color = "#6c63ff"
        else:
            circle = f"<div class='step-circle step-idle'>{i+1}</div>"
            color = "#3a3a5a"
        html += f"<div class='step-item'>{circle}<span style='color:{color}'>{step}</span></div>"
        if i < len(steps) - 1:
            html += "<div class='step-line'></div>"
    html += "</div>"
    return html


# ── run analysis ──────────────────────────────────────────────────
if analyze_btn and uploaded:
    image_bytes = uploaded.read()
    st.session_state.image_bytes = image_bytes
    st.session_state.chat_history = []

    # animated step indicator
    steps_placeholder = st.empty()
    steps = ["Detecting visual type", "Extracting data", "Analyzing trends", "Building report"]

    for i in range(4):
        steps_placeholder.markdown(render_steps(i, steps), unsafe_allow_html=True)
        time.sleep(0.6)

    with st.spinner(""):
        result = analyze_visual(image_bytes)
        parsed = parse_response(result["raw"])
        st.session_state.result = result
        st.session_state.parsed = parsed

    steps_placeholder.markdown(render_steps(4, steps), unsafe_allow_html=True)
    time.sleep(0.3)
    steps_placeholder.empty()

# ── display results ───────────────────────────────────────────────
if st.session_state.parsed:
    parsed = st.session_state.parsed
    df = to_dataframe(parsed["data"])

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Analysis", "Extracted Data", "Redrawn Chart", "Chat", "Export"
    ])

    # ── TAB 1: ANALYSIS ──────────────────────────────────────────
    with tab1:
        st.markdown(f"""
        <div class='visual-badge'>
            <span class='badge-dot'></span>
            {parsed['visual_type']}
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        if df is not None and "values" in parsed["data"]:
            values = parsed["data"]["values"]
            labels = parsed["data"].get("labels", [])
            peak_idx = values.index(max(values))
            with col1:
                st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-val' style='color:#fbbf24'>{labels[peak_idx] if labels else max(values)}</div>
                    <div class='stat-label'>Peak</div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='stat-card'>
                    <div class='stat-val' style='color:#34d399'>{len(values)}</div>
                    <div class='stat-label'>Data points</div>
                </div>""", unsafe_allow_html=True)
            with col3:
                if len(values) > 1:
                    growth = round(((values[-1] - values[0]) / values[0]) * 100)
                    color = "#34d399" if growth >= 0 else "#f87171"
                    sign = "+" if growth >= 0 else ""
                    st.markdown(f"""
                    <div class='stat-card'>
                        <div class='stat-val' style='color:{color}'>{sign}{growth}%</div>
                        <div class='stat-label'>Growth</div>
                    </div>""", unsafe_allow_html=True)

        col_img, col_analysis = st.columns([1, 1])
        with col_img:
            st.markdown("<div class='content-card'><div class='card-label'>Original image</div>", unsafe_allow_html=True)
            st.image(st.session_state.image_bytes, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_analysis:
            st.markdown("<div class='content-card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-label'>Trend analysis</div>",
                unsafe_allow_html=True)
            st.write(parsed['analysis'])
            st.markdown("</div>", unsafe_allow_html=True)

        if parsed["parse_error"]:
            st.warning(f"Note: {parsed['parse_error']}")

    # ── TAB 2: EXTRACTED DATA ─────────────────────────────────────
    with tab2:
        st.markdown("<div class='content-card'><div class='card-label'>Extracted data</div>", unsafe_allow_html=True)
        if df is not None:
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "extracted_data.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.markdown("<div class='analysis-text'>Could not extract structured data from this visual.</div>", unsafe_allow_html=True)
            if parsed["data"]:
                st.json(parsed["data"])
        st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 3: REDRAWN CHART ─────────────────────────────────────
    with tab3:
        fig = draw_chart(parsed["visual_type"], parsed["data"])
        if fig:
            st.markdown("<div class='content-card'><div class='card-label'>Redrawn with Plotly — hover to explore</div>", unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='content-card'>
                <div class='analysis-text'>Chart could not be redrawn — the visual may be a table or complex dashboard without extractable chart data.</div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 4: CHAT ───────────────────────────────────────────────
    with tab4:
        if st.session_state.image_bytes is None:
            st.markdown("<div class='analysis-text'>Please analyze an image first before using chat.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:10px;color:#3a3a5a;margin-bottom:16px;text-transform:uppercase;letter-spacing:.8px'>Ask follow-up questions about your visual</div>", unsafe_allow_html=True)

            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class='chat-label' style='text-align:right'>You</div>
                    <div style='display:flex;justify-content:flex-end'>
                        <div class='chat-user'>{msg['content']}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='chat-label'>Analyst</div>
                    <div class='chat-ai'>{msg['content']}</div>
                    """, unsafe_allow_html=True)

            user_input = st.chat_input("Ask anything about this visual...")
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("Thinking..."):
                    reply = chat_followup(
                        st.session_state.image_bytes,
                        st.session_state.chat_history[:-1],
                        user_input
                    )
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    # ── TAB 5: EXPORT ─────────────────────────────────────────────
    with tab5:
        st.markdown("""
        <div class='content-card'>
            <div class='card-label'>Export report</div>
            <div class='analysis-text' style='margin-bottom:16px'>
                Download a complete HTML report with the visual type, trend analysis,
                and extracted data table. Opens in any browser. Fully shareable.
            </div>
        </div>""", unsafe_allow_html=True)

        html_report = generate_report(parsed["visual_type"], parsed["analysis"], df)
        st.download_button(
            label="Download HTML Report",
            data=html_report,
            file_name="visual_analysis_report.html",
            mime="text/html",
            use_container_width=True
        )

else:
    # ── IDLE STATE ────────────────────────────────────────────────
    st.markdown("""
    <div class='idle-container'>
        <div style='font-size:40px;margin-bottom:16px'>📊</div>
        <div class='idle-title'>Upload a visual to get started</div>
        <div class='idle-sub'>Charts, tables, dashboards, screenshots</div>
        <div style='margin-top:20px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap'>
            <span class='chip' style='background:#1a1040;color:#6c63ff;border:0.5px solid #2a2060;font-size:11px;padding:5px 12px'>Bar chart</span>
            <span class='chip' style='background:#0a1a30;color:#38bdf8;border:0.5px solid #1a3a50;font-size:11px;padding:5px 12px'>Line chart</span>
            <span class='chip' style='background:#0a2010;color:#34d399;border:0.5px solid #1a4020;font-size:11px;padding:5px 12px'>Pie chart</span>
            <span class='chip' style='background:#20180a;color:#fbbf24;border:0.5px solid #3a2a10;font-size:11px;padding:5px 12px'>Data table</span>
            <span class='chip' style='background:#200a10;color:#f87171;border:0.5px solid #3a1a20;font-size:11px;padding:5px 12px'>Dashboard</span>
        </div>
        <div style='margin-top:28px;font-size:11px;color:#6a6a9a'>Upload an image in the sidebar and click Analyze</div>
    </div>
    """, unsafe_allow_html=True)
