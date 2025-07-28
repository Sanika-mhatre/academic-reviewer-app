import streamlit as st
import pandas as pd
import plotly.express as px
from read_pdf import extract_text_from_pdf
from check_grammar import check_grammar
from check_plagiarism import check_plagiarism
from check_structure import predict_scores
import base64

# --------------------------
# Set background image via app.py
# --------------------------
def set_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set page config
st.set_page_config(page_title="Academic Paper Reviewer Assistant", layout="wide")
set_bg_image("Picture1.jpeg")

# Inject external style.css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.title("📄 Academic Paper Reviewer Assistant")

# Upload research paper
uploaded_file = st.file_uploader("📤 Upload your research paper (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("📑 Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    st.subheader("📜 Extracted Text")
    st.text_area("Preview", text, height=300)

    # Analyze structure
    with st.spinner("🔍 Analyzing paper structure..."):
        clarity, novelty, citation_strength = predict_scores(text)

    # Score Dashboard
    st.subheader("📊 Score Dashboard")
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

    # Final Suggestion
    avg_score = (clarity + novelty + citation_strength) / 3
    st.subheader("📌 Final Suggestion")
    if avg_score < 5:
        st.warning("🛠️ Needs Modification — Consider revising the paper.")
    elif 5 <= avg_score < 8:
        st.info("✅ Good to Go — Paper is acceptable with minor edits.")
    else:
        st.success("🚀 Excellent — Great work! Ready for submission.")

    # Grammar Check
    with st.spinner("✍️ Checking grammar..."):
        grammar_errors = check_grammar(text)

    st.subheader("✍️ Grammar Report")
    st.write(f"📍 **Total Grammatical Errors Found:** {len(grammar_errors)}")

    if st.checkbox("📌 Show grammar errors"):
        for err in grammar_errors:
            error_msg = err.get('error', 'Unknown error')
            suggestions = ', '.join(err.get('suggestions', ['No suggestion']))
            st.markdown(
                f"<p class='black-text'>• <strong>Error:</strong> {error_msg}<br>↳ Suggestion: {suggestions}</p><hr>",
                unsafe_allow_html=True
            )

    # Plagiarism Check
    with st.spinner("🔍 Checking plagiarism..."):
        plagiarism_score = check_plagiarism(text, references=[])

    st.subheader("🔍 Plagiarism Result")
    st.metric("📊 Similarity %", f"{plagiarism_score:.2f}%")
