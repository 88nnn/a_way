import requests
import streamlit as st
import speech_recognition as sr
import pyttsx3
from tts_utils import play_tts_lines

st.set_page_config(page_title="교통약자 AI 이동 도우미", page_icon="🚶", layout="centered")
st.title("🚦 교통약자 이동 도우미")

# T-Map API 정보 설정
T_MAP_API_KEY = st.secrets["api_key"]#"YOUR_TMAP_API_KEY"
try:
    T_MAP_API_KEY = st.secrets["api_key"]
except Exception as e:
    st.error("API 키를 불러오지 못했습니다. ..streamlit/secrets.toml을 확인해 주세요.")
    st.stop()
st.write("DEBUG - secrets:", st.secrets)

# TTS 엔진 초기화
engine = pyttsx3.init()
def tts_speak(text):
    engine.say(text)
    engine.runAndWait()

# 상태 초기화
if "tts_index" not in st.session_state:
    st.session_state.tts_index = 0

# TTS 제어 버튼
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("◀ 이전 줄 듣기"):
        if st.session_state.tts_index > 0:
            st.session_state.tts_index -= 1
with col2:
    if st.button("🔁 다시 듣기"):
        st.text("ghhfhj")
with col3:
    if st.button("▶ 다음 줄 듣기"):
        if st.session_state.tts_index < 1:
            st.text("gh")

# 현재 읽는 줄 표시
#st.markdown(f"**📢 현재 안내:** {route_texts[st.session_state.tts_index]}")

def search_place(keyword):
    url = "https://apis.openapi.sk.com/tmap/pois"
    headers = {"appKey": T_MAP_API_KEY}
    params = {
        "version": 1,
        "searchKeyword": keyword,
        "resCoordType": "WGS84GEO",
        "reqCoordType": "WGS84GEO",
        "count": 5
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        pois = response.json().get("searchPoiInfo", {}).get("pois", {}).get("poi", [])
        return [
            {
                "name": poi["name"],
                "addr": poi["upperAddrName"] + " " + poi["middleAddrName"] + " " + poi["lowerAddrName"],
                "lat": float(poi["noorLat"]),
                "lon": float(poi["noorLon"]),
            }
            for poi in pois
        ]
    return []


# 출발지/목적지 입력 섹션
st.subheader("🗣 출발지/목적지 입력")

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

col8, col9 = st.columns([4, 1])
with col8:
    # 상태 초기화
    if "start_results" not in st.session_state:
        st.session_state.start_results = []
    if "end_results" not in st.session_state:
        st.session_state.end_results = []
    if "selected_start" not in st.session_state:
        st.session_state.selected_start = None
    if "selected_end" not in st.session_state:
        st.session_state.selected_end = None

    # 검색 버튼
    if st.button("🚩 출발지/목적지 검색 시작"):
        if not start_point:
            tts_speak("출발지를 입력해 주세요.")
            st.error("출발지를 입력해 주세요.")
        else:
            st.session_state.start_results = search_place(start_point)
            if st.session_state.start_results:
                st.session_state.selected_start = st.session_state.start_results[0]  # 기본 첫 번째 선택

        if not end_point:
            tts_speak("목적지를 입력해 주세요.")
            st.error("목적지를 입력해 주세요.")
        else:
            st.session_state.end_results = search_place(end_point)
            if st.session_state.end_results:
                st.session_state.selected_end = st.session_state.end_results[0]  # 기본 첫 번째 선택

    # 출발지 후보 선택 유지
    if st.session_state.start_results:
        st.session_state.selected_start = st.selectbox(
            "출발지 후보 중 선택하세요",
            options=st.session_state.start_results,
            format_func=lambda x: f'{x["name"]} ({x["addr"]})',
            index=st.session_state.start_results.index(st.session_state.selected_start)
            if st.session_state.selected_start in st.session_state.start_results else 0
        )

    # 도착지 후보 선택 유지
    if st.session_state.end_results:
        st.session_state.selected_end = st.selectbox(
            "도착지 후보 중 선택하세요",
            options=st.session_state.end_results,
            format_func=lambda x: f'{x["name"]} ({x["addr"]})',
            index=st.session_state.end_results.index(st.session_state.selected_end)
            if st.session_state.selected_end in st.session_state.end_results else 0
        )

    # 입력 완료 버튼
    if st.button("🚩 출발지/목적지 입력 완료"):
        if st.session_state.selected_start and st.session_state.selected_end:
            st.session_state.guide_data = {
                "start": st.session_state.selected_start["name"],
                "end": st.session_state.selected_end["name"],
                "start_coor": {
                    "lat": st.session_state.selected_start["lat"],
                    "lon": st.session_state.selected_start["lon"]
                },
                "end_coor": {
                    "lat": st.session_state.selected_end["lat"],
                    "lon": st.session_state.selected_end["lon"]
                }
            }
            confirm_text = f"출발지는 {st.session_state.selected_start['name']}, 목적지는 {st.session_state.selected_end['name']}로 설정되었습니다.\n아래의 경로 추천 시작 버튼을 눌러주세요!"
            tts_speak(confirm_text)
            st.success(confirm_text)
            st.page_link("pages/guide_way.py", label="경로 추천 시작", icon="📝")
        else:
            tts_speak("출발지와 목적지를 모두 선택해 주세요.")
            st.error("출발지와 목적지를 모두 선택해 주세요.")
