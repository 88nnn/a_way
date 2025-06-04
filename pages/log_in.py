import streamlit as st
from tts_utils import play_tts_lines

st.title("로그인")

username = st.text_input("이름")
password = st.text_input("비밀번호", type="password")

if st.button("로그인"):
    # 실제 로그인 로직 대체 필요
    if username and password:
        st.session_state.user = username
        st.success(f"{username}님, 환영합니다!")
        #login_success()
        st.switch_page("pages/set_way.py")
    else:
        st.error("이름 또는 비밀번호를 전부 입력하세요.")

#st.button("회원가입", on_click=go_to_signup)
st.page_link("pages/sign_up.py", label="회원가입", icon="📝")

st.markdown("---")
st.button("구글 로그인 (OIDC)", disabled=True)  # Google OIDC는 별도 구현 필요
