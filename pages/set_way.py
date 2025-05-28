# 탐색한 경로 안내
import streamlit as st
import speech_recognition as sr
import pyttsx3
import pyaudio

st.set_page_config(page_title="교통약자 AI 이동 도우미", page_icon="🚶", layout="centered")
st.title("🚦 성북구 교통약자 이동 도우미")

# 음성 합성 엔진 초기화
engine = pyttsx3.init()

def tts_speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 말씀해 주세요...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio, language='ko-KR')
        except sr.UnknownValueError:
            st.warning("음성을 인식하지 못했습니다.")
            return ""
        except sr.RequestError:
            st.error("음성 인식 서비스에 연결할 수 없습니다.")
            return ""

# 경로 안내 줄 리스트 예시
route_instructions = [
    "1. 정릉시장 앞 횡단보도를 건넙니다.",
    "2. 50m 직진 후 오른쪽 경사로를 따라 이동하세요.",
    "3. 엘리베이터를 타고 2층으로 올라가세요.",
    "4. 좌측 통로를 따라 30m 이동하면 도착입니다."
]

if "route_index" not in st.session_state:
    st.session_state.route_index = 0

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("◀ 이전 줄 듣기"):
        if st.session_state.route_index > 0:
            st.session_state.route_index -= 1
            tts_speak(route_instructions[st.session_state.route_index])
with col2:
    if st.button("🔁 다시 듣기"):
        tts_speak(route_instructions[st.session_state.route_index])
with col3:
    if st.button("▶ 다음 줄 듣기"):
        if st.session_state.route_index < len(route_instructions) - 1:
            st.session_state.route_index += 1
            tts_speak(route_instructions[st.session_state.route_index])

st.write("### 경로 안내:")
for idx, line in enumerate(route_instructions):
    if idx == st.session_state.route_index:
        st.markdown(f"**➡️ {line}**")
    else:
        st.markdown(line)

st.divider()

st.subheader("🗣 출발지/목적지 입력")

col4, col5 = st.columns([4, 1])
with col4:
    start_point = st.text_input("어디에서 출발하시나요?")
with col5:
    if st.button("🎙 출발지 음성 입력"):
        voice_input = recognize_voice()
        if voice_input:
            start_point = voice_input

col6, col7 = st.columns([4, 1])
with col6:
    end_point = st.text_input("어디로 가실 건가요?")
with col7:
    if st.button("🎙 목적지 음성 입력"):
        voice_input = recognize_voice()
        if voice_input:
            end_point = voice_input

if st.button("🚩 출발지/목적지 선택 완료"):
    if not start_point or not end_point:
        tts_speak("출발지와 목적지를 모두 입력해 주세요.")
        st.error("출발지와 목적지를 모두 입력해 주세요.")
    else:
        st.session_state.guide_data = {"start": start_point, "end": end_point}
        tts_speak(f"출발지는 {start_point}, 목적지는 {end_point}로 설정되었습니다.")
        st.success("경로 계산을 시작합니다...")
        st.page_link("pages/guide_way.py", label="경로 추천 시작", icon="📝")
