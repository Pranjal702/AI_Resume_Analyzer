import streamlit as st
import pypdf
import requests
import json
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Paste your API Gateway URL here
API_URL = "https://5x2e5i0cgj.execute-api.us-east-1.amazonaws.com/analyze"

# Set up page with a dark-mode first configuration layout
st.set_page_config(page_title="AI Resume Engine Pro", layout="wide", initial_sidebar_state="collapsed")

# # Inject Custom CSS Injector for a sleek modern Dark SaaS Theme UI
st.markdown("""
    <style>
    /* Floating subtle watermark footer */
    .watermark {
        position: fixed;
        bottom: 15px;
        left: 15px;
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 500;
        color: #8b949e;
        background-color: rgba(22, 27, 34, 0.8);
        padding: 6px 12px;
        border-radius: 6px;
        border: 1px solid #30363d;
        z-index: 999999;
        pointer-events: none;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
}
                                  !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 123, 0, 0.4) !important;
    }
    /* Text input formatting tweaks styling optimization */
    textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    /* Expander modern custom styling block */
    .conda-expander {
        border: 1px solid #30363d !important;
        background-color: #161b22 !important;
    }
    </style>
""", unsafe_allow_html=True)
# Render the floating watermark on screen
st.markdown('<div class="watermark">🚀 Built by Pranjal Sharma</div>', unsafe_allow_html=True)
# Persistent Session Memory initialization
if 'step' not in st.session_state: st.session_state.step = 1
if 'resume_text' not in st.session_state: st.session_state.resume_text = ""
if 'analysis' not in st.session_state: st.session_state.analysis = None
if 'merged_text' not in st.session_state: st.session_state.merged_text = ""

def generate_pdf(text_content):
    """Compiles string text paragraphs into a clean professional structural PDF file."""
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=6
    )
    
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
        job_desc = st.text_area("Paste role details and required engineering skills here", height=180, label_visibility="collapsed", placeholder="Paste the job description keywords here...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Analyze Match Parameters & Evaluate Scores 🚀"):
        if uploaded_file and job_desc:
            with st.spinner("Analyzing text alignment parameters across modern cloud architecture..."):
                text = ""
                if uploaded_file.type == "application/pdf":
                    reader = pypdf.PdfReader(uploaded_file)
                    for page in reader.pages: 
                        text += page.extract_text() + "\n"
                else:
                    text = uploaded_file.read().decode("utf-8")
                
                st.session_state.resume_text = text
                
                payload = {"action": "analyze", "resume_text": text, "job_description": job_desc}
                try:
                    response = requests.post(API_URL, json=payload)
                    st.session_state.analysis = response.json()
                    st.session_state.step = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to communicate with AWS Backend API: {str(e)}")
        else:
            st.warning("Please verify both file attachment data and target text field properties are completely populated.")

# ==========================================
# SCREEN 2: METRICS DASHBOARD & CHECKBOX MERGING
# ==========================================
elif st.session_state.step == 2:
    st.title("📊 ATS Evaluation Scorecard & Optimization Deck")
    data = st.session_state.analysis
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        # Custom HTML structural card container block layout
        st.markdown(f"""
            <div class="metric-card">
                <div style="color: #8b949e; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Overall Match Compatibility</div>
                <div class="score-text">{data.get('score', 0)}%</div>
                <p style="margin: 0; color: #c9d1d9; line-height: 1.5;">{data.get('summary', '')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("💡 Identified Strengths")
        for s in data.get('strengths', []): 
            st.markdown(f"⚡ &nbsp; {s}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("⚠️ Missing Core Competencies")
        for m in data.get('missing_skills', []): 
            st.markdown(f"<span style='color:#ff7b00;'>✕</span> &nbsp; {m}", unsafe_allow_html=True)

    with col2:
        st.subheader("🎯 Premium Actionable Recommendations")
        st.write("Review tailored modifications generated by AI. Select components below to automatically merge updates into your core document file structure:")
        
        selected_improvements = []
        for idx, imp in enumerate(data.get('improvements', [])):
            with st.expander(f"📌 Fix Context: {imp.get('context', 'Section Adjustments')}"):
                st.markdown(f"<span style='color:#8b949e;'>Current text segment:</span><br><code style='background-color:#21262d; padding:4px 8px; border-radius:4px; display:block; margin:5px 0;'> {imp.get('original','')} </code>", unsafe_allow_html=True)
                st.markdown(f"<span style='color:#ff7b00; font-weight:600;'>Suggested optimization structural update:</span><br><strong style='color:#ffffff;'> {imp.get('suggested','')} </strong>", unsafe_allow_html=True)
                st.caption(f"Strategy justification: {imp.get('reason','')}")
                if st.checkbox("Accept modification patch and auto-merge", key=f"merge_{idx}"):
                    selected_improvements.append(imp)
        
        st.write("---")
        if st.button("Auto-Merge Selected Corrections & Edit Draft ⚡"):
            with st.spinner("Processing structural adjustments dynamically..."):
                payload = {
                    "action": "merge", 
                    "resume_text": st.session_state.resume_text, 
                    "improvements": selected_improvements
                }
                res = requests.post(API_URL, json=payload)
                st.session_state.merged_text = res.json().get('updated_resume', '')
                st.session_state.step = 3
                st.rerun()

# ==========================================
# SCREEN 3: DEDICATED MANUAL WORKSPACE & DOWNLOAD
# ==========================================
elif st.session_state.step == 3:
    st.title("🪟 Interactive Tailoring Workspace Studio")
    st.write("Your accepted changes have been merged. Review, add technical configurations, or remove formatting lines within the production workspace block below.")
    
    # Live full editable workspace area block
    final_edited_text = st.text_area("Live Document Workspace", value=st.session_state.merged_text, height=480, label_visibility="collapsed")
    
    # Re-compile PDF dynamically on every change inside the editing block
    pdf_data = generate_pdf(final_edited_text)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_x, col_y = st.columns([1, 4])
    with col_x:
        st.download_button(
            label="📥 Download Tailored Resume (PDF)",
            data=pdf_data,
            file_name="tailored_optimized_resume.pdf",
            mime="application/pdf"
            )
    with col_y:
        if st.button("🔄 Reset Environment and Start Fresh"):
            st.session_state.clear()
            st.session_state.step = 1
            st.rerun()
