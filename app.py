import streamlit as st
import requests

st.set_page_config(page_title="Business Document Analyzer", page_icon="📄")
st.title("📄 Business Document Analyzer")

# Upload Section
st.header("Step 1 — Upload Your Document")
uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded:
    with st.spinner("Processing document..."):
        res = requests.post(
            "http://fastapi:8000/upload",
            files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
        )
    
    if res.status_code == 200:
        doc_id = res.json()["doc_id"]
        st.session_state["doc_id"] = doc_id
        st.success(f"✅ Document ingested! ID: `{doc_id}`")
    else:
        st.error("❌ Upload failed. Make sure FastAPI is running.")

# Query Section
if "doc_id" in st.session_state:
    st.header("Step 2 — Ask Questions")
    question = st.text_input("Ask anything about this document:")

    if question:
        with st.spinner("Thinking..."):
            res = requests.post(
                "http://fastapi:8000/query",
                json={"question": question, "doc_id": st.session_state["doc_id"]}
            )

        if res.status_code == 200:
            data = res.json()
            st.write("### 💬 Answer")
            st.write(data["answer"])
            st.write("### 📚 Sources")
            for src in data["sources"]:
                st.caption(src)
        else:
            st.error("❌ Query failed.")

