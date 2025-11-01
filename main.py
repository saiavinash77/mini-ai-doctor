# main.py
import streamlit as st 
from app.ui import pdf_upload
from app.pdf_utils import extract_text_from_pdf
from app.chat_utils import get_chat_model, ask_chat_model
from app.config import EURI_API_KEY
from app.vectorstore_utils import create_faiss_index, retrieve_similar_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time

# Page setup
st.set_page_config(page_title="MediChat-Pro -Medical Document Assistant", page_icon="🏥-🤖", layout="wide")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_model" not in st.session_state:
    st.session_state.chat_model = None



# Sidebar: PDF Upload
with st.sidebar:
    st.markdown("### 📁 Document Upload")
    uploaded_files = pdf_upload()
    if uploaded_files:
        st.success(f"📄 {len(uploaded_files)} document(s) uploaded")
        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing your medical documents..."):
                all_texts = [extract_text_from_pdf(file) for file in uploaded_files]
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = [chunk for text in all_texts for chunk in splitter.split_text(text)]
                st.session_state.vectorstore = create_faiss_index(chunks)
                st.session_state.chat_model = get_chat_model(EURI_API_KEY)
                st.success("✅ Documents processed successfully!")
                st.balloons()

# Chat interface
st.markdown("### 💬 Chat with Your Medical Documents")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Chat input
if prompt := st.chat_input("Ask about your medical documents..."):
    timestamp = time.strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching documents..."):
                relevant_docs = retrieve_similar_documents(st.session_state.vectorstore, prompt)
                context = "\n\n".join(relevant_docs)
                system_prompt = f"""You are MediChat Pro...Medical Documents:\n{context}\nUser Question: {prompt}\nAnswer:"""
                response = ask_chat_model(st.session_state.chat_model, system_prompt)
            st.markdown(response)
            st.caption(timestamp)
            st.session_state.messages.append({"role": "assistant", "content": response, "timestamp": timestamp})
    else:
        with st.chat_message("assistant"):
            st.error("⚠️ Please upload and process documents first!")
            st.caption(timestamp)

# Footer
st.markdown("---")
st.markdown("""<div style="text-align: center;">🤖 Powered by Euri AI & LangChain</div>""", unsafe_allow_html=True)

st.markdown("""<div style = "text-align: center;">powered by euri ai &langchain</div>""")

















###################################
# Sidebar: PDF Upload
with st.sidebar:
    st.markdown("### 📁 Document Upload")
    uploaded_files = pdf_upload()
    if uploaded_files:
        st.success(f"📄 {len(uploaded_files)} document(s) uploaded")
        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing your medical documents..."):
                all_texts = [extract_text_from_pdf(file) for file in uploaded_files]
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = [chunk for text in all_texts for chunk in splitter.split_text(text)]
                st.session_state.vectorstore = create_faiss_index(chunks)
                st.session_state.chat_model = get_chat_model(EURI_API_KEY)
                st.success("✅ Documents processed successfully!")
                st.balloons()