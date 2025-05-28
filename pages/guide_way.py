import streamlit as st
import requests
import polyline
import pydeck as pdk
import pyttsx3

# T-Map API 정보 설정
T_MAP_API_KEY = st.secrets["api_key"]#"YOUR_TMAP_API_KEY"

# TTS 엔진 초기화
tts_engine = pyttsx3.init()
tts_lines = []  # 경로 안내 문장 리스트
line_index = st.session_state.get("tts_line_index", 0)

# 예시 안내 문장 리스트 생성 (실제 데이터로 교체 가능)
tts_lines = [step['properties']['description'] for step in route_data['features'] if step['geometry']['type'] == 'Point']

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("◀ 이전 줄 듣기") and line_index > 0:
        line_index -= 1
        tts_engine.say(tts_lines[line_index])
        tts_engine.runAndWait()
with col2:
    if st.button("🔁 다시 듣기") and tts_lines:
        tts_engine.say(tts_lines[line_index])
        tts_engine.runAndWait()
with col3:
    if st.button("▶ 다음 줄 듣기") and line_index < len(tts_lines) - 1:
        line_index += 1
        tts_engine.say(tts_lines[line_index])
        tts_engine.runAndWait()

# 현재 줄 인덱스를 세션에 저장
st.session_state.tts_line_index = line_index

# 현재 줄 시각화
if tts_lines:
    st.info(f"📢 현재 안내: {tts_lines[line_index]}")

st.set_page_config(page_title="이동 경로 안내", page_icon="🗺️", layout="wide")
st.title("📍 경로 안내 (T-Map API 기반)")

# 주소 → 좌표 변환 함수 (T-Map Geocoding API)
def geocode_address(address):
    url = "https://apis.openapi.sk.com/tmap/geo/geocoding"
    headers = {"appKey": T_MAP_API_KEY}
    params = {
        "version": 1,
        "format": "json",
        "callback": "result",
        "addressFlag": "F00",
        "fullAddr": address
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['addressInfo']:  # 유효한 주소일 경우
            info = result['addressInfo']
            return {"lat": float(info["lat"]), "lon": float(info["lon"])}
    return None

# 세션 상태에서 주소 불러오기
text_data = st.session_state.get("guide_data", {"start": "", "end": ""})
start_text = text_data.get("start", "")
end_text = text_data.get("end", "")

# 주소를 좌표로 변환
start = geocode_address(start_text) if start_text else None
end = geocode_address(end_text) if end_text else None

if start and end:
    # T-Map 길찾기 API 호출 함수
    def get_route(start, end):
        url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"
        headers = {
            "appKey": T_MAP_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "startX": str(start["lon"]),
            "startY": str(start["lat"]),
            "endX": str(end["lon"]),
            "endY": str(end["lat"]),
            "searchOption": 30,
            "reqCoordType": "WGS84GEO",
            "resCoordType": "WGS84GEO",
            "startName": "출발지",
            "endName": "도착지"
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API 호출 오류: {response.status_code}")
            return None

    route_data = get_route(start, end)

    if route_data:
        # 경로 디코딩 및 시각화
        route_polyline = route_data['features'][0]['geometry']['coordinates']
        route_coords = [(coord[1], coord[0]) for coord in route_polyline]  # 위도, 경도 순서로 변경

        st.subheader("🗺️ 경로 시각화")
        st.map(data={"lat": [p[0] for p in route_coords], "lon": [p[1] for p in route_coords]})

        # pydeck Layer 시각화
        path_layer = pdk.Layer(
            "PathLayer",
            data=[{"path": route_coords}],
            get_path="path",
            get_width=6,
            get_color=[0, 100, 200],
            width_min_pixels=2,
            pickable=True
        )

        st.pydeck_chart(pdk.Deck(
            layers=[path_layer],
            initial_view_state=pdk.ViewState(
                latitude=route_coords[0][0],
                longitude=route_coords[0][1],
                zoom=15,
                pitch=45
            )
        ))

        st.success("경로 안내가 완료되었습니다!")

        # 입력 요약 표시
        with st.expander("📌 입력한 출발지/도착지 정보 보기"):
            st.markdown(f"**출발지:** {start_text}")
            st.markdown(f"**도착지:** {end_text}")
    else:
        st.warning("경로 데이터를 불러오는 데 실패했습니다.")

else:
    st.warning("출발지 또는 목적지 정보를 확인할 수 없습니다.")
