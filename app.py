import streamlit as st
from analyzer import analyze_transcript
from rag import load_case_studies, create_vector_store, search_similar_cases
from generator import generate_solution_document

st.set_page_config(
    page_title="Enterprise Integration Sales Agent",
    page_icon="🤝",
    layout="centered"
)

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f4f6f9;
    }

    /* Header banner */
    .header-banner {
        background: linear-gradient(135deg, #1a3c5e, #2d6a9f);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .header-banner h1 {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .header-banner p {
        color: #b8d4f0;
        font-size: 1rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }

    /* Card container */
    .card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
    }

    /* Step badges */
    .step-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;
        gap: 1rem;
    }
    .step-box {
        flex: 1;
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        border-top: 4px solid #2d6a9f;
    }
    .step-number {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d6a9f;
    }
    .step-label {
        font-size: 0.78rem;
        color: #555;
        margin-top: 0.3rem;
    }

    /* Upload area */
    .upload-label {
        font-size: 1rem;
        font-weight: 600;
        color: #1a3c5e;
        margin-bottom: 0.5rem;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #1a3c5e, #2d6a9f);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.9;
    }

    /* Success box */
    .result-box {
        background: #eaf4ea;
        border-left: 5px solid #2e7d32;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-top: 1rem;
    }
    .result-box h4 {
        color: #2e7d32;
        margin: 0 0 0.5rem 0;
    }
    .result-box p {
        color: #444;
        margin: 0;
        font-size: 0.9rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-bottom: 1rem;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Header ──────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <h1>🤝 Enterprise Integration Sales Agent</h1>
    <p>AI-powered Solution Design Document Generator</p>
</div>
""", unsafe_allow_html=True)


# ── How it works steps ───────────────────────────────────
st.markdown("""
<div class="step-row">
    <div class="step-box">
        <div class="step-number">01</div>
        <div class="step-label">Upload Transcript</div>
    </div>
    <div class="step-box">
        <div class="step-number">02</div>
        <div class="step-label">AI Analyzes Client</div>
    </div>
    <div class="step-box">
        <div class="step-number">03</div>
        <div class="step-label">RAG Finds Cases</div>
    </div>
    <div class="step-box">
        <div class="step-number">04</div>
        <div class="step-label">Document Generated</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Upload card ──────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="upload-label">Upload Client Meeting Transcript</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["txt"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    transcript = uploaded_file.read().decode("utf-8")
    st.success(f"✅ Transcript uploaded: **{uploaded_file.name}**")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate Solution Design Document"):

        with st.spinner("Step 1/3 — Analyzing transcript with Gemini AI..."):
            client_info = analyze_transcript(transcript)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pain Points Found", len(client_info['pain_points']))
        with col2:
            st.metric("Tech Stack Items", len(client_info['current_tech_stack']))

        with st.spinner("Step 2/3 — Searching similar case studies (RAG)..."):
            documents = load_case_studies()
            index = create_vector_store(documents)
            query = " ".join(client_info["pain_points"])
            similar_cases = search_similar_cases(query, documents, index)

        st.info(f"📂 Found **{len(similar_cases)}** similar past projects")

        with st.spinner("Step 3/3 — Generating Solution Design Document..."):
            output_file = generate_solution_document(client_info, similar_cases)

        st.markdown("""
        <div class="result-box">
            <h4>Document Ready!</h4>
            <p>Your AI-generated Solution Design Document is ready to download.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with open(output_file, "rb") as f:
            st.download_button(
                label="⬇️ Download Solution Design Document",
                data=f,
                file_name="solution_design_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Enterprise Integration Sales Agent &nbsp;|&nbsp; Powered by Gemini AI + FAISS RAG
</div>
""", unsafe_allow_html=True)