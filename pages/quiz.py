import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="역사 속 서울 기온 맞히기",
    page_icon="🌡️",
    layout="centered"
)

@st.cache_data
def load_data():
    df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8-sig")

    df["날짜"] = df["날짜"].astype(str).str.strip()
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["평균기온(℃)"] = pd.to_numeric(df["평균기온(℃)"], errors="coerce")

    df = df.dropna(subset=["날짜", "평균기온(℃)"])
    df["날짜문자"] = df["날짜"].dt.strftime("%Y-%m-%d")
    df["반올림기온"] = df["평균기온(℃)"].round().astype(int)

    return df

df = load_data()

history_days = [
    {
        "date": "1919-03-01",
        "event": "3·1 운동",
        "emoji": "🇰🇷",
        "story": "1919년 3월 1일, 독립을 외친 만세 운동이 전국으로 퍼져나갔어요."
    },
    {
        "date": "1945-08-15",
        "event": "광복절",
        "emoji": "🎉",
        "story": "1945년 8월 15일, 우리나라는 일본의 식민 지배에서 벗어나 광복을 맞이했어요."
    },
    {
        "date": "1948-08-15",
        "event": "대한민국 정부 수립",
        "emoji": "🏛️",
        "story": "1948년 8월 15일, 대한민국 정부가 공식적으로 수립되었어요."
    },
    {
        "date": "1950-06-25",
        "event": "6·25 전쟁 발발",
        "emoji": "🕊️",
        "story": "1950년 6월 25일, 한반도에 큰 비극을 남긴 전쟁이 시작되었어요."
    },
    {
        "date": "1960-04-19",
        "event": "4·19 혁명",
        "emoji": "🔥",
        "story": "1960년 4월 19일, 학생과 시민들이 민주주의를 위해 거리로 나섰어요."
    },
    {
        "date": "1987-06-10",
        "event": "6월 민주항쟁",
        "emoji": "📢",
        "story": "1987년 6월 10일, 민주화를 요구하는 시민들의 목소리가 전국으로 퍼졌어요."
    },
    {
        "date": "1988-09-17",
        "event": "서울 올림픽 개막",
        "emoji": "🏅",
        "story": "1988년 9월 17일, 서울에서 세계인의 축제 올림픽이 열렸어요."
    },
    {
        "date": "2002-06-22",
        "event": "월드컵 4강 진출",
        "emoji": "⚽",
        "story": "2002년 6월 22일, 대한민국 축구 대표팀이 월드컵 4강에 진출했어요."
    },
    {
        "date": "2018-02-09",
        "event": "평창 동계올림픽 개막",
        "emoji": "⛷️",
        "story": "2018년 2월 9일, 평창에서 동계올림픽이 개막했어요."
    },
    {
        "date": "2020-03-02",
        "event": "코로나19로 개학 연기",
        "emoji": "😷",
        "story": "2020년 봄, 코로나19로 인해 학교의 개학이 연기되는 큰 변화가 있었어요."
    },
]

available_days = []

for item in history_days:
    row = df[df["날짜문자"] == item["date"]]

    if not row.empty:
        item["answer"] = int(row.iloc[0]["반올림기온"])
        item["real_temp"] = float(row.iloc[0]["평균기온(℃)"])
        available_days.append(item)

if len(available_days) == 0:
    st.error("사용 가능한 역사 날짜 데이터가 없습니다. CSV 파일을 확인해주세요.")
    st.stop()

if "question" not in st.session_state:
    st.session_state.question = random.choice(available_days)
    st.session_state.chances = 5
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.message = "역사 속 그날의 서울 평균기온을 맞혀보세요!"
    st.session_state.try_count = 0

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff1c1, #ffd6e8, #d7f6ff);
}

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 900;
    color: #ff5c8a;
    margin-bottom: 10px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 28px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    text-align: center;
    margin-bottom: 18px;
}

.event-emoji {
    font-size: 60px;
}

.event-title {
    font-size: 30px;
    font-weight: 900;
    color: #333;
}

.event-date {
    font-size: 22px;
    color: #666;
}

.info-box {
    background: #ffffffcc;
    padding: 18px;
    border-radius: 20px;
    text-align: center;
    font-size: 22px;
    font-weight: 800;
    box-shadow: 0 5px 12px rgba(0,0,0,0.1);
}

.hint-box {
    background: #fff;
    padding: 22px;
    border-radius: 24px;
    text-align: center;
    font-size: 24px;
    font-weight: 900;
    color: #ff7a00;
    box-shadow: 0 6px 16px rgba(0,0,0,0.12);
}

.story-box {
    background: #f8ffff;
    padding: 22px;
    border-radius: 24px;
    font-size: 18px;
    line-height: 1.7;
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

q = st.session_state.question

st.markdown("<div class='main-title'>🌡️ 역사 속 서울 기온 맞히기 🎲</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>역사적인 날, 서울의 평균기온은 몇 ℃였을까요?</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
    <div class="event-emoji">{q['emoji']}</div>
    <div class="event-title">{q['event']}</div>
    <div class="event-date">{q['date']}</div>
    <br>
    <div style="font-size:20px;">
        이날 서울의 <b>평균기온을 반올림한 값</b>을 맞혀보세요!
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"<div class='info-box'>⭐ 점수<br>{st.session_state.score}점</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<div class='info-box'>💖 남은 기회<br>{st.session_state.chances}번</div>",
        unsafe_allow_html=True
    )

st.write("")

guess = st.number_input(
    "🌡️ 예상 기온을 입력하세요",
    min_value=-30,
    max_value=45,
    step=1
)

if st.button("정답 확인하기 🔍", use_container_width=True):
    if not st.session_state.game_over:
        answer = q["answer"]
        st.session_state.try_count += 1

        if guess == answer:
            earned = st.session_state.chances * 10
            st.session_state.score += earned
            st.session_state.message = f"🎉 정답이에요! +{earned}점 획득!"
            st.session_state.game_over = True

        else:
            st.session_state.chances -= 1

            if st.session_state.chances == 0:
                st.session_state.message = f"😭 아쉬워요! 정답은 {answer}℃였어요."
                st.session_state.game_over = True
            elif guess < answer:
                st.session_state.message = "⬆️ 더 높아요! 생각보다 따뜻한 날이었어요."
            else:
                st.session_state.message = "⬇️ 더 낮아요! 생각보다 선선하거나 추웠어요."

st.markdown(f"<div class='hint-box'>{st.session_state.message}</div>", unsafe_allow_html=True)

if not st.session_state.game_over:
    answer = q["answer"]

    if st.session_state.chances <= 3:
        if answer <= 0:
            st.info("❄️ 계절 힌트: 아주 추운 날씨였을 가능성이 높아요.")
        elif answer <= 10:
            st.info("🧥 계절 힌트: 쌀쌀한 날씨였을 가능성이 높아요.")
        elif answer <= 20:
            st.info("🌸 계절 힌트: 봄이나 가을 같은 날씨였을 가능성이 높아요.")
        else:
            st.info("☀️ 계절 힌트: 꽤 따뜻하거나 더운 날씨였을 가능성이 높아요.")

    if st.session_state.chances <= 2:
        ten = answer // 10 * 10
        st.warning(f"🎯 범위 힌트: 정답은 대략 {ten}℃대예요.")

if st.session_state.game_over:
    st.write("")

    st.markdown(f"""
    <div class="story-box">
        <h3>📖 역사 이야기</h3>
        <p>{q['story']}</p>
        <hr>
        <p>
        이날 서울의 실제 평균기온은 <b>{q['real_temp']:.1f}℃</b>였고,<br>
        게임 정답은 반올림한 <b>{q['answer']}℃</b>였어요.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.session_state.score >= 100:
        st.success("🏆 역사 기온 마스터! 대단해요!")
    elif st.session_state.score >= 50:
        st.success("🌟 훌륭해요! 역사와 날씨 감각이 좋아요!")
    else:
        st.info("🐣 계속 도전하면 역사 기온 탐험가가 될 수 있어요!")

    if st.button("다음 역사 문제 풀기 🎯", use_container_width=True):
        st.session_state.question = random.choice(available_days)
        st.session_state.chances = 5
        st.session_state.game_over = False
        st.session_state.message = "새로운 역사 속 날짜가 나왔어요!"
        st.session_state.try_count = 0
        st.rerun()

with st.expander("🎮 게임 방법"):
    st.write("""
    - 역사적인 날짜의 서울 평균기온을 맞히는 게임입니다.
    - 정답은 평균기온을 반올림한 정수입니다.
    - 기회는 총 5번입니다.
    - 입력한 기온이 낮으면 “더 높아요” 힌트가 나옵니다.
    - 입력한 기온이 높으면 “더 낮아요” 힌트가 나옵니다.
    - 빨리 맞힐수록 점수를 많이 얻습니다.
    """)

with st.expander("🏫 수업 활용 아이디어"):
    st.write("""
    이 앱은 역사와 데이터 과학을 연결하는 활동으로 활용할 수 있습니다.

    학생들은 역사적 사건이 일어난 날짜를 보고,
    당시의 계절과 날씨를 추측하며 기온을 맞힙니다.

    정답을 맞힌 뒤에는 사건의 의미와 당시 사회적 배경을 함께 이야기할 수 있습니다.
    """)
