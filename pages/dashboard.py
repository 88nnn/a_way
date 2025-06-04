import streamlit as st
import datetime

now = datetime.datetime.now()
st.markdown("## 📋 게시글 목록")

# 탭 및 글쓰기 버튼
col1, col2 = st.columns([8, 2])
with col1:
    tab_titles = ['불편 경로 제보', '동네 마당', '문의']
    tab1, tab2, tab3 = st.tabs(tab_titles)
with col2:
    if st.button("글쓰기"):
        st.switch_page("pages/posting.py")

create_at = now.strftime('%Y-%m-%d %H:%M:%S')

# 각 탭에 콘텐츠 추가
def example_list(author, date_time):
    # 게시글 목록 예시
    for i in range(1, 11):
        col1, col2 = st.columns([8, 2])
        with col1:
            st.markdown(f"**{i}. 제목 예시 [{i % 5}]**")
        with col2:
            st.markdown(f"`{author}` | `{date_time}`")

    # 페이지 네비게이션
    st.markdown(" ".join([f"{n}" for n in range(1, 6)]) + " >")

author = ""

with tab1:
    if author == "":
        author = "비회원"
        example_list(author, create_at)

with tab2:
    if author == "":
        author = "비회원"
        example_list(author, create_at)

with tab3:
    if author == "":
        author = "비회원"
        example_list(author, create_at)
