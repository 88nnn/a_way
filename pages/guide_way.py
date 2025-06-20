
import requests
import polyline
import pydeck as pdk
import os
import threading

import streamlit as st
import streamlit.components.v1 as components

# T-Map API 정보 설정
T_MAP_API_KEY = st.secrets["api_key"]
try:
    T_MAP_API_KEY = st.secrets["api_key"]
except Exception as e:
    st.error("API 키를 불러오지 못했습니다. ..streamlit/secrets.toml을 확인해 주세요.")
    st.stop()
st.write("DEBUG - secrets:", st.secrets)

guide_data = st.session_state.get("guide_data")
if not guide_data:
    st.error("출발지와 목적지 정보가 없습니다.")
    st.stop()

st.write("DEBUG - select:", guide_data)

start_text = guide_data["start"]
end_text = guide_data["end"]
start_coor = guide_data["start_coor"]
end_coor = guide_data["end_coor"]

# 경로 안내 문장을 저장할 공간
if "tts_lines" not in st.session_state:
    st.session_state.tts_lines = []

if "tts_line_index" not in st.session_state:
    st.session_state.tts_line_index = 0

# T-Map API 호출 함수
def get_route():
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"
    headers = {
        "appKey": T_MAP_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "startX": start_coor["lon"],
        "startY": start_coor["lat"],
        "endX": end_coor["lon"],
        "endY": end_coor["lat"],
        "searchOption": 30,
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "startName": start_text,
        "endName": end_text
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API 호출 오류: {response.status_code}")
        return None

# 경로 정보 받아오기
if start_text and end_text and start_coor and end_coor:
    route_data = get_route()

    if route_data:
        features = route_data.get("features", [])
        if features:
            # 경로 안내 문장 만들기
            # TTS 문장 추출: Point 타입에서 description만 추출
            st.session_state.tts_lines = [
                feature["properties"]["description"]
                for feature in features
                if feature["geometry"]["type"] == "Point"
                   and feature["properties"].get("description")
            ]

            route_coords = [
                (pt[1], pt[0])
                for feature in features
                if feature["geometry"]["type"] == "LineString"
                for pt in feature["geometry"]["coordinates"]
            ]

            # 경로 시각화
            st.subheader("🗺️ 경로 시각화")
            st.pydeck_chart(pdk.Deck(
                layers=[pdk.Layer(
                    "PathLayer",
                    data=[{"path": route_coords}],
                    get_path="path",
                    get_width=6,
                    get_color=[0, 100, 200]
                )],
                initial_view_state=pdk.ViewState(
                    latitude=route_coords[0][0],
                    longitude=route_coords[0][1],
                    zoom=15,
                    pitch=45
                )
            ))
        else:
            st.warning("경로 정보가 없습니다.")
    else:
        st.warning("API 호출 실패 또는 유효하지 않은 좌표입니다.")
else:
    st.warning("출발지 또는 도착지 정보가 부족합니다.")


# 경로 안내 문장 리스트 예시 (API 연동 시 여기 자동 구성 가능)
tts_lines = []

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

st.write(tts_lines)
