import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
import plotly.express as px

# =========================
# Streamlit 기본 설정
# =========================
st.set_page_config(
    page_title="서울 역사 날씨 퀴즈",
    page_icon="🌡️",
    layout="wide"
)

# GitHub Raw URL로 수정하세요
DATA_URL = "https://raw.githubusercontent.com/아이디/저장소명/main/ta_20260619190504.csv"

AVG_COL = "평균기온(℃)"
MIN_COL = "최저기온(℃)"
MAX_COL = "최고기온(℃)"

# =========================
# 디자인
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff3e0 0%, #e3f2fd 100%);
}
.big-title {
    font-size: 44px;
    font-weight: 900;
    text-align: center;
    color: #ff7043;
}
.sub-title {
    text-align: center;
    font-size: 20px;
    color: #444;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.15);
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 데이터 불러오기
# =========================
@st.cache_data
def load_data():
    encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]

    df = None

    for enc in encodings:
        try:
            df = pd.read_csv(DATA_URL, encoding=enc)
            break
        except UnicodeDecodeError:
            continue

    if df is None:
        df = pd.read_csv(DATA_URL, encoding="utf-8-sig", encoding_errors="ignore")

    df.columns = df.columns.str.strip()

    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df[AVG_COL] = pd.to_numeric(df[AVG_COL], errors="coerce")
    df[MIN_COL] = pd.to_numeric(df[MIN_COL], errors="coerce")
    df[MAX_COL] = pd.to_numeric(df[MAX_COL], errors="coerce")

    df = df.dropna(subset=["날짜", AVG_COL, MIN_COL, MAX_COL])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df


df = load_data()

# =========================
# 역사 사건 데이터
# =========================
history_events = [
    {"date": "1919-03-01", "event": "3·1 운동", "hint": "대한민국 독립운동의 상징적인 날이에요."},
    {"date": "1945-08-15", "event": "광복절", "hint": "우리나라가 해방된 날이에요."},
    {"date": "1948-08-15", "event": "대한민국 정부 수립", "hint": "대한민국 정부가 공식적으로 수립된 날이에요."},
    {"date": "1950-06-25", "event": "6·25 전쟁 발발", "hint": "한국전쟁이 시작된 날이에요."},
    {"date": "1960-04-19", "event": "4·19 혁명", "hint": "학생과 시민들이 민주주의를 외친 날이에요."},
    {"date": "1980-05-18", "event": "5·18 민주화운동", "hint": "민주주의 역사에서 중요한 사건이에요."},
    {"date": "1987-06-10", "event": "6월 민주항쟁", "hint": "대한민국 민주주의 발전에 큰 영향을 준 날이에요."},
    {"date": "1988-09-17", "event": "서울 올림픽 개막", "hint": "서울에서 세계적인 스포츠 축제가 열린 날이에요."},
    {"date": "2002-06-22", "event": "월드컵 4강 신화", "hint": "대한민국 축구가 세계를 놀라게 한 날이에요."},
    {"date": "2018-02-09", "event": "평창 동계올림픽 개막", "hint": "한국에서 열린 겨울 스포츠 축제의 시작일이에요."},
    {"date": "2020-03-02", "event": "코로나19 시기 개학 연기", "hint": "학교와 일상이 크게 바뀌기 시작한 시기예요."},
]

available_dates = set(df["날짜"].dt.strftime("%Y-%m-%d"))
history_events = [e for e in history_events if e["date"] in available_dates]

if len(history_events) == 0:
    st.error("역사 사건 날짜가 CSV 데이터에 없습니다. 날짜 형식이나 데이터 범위를 확인해주세요.")
    st.stop()

# =========================
# 새 문제 생성 함수
# =========================
def new_question():
    st.session_state.current_event = random.choice(history_events)
    st.session_state.attempt = 0
    st.session_state.answered = False
    st.session_state.guess_history = []
    st.session_state.hint_message = ""

# =========================
# 세션 상태 초기화
# =========================
if "score" not in st.session_state:
    st.session_state.score = 100

if "round" not in st.session_state:
    st.session_state.round = 1

if "score_history" not in st.session_state:
    st.session_state.score_history = [100]

if "current_event" not in st.session_state:
    new_question()

if "attempt" not in st.session_state:
    st.session_state.attempt = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "guess_history" not in st.session_state:
    st.session_state.guess_history = []

if "hint_message" not in st.session_state:
    st.session_state.hint_message = ""

# =========================
# 제목
# =========================
st.markdown('<div class="big-title">🕰️ 역사 속 서울 평균기온 맞히기 🌡️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">역사적인 그날, 서울의 평균기온은 몇 ℃였을까요?</div>', unsafe_allow_html=True)

st.divider()

# =========================
# 현재 문제 데이터
# =========================
event = st.session_state.current_event
event_date = pd.to_datetime(event["date"])
row = df[df["날짜"] == event_date].iloc[0]

actual_avg = round(row[AVG_COL], 1)
actual_min = round(row[MIN_COL], 1)
actual_max = round(row[MAX_COL], 1)

# =========================
# 화면 구성
# =========================
left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📜 역사 카드")
    st.markdown(f"## {event['event']}")
    st.markdown(f"### 📅 {event['date']}")
    st.info(event["hint"])

    st.markdown("### 🎯 이 날의 서울 평균기온을 맞혀보세요!")
    guess = st.slider(
        "평균기온(℃)",
        -20.0,
        40.0,
        15.0,
        0.1
    )

    st.markdown(f"### 남은 기회: {5 - st.session_state.attempt}번")

    if st.session_state.hint_message:
        st.warning(st.session_state.hint_message)

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏆 게임 현황")
    st.metric("현재 점수", f"{st.session_state.score}점")
    st.metric("현재 라운드", f"{st.session_state.round}라운드")
    st.progress(min(max(st.session_state.score, 0) / 300, 1.0))

    if st.session_state.score >= 300:
        st.success("🌟 역사 날씨 마스터!")
    elif st.session_state.score >= 200:
        st.info("🔥 날씨 추리 고수!")
    elif st.session_state.score >= 100:
        st.warning("🙂 아직 도전 중!")
    else:
        st.error("🥶 점수가 위험해요!")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 정답 도전
# =========================
if not st.session_state.answered:
    if st.button("✅ 평균기온 도전하기"):
        st.session_state.attempt += 1
        st.session_state.guess_history.append(guess)

        error = abs(guess - actual_avg)

        # 오차 1도 이내면 정답
        if error <= 1:
            add_score = max(10, 100 - (st.session_state.attempt - 1) * 15)
            st.session_state.score += add_score
            st.session_state.score_history.append(st.session_state.score)
            st.session_state.answered = True

            st.success(f"🎉 정답에 가까워요! 실제 평균기온은 {actual_avg}℃입니다.")
            st.balloons()

        else:
            if st.session_state.attempt < 5:
                if guess < actual_avg:
                    st.session_state.hint_message = "📈 힌트: 실제 평균기온은 네가 고른 온도보다 더 높아요!"
                else:
                    st.session_state.hint_message = "📉 힌트: 실제 평균기온은 네가 고른 온도보다 더 낮아요!"

                st.rerun()

            else:
                st.session_state.score -= 30
                st.session_state.score_history.append(st.session_state.score)
                st.session_state.answered = True
                st.error(f"😢 실패! 실제 평균기온은 {actual_avg}℃였습니다. 점수 30점 감소!")

st.divider()

# =========================
# 점수 변화 그래프
# =========================
st.markdown("## 📈 점수 변화 그래프")

score_fig = go.Figure()

score_fig.add_trace(go.Scatter(
    x=list(range(len(st.session_state.score_history))),
    y=st.session_state.score_history,
    mode="lines+markers",
    line=dict(width=5),
    marker=dict(size=12),
    name="점수"
))

score_fig.update_layout(
    title="게임 진행에 따른 점수 변화",
    xaxis_title="라운드 결과",
    yaxis_title="점수",
    height=350
)

st.plotly_chart(score_fig, use_container_width=True)

# =========================
# 정답 공개
# =========================
if st.session_state.answered:
    st.markdown("## 🔍 정답 공개")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("정답 평균기온", f"{actual_avg}℃")
    c2.metric("최저기온", f"{actual_min}℃")
    c3.metric("최고기온", f"{actual_max}℃")
    c4.metric("사용한 기회", f"{st.session_state.attempt}번")

    st.markdown("### 🧠 내가 입력한 평균기온 기록")

    guess_df = pd.DataFrame({
        "시도": [f"{i+1}번째" for i in range(len(st.session_state.guess_history))],
        "입력한 평균기온": st.session_state.guess_history
    })

    fig_guess = px.line(
        guess_df,
        x="시도",
        y="입력한 평균기온",
        markers=True,
        title="내가 추리한 평균기온 변화"
    )

    fig_guess.add_hline(
        y=actual_avg,
        line_dash="dash",
        annotation_text=f"정답 {actual_avg}℃"
    )

    st.plotly_chart(fig_guess, use_container_width=True)

    year_df = df[df["연도"] == event_date.year]
    month_df = year_df.groupby("월", as_index=False)[AVG_COL].mean()

    fig_month = px.bar(
        month_df,
        x="월",
        y=AVG_COL,
        title=f"{event_date.year}년 서울 월별 평균기온",
        text_auto=".1f"
    )

    st.plotly_chart(fig_month, use_container_width=True)

    if st.button("➡️ 다음 문제로 이동"):
        st.session_state.round += 1
        new_question()
        st.rerun()

# =========================
# 사이드바
# =========================
with st.sidebar:
    st.title("🎮 메뉴")

    if st.button("🔄 게임 초기화"):
        st.session_state.score = 100
        st.session_state.round = 1
        st.session_state.score_history = [100]
        new_question()
        st.rerun()

    st.markdown("---")
    st.markdown("### 점수 규칙")
    st.markdown("""
    - 문제는 역사적 사건이 있었던 날의 **평균기온** 맞히기
    - 5번 안에 맞히면 점수 상승
    - 빨리 맞힐수록 높은 점수
    - 오차 1℃ 이내면 정답 처리
    - 5번 안에 못 맞히면 30점 감소
    - 틀릴 때마다 정답이 더 높은지 낮은지 힌트 제공
    """)

# =========================
# 데이터 탐구 모드
# =========================
with st.expander("🌍 데이터 탐구 모드"):
    yearly = df.groupby("연도", as_index=False)[AVG_COL].mean()

    fig_year = px.line(
        yearly,
        x="연도",
        y=AVG_COL,
        title="1907~2026 서울 연도별 평균기온 변화",
        markers=True
    )

    st.plotly_chart(fig_year, use_container_width=True)

    st.markdown("""
    ### 탐구 질문
    - 역사적 사건이 있었던 날의 평균기온은 어땠나요?
    - 서울의 평균기온은 장기적으로 상승하고 있을까요?
    - 기후 데이터와 역사 수업을 연결하면 어떤 점이 좋을까요?
    """)

st.caption("서울 기온 데이터 기반 역사 평균기온 추리 게임")
