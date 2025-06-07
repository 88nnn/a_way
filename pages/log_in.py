import streamlit as st
import json
import os

st.title("로그인")

# 초기 세션 상태 설정
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = None

# 로그인 안 되어 있을 때만 입력 받기
if not st.session_state.logged_in:
    input_name = st.text_input("이름")
    input_pw = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        auth_file = "data/auth_list.json"

        if not os.path.exists(auth_file):
            st.error("가입된 유저 정보가 없습니다.")
        else:
            with open(auth_file, "r", encoding="utf-8") as f:
                try:
                    user_list = json.load(f)
                except json.JSONDecodeError:
                    user_list = []

            # 유저 확인
            user = next((u for u in user_list if u["이름"] == input_name and u["비밀번호"] == input_pw), None)

            if user:
                st.session_state.logged_in = True
                st.session_state.user_name = input_name
                st.success(f"{input_name}님, 로그인 성공!")
            else:
                st.error("이름 또는 비밀번호가 잘못되었습니다.")

else:
    st.success(f"이미 로그인됨: {st.session_state.user_name}")
    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.user_name = None
        st.rerun()
