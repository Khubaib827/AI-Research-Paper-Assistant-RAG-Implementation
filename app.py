# app.py - Complete Working Version with Chat at Bottom
import streamlit as st
import tempfile
import os
from datetime import datetime
from document_processor import PaperProcessor
from vector_store import VectorStore
from rag_pipeline import ResearchRAG
from analytics import ResearchAnalytics

# Page config
st.set_page_config(
    page_title="AI Research Paper Assistant",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        background: #f8f9ff;
        margin-bottom: 1.5rem;
    }
    .upload-area:hover {
        background: #f0f2ff;
        border-color: #764ba2;
    }
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    .weather-widget {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
    }
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        transition: all 0.3s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    .chat-container {
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if "ready" not in st.session_state:
    st.session_state.ready = False
if "rag" not in st.session_state:
    st.session_state.rag = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []
if "documents" not in st.session_state:
    st.session_state.documents = []
if "analytics" not in st.session_state:
    st.session_state.analytics = None
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "literature_review" not in st.session_state:
    st.session_state.literature_review = ""
if "comparison" not in st.session_state:
    st.session_state.comparison = ""
if "citations" not in st.session_state:
    st.session_state.citations = ""

# Header
st.markdown('<div class="main-header">📚 AI Research Paper Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">⚡ Powered by RAG + LangChain + FAISS + Local AI</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📄 Upload Papers")
    
    st.markdown("""
    <div class="upload-area">
        <h3 style="color: #667eea;">📁 Drag and drop files here</h3>
        <p style="color: #999;">Limit 200MB per file • PDF</p>
    </div>
    """, unsafe_allow_html=True)
    
    files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if files:
        st.info(f"📎 {len(files)} files selected")
    
    st.divider()
    
    st.markdown("### ⚙️ Configuration")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        chunk_size = st.slider("Chunk Size", 500, 2000, 1000, 100)
    with col2:
        chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200, 50)
    with col3:
        retrieval_k = st.slider("Retrieval K", 3, 10, 5, 1)
    
    st.divider()
    
    if st.button("🚀 Process Papers", use_container_width=True):
        if files:
            with st.spinner("Processing papers... This may take a few minutes..."):
                try:
                    temp_dir = tempfile.mkdtemp()
                    paths = []
                    for f in files:
                        path = os.path.join(temp_dir, f.name)
                        with open(path, "wb") as w:
                            w.write(f.getvalue())
                        paths.append(path)
                    
                    processor = PaperProcessor(chunk_size, chunk_overlap)
                    docs = processor.load_pdfs(paths)
                    
                    if not docs:
                        st.error("❌ No text extracted. Make sure PDFs contain text.")
                    else:
                        chunks = processor.chunk_docs(docs)
                        st.session_state.documents = docs
                        
                        vs = VectorStore()
                        index = vs.create_index(chunks)
                        
                        st.session_state.rag = ResearchRAG(index)
                        st.session_state.ready = True
                        st.session_state.processed_files = [f.name for f in files]
                        st.session_state.analytics = ResearchAnalytics(docs)
                        
                        st.success(f"✅ Processed {len(files)} papers successfully!")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please upload PDF files first")
    
    st.divider()
    
    if st.session_state.ready:
        st.success("✅ System Ready!")
        st.info(f"📚 {len(st.session_state.processed_files)} papers loaded")
    else:
        st.info("⏳ Upload papers and click Process")
    
    st.divider()
    
    st.markdown("### 🎯 Features")
    features = ["📝 Summary", "📚 Literature Review", "⚖️ Compare", "📖 Citations", "💬 Q&A"]
    for feature in features:
        st.markdown(f'<span class="feature-badge">{feature}</span>', unsafe_allow_html=True)

# Main content with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Summary", 
    "📚 Literature Review", 
    "⚖️ Compare", 
    "📖 Citations", 
    "📊 Analytics"
])

with tab1:
    st.markdown("### Generate Paper Summary")
    if st.button("📄 Generate Summary", key="summary_btn"):
        if st.session_state.ready:
            with st.spinner("Generating summary..."):
                try:
                    st.session_state.summary = st.session_state.rag.summarize()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please process papers first")
    
    if st.session_state.summary:
        st.markdown(st.session_state.summary)

with tab2:
    st.markdown("### Literature Review")
    topic = st.text_input("Research Topic", placeholder="Enter research topic...", key="topic_input")
    if st.button("📚 Generate Review", key="review_btn") and topic:
        if st.session_state.ready:
            with st.spinner(f"Generating literature review..."):
                try:
                    st.session_state.literature_review = st.session_state.rag.literature_review(topic)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please process papers first")
    
    if st.session_state.literature_review:
        st.markdown(st.session_state.literature_review)

with tab3:
    st.markdown("### Compare Papers")
    if st.button("⚖️ Compare Papers", key="compare_btn"):
        if st.session_state.ready:
            with st.spinner("Comparing papers..."):
                try:
                    st.session_state.comparison = st.session_state.rag.compare_papers()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please process papers first")
    
    if st.session_state.comparison:
        st.markdown(st.session_state.comparison)

with tab4:
    st.markdown("### Generate Citations")
    if st.button("📖 Generate Citations", key="citation_btn"):
        if st.session_state.ready:
            with st.spinner("Generating citations..."):
                try:
                    st.session_state.citations = st.session_state.rag.get_citations()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please process papers first")
    
    if st.session_state.citations:
        st.markdown(st.session_state.citations)

with tab5:
    st.markdown("### 📊 Analytics Dashboard")
    if st.session_state.ready and st.session_state.analytics:
        stats = st.session_state.analytics.get_summary_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Total Papers", stats['total_papers'])
        with col2:
            st.metric("📝 Total Words", f"{stats['total_words']:,}")
        with col3:
            avg = stats.get('avg_words_per_paper', 0)
            st.metric("📊 Avg Words/Paper", f"{avg:,}")
        
        st.divider()
        st.subheader("🔤 Top Keywords")
        word_freq = st.session_state.analytics.get_word_frequency(15)
        for word, count in word_freq:
            st.progress(count / word_freq[0][1], text=f"{word}: {count}")
    else:
        st.info("📊 Process papers first to see analytics")

# ============================================
# CHAT SECTION - COMPLETELY OUTSIDE TABS
# ============================================

st.divider()
st.markdown("### 💬 Q&A Chat")

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Empty space for chat input
st.markdown("---")

# CHAT INPUT - NOT INSIDE ANY CONTAINER
# Using a simple container but with chat_input at the root level
question = st.chat_input("Type your question about the research papers...", key="chat_input_main")

if question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    
    if st.session_state.ready:
        with st.spinner("💭 Analyzing papers..."):
            try:
                answer = st.session_state.rag.ask_question(question)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "⚠️ Please upload and process papers first."})
    
    st.rerun()

# Footer
st.divider()
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
        <div style="color: #999; font-size: 0.8rem;">
            Built with ❤️ using LangChain, FAISS, and Local AI
        </div>
    """, unsafe_allow_html=True)
with col2:
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(f"""
        <div style="text-align: right;">
            <span class="weather-widget">
                🌤️ 98°F • Mostly sunny • {current_time}
            </span>
        </div>
    """, unsafe_allow_html=True)