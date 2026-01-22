import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8011"

st.set_page_config(
    page_title="Clinical Decision Support System",
    layout="wide"
)

st.title("🩺 Clinical Decision Support Assistant (CDSS)")
st.caption("RAG-based Clinical Evidence Retrieval System")

# -----------------------------
# PDF Upload Section
# -----------------------------
st.header("📄 Upload Clinical Guidelines")

uploaded_file = st.file_uploader(
    "Upload a medical guideline PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    with st.spinner("Uploading and indexing PDF..."):
        files = {
            "file": (uploaded_file.name, uploaded_file, "application/pdf")
        }
        response = requests.post(
            f"{BACKEND_URL}/guidelines/upload",
            files=files
        )

    if response.status_code == 200:
        st.success("✅ PDF uploaded and indexed successfully")
        st.json(response.json())
    else:
        st.error("❌ Failed to upload PDF")
        st.text(response.text)

# -----------------------------
# Question Answering Section
# -----------------------------
st.header("❓ Ask a Clinical Question")

query = st.text_input(
    "Enter your clinical question",
    placeholder="e.g. What is the emergency referral procedure?"
)

if st.button("Ask CDSS"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving evidence and generating answer..."):
            response = requests.post(
                f"{BACKEND_URL}/cdss/ask",
                params={"query": query}
            )

        if response.status_code == 200:
            result = response.json()

            st.subheader("🧠 Answer")
            st.write(result["answer"])

            st.subheader("📚 Citations")
            for c in result["citations"]:
                st.markdown(f"- **{c}**")

            st.subheader("🔍 Evidence Used")
            for i, ev in enumerate(result["evidence_used"], 1):
                with st.expander(f"Evidence {i} ({ev['source']})"):
                    st.write(ev["text"])

        else:
            st.error("❌ Error from backend")
            st.text(response.text)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("⚠️ This system assists clinical decision-making and does not replace professional medical judgment.")
