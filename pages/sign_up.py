# 회원가입
# 교통약자 유형 선택
import streamlit as st
import re
from tts_utils import play_tts_lines

st.title("회원가입")

# 필수 입력
st.text("필수: 가입 후 식별을 위해 필요합니다.")
name = st.text_input("이름 (중복 시 숫자가 자동 추가됩니다.)")
password = st.text_input("비밀번호 (영문/숫자 포함 8자 이상)", type="password")

# 정규식 검사
def valid_password(pw):
    return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', pw))

st.text("필수: 경로 탐색을 위해 필요합니다.")
transport = st.selectbox("주로 어떤 이동수단과 함께하시나요?", ["목발/지팡이", "(전동) 휠체어", "유모차", "도보"])
if transport == "목발/지팡이":
    transport = "cane"
elif transport == "(전동) 휠체어":
    transport = "wheelchair"
elif transport == "유모차":
    transport = "stroller"
elif transport == "도보":
    transport = "walk"
else:
    st.error("유효하지 않은 이동수단입니다. 해당사항이 없으실 경우 일단 휠체어를 선택해 주시기 바랍니다.")

# 장애 사항: 정도, 소분류, 세분류 입력 가능하게
# 가중치 분배를 어케야 할까
st.text("필수: 경로 탐색을 위해 필요합니다.")

options = {
    "장애인 화장실(기저귀 교환대) 이용": "toilet",
    "엘리베이터 이용": "elevator",
    "점자 보도블록, 음향신호기(횡단보도 앞 안내 스피커) 등 청취": "eye",
    "안내견 동행": "dog",
    "장애인 활동지원사 동행": "volunteer",
    "전동 보장구 급속 충전기 이용": "charger",
    "기타": "other"
}

selected = st.multiselect(
    "이동 시 필요한 도움으로는 어떤 것들이 있으신가요?",
    options.keys()
)
disability_option = [options[sel] for sel in selected]
st.write("선택된 도움 옵션 코드:", disability_option)

disability_detail = st.text_area("필요할 시 관련된 추가사항을 입력해 주세요.")

# 선택 입력
age = st.selectbox("나이대를 알려 주시겠어요?(필수적이진 않으나 경로 정확도가 저하될 수 있습니다.)", ["미성년자", "20대 이상~30대 이하(20~39세)", "40대 이상~50대 이하(40~59세)", "60대 이상(60세~)"])
if age == "미성년자":
    age = 0
elif age == "20대 이상~30대 이하(20~39세)":
    age = 20
elif age == "40대 이상~50대 이하(40~59세)":
    age = 40
elif age == "60대 이상(60세~)":
    age = 60
else:
    st.error("유효하지 않은 나이대입니다.")

gender = st.selectbox("성별을 알려주시겠어요?(필수적이진 않으나 화장실 탐색 시 정확도가 저하됩니다.)", ["남성", "여성"])
if gender == "여성":
    gender = "female"
elif gender == "남성":
    gender = "male"
else:
    st.error("유효하지 않은 성별입니다. 해당사항이 없으실 경우 일단 아무것도 입력하지 말아 주시기 바랍니다.")

st.markdown("### 비상 연락처 (선택)")
phone1 = st.text_input("전화번호1")
relation1 = st.text_input("관계1")
phone2 = st.text_input("전화번호2")
relation2 = st.text_input("관계2")
email = st.text_input("이메일")

if st.button("회원가입 완료"):
    if not name or not password or not valid_password(password) or not transport:
        st.error("필수 항목을 정확히 입력해 주세요.")
    else:
        # 저장 로직 (예: DB 저장 또는 세션에 저장)
        #user_data = {
        st.session_state.user_data = {
            "이름": name,
            "비밀번호": password,
            "이동수단": transport,
            "장애 사항":  disability_option,
            "장애 설명": disability_detail,
            "나이": age or None,
            "성별": gender or None,
            "전화번호1": phone1 or None,
            "관계1": relation1 or None,
            "전화번호2": phone2 or None,
            "관계2": relation2 or None,
            "이메일": email or None
        }
        st.success("회원가입이 완료되었습니다!")
        st.switch_page("pages/log_in.py")
