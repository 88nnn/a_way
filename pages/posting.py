import streamlit as st
import datetime
from streamlit_folium import st_folium
import folium
import json
import os
#import google.generativeai as genai
"""
# Gemini API 설정 (실제 API 키로 대체)
#genai.configure(g_api_key="YOUR_GEMINI_API_KEY")
try:
    genai.configure(st.secrets["g_api_key"])
except Exception as e:
    st.error("API 키를 불러오지 못했습니다. ..streamlit/secrets.toml을 확인해 주세요.")
    st.stop()
st.write("DEBUG - secrets:", st.secrets)
"""
user_data = st.session_state.get("user_data")
if not user_data:
    st.write("이용자 정보가 없습니다. 익명으로 작성됩니다.")
    author = "비회원"
else:
    author = st.session_state.user_data.name

st.write("DEBUG - select:", user_data)
# 데이터 파일 경로 정의
DATA_DIR = "data"
POST_LIST_FILE = os.path.join(DATA_DIR, "post_list.json")
OBSTACLE_FILE = os.path.join(DATA_DIR, "obstacle.json")

now = datetime.datetime.now()

st.markdown("## ✍️ 글쓰기")

# 카테고리 선택
category = st.selectbox("카테고리를 선택하세요", ["불편 경로 제보", "커뮤니티", "문의"])

# 글 제목 입력
title = st.text_input("글 제목을 작성해 주세요")

if category == "불편 경로 제보":
    obstacle = {
        "심한 경사로": "wheelchair_ramp",
        "턱 있음": "doorway_threshold",
        "문턱 있음": "doorway_threshold",
        "계단 있음": "stairs",
        "좁은 통로": "narrow_passage",
        "자동문 아님": "not_automatic_door",
        "휠체어 통행 불가": "no_wheelchair",
        "장애인 화장실 이용 불가": "bo_toilet",
        "점자 도보 끊김": "no_braille Walk",
        "엘리베이터 이용 불가": "no_elevator",
        "음향 안내기 고장": "no_sound",
        "통로 폐쇄(진입 불가)": "no_entry",
        "기타": "other"
    }
    
    selected = st.multiselect(
        "불편 상황을 선택하세요",
        obstacle.keys()
    )
    obstacle = [obstacle[sel] for sel in selected]
    st.write("선택된 장애물 코드:", obstacle)

# 좌표 입력
st.markdown("**아래 지도에서 핀을 찍어 위치를 선택하세요.**")
# 지도 표시
m = folium.Map(location=[37.5665, 126.9780], zoom_start=13)
m.add_child(folium.LatLngPopup())  # 클릭 시 좌표 표시

# 사용자 지도 상 클릭 좌표 얻기
map_data = st_folium(m, width=700, height=500)
lon = map_data.get("last_clicked", {}).get("lng", "")
lat = map_data.get("last_clicked", {}).get("lat", "")

if lon and lat:
    st.success(f"선택된 위치: 경도 {lon:.6f}, 위도 {lat:.6f}")

# 본문 입력
content = st.text_area("본문을 입력해 주세요", height=300)

create_at = now.strftime('%Y-%m-%d %H:%M:%S')

if st.button("작성"):
    else:
        # 파일 경로
        report_path = "data/reports.json"
        os.makedirs("data", exist_ok=True)

        # 기존 JSON 불러오기
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                try:
                    report_list = json.load(f)
                    if not isinstance(report_list, list):
                        report_list = []
                except json.JSONDecodeError:
                    report_list = []
        else:
            report_list = []

        # idx 자동 증가
        max_idx = max([item.get("idx", 0) for item in report_list], default=0)
        new_idx = max_idx + 1

        # 새로운 제보/장애물 객체        
        obstacle = {
            "idx": new_idx,
            "dataframe": {"lon": str(lon), "lat": str(lat)},
            "obstacle_option": obstacle
        }
        report = {
            "idx": new_idx,
            "author": author,
            "title": "title",
            "content": content,
            "dataframe": {"lon": str(lon), "lat": str(lat)},
            "obstacle": obstacle
        }
        obstacle.append(obstacle)
        report_list.append(report)

        # 저장
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_list, f, ensure_ascii=False, indent=2)

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_list, f, ensure_ascii=False, indent=2)
        st.success(f"제보가 접수되었습니다. (제보 번호: {new_idx})")
