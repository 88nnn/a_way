import streamlit as st
import datetime

now = datetime.datetime.now()

st.markdown("## ✍️ 글쓰기")

# 카테고리 선택
category = st.selectbox("카테고리를 선택하세요", ["불편 경로 제보", "커뮤니티", "문의"])

# 글 제목 입력
title = st.text_input("글 제목을 작성해 주세요")

if category == "불편 경로 제보":
    obstacle = {
        "휠체어 통행 불가": "wheelchair",
        "장애인 화장실 이용 불가": "toilet",
        "점자 도보 끊김": ["eye", "braille Walk"],
        "엘리베이터 폐쇄": "elevator",
        "음향 안내기 고장": ["eye","sound"],
        "통로 폐쇄(진입 불가)": "no entry",
        "기타": "other"
    }

    selected = st.multiselect(
        "불편 상황을 선택하세요",
        obstacle.keys()
    )
    obstacle = [obstacle[sel] for sel in selected]
    st.write("선택된 장애물 코드:", obstacle)

# 좌표 입력
st.map()

# 본문 입력
body = st.text_area("본문을 입력해 주세요", height=300)

create_at = now.strftime('%Y-%m-%d %H:%M:%S')

if st.button("작성"):
    st.success("글이 등록되었습니다.")
    st.switch_page("dashboard.py")
