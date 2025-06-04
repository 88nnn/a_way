import streamlit as st
from tts_utils import play_tts_lines

# 탭 및 글쓰기 버튼
col1, col2 = st.columns([8, 2])
with col1:
    tab_titles = ['불편 경로 제보', '동네 마당', '문의']
    tab1, tab2, tab3 = st.tabs(tab_titles)
with col2:
    if st.button("글쓰기"):
        st.switch_page("posting.py")

st.markdown("## 📝 글 제목")

# 글 정보
st.markdown("`작성자` | `2025-06-02` | `불편 경로 제보`")
st.markdown("---")

# 지도 API 예시 (좌표 핀 생략)
st.map()  # 실제 좌표 사용 시 st.map(dataframe)

# 글 본문
st.write("이곳에 본문 내용이 들어갑니다.")

# 댓글 섹션
st.markdown("---")
st.markdown("### 💬 댓글 [3]")
comment = st.text_input("댓글을 입력해 주세요")
if st.button("댓글 작성"):
    st.success("댓글이 등록되었습니다.")

# 댓글 리스트
for i in range(1, 4):
    st.markdown("---")
    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown(f"**댓글 작성자 {i}**")
    with col2:
        st.markdown("`2025-06-02`")
    st.write("댓글 내용 예시입니다.")

# 글 목록 돌아가기
if st.button("글 목록으로 돌아가기"):
    st.switch_page("dashboard.py")
