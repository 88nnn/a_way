import requests
import streamlit as st
import speech_recognition as sr
import streamlit as st
import streamlit.components.v1 as components

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
def browser_tts(text):
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
            browser_tts("출발지를 입력해 주세요.")
            st.error("출발지를 입력해 주세요.")
        else:
            st.session_state.start_results = search_place(start_point)
            if st.session_state.start_results:
                st.session_state.selected_start = st.session_state.start_results[0]  # 기본 첫 번째 선택

        if not end_point:
            browser_tts("목적지를 입력해 주세요.")
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
            browser_tts(confirm_text)
            st.success(confirm_text)
            st.page_link("pages/guide_way.py", label="경로 추천 시작", icon="📝")
        else:
            browser_tts("출발지와 목적지를 모두 선택해 주세요.")
            st.error("출발지와 목적지를 모두 선택해 주세요.")


# 경로 안내 문장 리스트 예시 (API 연동 시 여기 자동 구성 가능)
tts_lines = [
    "출발지에서 30미터 직진하세요.",
    "횡단보도를 건너고 좌회전하세요.",
    "엘리베이터를 이용해 2층으로 이동하세요.",
    "목적지는 오른쪽에 있습니다."
]

# 현재 줄 인덱스 저장
if "tts_line_index" not in st.session_state:
    st.session_state.tts_line_index = 0

# 현재 줄 가져오기
line_index = st.session_state.tts_line_index
current_line = tts_lines[line_index]

# 브라우저 기반 TTS 함수
def browser_tts(text):
    escaped = text.replace("'", "\\'")
    components.html(f"""
        <script>
        const msg = new SpeechSynthesisUtterance('{escaped}');
        msg.lang = 'ko-KR';
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# 버튼 인터페이스
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("◀ 이전 줄") and line_index > 0:
        st.session_state.tts_line_index -= 1
        browser_tts(tts_lines[st.session_state.tts_line_index])

with col2:
    if st.button("🔁 다시 듣기"):
        browser_tts(current_line)

with col3:
    if st.button("▶ 다음 줄") and line_index < len(tts_lines) - 1:
        st.session_state.tts_line_index += 1
        browser_tts(tts_lines[st.session_state.tts_line_index])

# 현재 줄 시각화
st.info(f"📢 현재 안내: {current_line}")

