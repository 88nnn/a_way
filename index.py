# 첫 화면
import streamlit as st

# 세션 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'index'

def go_to_login():
    st.session_state.page = 'login'

st.set_page_config(page_title="접근성 내비 앱", layout="centered")
#st.title("접근성 내비게이션 앱")
st.markdown("이용자님의 정보를 저장해 더 최적화된 기능을 제공받으실 수 있습니다.")
st.page_link("pages/log_in.py", label="🔐 로그인", icon="🔑")
st.markdown("바로 이용")#, use_container_width=True)  # 바로 이용 로직은 이후 구현
st.page_link("pages/set_way.py", label="🌏 바로 이용", icon="🚦")

st.markdown("---")
st.caption("로그인 없이도 사용 가능합니다.")

st.page_link("pages/sign_up.py", label="회원가입", icon="📝")
# 홈페이지로 이동 유도
# st.page_link("set_way.py", label="🏠 처음 화면으로", icon="🏠")
