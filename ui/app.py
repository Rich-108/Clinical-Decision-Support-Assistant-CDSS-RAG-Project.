import streamlit as st
import requests

# =============================
# CONFIG
# =============================
BACKEND_URL = "http://127.0.0.1:8020"

st.set_page_config(
    page_title="Clinical Decision Support System",
    layout="wide"
)

# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.header("⚙️ Settings")
    timeout_seconds = st.slider(
        "Request Timeout (seconds)",
        min_value=60,
        max_value=1200,
        value=600,
        step=60,
        help="Increase this if you encounter timeout errors during PDF upload or query."
    )

# =============================
# HEADER
# =============================
st.title("🩺 Clinical Decision Support Assistant (CDSS)")
st.caption("RAG-based Clinical Evidence Retrieval System")

st.markdown(
    """
    ⚠️ **Disclaimer:**  
    This system assists clinical decision-making using uploaded clinical guidelines.
    It does **NOT** replace professional medical judgment.
    """
)

st.divider()

# =============================
# PDF UPLOAD SECTION
# =============================
st.header("📄 Upload Clinical Guidelines (PDF)")

uploaded_file = st.file_uploader(
    "Upload a clinical guideline PDF",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Uploading and indexing PDF..."):
        files = {
            "file": (uploaded_file.name, uploaded_file, "application/pdf")
        }
        try:
            response = requests.post(
                f"{BACKEND_URL}/guidelines/upload",
                files=files,
                timeout=timeout_seconds
            )
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The backend took too long to process the PDF. You might want to try again or check the backend server.")
            st.stop()
        except requests.exceptions.ConnectionError:
            st.error("❌ Backend not reachable. Please ensure the backend server is running.")
            st.stop()
        except requests.exceptions.RequestException as e:
            st.error("❌ An error occurred while communicating with the backend.")
            st.code(str(e))
            st.stop()

    if response.status_code == 200:
        st.success("✅ PDF uploaded and indexed successfully")
        st.json(response.json())
    else:
        st.error("❌ Failed to upload PDF")
        st.code(response.text)

st.divider()

# =============================
# QUESTION ANSWERING SECTION
# =============================
st.header("❓ Ask a Clinical Question")

query = st.text_input(
    "Enter your clinical question",
    placeholder="e.g. What is the emergency referral procedure?"
)

ask_button = st.button("Ask CDSS", type="primary")

if ask_button:
    if not query.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Retrieving evidence and generating answer..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/cdss/ask",
                    params={"query": query},
                    timeout=timeout_seconds
                )
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The backend is taking too long to generate an answer. Please try a simpler query or check the backend server.")
                st.stop()
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not reachable. Please ensure the backend server is running.")
                st.stop()
            except requests.exceptions.RequestException as e:
                st.error("❌ An error occurred while communicating with the backend.")
                st.code(str(e))
                st.stop()

        if response.status_code == 200:
            result = response.json()

            # -------- Answer --------
            st.subheader("🧠 Answer")
            st.write(result.get("answer", "No answer returned"))

            # -------- Citations --------
            st.subheader("📚 Citations")
            citations = result.get("citations", [])
            if citations:
                for c in citations:
                    st.markdown(f"- **{c}**")
            else:
                st.info("No citations returned")

            # -------- Evidence --------
            st.subheader("🔍 Evidence Used")
            evidence = result.get("evidence_used", [])
            if evidence:
                for i, ev in enumerate(evidence, 1):
                    with st.expander(f"Evidence {i} ({ev.get('source', 'Unknown')})"):
                        st.write(ev.get("text", ""))
            else:
                st.info("No evidence chunks returned")

        else:
            st.error("❌ Error from backend")
            st.code(response.text)

# =============================
# FOOTER
# =============================
st.divider()
st.caption(
    "CDSS RAG System • FastAPI + FAISS + SentenceTransformers + Streamlit"
)
