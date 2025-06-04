
from gtts import gTTS
import os
import tempfile
import streamlit as st
import base64

def play_tts(text, lang="ko"):
    """
    Play a single line of text using gTTS and stream it in Streamlit.
    """
    if not text:
        return

    # Create a temporary MP3 file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts = gTTS(text=text, lang=lang)
        tts.save(fp.name)
        audio_path = fp.name

    # Encode audio to base64
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()

    # Create HTML audio player
    audio_html = f"""
    <audio autoplay controls>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
    os.remove(audio_path)


def play_tts_lines(tts_lines, index_key="tts_line_index"):
    """
    Display navigation buttons for a list of TTS lines and play audio accordingly.
    """
    if not tts_lines:
        st.warning("📭 현재 안내할 내용이 없습니다.")
        return

    line_index = st.session_state.get(index_key, 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("◀ 이전 줄 듣기") and line_index > 0:
            line_index -= 1
            play_tts(tts_lines[line_index])
    with col2:
        if st.button("🔁 다시 듣기"):
            play_tts(tts_lines[line_index])
    with col3:
        if st.button("▶ 다음 줄 듣기") and line_index < len(tts_lines) - 1:
            line_index += 1
            play_tts(tts_lines[line_index])

    st.session_state[index_key] = line_index
    st.info(f"📢 현재 안내: {tts_lines[line_index]}")
