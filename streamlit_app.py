import streamlit as st
import subprocess
import json
import sys
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.resolve()

# Initialize session state BEFORE functions that use it
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'video_url' not in st.session_state:
    st.session_state.video_url = ""
if 'transcript_data' not in st.session_state:
    st.session_state.transcript_data = None
if 'topics_data' not in st.session_state:
    st.session_state.topics_data = None
if 'research_data' not in st.session_state:
    st.session_state.research_data = None
if 'script_content' not in st.session_state:
    st.session_state.script_content = None

# ... (rest of config)

def run_command(command):
    # Ensure command uses the current python interpreter
    if command[0] == "python3":
        command[0] = sys.executable
    
    result = subprocess.run(command, shell=False, capture_output=True, text=True, cwd=str(BASE_DIR))
    return result.returncode == 0, result.stderr

def render_step_indicator():
    steps = ["📝 URL", "🎙️ Trascrivi", "🧠 Analizza", "🌍 Ricerca", "✍️ Genera"]
    cols = st.columns(5)
    for i, (col, step_name) in enumerate(zip(cols, steps)):
        with col:
            if i < st.session_state.current_step:
                st.markdown(f"<div style='text-align:center'><div style='width:40px;height:40px;border-radius:50%;background:#22c55e;color:white;display:inline-flex;align-items:center;justify-content:center;font-weight:bold'>✓</div><br><small>{step_name}</small></div>", unsafe_allow_html=True)
            elif i == st.session_state.current_step:
                st.markdown(f"<div style='text-align:center'><div style='width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#9d4edd,#d946ef);color:white;display:inline-flex;align-items:center;justify-content:center;font-weight:bold'>{i+1}</div><br><small style='color:#9d4edd'><b>{step_name}</b></small></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:center'><div style='width:40px;height:40px;border-radius:50%;background:#1e293b;color:#64748b;border:2px solid #334155;display:inline-flex;align-items:center;justify-content:center;font-weight:bold'>{i+1}</div><br><small style='color:#64748b'>{step_name}</small></div>", unsafe_allow_html=True)

# Header
st.title("🚀 Fuze Video Repurposer Agent")
st.caption("Trasforma video YouTube in nuovi script virali con l'IA.")
st.divider()

# Step Indicator
render_step_indicator()
st.markdown("<br>", unsafe_allow_html=True)

# ===== STEP 0: URL Input =====
if st.session_state.current_step == 0:
    st.header("📝 Step 1: Inserisci URL Video")
    st.markdown("<div class='big-card'>", unsafe_allow_html=True)
    
    url = st.text_input("🔗 URL del video YouTube:", placeholder="https://youtube.com/watch?v=...", value=st.session_state.video_url)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ Procedi alla Trascrizione", disabled=not url, use_container_width=True):
            st.session_state.video_url = url
            st.session_state.current_step = 1
            st.rerun()

# ===== STEP 1: Transcription =====
elif st.session_state.current_step == 1:
    st.header("🎙️ Step 2: Trascrizione Video")
    st.markdown("<div class='big-card'>", unsafe_allow_html=True)
    
    st.info(f"**Video:** {st.session_state.video_url}")
    
    if st.session_state.transcript_data is None:
        st.write("Clicca il pulsante per avviare la trascrizione del video usando Apify.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎙️ Avvia Trascrizione", use_container_width=True):
                with st.spinner("Trascrizione in corso... (può richiedere 30-60 secondi)"):
                    success, error = run_command(["python3", "execution/transcribe_video.py", "--url", st.session_state.video_url])
                    if success:
                        with open(BASE_DIR / ".tmp/transcript.json") as f:
                            st.session_state.transcript_data = json.load(f)
                        st.success("✅ Trascrizione completata!")
                        st.rerun()
                    else:
                        st.error(f"Errore: {error}")
    else:
        st.success("✅ Trascrizione completata!")
        transcript_text = st.session_state.transcript_data.get("transcript", "")
        st.text_area("Preview Trascrizione:", transcript_text[:1000] + "..." if len(transcript_text) > 1000 else transcript_text, height=200)
        st.caption(f"Lunghezza totale: {len(transcript_text)} caratteri")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            st.session_state.current_step = 0
            st.rerun()
    with col2:
        if st.button("▶️ Procedi all'Analisi", disabled=st.session_state.transcript_data is None, use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()

# ===== STEP 2: Analysis =====
elif st.session_state.current_step == 2:
    st.header("🧠 Step 3: Analisi Topic")
    st.markdown("<div class='big-card'>", unsafe_allow_html=True)
    
    if st.session_state.topics_data is None:
        st.write("Claude AI analizzerà la trascrizione ed estrarrà i topic principali.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🧠 Analizza Topic", use_container_width=True):
                with st.spinner("Analisi in corso con Claude..."):
                    success, error = run_command(["python3", "execution/analyze_topics.py"])
                    if success:
                        with open(BASE_DIR / ".tmp/topics.json") as f:
                            st.session_state.topics_data = json.load(f)
                        st.success("✅ Analisi completata!")
                        st.rerun()
                    else:
                        st.error(f"Errore: {error}")
    else:
        st.success("✅ Analisi completata!")
        st.json(st.session_state.topics_data)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with col2:
        if st.button("▶️ Procedi alla Ricerca", disabled=st.session_state.topics_data is None, use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()

# ===== STEP 3: Research =====
elif st.session_state.current_step == 3:
    st.header("🌍 Step 4: Ricerca Web")
    st.markdown("<div class='big-card'>", unsafe_allow_html=True)
    
    if st.session_state.research_data is None:
        st.write("Perplexity cercherà articoli e fonti aggiornate per ogni topic.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌍 Avvia Ricerca", use_container_width=True):
                with st.spinner("Ricerca in corso con Perplexity... (può richiedere 1-2 minuti)"):
                    success, error = run_command(["python3", "execution/research_topics.py"])
                    if success:
                        with open(BASE_DIR / ".tmp/research.json") as f:
                            st.session_state.research_data = json.load(f)
                        st.success("✅ Ricerca completata!")
                        st.rerun()
                    else:
                        st.error(f"Errore: {error}")
    else:
        st.success("✅ Ricerca completata!")
        with st.expander("📚 Vedi Risultati Ricerca", expanded=True):
            for item in st.session_state.research_data.get("research_results", []):
                st.markdown(f"**{item.get('topic', 'Topic')}**")
                st.write(item.get('content', '')[:500] + "...")
                st.divider()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            st.session_state.current_step = 2
            st.rerun()
    with col2:
        if st.button("▶️ Genera Script Finale", disabled=st.session_state.research_data is None, use_container_width=True):
            st.session_state.current_step = 4
            st.rerun()

# ===== STEP 4: Generation =====
elif st.session_state.current_step == 4:
    st.header("✍️ Step 5: Generazione Script")
    st.markdown("<div class='big-card'>", unsafe_allow_html=True)
    
    if st.session_state.script_content is None:
        st.write("Claude genererà un nuovo script video basato sullo stile originale e le nuove ricerche.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✍️ Genera Script", use_container_width=True):
                with st.spinner("Generazione in corso con Claude..."):
                    success, error = run_command(["python3", "execution/generate_script.py"])
                    if success:
                        with open(BASE_DIR / ".tmp/new_script.md") as f:
                            st.session_state.script_content = f.read()
                        st.balloons()
                        st.success("🎉 Script Generato con Successo!")
                        st.rerun()
                    else:
                        st.error(f"Errore: {error}")
    else:
        st.success("🎉 Script Generato con Successo!")
        st.markdown("### 📝 Il Tuo Nuovo Script")
        st.markdown(st.session_state.script_content)
        
        st.download_button(
            label="📥 Scarica Script (.md)",
            data=st.session_state.script_content,
            file_name="new_video_script.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro", use_container_width=True):
            st.session_state.current_step = 3
            st.rerun()
    with col2:
        if st.button("🔄 Ricomincia da Capo", use_container_width=True):
            for key in ['current_step', 'video_url', 'transcript_data', 'topics_data', 'research_data', 'script_content']:
                st.session_state[key] = None if key != 'current_step' else 0
            st.session_state.video_url = ""
            st.rerun()

# Footer
st.markdown("---")
st.markdown("<center style='color: #64748b;'>Powered by Fuze Agency AI Engine • Built with Antigravity</center>", unsafe_allow_html=True)
