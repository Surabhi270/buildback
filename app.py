import streamlit as st
import os
import zipfile
import tempfile
import json
import re
import requests
import google.generativeai as genai
from pypdf import PdfReader

# --- CONFIGURATION ---
st.set_page_config(page_title="BuildBack: Architecture & MCQ Prep", page_icon="🏗️", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS INJECTION ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1200px; }
    .stApp { background-color: #0E1117; font-family: 'Inter', sans-serif; }
    
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: white; border: none; padding: 0.5rem 1.5rem; border-radius: 8px;
        font-weight: 600; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        transition: all 0.2s ease; width: 100%;
    }
    div.stButton > button:first-child:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    
    div[data-baseweb="input"] { background-color: #1A1D24; border: 1px solid #2D3748; border-radius: 8px; }
    div[data-testid="stFileUploadDropzone"] { background-color: #1A1D24; border: 2px dashed #4A5568; border-radius: 12px; }
    div[data-testid="stExpander"] { background-color: #1A1D24; border: 1px solid #2D3748; border-radius: 10px; }
    div[data-testid="stExpander"] summary { background-color: #1A1D24; color: #F8F9FA; font-weight: 600; }
    div.row-widget.stRadio > div { background-color: #1A1D24; border: 1px solid #2D3748; padding: 1.5rem; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.12); }
    pre { background-color: #0D1117 !important; border: 1px solid #30363D !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# Replace with your actual API key
API_KEY = "AIzaSyDwu1BI3OHerTm7elDr_xzNT2aDdFctLCI"
genai.configure(api_key=API_KEY)
MODEL_NAME = 'gemini-3-flash-preview'

# --- SESSION STATE INITIALIZATION ---
if "analysis_ready" not in st.session_state: st.session_state.analysis_ready = False
if "ai_report" not in st.session_state: st.session_state.ai_report = ""
if "mcq_data" not in st.session_state: st.session_state.mcq_data = []
if "current_q_idx" not in st.session_state: st.session_state.current_q_idx = 0
if "score" not in st.session_state: st.session_state.score = 0
if "answered_current" not in st.session_state: st.session_state.answered_current = False
if "selected_option" not in st.session_state: st.session_state.selected_option = None
if "project_name" not in st.session_state: st.session_state.project_name = "Project"

# --- CORE FUNCTIONS ---
def get_github_data(repo_url):
    try:
        url_parts = repo_url.rstrip('/').split('/')
        if len(url_parts) < 2: return "Invalid URL format.", []
        owner, repo = url_parts[-2], url_parts[-1]
        st.session_state.project_name = repo
        
        repo_info = requests.get(f"https://api.github.com/repos/{owner}/{repo}").json()
        if 'default_branch' not in repo_info: return "Repository not found.", []
        branch = repo_info['default_branch']
        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        tree_data = requests.get(tree_url).json()
        tree_str = ""
        if 'tree' in tree_data:
            for item in tree_data['tree']:
                path = item['path']
                if any(ign in path for ign in ['node_modules', 'venv', '.git', '__pycache__', 'dist']): continue
                tree_str += f"📄 {path}\n"
        frameworks = []
        raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/"
        for pkg in ["package.json", "requirements.txt"]:
            res = requests.get(raw_base + pkg)
            if res.status_code == 200:
                deps = res.text.lower()
                if 'react' in deps: frameworks.append('React')
                if 'express' in deps: frameworks.append('Express.js')
                if 'django' in deps: frameworks.append('Django')
        return tree_str, frameworks if frameworks else ["Unknown Stack"]
    except Exception as e: return f"Error: {e}", []

def extract_zip(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref: zip_ref.extractall(temp_dir)
    st.session_state.project_name = uploaded_file.name.split('.')[0]
    return temp_dir

def generate_file_tree(startpath, max_depth=3):
    tree_str = ""
    start_depth = startpath.count(os.sep)
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '__pycache__']]
        if root.count(os.sep) - start_depth > max_depth: continue
        indent = ' ' * 4 * (root.count(os.sep) - start_depth)
        tree_str += f"{indent}📂 {os.path.basename(root)}/\n"
        for f in files: tree_str += f"{indent}    📄 {f}\n"
    return tree_str

def detect_frameworks(temp_dir):
    frameworks = []
    if os.path.exists(os.path.join(temp_dir, 'package.json')): frameworks.append('Node.js Environment')
    if os.path.exists(os.path.join(temp_dir, 'requirements.txt')): frameworks.append('Python Environment')
    return frameworks if frameworks else ["Unknown Stack"]

def extract_text_from_pdf(file_obj):
    st.session_state.project_name = file_obj.name.split('.')[0]
    return "\n".join([page.extract_text() for page in PdfReader(file_obj).pages])

def extract_text_from_pptx(file_obj):
    st.session_state.project_name = file_obj.name.split('.')[0]
    text = ""
    for slide in Presentation(file_obj).slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"): text += shape.text + "\n"
    return text

def perform_analysis_and_generate_mcqs(content_type, content_data, frameworks):
    safe_data = content_data[:6000]
    context = f"Frameworks: {', '.join(frameworks)}\n\nData (Truncated):\n{safe_data}"
    model = genai.GenerativeModel(MODEL_NAME)
    
    report_prompt = f"""
    Reverse-engineer this {content_type} data and provide a comprehensive guide.
    Context Data:
    {context}
    
    Format EXACTLY in Markdown with these specific headers:
    ### 🏗️ System Architecture Summary
    (2-3 sentences high-level explanation of the project's purpose)
    ### 🧠 Component Breakdown
    (Detailed explanation of every major project detail, folder, and framework detected. Explain WHAT it is and WHY it is there in plain English.)
    ### 📊 Architecture Diagram
    (Mermaid.js `graph TD` inside a ```mermaid ``` block showing the system flow)
    ### 🗺️ Diagram Walkthrough
    (A step-by-step plain English explanation of the diagram above.)
    ### 🎙️ How to Explain This (The Pitch)
    (A simple script to explain this architecture to a professor.)
    """
    st.session_state.ai_report = model.generate_content(report_prompt).text
    
    mcq_prompt = f"""
    Based on the architecture context, create a 5-question Multiple Choice mock test.
    Context: {context}
    You MUST respond ONLY with a valid JSON array of objects.
    Format exactly like this:
    [
      {{
        "question": "Sample Question?",
        "options": ["A", "B", "C", "D"],
        "answer": "A",
        "explanation": "Because A is correct."
      }}
    ]
    """
    mcq_response = model.generate_content(mcq_prompt).text
    try:
        clean_json = re.sub(r'```json\n|\n```|```', '', mcq_response).strip()
        st.session_state.mcq_data = json.loads(clean_json)
    except json.JSONDecodeError:
        st.error("Failed to parse MCQs. Please try generating again.")
        return

    st.session_state.current_q_idx = 0
    st.session_state.score = 0
    st.session_state.answered_current = False
    st.session_state.selected_option = None
    st.session_state.analysis_ready = True

# --- NEW HERO HEADER ---
st.markdown("""
<div style='text-align: center; padding: 1rem 0 2rem 0;'>
    <h1 style='font-size: 4rem; margin-bottom: 0; background: -webkit-linear-gradient(135deg, #6366F1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>BuildBack</h1>
    <p style='font-size: 1.2rem; color: #A0AEC0; font-weight: 500;'>The Ultimate Architecture Reverse-Engineering & Defense Prep Tool</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR UI ---
with st.sidebar:
    st.header("⚙️ Project Input")
    st.markdown("Upload your code or docs here.")
    
    input_method = st.radio("Choose Source:", ["🔗 GitHub Repository", "📁 Local File Upload"])
    
    if input_method == "🔗 GitHub Repository":
        repo_url = st.text_input("Paste Public GitHub URL:")
        if st.button("🚀 Analyze Repository") and repo_url:
            with st.spinner("Fetching repo & analyzing..."):
                data, fw = get_github_data(repo_url)
                if "Error" not in data and "not found" not in data:
                    perform_analysis_and_generate_mcqs("code", data, fw)
                else: st.error(data)

    elif input_method == "📁 Local File Upload":
        uploaded_file = st.file_uploader("Upload (.zip, .pdf, .pptx)", type=["zip", "pdf", "ppt", "pptx"])
        if st.button("🚀 Analyze File") and uploaded_file:
            with st.spinner("Analyzing files..."):
                ext = uploaded_file.name.split('.')[-1].lower()
                if ext == "zip":
                    dir_path = extract_zip(uploaded_file)
                    perform_analysis_and_generate_mcqs("code", generate_file_tree(dir_path), detect_frameworks(dir_path))
                elif ext == "pdf": perform_analysis_and_generate_mcqs("document", extract_text_from_pdf(uploaded_file), [])
                elif ext in ["ppt", "pptx"]: perform_analysis_and_generate_mcqs("document", extract_text_from_pptx(uploaded_file), [])

    if st.session_state.analysis_ready:
        st.divider()
        if st.button("🔄 Start Over"):
            st.session_state.clear()
            st.rerun()

# --- MAIN DASHBOARD AREA ---
if not st.session_state.analysis_ready:
    st.info("👈 Please select a GitHub repository or upload a project file in the sidebar to begin.")
else:
    # Architecture Report
    st.subheader("📚 Reverse-Engineered Documentation")
    
    with st.expander("📖 View In-Depth Architecture Guide & Diagram Walkthrough", expanded=False):
        report = st.session_state.ai_report
        if "```mermaid" in report:
            parts = report.split("```mermaid")
            st.markdown(parts[0])
            bottom_parts = parts[1].split("```", 1)
            st.markdown(f"```mermaid\n{bottom_parts[0].strip()}\n```")
            if len(bottom_parts) > 1: st.markdown(bottom_parts[1])
        else:
            st.markdown(report)
            
    # THE NEW DOWNLOAD BUTTON
    st.download_button(
        label="📄 Download Full Architecture Report (.md)",
        data=st.session_state.ai_report,
        file_name=f"{st.session_state.project_name}_Architecture_Report.md",
        mime="text/markdown",
        use_container_width=True
    )
            
    st.divider()
    
    # MCQ UI
    st.header("📝 Defense Preparation Test")
    
    if st.session_state.mcq_data and st.session_state.current_q_idx < len(st.session_state.mcq_data):
        current_q = st.session_state.mcq_data[st.session_state.current_q_idx]
        total_q = len(st.session_state.mcq_data)
        
        progress_val = st.session_state.current_q_idx / total_q
        st.progress(progress_val, text=f"Progress: Question {st.session_state.current_q_idx + 1} of {total_q}")
        
        st.markdown(f"### **{current_q['question']}**")
        user_choice = st.radio("Select your answer:", current_q['options'], key=f"q_{st.session_state.current_q_idx}", disabled=st.session_state.answered_current, label_visibility="collapsed")
        
        st.write("") # Spacing
        
        if not st.session_state.answered_current:
            if st.button("Check Answer"):
                st.session_state.selected_option = user_choice
                st.session_state.answered_current = True
                if user_choice == current_q['answer']:
                    st.session_state.score += 1
                st.rerun() 
                
        if st.session_state.answered_current:
            if st.session_state.selected_option == current_q['answer']:
                st.success(f"✅ **Correct!** The answer is {current_q['answer']}.")
            else:
                st.error(f"❌ **Incorrect.** You chose {st.session_state.selected_option}, but the correct answer is {current_q['answer']}.")
            
            st.info(f"**💡 Explanation:** {current_q['explanation']}")
            
            if st.session_state.current_q_idx < total_q - 1:
                if st.button("Next Question ➡️"):
                    st.session_state.current_q_idx += 1
                    st.session_state.answered_current = False
                    st.session_state.selected_option = None
                    st.rerun()
            else:
                if st.button("See Final Score 🏆"):
                    st.session_state.current_q_idx += 1
                    st.rerun()

    # Final Score Dashboard
    elif st.session_state.current_q_idx >= len(st.session_state.mcq_data):
        st.progress(1.0, text="Progress: Complete!")
        st.balloons()
        st.success("🎉 **Mock Test Complete!** You are ready for the evaluation.")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            st.metric(label="Final Score", value=f"{st.session_state.score} / {len(st.session_state.mcq_data)}", delta="Completed")