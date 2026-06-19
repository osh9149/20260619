import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="역사 속 서울 기온 맞히기", page_icon="🌡️", layout="centered")

# =========================
# 데이터 불러오기
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8-sig")

    df["날짜"] = df["날짜"].astype(str).str.replace("\t", "", regex=False).str.strip()
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    df["평균기온(℃)"] = pd.to_numeric(df["평균기온(℃)"], errors="coerce")

    df = df.dropna(subset=["날짜", "평균기온(℃)"])
    df["날짜문자"] = df["날짜"].dt.strftime("%Y-%m-%d")

    return df

df = load_data()

# =========================
# 역사적인 날 목록
# =========================
history_days = [
    {"date": "1919-03-01", "event": "3·1 운동", "emoji": "🇰🇷"},
    {"date": "1945-08-15", "event": "광복절", "emoji": "🎉"},
    {"date": "1948-08-15", "event": "대한민국 정부 수립", "emoji": "🏛️"},
    {"date": "1950-06-25", "event": "6·25 전쟁 발발", "emoji": "🕊️"},
    {"date": "1960-04-19", "event": "4·19 혁명", "emoji": "🔥"},
    {"date": "1987-06-10", "event": "6월 민주항쟁", "emoji": "📢"},
    {"date": "1988-09-17", "event": "서울 올림픽 개막", "emoji": "🏅"},
    {"date": "2002-06-22", "event": "월드컵 4강 진출", "emoji": "⚽"},
    {"date": "2018-02-09", "event": "평창 동계올림픽 개막", "emoji": "⛷️"},
    {"date": "2020-03-02", "event": "코로나19로 개학 연기", "emoji": "😷"},
]

available_days = []
for item in history_days:
    row = df[df["날짜문자"] == item["date"]]
    if not row.empty:
        temp = round(float(row.iloc[0]["평균기온(℃)"]), 1)
        item["temp"] = temp
        available_days.append(item)

# =========================
# 상태 초기화
# =========================
if "question" not in st.session_state:
    st.session_state.question = random.choice(available_days)
    st.session_state.chances = 5
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.message = "역사 속 그날의 서울 평균기온을 맞혀보세요!"

# =========================
# 디자인
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff3c4, #ffd6e8, #d6f5ff);
}
.title {
    text-align:center;
    font-size:38px;
    font-weight:900;
    color:#ff5c8a;
}
.card {
    background:white;
    padding:25px;
    border-radius:25px;
    box-shadow:0 8px 20px rgba(0,0,0,0.12);
    text-align:center;
}
.event {
    font-size:28px;
    font-weight:800;
    color:#333;
}
.date {
    font-size:22px;
    color:#555;
}
.hint {
    font-size:24px;
    font-weight:800;
    color:#ff7a00;
}
.score {
    font-size:22px;
    font-weight:800;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🌡️ 역사 속 서울 기온 맞히기 🎲</div>", unsafe_allow_html=True)
st.write("")

q = st.session_state.question

st.markdown(f"""
<div class="card">
    <div style="font-size:55px;">{q['emoji']}</div>
    <div class="event">{q['event']}</div>
    <div class="date">{q['date']}</div>
    <br>
    <div>이날 서울의 <b>평균기온</b>은 몇 ℃였을까요?</div>
</div>
""", unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='score'>⭐ 점수: {st.session_state.score}점</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='score'>💖 남은 기회: {st.session_state.chances}번</div>", unsafe_allow_html=True)

guess = st.number_input(
    "기온을 입력하세요!",
    min_value=-30.0,
    max_value=45.0,
    step=0.1,
    format="%.1f"
)

if st.button("정답 확인하기 🔍", use_container_width=True):
    if not st.session_state.game_over:
        answer = q["temp"]

        if abs(guess - answer) < 0.05:
            st.session_state.score += st.session_state.chances * 10
            st.session_state.message = f"🎉 정답! 이날 평균기온은 {answer}℃였어요!"
            st.session_state.game_over = True

        else:
            st.session_state.chances -= 1

            if st.session_state.chances == 0:
                st.session_state.message = f"😭 실패! 정답은 {answer}℃였어요."
                st.session_state.game_over = True
            elif guess < answer:
                st.session_state.message = "⬆️ 더 높아요! 조금 더 따뜻한 날이었어요."
            else:
                st.session_state.message = "⬇️ 더 낮아요! 생각보다 선선하거나 추웠어요."

st.write("")
st.markdown(f"<div class='card hint'>{st.session_state.message}</div>", unsafe_allow_html=True)

if st.session_state.game_over:
    st.write("")
    if st.button("다음 역사 문제 풀기 🎯", use_container_width=True):
        st.session_state.question = random.choice(available_days)
        st.session_state.chances = 5
        st.session_state.game_over = False
        st.session_state.message = "새로운 역사 속 날짜가 나왔어요!"
        st.rerun()

st.write("")
with st.expander("📚 게임 방법 보기"):
    st.write("""
    - 역사적인 날짜의 서울 평균기온을 맞히는 게임입니다.
    - 기회는 총 5번입니다.
    - 입력한 기온이 정답보다 낮으면 “더 높아요” 힌트가 나옵니다.
    - 입력한 기온이 정답보다 높으면 “더 낮아요” 힌트가 나옵니다.
    - 빨리 맞힐수록 점수를 많이 얻습니다.
    """)

with st.expander("🌈 수업 활용 아이디어"):
    st.write("""
    학생들에게 역사적 사건을 먼저 소개한 뒤,
    그날의 날씨를 추측하게 하면 역사와 데이터가 자연스럽게 연결됩니다.
    기온을 맞힌 후에는 당시 계절, 사회적 상황, 사건의 의미를 함께 이야기해 볼 수 있습니다.
    """)
