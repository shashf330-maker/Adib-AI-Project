import streamlit as st
from groq import Groq
import os

# 1. Page Configuration & Full Professional Styling
st.set_page_config(page_title="ADIB - Smart AI Summarizer", page_icon="🎙️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0f172a; }

    /* Glassmorphism Results Cards */
    .result-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 24px;
        border-radius: 16px;
        color: #f1f5f9;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        direction: auto;
    }

    /* Gradient Title */
    .title-text {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Sidebar and Button Styling */
    .stSidebar { background-color: #1e293b !important; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 12px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar - Settings & Logic
with st.sidebar:
    st.markdown("## ⚙️ ADIB Settings")
    
    # تفاصيل حفظ المفتاح التي طلبتِها
    if 'api_key_saved' not in st.session_state:
        st.session_state['api_key_saved'] = False

    api_key_input = st.text_input("Groq API Key", type="password", help="Enter your valid Groq API key.")
    
    if api_key_input:
        st.session_state['api_key'] = api_key_input
        st.session_state['api_key_saved'] = True
        st.success("✅ API Key Saved Successfully!")
    
    st.markdown("---")
    summary_style = st.selectbox("Summary Style:", ["Key Points", "Detailed Executive Summary", "Q&A Study Guide"])
    st.info("🌍 ADIB automatically detects and responds in the same language as the audio.")

# 3. Main Interface
st.markdown('<h1 class="title-text">ADIB - Smart AI Summarizer</h1>', unsafe_allow_html=True)

col_up1, col_up2 = st.columns([3, 1])

with col_up1:
    uploaded_file = st.file_uploader("Upload Audio (Arabic & English supported)", type=["mp3", "wav", "m4a"])

with col_up2:
    st.write("###") 
    process_btn = st.button("🪄 Start AI Magic")

# 4. Processing Logic
if uploaded_file and process_btn:
    if not st.session_state.get('api_key_saved'):
        st.error("Access Denied: Please provide a valid Groq API Key in the sidebar.")
    else:
        with st.spinner("ADIB is processing your audio..."):
            try:
                # Save temp file
                with open("temp_audio.mp3", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                client = Groq(api_key=st.session_state['api_key'])

                # Step 1: Transcription (Stable Model)
                with open("temp_audio.mp3", "rb") as file:
                    transcription = client.audio.transcriptions.create(
                        file=("temp_audio.mp3", file.read()),
                        model="whisper-large-v3",
                        response_format="text",
                    )
                full_text = transcription

                # Step 2: Intelligent Summary (Language Auto-Detection)
                system_prompt = f"""
                You are ADIB, a professional academic assistant. 
                Summarize the text as {summary_style}.
                IMPORTANT: Respond in the SAME language as the audio transcription.
                """

                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_text}
                    ],
                    model="llama-3.1-8b-instant",
                )
                summary = completion.choices[0].message.content

                # UI Layout for Results
                st.markdown("---")
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.markdown(f'<div class="result-card"><h3>📝 Transcription</h3><p style="font-size:0.9rem; color:#cbd5e1;">{full_text}</p></div>', unsafe_allow_html=True)
                
                with res_col2:
                    st.markdown(f'<div class="result-card" style="border-left: 4px solid #3b82f6;"><h3>💡 AI Summary</h3><p style="font-size:0.9rem;">{summary}</p></div>', unsafe_allow_html=True)

                # --- 5. Professional HTML Report Generation ---
                html_report = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; color: #1e293b; background-color: #f8fafc; line-height: 1.6; }}
                        .header {{ text-align: center; border-bottom: 5px solid #3b82f6; padding-bottom: 20px; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                        .section {{ margin-top: 30px; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 6px solid #3b82f6; }}
                        h1 {{ color: #0f172a; margin: 0; }}
                        h2 {{ color: #2563eb; margin-top: 0; }}
                        .footer {{ margin-top: 50px; font-size: 0.8em; color: #94a3b8; text-align: center; }}
                    </style>
                </head>
                <body dir="auto">
                    <div class="header">
                        <h1>ADIB AI PROFESSIONAL REPORT</h1>
                        <p>Smart Academic Summary & Transcription</p>
                    </div>
                    <div class="section">
                        <h2>📝 Transcription</h2>
                        <p>{full_text}</p>
                    </div>
                    <div class="section">
                        <h2>💡 AI Summary ({summary_style})</h2>
                        <p>{summary}</p>
                    </div>
                    <div class="footer">Generated by ADIB AI Assistant | {st.date_input("Today", disabled=True)}</div>
                </body>
                </html>
                """

                st.download_button(
                    label="📥 Download Professional HTML Report",
                    data=html_report,
                    file_name="Adib_Report.html",
                    mime="text/html"
                )
                
                os.remove("temp_audio.mp3")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# تجربة التشغيل
# text, brief = adib_process("voice.mp3")
# print("--- النص الكامل ---\n", text)
# print("--- الملخص الذكي ---\n", brief)
# file_to_test = r"C:\Users\WinDows\Downloads\voice.mp3"
# python -m streamlit run adib_app.py
