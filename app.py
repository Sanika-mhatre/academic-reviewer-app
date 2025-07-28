import streamlit as st
import pandas as pd
import plotly.express as px
from read_pdf import extract_text_from_pdf
from check_grammar import check_grammar
from check_plagiarism import check_plagiarism
from check_structure import predict_scores
import base64

# Inject external CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set background using base64 encoding
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Page config and styles
st.set_page_config(page_title="Academic Paper Reviewer Assistant", layout="wide")
local_css("style.css")
set_background("Picture1.jpeg")

st.markdown("<h1 class='main-heading'>📄 Academic Paper Reviewer Assistant</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📎 Upload your research paper (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("📑 Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    st.markdown("### 📝 Preview", unsafe_allow_html=True)
    st.text_area("Preview", text, height=300)

    with st.spinner("🔍 Analyzing paper structure..."):
        clarity, novelty, citation_strength = predict_scores(text)

    st.markdown("### 📊 Score Dashboard", unsafe_allow_html=True)
    scores = {
        "Clarity": clarity,
        "Novelty": novelty,
        "Citation Strength": citation_strength
    }
    score_df = pd.DataFrame.from_dict(scores, orient='index', columns=['Score'])

    fig = px.bar(score_df, x=score_df.index, y='Score', color='Score',
                 color_continuous_scale='Blues', range_y=[0, 10],
                 title="Paper Review Scores")
    st.plotly_chart(fig)

    avg_score = (clarity + novelty + citation_strength) / 3
    st.markdown("### 📌 Final Suggestion", unsafe_allow_html=True)
    if avg_score < 5:
        st.warning("🛠️ Needs Modification — Consider revising the paper based on suggestions.")
    elif 5 <= avg_score < 8:
        st.info("✅ Good to Go — Paper is acceptable with minor edits.")
    else:
        st.success("🚀 Excellent — Great work! Ready for submission.")

    with st.spinner("✍️ Checking grammar..."):
        grammar_errors = check_grammar(text)

    st.markdown("### ✍️ Grammar Report", unsafe_allow_html=True)
    st.markdown(f"<p class='black-text'>📝 Total Grammatical Errors Found: {len(grammar_errors)}</p>", unsafe_allow_html=True)

    if st.checkbox("🔎 Show grammar errors"):
        for err in grammar_errors:
            st.markdown(f"<p class='black-text'>• <strong>Error:</strong> {err['error']}<br>↳ Suggestion: {', '.join(err['suggestions'])}</p><hr>", unsafe_allow_html=True)

    with st.spinner("🧠 Checking plagiarism..."):
        plagiarism_score = check_plagiarism(text, references=[])

    st.markdown("### 🔍 Plagiarism Result", unsafe_allow_html=True)
    st.markdown(f"<p class='black-text'>🧪 Similarity %: <strong>{plagiarism_score:.2f}%</strong></p>", unsafe_allow_html=True)
