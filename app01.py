import streamlit as st
import random

st.set_page_config(
    page_title="MBTI 여행지 추천",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff1eb 0%, #ace0f9 50%, #fbc2eb 100%);
}

.hero {
    padding: 38px;
    border-radius: 35px;
    text-align: center;
    background: linear-gradient(120deg, #ff9a9e, #fad0c4, #a18cd1);
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
    color: white;
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 20px;
}

.card {
    background: rgba(255,255,255,0.88);
    padding: 25px;
    border-radius: 28px;
    margin: 18px 0;
    box-shadow: 0 6px 22px rgba(0,0,0,0.13);
}

.place-card {
    background: linear-gradient(135deg, #ffffff, #fff3fb);
    padding: 22px;
    border-radius: 24px;
    margin: 14px 0;
    border: 2px solid white;
    box-shadow: 0 5px 18px rgba(255,105,180,0.22);
}

.big {
    font-size: 25px;
    font-weight: 800;
}

.tag {
    display: inline-block;
    background: #fff0f7;
    color: #ff4fa3;
    padding: 7px 12px;
    margin: 5px;
    border-radius: 20px;
    font-weight: bold;
}

.notice {
    text-align: center;
    color: #666;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)


travel_data = {
    "INTJ": {
        "title": "계획형 세계관 설계자 🧠🗺️",
        "desc": "조용히 깊이 탐색하고, 의미 있는 장소를 체계적으로 여행하는 스타일이에요.",
        "places": [
            ("교토, 일본 🇯🇵", "고즈넉한 사찰과 골목을 따라 혼자만의 생각을 정리하기 좋아요."),
            ("경주, 한국 🇰🇷", "역사와 건축, 문화유산을 차분하게 탐구하기 좋은 도시예요."),
            ("프라하, 체코 🇨🇿", "중세 도시 분위기와 건축미를 깊이 감상하기 좋아요.")
        ],
        "style": ["역사 탐방", "건축 감상", "조용한 카페", "계획 여행"]
    },
    "INTP": {
        "title": "호기심 많은 탐구 여행자 🔍🌌",
        "desc": "새로운 지식, 과학, 독특한 문화가 있는 여행지에서 에너지를 얻어요.",
        "places": [
            ("아이슬란드 🇮🇸", "화산, 빙하, 오로라까지 자연과 과학적 호기심을 모두 채울 수 있어요."),
            ("대전, 한국 🇰🇷", "과학관, 연구단지, 카이스트 주변 탐방 코스로 좋아요."),
            ("런던, 영국 🇬🇧", "박물관과 도서관, 과학·역사 콘텐츠가 풍부해요.")
        ],
        "style": ["박물관", "과학관", "자연현상", "자유 일정"]
    },
    "ENTJ": {
        "title": "성취형 글로벌 리더 👑✈️",
        "desc": "도시의 에너지, 비즈니스 감각, 멋진 전망이 있는 곳과 잘 맞아요.",
        "places": [
            ("뉴욕, 미국 🇺🇸", "강한 도시 에너지와 다양한 문화, 전망대, 뮤지컬까지 즐길 수 있어요."),
            ("싱가포르 🇸🇬", "깨끗하고 효율적인 도시 시스템과 미래적인 분위기가 매력적이에요."),
            ("서울, 한국 🇰🇷", "쇼핑, 문화, 전시, 맛집을 빠르게 즐기기 좋아요.")
        ],
        "style": ["도시 여행", "전망대", "핫플", "효율적 일정"]
    },
    "ENTP": {
        "title": "즉흥 아이디어 모험가 ⚡🎒",
        "desc": "예상 밖의 재미, 사람들과의 만남, 새로운 자극이 많은 곳을 좋아해요.",
        "places": [
            ("방콕, 태국 🇹🇭", "야시장, 맛집, 루프탑, 골목 탐험까지 즉흥 여행에 딱 좋아요."),
            ("홍대·성수, 한국 🇰🇷", "팝업스토어, 전시, 카페, 거리 문화가 풍부해요."),
            ("바르셀로나, 스페인 🇪🇸", "예술, 건축, 해변, 축제 분위기를 모두 즐길 수 있어요.")
        ],
        "style": ["즉흥 여행", "야시장", "핫플", "로컬 체험"]
    },
    "INFJ": {
        "title": "감성 깊은 힐링 여행자 🌙🌿",
        "desc": "조용하고 의미 있는 공간에서 마음을 회복하는 여행을 좋아해요.",
        "places": [
            ("제주 동쪽, 한국 🇰🇷", "바다, 오름, 조용한 카페에서 감성 충전하기 좋아요."),
            ("스위스 루체른 🇨🇭", "호수와 산이 어우러진 풍경이 마음을 편안하게 해줘요."),
            ("전주 한옥마을, 한국 🇰🇷", "전통과 감성이 어우러져 천천히 걷기 좋은 곳이에요.")
        ],
        "style": ["힐링", "산책", "감성 카페", "자연"]
    },
    "INFP": {
        "title": "꿈꾸는 감성 여행 시인 🌷📷",
        "desc": "예쁜 풍경, 작은 골목, 사진 찍기 좋은 공간에서 행복을 느껴요.",
        "places": [
            ("파리, 프랑스 🇫🇷", "거리, 미술관, 카페까지 감성 여행의 정석이에요."),
            ("여수, 한국 🇰🇷", "밤바다와 낭만적인 풍경이 감성 충전에 좋아요."),
            ("타이베이, 대만 🇹🇼", "골목 감성, 야시장, 따뜻한 분위기를 즐기기 좋아요.")
        ],
        "style": ["감성 사진", "골목길", "카페", "노을"]
    },
    "ENFJ": {
        "title": "함께 빛나는 여행 리더 ☀️🤝",
        "desc": "사람들과 함께 추억을 만들고, 따뜻한 교류가 있는 여행을 좋아해요.",
        "places": [
            ("부산, 한국 🇰🇷", "바다, 맛집, 야경을 친구들과 함께 즐기기 좋아요."),
            ("다낭, 베트남 🇻🇳", "리조트, 바다, 야시장까지 가족·친구 여행에 잘 맞아요."),
            ("로마, 이탈리아 🇮🇹", "역사와 음식, 활기찬 분위기를 함께 나누기 좋아요.")
        ],
        "style": ["단체 여행", "맛집", "야경", "문화 체험"]
    },
    "ENFP": {
        "title": "설렘 폭발 자유 여행자 🌈🎉",
        "desc": "다채로운 색감, 사람, 음악, 음식이 있는 여행지에서 반짝여요.",
        "places": [
            ("발리, 인도네시아 🇮🇩", "바다, 요가, 카페, 자연을 자유롭게 즐기기 좋아요."),
            ("강릉, 한국 🇰🇷", "바다와 카페, 감성 숙소가 많아 즉흥 힐링에 좋아요."),
            ("리스본, 포르투갈 🇵🇹", "알록달록한 거리와 따뜻한 분위기가 매력적이에요.")
        ],
        "style": ["자유 여행", "바다", "카페 투어", "사진"]
    },
    "ISTJ": {
        "title": "꼼꼼한 안정 여행자 📋🧳",
        "desc": "일정이 안정적이고 교통이 편리하며 볼거리가 확실한 여행지를 선호해요.",
        "places": [
            ("오사카, 일본 🇯🇵", "교통이 편하고 먹거리, 쇼핑, 관광 코스가 분명해요."),
            ("대구, 한국 🇰🇷", "근대골목, 맛집, 카페를 체계적으로 둘러보기 좋아요."),
            ("비엔나, 오스트리아 🇦🇹", "음악, 미술관, 궁전 등 클래식한 관광지가 잘 정리되어 있어요.")
        ],
        "style": ["계획 여행", "교통 편리", "맛집 지도", "문화유산"]
    },
    "ISFJ": {
        "title": "따뜻한 추억 수집가 🍀💗",
        "desc": "편안하고 안전한 분위기에서 소중한 사람과 추억을 쌓는 여행을 좋아해요.",
        "places": [
            ("남해, 한국 🇰🇷", "조용한 바다와 예쁜 마을에서 편안히 쉬기 좋아요."),
            ("후쿠오카, 일본 🇯🇵", "가깝고 편안하며 음식과 쇼핑을 부담 없이 즐길 수 있어요."),
            ("치앙마이, 태국 🇹🇭", "여유로운 분위기와 따뜻한 감성이 있는 도시예요.")
        ],
        "style": ["힐링", "가족 여행", "편안한 숙소", "맛집"]
    },
    "ESTJ": {
        "title": "알찬 코스 완성형 여행자 🏆🗺️",
        "desc": "짧은 시간 안에 핵심 코스를 효율적으로 즐기는 여행을 좋아해요.",
        "places": [
            ("도쿄, 일본 🇯🇵", "쇼핑, 맛집, 전시, 근교까지 체계적으로 즐길 수 있어요."),
            ("상하이, 중국 🇨🇳", "도시 전망, 쇼핑, 근대 건축을 알차게 볼 수 있어요."),
            ("속초, 한국 🇰🇷", "바다, 시장, 설악산까지 짧은 일정에 다양하게 즐길 수 있어요.")
        ],
        "style": ["핵심 코스", "맛집", "쇼핑", "시간 관리"]
    },
    "ESFJ": {
        "title": "모두가 즐거운 여행 메이트 💐👥",
        "desc": "함께 먹고 웃고 사진 찍는 따뜻한 여행에서 행복을 느껴요.",
        "places": [
            ("제주 서쪽, 한국 🇰🇷", "카페, 바다, 맛집이 많아 친구·가족 여행에 좋아요."),
            ("괌 🇬🇺", "휴양, 쇼핑, 해변을 편하게 즐길 수 있어요."),
            ("호이안, 베트남 🇻🇳", "등불 거리와 따뜻한 분위기가 추억 만들기에 좋아요.")
        ],
        "style": ["친구 여행", "사진", "맛집", "편한 일정"]
    },
    "ISTP": {
        "title": "액티비티 실전 여행자 🛠️🏄",
        "desc": "직접 해보고 몸으로 느끼는 여행에서 재미를 찾아요.",
        "places": [
            ("양양, 한국 🇰🇷", "서핑, 바다, 자유로운 분위기를 즐기기 좋아요."),
            ("뉴질랜드 퀸스타운 🇳🇿", "번지점프, 트레킹, 액티비티의 천국이에요."),
            ("코타키나발루, 말레이시아 🇲🇾", "섬투어, 스노클링, 선셋을 즐기기 좋아요.")
        ],
        "style": ["액티비티", "서핑", "트레킹", "자유 일정"]
    },
    "ISFP": {
        "title": "감각적인 풍경 수집가 🎨🌿",
        "desc": "예쁜 색감, 자연, 음악, 여유로운 분위기와 잘 어울려요.",
        "places": [
            ("통영, 한국 🇰🇷", "바다와 섬, 예술적인 마을 풍경이 아름다워요."),
            ("하와이 🇺🇸", "바다, 음악, 자연, 여유가 조화로운 여행지예요."),
            ("니스, 프랑스 🇫🇷", "푸른 해변과 감각적인 도시 분위기가 매력적이에요.")
        ],
        "style": ["예쁜 풍경", "예술", "바다", "여유"]
    },
    "ESTP": {
        "title": "짜릿한 현장형 모험가 🔥🎯",
        "desc": "움직임이 많고 재미있는 사건이 생기는 여행을 좋아해요.",
        "places": [
            ("세부, 필리핀 🇵🇭", "호핑투어, 스노클링, 액티비티를 즐기기 좋아요."),
            ("가평, 한국 🇰🇷", "수상레저, 캠핑, 짚라인 등 활동적인 여행에 좋아요."),
            ("라스베이거스, 미국 🇺🇸", "화려한 쇼, 야경, 근교 투어까지 자극이 가득해요.")
        ],
        "style": ["액션", "레저", "야경", "즉흥"]
    },
    "ESFP": {
        "title": "인생샷 파티 여행자 🎤🌟",
        "desc": "화려하고 즐거운 분위기, 맛있는 음식, 멋진 사진을 좋아해요.",
        "places": [
            ("홍콩 🇭🇰", "야경, 쇼핑, 맛집, 감성 사진까지 모두 즐길 수 있어요."),
            ("부산 광안리, 한국 🇰🇷", "바다, 야경, 카페, 분위기 좋은 식당이 많아요."),
            ("칸쿤, 멕시코 🇲🇽", "해변과 리조트, 화려한 휴양 분위기가 매력적이에요.")
        ],
        "style": ["인생샷", "야경", "쇼핑", "파티"]
    }
}

tips = [
    "여행은 MBTI보다 내 체력과 예산이 더 중요할 수도 있어요 💸",
    "친구와 여행한다면 서로의 여행 스타일을 먼저 이야기해보세요 🧡",
    "사진보다 중요한 건 그 순간의 기분이에요 📷",
    "계획형 친구와 즉흥형 친구가 함께 가면 의외로 최고의 조합이 될 수 있어요 ✨",
    "가고 싶은 곳을 하나 정했다면, 그 이유를 적어보는 것도 좋은 진로·자기이해 활동이에요 📝"
]

st.markdown("""
<div class="hero">
    <h1>✈️ MBTI 여행지 추천 앱 🌈</h1>
    <p>나의 성향에 딱 맞는 국내·해외 여행지를 찾아보세요 🧳✨</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🧳 여행자 정보")
name = st.sidebar.text_input("이름 또는 별명 ✏️", placeholder="예: 여행요정, 민지")
season = st.sidebar.selectbox("떠나고 싶은 계절 🌤️", ["봄 🌸", "여름 🌊", "가을 🍁", "겨울 ❄️"])
partner = st.sidebar.radio("누구와 떠나나요? 👥", ["혼자 🧘", "친구와 👯", "가족과 👨‍👩‍👧", "연인과 💕"])
budget = st.sidebar.select_slider(
    "여행 예산 느낌 💰",
    options=["가성비", "적당히", "플렉스"]
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💎 나의 MBTI 선택하기")
selected = st.selectbox("MBTI를 골라주세요", list(travel_data.keys()))
st.markdown("</div>", unsafe_allow_html=True)

data = travel_data[selected]
user_name = name if name else "여행자"

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f"""
<p class="big">🌟 {user_name}님의 여행 성향은?</p>
<h2>{selected} · {data["title"]}</h2>
<p>{data["desc"]}</p>
""", unsafe_allow_html=True)

for tag in data["style"]:
    st.markdown(f'<span class="tag">#{tag}</span>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌍 추천 여행지 TOP 3")

    for i, place in enumerate(data["places"], 1):
        st.markdown(f"""
        <div class="place-card">
            <h3>{i}. {place[0]}</h3>
            <p>{place[1]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎒 여행 스타일 분석")
    st.write(f"🌤️ **추천 계절:** {season}")
    st.write(f"👥 **동행 유형:** {partner}")
    st.write(f"💰 **예산 스타일:** {budget}")

    st.write("")
    st.subheader("📌 준비물 추천")
    items = ["보조배터리 🔋", "편한 신발 👟", "여권 또는 신분증 🪪", "이어폰 🎧", "작은 노트 📝"]
    for item in items:
        st.write(f"- {item}")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📝 여행 탐색 미션")
st.write("1. 추천 여행지 중 가장 끌리는 곳 하나 고르기 💖")
st.write("2. 그 여행지에서 꼭 해보고 싶은 활동 3가지 적기 🎯")
st.write("3. 예상 경비를 검색해서 간단한 예산표 만들기 💰")
st.write("4. 친구와 함께 간다면 역할 나누기: 일정 담당, 맛집 담당, 사진 담당 📷")
st.write("5. 여행 후기를 상상해서 한 문단으로 작성하기 ✍️")
st.markdown("</div>", unsafe_allow_html=True)

if st.button("🎁 나만의 랜덤 여행 카드 뽑기"):
    st.balloons()
    place = random.choice(data["places"])
    st.markdown(f"""
    <div class="card">
        <h2>🎫 {user_name}님의 랜덤 여행 카드</h2>
        <h3>오늘의 추천 여행지는 {place[0]}</h3>
        <p>{place[1]}</p>
        <p><b>✨ 여행 키워드:</b> {", ".join(data["style"])}</p>
        <p><b>💌 한 줄 메시지:</b> {random.choice(tips)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<br>
<div class="notice">
    🌈 이 앱은 MBTI를 활용한 재미있는 여행 성향 추천 앱입니다.<br>
    실제 여행지는 예산, 일정, 안전, 날씨, 여권·비자 등을 함께 고려해 선택하세요.
</div>
""", unsafe_allow_html=True)
