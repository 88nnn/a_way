
import streamlit as st
import streamlit_folium
import folium
import streamlit_TTS as st_tts
import pyaudio2
import pyttsx3
import speech_recognition as sr

#스트림릿 체크박스
# 사용자 유형 감지

import streamlit as st

st.set_page_config(page_title="접근성 내비 앱", layout="centered")
st.write("앱에 오신 것을 환영합니다! 왼쪽 사이드바에서 원하는 기능을 선택하세요.")

# 홈페이지로 이동 유도
st.page_link("Home.py", label="🏠 처음 화면으로", icon="🏠")

def detect_user_type(text):
    if "휠체어" in text:
        return "wheelchair"
    elif "유모차" in text or "아기" in text:
        return "stroller"
    else:
        return "elderly" #저체력자



# 샘플 경로 데이터
paths = [
    {"id": 1, "distance": 500, "slope": 2.1, "sidewalk": True, "stairs": False, "safety_score": 8.5, "lat": 37.602, "lon": 127.015},
    {"id": 2, "distance": 420, "slope": 7.0, "sidewalk": False, "stairs": True, "safety_score": 6.0, "lat": 37.603, "lon": 127.018},
]

st.set_page_config(page_title="교통약자 AI 이동 도우미", page_icon="🚶", layout="centered")
st.title("🚦 성북구 교통약자 이동 도우미")

user_input = st.chat_input("이동 도우미에게 말을 걸어보세요!")

if user_input:
    st.chat_message("user").write(user_input)

    user_type = detect_user_type(user_input)
    best = recommend_best_path(paths, user_type)

    reply = f"🧭 추천 경로 ID: {best['id']}, 거리 {best['distance']}m, 안전점수 {best['safety_score']}점입니다."
    st.chat_message("assistant").write(reply)

    # 지도 출력
    m = folium.Map(location=[best["lat"], best["lon"]], zoom_start=17)
    folium.Marker([best["lat"], best["lon"]], tooltip="추천 경로").add_to(m)
    streamlit_folium.st_folium(m, width=700, height=400)

#model