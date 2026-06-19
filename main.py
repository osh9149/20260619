import streamlit as st
import random

st.set_page_config(
    page_title="MBTI 진로 추천",
    page_icon="🌈",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffe6f0 0%, #e6f7ff 45%, #fff7d6 100%);
}

.title-box {
    background: linear-gradient(90deg, #ff7eb3, #8ec5fc, #f9f586);
    padding: 30px;
    border-radius: 30px;
    text-align: center;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
}

.title-box h1 {
    color: white;
    font-size: 48px;
    margin-bottom: 10px;
}

.title-box p {
    color: white;
    font-size: 20px;
}

.card {
    background-color: rgba(255,255,255,0.85);
    padding: 25px;
    border-radius: 25px;
    margin: 15px 0;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.12);
    border: 2px solid #ffffff;
}

.job-card {
    background: linear-gradient(135deg, #ffffff, #fff0f6);
    padding: 20px;
    border-radius: 22px;
    margin: 12px 0;
    box-shadow: 0px 4px 15px rgba(255,126,179,0.25);
}

.big-text {
    font-size: 24px;
    font-weight: bold;
}

.small-text {
    font-size: 17px;
    line-height: 1.7;
}

.highlight {
    color: #ff4f9a;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
career_data = {
    "INTJ": {
        "emoji": "🧠🚀📊",
        "nickname": "전략적인 미래 설계자",
        "desc": "계획적이고 분석적이며, 복잡한 문제를 해결하는 데 강점이 있어요.",
        "jobs": ["AI 연구원 🤖", "데이터 과학자 📊", "소프트웨어 개발자 💻", "전략 컨설턴트 🧩", "건축가 🏛️"],
        "subjects": ["수학", "정보", "과학", "경제"],
        "keywords": ["분석력", "기획력", "문제해결", "독립성"]
    },
    "INTP": {
        "emoji": "🔍🧪💡",
        "nickname": "호기심 많은 아이디어 탐험가",
        "desc": "새로운 원리를 탐구하고 깊이 생각하는 것을 좋아해요.",
        "jobs": ["연구원 🔬", "프로그래머 💻", "게임 개발자 🎮", "철학자 📚", "발명가 💡"],
        "subjects": ["정보", "물리", "수학", "철학"],
        "keywords": ["탐구심", "논리력", "창의성", "독창성"]
    },
    "ENTJ": {
        "emoji": "👑📈🔥",
        "nickname": "목표를 향해 달리는 리더",
        "desc": "리더십이 강하고 목표를 세워 추진하는 능력이 뛰어나요.",
        "jobs": ["CEO 🏢", "기획자 📝", "변호사 ⚖️", "프로젝트 매니저 📌", "창업가 🚀"],
        "subjects": ["경제", "사회", "정보", "국어"],
        "keywords": ["리더십", "추진력", "전략", "결단력"]
    },
    "ENTP": {
        "emoji": "⚡🎤💬",
        "nickname": "톡톡 튀는 아이디어 메이커",
        "desc": "새로운 아이디어를 내고 사람들과 토론하는 것을 즐겨요.",
        "jobs": ["마케터 📣", "콘텐츠 기획자 🎬", "창업가 🚀", "광고 기획자 🎨", "방송인 🎙️"],
        "subjects": ["국어", "사회", "정보", "미디어"],
        "keywords": ["창의력", "설득력", "도전", "순발력"]
    },
    "INFJ": {
        "emoji": "🌙💌🌱",
        "nickname": "따뜻한 통찰력의 조언자",
        "desc": "사람의 마음을 잘 이해하고 의미 있는 일을 중요하게 생각해요.",
        "jobs": ["상담사 💬", "작가 ✍️", "교사 👩‍🏫", "심리학자 🧠", "사회복지사 🤝"],
        "subjects": ["국어", "윤리", "사회", "심리"],
        "keywords": ["공감", "통찰", "책임감", "이상"]
    },
    "INFP": {
        "emoji": "🌷🎨📖",
        "nickname": "감성 가득한 꿈꾸는 예술가",
        "desc": "자신만의 가치와 감성을 중요하게 여기며 표현력이 좋아요.",
        "jobs": ["작가 ✍️", "디자이너 🎨", "음악가 🎧", "상담사 💬", "일러스트레이터 🖌️"],
        "subjects": ["국어", "미술", "음악", "윤리"],
        "keywords": ["감수성", "창의성", "공감", "표현"]
    },
    "ENFJ": {
        "emoji": "☀️🤝🎤",
        "nickname": "사람을 성장시키는 따뜻한 리더",
        "desc": "사람들과 함께 성장하고 긍정적인 영향을 주는 것을 좋아해요.",
        "jobs": ["교사 👩‍🏫", "상담가 💬", "강연가 🎤", "HR 전문가 👥", "사회운동가 🌍"],
        "subjects": ["국어", "사회", "윤리", "교육"],
        "keywords": ["소통", "공감", "리더십", "동기부여"]
    },
    "ENFP": {
        "emoji": "🌈🎉✨",
        "nickname": "에너지 넘치는 가능성 탐험가",
        "desc": "밝고 자유로운 분위기에서 다양한 가능성을 발견하는 데 강해요.",
        "jobs": ["크리에이터 📱", "마케터 📣", "배우 🎭", "기획자 📝", "여행 작가 ✈️"],
        "subjects": ["국어", "미디어", "사회", "예술"],
        "keywords": ["열정", "창의성", "소통", "자유로움"]
    },
    "ISTJ": {
        "emoji": "📚🧾🛡️",
        "nickname": "믿음직한 원칙 지킴이",
        "desc": "책임감이 강하고 정확하고 체계적인 일을 잘해요.",
        "jobs": ["공무원 🏛️", "회계사 🧾", "법무사 ⚖️", "데이터 관리자 📊", "품질관리 전문가 ✅"],
        "subjects": ["수학", "사회", "경제", "법"],
        "keywords": ["성실함", "책임감", "정확성", "체계성"]
    },
    "ISFJ": {
        "emoji": "🍀💗🏥",
        "nickname": "섬세하고 따뜻한 보호자",
        "desc": "다른 사람을 세심하게 챙기고 안정적인 환경에서 강점을 보여요.",
        "jobs": ["간호사 🏥", "교사 👩‍🏫", "사회복지사 🤝", "행정직 📋", "보육교사 🧸"],
        "subjects": ["생명과학", "윤리", "사회", "보건"],
        "keywords": ["배려", "성실", "안정", "섬세함"]
    },
    "ESTJ": {
        "emoji": "📢📋🏆",
        "nickname": "현실적인 실행 관리자",
        "desc": "규칙과 목표를 중요하게 여기며 일을 효율적으로 추진해요.",
        "jobs": ["관리자 📋", "경찰관 👮", "공무원 🏛️", "경영자 💼", "군인 🪖"],
        "subjects": ["사회", "경제", "체육", "법"],
        "keywords": ["실행력", "관리", "책임", "질서"]
    },
    "ESFJ": {
        "emoji": "💐👥🎀",
        "nickname": "분위기를 밝히는 친화력 부자",
        "desc": "사람들과 어울리며 도움을 주는 일에서 큰 만족을 느껴요.",
        "jobs": ["교사 👩‍🏫", "간호사 🏥", "승무원 ✈️", "상담사 💬", "이벤트 플래너 🎉"],
        "subjects": ["국어", "사회", "보건", "윤리"],
        "keywords": ["친화력", "배려", "협력", "책임감"]
    },
    "ISTP": {
        "emoji": "🛠️🏍️🎮",
        "nickname": "손으로 해결하는 현실 탐험가",
        "desc": "직접 만들고 고치고 실험하는 활동에서 능력을 발휘해요.",
        "jobs": ["엔지니어 ⚙️", "정비사 🛠️", "파일럿 ✈️", "개발자 💻", "스포츠 선수 🏅"],
        "subjects": ["기술", "정보", "물리", "체육"],
        "keywords": ["실용성", "문제해결", "침착함", "손재주"]
    },
    "ISFP": {
        "emoji": "🎨🌿🎧",
        "nickname": "감각적인 자유 예술가",
        "desc": "아름다움과 감성을 잘 느끼고 자신만의 방식으로 표현해요.",
        "jobs": ["디자이너 🎨", "사진작가 📷", "음악가 🎧", "플로리스트 🌸", "패션 스타일리스트 👗"],
        "subjects": ["미술", "음악", "기술", "국어"],
        "keywords": ["감각", "예술성", "자유", "섬세함"]
    },
    "ESTP": {
        "emoji": "🔥🏃‍♂️🎯",
        "nickname": "도전하는 액션 히어로",
        "desc": "활동적이고 빠르게 판단하며 현장에서 능력을 발휘해요.",
        "jobs": ["경찰관 👮", "소방관 🚒", "운동선수 🏅", "영업 전문가 💼", "응급구조사 🚑"],
        "subjects": ["체육", "사회", "기술", "경제"],
        "keywords": ["도전", "순발력", "행동력", "현장감"]
    },
    "ESFP": {
        "emoji": "🎤🌟🎬",
        "nickname": "무대를 빛내는 즐거움 메이커",
        "desc": "사람들 앞에서 표현하고 즐거운 분위기를 만드는 데 강해요.",
        "jobs": ["배우 🎭", "가수 🎤", "유튜버 📱", "이벤트 기획자 🎉", "뷰티 아티스트 💄"],
        "subjects": ["음악", "미술", "체육", "미디어"],
        "keywords": ["표현력", "사교성", "즐거움", "감각"]
    }
}

quotes = [
    "너의 가능성은 아직 전부 펼쳐지지 않았어 🌱",
    "좋아하는 것을 찾는 과정도 멋진 진로 탐색이야 ✨",
    "진로는 정답을 맞히는 것이 아니라 나를 알아가는 여행이야 🧭",
    "오늘의 작은 선택이 내일의 멋진 나를 만든다 🌈",
    "너만의 속도로 충분히 잘 가고 있어 💖"
]

# ---------------- TITLE ----------------
st.markdown("""
<div class="title-box">
    <h1>🌈 MBTI 진로 추천 연구소 ✨</h1>
    <p>나의 성향을 선택하면 어울리는 직업과 과목을 추천해드려요 💖</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌟 진로 탐색 메뉴")
student_name = st.sidebar.text_input("이름 또는 별명 입력하기 ✏️", placeholder="예: 민지, 코딩왕, 햄찌")
grade = st.sidebar.selectbox("학년 선택 🎒", ["중학생", "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"])
mood = st.sidebar.radio("오늘의 기분은? 💭", ["신남 😆", "차분함 🌙", "궁금함 🤔", "설렘 💖", "졸림 😴"])

# ---------------- MBTI SELECT ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💎 나의 MBTI를 선택해보세요!")

mbti_list = list(career_data.keys())
selected_mbti = st.selectbox("MBTI 선택", mbti_list)

st.markdown("</div>", unsafe_allow_html=True)

data = career_data[selected_mbti]

# ---------------- RESULT ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

name_text = student_name if student_name else "학생"
st.markdown(f"""
<p class="big-text">✨ {name_text}님의 MBTI는 <span class="highlight">{selected_mbti}</span> {data['emoji']}</p>
<h2>💖 {data['nickname']}</h2>
<p class="small-text">{data['desc']}</p>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- COLUMNS ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 추천 직업 TOP 5")
    for job in data["jobs"]:
        st.markdown(f"""
        <div class="job-card">
            <span class="big-text">{job}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📚 잘 맞는 과목")
    for subject in data["subjects"]:
        st.markdown(f"### 🌟 {subject}")

    st.write("")
    st.subheader("💡 나의 강점 키워드")
    st.write(" ".join([f"🌈 **{k}**" for k in data["keywords"]]))
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CAREER GUIDE ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧭 진로 탐색 미션")

missions = [
    "관심 직업 1개를 골라 어떤 일을 하는지 조사하기 🔍",
    "그 직업에 필요한 과목이나 역량 찾아보기 📚",
    "관련 학과나 대학 전공 검색해보기 🎓",
    "비슷한 직업 3개 더 찾아보기 🌱",
    "나의 장점과 연결해서 진로 발표문 작성하기 🎤"
]

for i, mission in enumerate(missions, 1):
    st.write(f"**Mission {i}.** {mission}")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RANDOM QUOTE ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💌 오늘의 응원 메시지")
st.success(random.choice(quotes))
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- BUTTON ----------------
if st.button("🎁 나에게 주는 진로 응원 카드 만들기"):
    st.balloons()
    st.markdown(f"""
    <div class="card">
        <h2>💖 {name_text}님의 진로 응원 카드 💖</h2>
        <p class="big-text">{selected_mbti} {data['emoji']}</p>
        <p class="small-text">
        {name_text}님은 <b>{data['nickname']}</b> 유형이에요.<br>
        앞으로 <b>{data['jobs'][0]}</b>, <b>{data['jobs'][1]}</b>, <b>{data['jobs'][2]}</b> 같은 분야를 탐색해보면 좋아요.<br><br>
        🌈 중요한 것은 MBTI가 정답이 아니라, 나를 이해하는 출발점이라는 거예요!
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<br><br>
<div style="text-align:center; color:#777;">
    🌸 MBTI는 참고 자료일 뿐이에요. 진로는 흥미, 가치관, 역량, 경험을 함께 살펴보며 선택해요 🌸
</div>
""", unsafe_allow_html=True)
