# chalooooooo...
import streamlit as st
import pickle
import time
import base64
from collections import Counter
import streamlit.components.v1 as components
import pandas as pd

# page configuration...
st.set_page_config(page_title="Email Spam Detector", layout="wide")

# audio helper...
def get_audio_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# CSS (kuch naya try kiya)...
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&display=swap');

    .stApp {
        background-color: #000808;
        background-image: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                          linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 2px, 3px 100%;
        font-family: 'Fira Code', monospace;
        color: #00ff41;
    }

    .terminal-header {
        border-bottom: 2px solid #00ff41; padding: 15px; text-align: center;
        text-shadow: 0 0 15px #00ff41; letter-spacing: 8px;
        text-transform: uppercase; margin-bottom: 25px;
    }

    .custom-container { display: flex; gap: 20px; margin-bottom: 25px; }
    
    .box-left {
        flex: 1; border: 1px solid #00ff41; padding: 10px;
        font-size: 32px; font-weight: bold; text-shadow: 0 0 10px #00ff41;
        display: flex; align-items: center; justify-content: center;
        background: rgba(0, 255, 65, 0.02);
    }
    
    .box-right {
        flex: 2; border: 1px solid #00ff41; padding: 10px;
        overflow: hidden; background: rgba(0, 255, 65, 0.05);
        display: flex; align-items: center;
        min-width: 0;
    }

    .binary-small {
        font-size: clamp(14px, 4vw, 22px); 
        white-space: nowrap;
        animation: binary-scroll 10s linear infinite; opacity: 0.8;
        letter-spacing: 2px;
    }

    @keyframes binary-scroll { 0% { transform: translateX(0%); } 100% { transform: translateX(-50%); } }

    @media (max-width: 768px) {
        .custom-container { flex-direction: column; gap: 10px; }
        .box-left { font-size: 20px; }
        .binary-small { font-size: 16px; animation-duration: 6s; }
    }

    .radar-circle {
        width: 160px; height: 160px; border: 2px solid #00ff41; border-radius: 50%;
        position: relative; margin: 0 auto; overflow: hidden;
        background: radial-gradient(circle, rgba(0,255,65,0.1) 0%, transparent 80%);
        transition: 0.5s;
    }

    .radar-sweep {
        width: 100%; height: 100%;
        background: conic-gradient(from 0deg, transparent, #00ff41);
        animation: rotate 4s linear infinite; opacity: 0.5;
    }
    
    .threat-dot {
        position: absolute; width: 10px; height: 10px; background-color: #ff003c;
        border-radius: 50%; box-shadow: 0 0 15px #ff003c, 0 0 30px #ff003c;
        z-index: 10; animation: blink 0.6s infinite;
    }

    @keyframes blink { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.8); } }
    @keyframes rotate { 100% { transform: rotate(360deg); } }

    div[data-baseweb="textarea"] { border: 1px solid #00ff41 !important; background: transparent !important; }
    textarea { color: #00ff41 !important; font-size: 16px !important; }
    
    .stButton>button {
        background: transparent !important; color: #00ff41 !important; border: 1px solid #00ff41 !important;
        width: 100%; font-weight: bold;
    }
    .stButton>button:hover { background: #00ff41 !important; color: black !important; box-shadow: 0 0 20px #00ff41; }

    .stProgress > div > div > div > div {
        background-color: var(--p-color) !important;
    }

    .element-container iframe {
        filter: invert(100%) hue-rotate(100deg) brightness(1.2);
        border: 1px solid #00ff41 !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def system_init():
    try:
        with open('spam_model.pkl', 'rb') as f: m = pickle.load(f)
        with open('words_list.pkl', 'rb') as f: w = pickle.load(f)
        return m, w
    except:
        return None, None

model, words_list = system_init()

st.markdown('<div class="terminal-header"><h1>[ NEURAL SCANNER v1.0 ]</h1></div>', unsafe_allow_html=True)

binary_text = "0101001100101100101011001011010100101001101010" * 7
st.markdown(f"""
    <div class="custom-container">
        <div class="box-left">SYSTEM ONLINE</div>
        <div class="box-right"><div class="binary-small">{binary_text}</div></div>
    </div>
""", unsafe_allow_html=True)

if "is_spam" not in st.session_state:
    st.session_state.is_spam = False
if "has_run" not in st.session_state:
    st.session_state.has_run = False

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### SYSTEM_RADAR")
    alert_style = "border: 2px solid #ff003c; box-shadow: 0 0 20px #ff003c;" if st.session_state.is_spam else ""
    st.markdown(f"""
        <div class="radar-circle" style="{alert_style}">
            <div class="radar-sweep"></div>
            {'''<div class="threat-dot" style="top:25%; left:60%;"></div>
                <div class="threat-dot" style="top:75%; left:45%;"></div>
                <div class="threat-dot" style="top:45%; left:25%;"></div>''' if st.session_state.is_spam else ''}
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    status_text = "ALERT" if st.session_state.is_spam else "OPERATIONAL"
    threat_text = "DETECTED" if st.session_state.is_spam else "NONE"
    st.code(f"STATUS: {status_text}\nTHREATS: {threat_text}\nCORE: MNB-V1")

with col2:
    st.markdown("### SIGNAL_ANALYSIS")
    user_input = st.text_area("", height=300, placeholder="Paste Email or SMS here...", key="main_input")
    
    if st.button("EXECUTE SCAN"):
        if user_input and model:
            with st.spinner("Intercepting Signals..."):
                time.sleep(1)
                words = user_input.lower().split()
                counts = Counter(words)
                vec = [counts.get(w, 0) for w in words_list]
                res = model.predict([vec])
                st.session_state.is_spam = True if res[0] == 1 else False
                st.session_state.has_run = True
            st.rerun()
        else:
            st.warning("NO DATA DETECTED.")

    if st.session_state.has_run:
        bar_color = "#ff003c" if st.session_state.is_spam else "#00ff41"
        st.markdown(f'<style>:root {{ --p-color: {bar_color}; }}</style>', unsafe_allow_html=True)
        st.write("SCAN COMPLETE")
        st.progress(100)
        
        if st.session_state.is_spam:
            st.markdown("<h2 style='color:#ff003c; text-align:center;'>[ !! THREAT DETECTED: SPAM !! ]</h2>", unsafe_allow_html=True)
            audio_file = "spam.mp3"
        else:
            st.markdown("<h2 style='color:#00ff41; text-align:center;'>[ SIGNAL SECURE: SAFE ]</h2>", unsafe_allow_html=True)
            audio_file = "safe.mp3"
            
        audio_data = get_audio_base64(audio_file)
        if audio_data:
            components.html(f"""
                <script>
                    var audio = new Audio("data:audio/mp3;base64,{audio_data}");
                    audio.play();
                </script>
            """, height=0)
    else:
        st.markdown('<style>:root { --p-color: #00ff41; }</style>', unsafe_allow_html=True)
        st.write("WAITING FOR SIGNAL...")
        st.progress(0)

with col3:
    st.markdown("### GEO_LOCATION")
    map_data = pd.DataFrame({'lat': [33.6844], 'lon': [73.0479]})
    st.map(map_data, zoom=4, use_container_width=True)
    st.code("SOURCE_IP: 192.168.10.1\nREGION: PK-IS\nLOC: 33.68, 73.04")

st.markdown("<p style='text-align:center; opacity:0.5; font-size:12px; margin-top:50px;'>USER: SHAHEER_AHMIII | SYSTEM: NEURAL_CORE_V1</p>", unsafe_allow_html=True)