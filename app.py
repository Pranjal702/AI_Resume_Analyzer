import streamlit as st
import pypdf
import requests
import json
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Consolidated deployment URL
API_URL = "https://amazonaws.com"

st.set_page_config(page_title="AI Resume Engine Pro", layout="wide", initial_sidebar_state="collapsed")

# Complete CSS UI Injector with Bottom Left Watermark configuration
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    h1 { font-family: 'Inter', sans-serif; font-weight: 800; background: linear-gradient(45deg, #ff7b00, #ffae00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 25px !important; }
    h2, h3 { color: #f0f6fc !important; font-family: 'Inter', sans-serif; font-weight: 600; }
    .metric-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
    .score-text { font-size: 48px; font-weight: 800; color: #ffaa00; margin-bottom: 5px; }
    .stButton>button { background: linear-gradient(135deg, #ff7b00 0%, #e66e00 100%) !important; color: white !important; border: none !important; font-weight: 600 !important; padding: 12px 30px !important; border-radius: 8px !important; transition: all 0.3s ease !important; width: 100%; }
    .stButton>button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(255, 123, 0, 0.4) !important; }
    textarea { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
    
    /* Watermark - Anchored securely to the Bottom-Left */
    .watermark {
        position: fixed; bottom: 15px; left: 15px; font-family: 'Inter', sans-serif; font-size: 12px;
        font-weight: 500; color: #8b949e; background-color: rgba(22, 27, 34, 0.9); padding: 6px 12px;
        border-radius: 6px; border: 1px solid #30363d; z-index: 999999; pointer-events: none;
        letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="watermark">🚀 Pranjal Sharma</div>', unsafe_allow_html=True)

# Strict session state initialization schema
if 'step' not in st.session_state: st.session_state.step = 1
if 'resume_text' not in st.session_state: st.session_state.resume_text = ""
if 'analysis' not in st.session_state: st.session_state.analysis = None
if 'merged_text' not in st.session_state: st.session_state.merged_text = ""
if 'checked_improvements' not in st.session_state: st.session_state.checked_improvements = {}

def generate_pdf(text_content):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle('ResumeBody', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6, textColor='#000000')
    story = []
    for line in text_content.split('\n'):
        if line.strip() == "":
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(line, body_style))
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# ==========================================
# SCREEN 1: INPUT AND UPLOAD INTERFACE
# ==========================================
if st.session_state.step == 1:
    st.title("✨ AI Resume Analyzer & Match Optimization Engine")
    st.write("Optimize your application for Applicant Tracking Systems (ATS) instantly using serverless AI analytics.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📂 Upload Current Resume")
        uploaded_file = st.file_uploader("Select original file data", type=["pdf", "txt"], label_visibility="collapsed")
    with col_b:
        st.subheader("🎯 Target Job Description")
        job_desc = st.text_area("Paste role details and required engineering skills here", height=180, label_visibility="collapsed", placeholder="Paste job description keywords here...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Analyze Match Parameters & Evaluate Scores 🚀"):
        if uploaded_file and job_desc:
            with st.spinner("Extracting contents and evaluation scores via AWS Gateway..."):
                text = ""
                if uploaded_file.type == "application/pdf":
                    reader = pypdf.PdfReader(uploaded_file)
                    for page in reader.pages: text += page.extract_text() + "\n"
                else:
                    text = uploaded_file.read().decode("utf-8")
                
                st.session_state.resume_text = text
                
                try:
                    response = requests.post(API_URL, json={"action": "analyze", "resume_text": text, "job_description": job_desc})
                    st.session_state.analysis = response.json()
                    st.session_state.checked_improvements = {i: False for i in range(len(st.session_state.analysis.get('improvements', [])))}
                    st.session_state.step = 2
                    st.经济_rerun = st.rerun()
                except Exception as e:
                    st.error(f"Backend API Communication Error: {str(e)}")
        else:
            st.warning("Please upload a file and fill out the job description before continuing.")

# ==========================================
# SCREEN 2: SCORECARD & ISOLATED SELECTIONS
# ==========================================
elif st.session_state.step == 2:
    st.title("📊 ATS Evaluation Scorecard & Optimization Deck")
    data = st.session_state.analysis
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="color: #8b949e; font-size: 14px; font-weight: 600; text-transform: uppercase;">Overall Match Compatibility</div>
                <div class="score-text">{data.get('score', 0)}%</div>
                <p style="margin: 0; color: #c9d1d9; line-height: 1.5;">{data.get('summary', '')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("💡 Identified Strengths")
        for s in data.get('strengths', []): st.markdown(f"⚡ &nbsp; {s}")
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("⚠️ Missing Core Competencies")
        for m in data.get('missing_skills', []): st.markdown(f"<span style='color:#ff7b00;'>✕</span> &nbsp; {m}", unsafe_allow_html=True)

    # Use st.fragment callback logic wrapper to isolate checkbox operations from total app refreshes
    @st.fragment
    def render_improvement_matrix():
        st.subheader("🎯 Premium Actionable Recommendations")
        st.write("Select the specific changes you want to merge seamlessly into your original document layout structure:")
        
        for idx, imp in enumerate(data.get('improvements', [])):
            with st.expander(f"📌 Section Correction Context: {imp.get('context', 'Experience Updates')}"):
                st.markdown(f"<span style='color:#8b949e;'>Current segment text:</span><code style='background-color:#21262d; padding:4px 8px; border-radius:4px; display:block; margin:5px 0;'>{imp.get('original','')}</code>", unsafe_allow_html=True)
                st.markdown(f"<span style='color:#ff7b00; font-weight:600;'>Suggested update variant:</span><br><strong style='color:#ffffff;'>{imp.get('suggested','')}</strong>", unsafe_allow_html=True)
                st.caption(f"Strategy reasoning: {imp.get('reason','')}")
                
                # Persist state variable selection instantly into memory without triggering a full layout rebuild
                st.session_state.checked_improvements[idx] = st.checkbox("Merge optimization", key=f"patch_{idx}", value=st.session_state.checked_improvements.get(idx, False))

        st.write("---")
        if st.button("Auto-Merge Selected Corrections & Edit Draft ⚡"):
            improvements_to_send = [imp for idx, imp in enumerate(data.get('improvements', [])) if st.session_state.checked_improvements.get(idx)]
            with st.spinner("Processing structural adjustments dynamically..."):
                try:
                    res = requests.post(API_URL, json={"action": "merge", "resume_text": st.session_state.resume_text, "improvements": improvements_to_send})
                    st.session_state.merged_text = res.json().get('updated_resume', '')
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e:
                    st.error(f"Merging failed: {str(e)}")

    render_improvement_matrix()

# ==========================================
# SCREEN 3: WORKSPACE STUDIO
# ==========================================
elif st.session_state.step == 3:
    st.title("🪟 Interactive Tailoring Workspace Studio")
    st.write("Your accepted changes have been merged. Review, add technical configurations, or remove formatting lines within the production workspace block below.")
    
    # Store work area text data securely
    final_text = st.text_area("Live Document Workspace", value=st.session_state.merged_text, height=480, label_visibility="collapsed")
    
    col_x, col_y = st.columns(2)
    with col_x:
        # Generate the PDF binary array directly from the live edited state variable window frame contents
        st.download_button(label="📥 Download Tailored Resume (PDF)", data=generate_pdf(final_text), file_name="tailored_optimized_resume.pdf", mime="application/pdf")
    with col_y:
        if st.button("🔄 Reset Environment and Start Fresh"):
            st.session_state.clear()
            st.session_state.step = 1
            st.rerun()
