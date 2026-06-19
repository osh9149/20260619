import streamlit as st
import random
import base64

st.set_page_config(
    page_title="전생 캐릭터 테스트",
    page_icon="🔮",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1f1c2c, #928dab, #fbc2eb);
}
.hero {
    padding: 35px;
    border-radius: 35px;
    text-align: center;
    background: linear-gradient(120deg, #ff9a9e, #fad0c4, #a18cd1);
    color: white;
    box-shadow: 0 10px 35px rgba(0,0,0,0.3);
}
.card {
    background: rgba(255,255,255,0.2);
    padding: 25px;
    border-radius: 28px;
    margin: 18px 0;
    border: 2px solid rgba(255,255,255,0.35);
    color: white;
}
.result {
    background: rgba(255,255,255,0.95);
    color: #333;
    padding: 25px;
    border-radius: 30px;
    margin: 18px 0;
}
.tag {
    display: inline-block;
    background: #fff0f7;
    color: #ff4fa3;
    padding: 8px 13px;
    margin: 5px;
    border-radius: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


past_life_data = [
    {
        "name": "달빛 왕국의 비밀 기록관",
        "emoji": "📜🌙",
        "color1": "#667eea",
        "color2": "#764ba2",
        "symbol": "📖",
        "desc": "전생의 당신은 왕국의 중요한 이야기를 기록하던 지혜로운 사람이었어요.",
        "place": "고대의 달빛 도서관",
        "talent": "사람의 마음을 읽는 능력",
        "keywords": ["지혜", "기록", "직관", "신비로움"]
    },
    {
        "name": "별을 읽는 항해사",
        "emoji": "🚢⭐",
        "color1": "#00c6ff",
        "color2": "#0072ff",
        "symbol": "🧭",
        "desc": "전생의 당신은 별자리를 보고 바다를 건너던 용감한 항해사였어요.",
        "place": "푸른 바다 위의 은빛 배",
        "talent": "어디서든 길을 찾는 능력",
        "keywords": ["모험", "용기", "방향감각", "자유"]
    },
    {
        "name": "꽃의 나라를 지키던 정원사",
        "emoji": "🌷🦋",
        "color1": "#fbc2eb",
        "color2": "#a6c1ee",
        "symbol": "🌸",
        "desc": "전생의 당신은 꽃과 나무를 돌보며 사람들에게 위로를 주던 따뜻한 사람이었어요.",
        "place": "비밀의 장미 정원",
        "talent": "상처받은 마음을 치유하는 능력",
        "keywords": ["따뜻함", "치유", "섬세함", "평화"]
    },
    {
        "name": "왕실의 천재 화가",
        "emoji": "🎨👑",
        "color1": "#ff9a9e",
        "color2": "#fad0c4",
        "symbol": "🎨",
        "desc": "전생의 당신은 감정을 색으로 표현하던 예술가였어요.",
        "place": "황금빛 궁전의 작업실",
        "talent": "감정을 그림으로 바꾸는 능력",
        "keywords": ["예술", "감성", "표현력", "아름다움"]
    },
    {
        "name": "숲속 마을의 마법 치료사",
        "emoji": "🌿🔮",
        "color1": "#84fab0",
        "color2": "#8fd3f4",
        "symbol": "🔮",
        "desc": "전생의 당신은 숲에서 약초와 마법을 연구하던 치료사였어요.",
        "place": "안개 낀 초록 숲",
        "talent": "자연의 목소리를 듣는 능력",
        "keywords": ["자연", "회복", "신비", "공감"]
    },
    {
        "name": "사막 도시의 보석 상인",
        "emoji": "💎🐫",
        "color1": "#f6d365",
        "color2": "#fda085",
        "symbol": "💎",
        "desc": "전생의 당신은 먼 나라를 오가며 아름다운 보석을 찾아다니던 상인이었어요.",
        "place": "황금빛 사막 시장",
        "talent": "숨겨진 가치를 발견하는 능력",
        "keywords": ["매력", "눈썰미", "교류", "풍요"]
    },
    {
        "name": "천상의 음악가",
        "emoji": "🎻☁️",
        "color1": "#a1c4fd",
        "color2": "#c2e9fb",
        "symbol": "🎻",
        "desc": "전생의 당신은 사람들의 마음을 움직이는 음악을 연주하던 존재였어요.",
        "place": "구름 위의 음악당",
        "talent": "마음을 울리는 선율을 만드는 능력",
        "keywords": ["음악", "감동", "감성", "위로"]
    },
    {
        "name": "비밀 조직의 천재 탐정",
        "emoji": "🕵️‍♀️🗝️",
        "color1": "#434343",
        "color2": "#000000",
        "symbol": "🗝️",
        "desc": "전생의 당신은 작은 단서도 놓치지 않는 탐정이었어요.",
        "place": "안개 낀 골목의 탐정 사무소",
        "talent": "숨겨진 진실을 발견하는 능력",
        "keywords": ["관찰력", "추리", "분석", "집중"]
    },
    {
        "name": "무지개 축제의 분위기 요정",
        "emoji": "🌈🎉",
        "color1": "#ff758c",
        "color2": "#ff7eb3",
        "symbol": "🌈",
        "desc": "전생의 당신은 축제마다 나타나 사람들에게 즐거움을 주던 존재였어요.",
        "place": "무지개빛 축제 광장",
        "talent": "분위기를 밝히는 능력",
        "keywords": ["에너지", "즐거움", "사교성", "긍정"]
    }
]


def get_zodiac(month, day):
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "♒ 물병자리", "독창적이고 자유로운 영혼"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "♓ 물고기자리", "상상력과 감성이 풍부한 영혼"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "♈ 양자리", "도전 정신이 강한 모험가"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "♉ 황소자리", "안정과 아름다움을 추구하는 영혼"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "♊ 쌍둥이자리", "호기심 많은 탐험가"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "♋ 게자리", "따뜻하고 배려심 많은 영혼"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "♌ 사자자리", "빛나는 리더형 영혼"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 23):
        return "♍ 처녀자리", "분석적이고 섬세한 영혼"
    elif (month == 9 and day >= 24) or (month == 10 and day <= 22):
        return "♎ 천칭자리", "균형과 조화를 사랑하는 영혼"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "♏ 전갈자리", "신비롭고 강렬한 영혼"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "♐ 사수자리", "자유로운 여행자"
    else:
        return "♑ 염소자리", "책임감 있는 전략가"


def is_valid_date(month, day):
    days = {
        1: 31, 2: 29, 3: 31, 4: 30,
        5: 31, 6: 30, 7: 31, 8: 31,
        9: 30, 10: 31, 11: 30, 12: 31
    }
    return day <= days[month]


def pick_result(month, day, name, photo_uploaded):
    name_score = sum(ord(c) for c in name) if name else 333
    photo_score = 77 if photo_uploaded else 11
    index = (month * day + name_score + photo_score) % len(past_life_data)
    return past_life_data[index]


def make_svg_card(result, user_name, zodiac_sign, zodiac_desc):
    svg = f"""
    <svg width="760" height="520" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="{result['color1']}"/>
          <stop offset="100%" stop-color="{result['color2']}"/>
        </linearGradient>
      </defs>

      <rect width="760" height="520" rx="40" fill="url(#bg)"/>

      <circle cx="110" cy="100" r="55" fill="rgba(255,255,255,0.25)"/>
      <circle cx="650" cy="90" r="75" fill="rgba(255,255,255,0.18)"/>
      <circle cx="620" cy="420" r="95" fill="rgba(255,255,255,0.16)"/>

      <text x="380" y="75" font-size="34" fill="white" text-anchor="middle" font-weight="bold">
        🔮 전생 캐릭터 카드 🔮
      </text>

      <text x="380" y="150" font-size="72" text-anchor="middle">
        {result['symbol']}
      </text>

      <text x="380" y="215" font-size="36" fill="white" text-anchor="middle" font-weight="bold">
        {result['name']}
      </text>

      <text x="380" y="260" font-size="28" fill="white" text-anchor="middle">
        {result['emoji']}
      </text>

      <rect x="90" y="300" width="580" height="155" rx="25" fill="rgba(255,255,255,0.88)"/>

      <text x="380" y="345" font-size="23" fill="#333" text-anchor="middle" font-weight="bold">
        {user_name}님의 별자리: {zodiac_sign}
      </text>

      <text x="380" y="382" font-size="20" fill="#333" text-anchor="middle">
        {zodiac_desc}
      </text>

      <text x="380" y="418" font-size="20" fill="#333" text-anchor="middle">
        전생의 장소: {result['place']}
      </text>

      <text x="380" y="448" font-size="20" fill="#333" text-anchor="middle">
        특별한 능력: {result['talent']}
      </text>

      <text x="380" y="495" font-size="18" fill="white" text-anchor="middle">
        재미로 보는 전생 테스트 · 지금의 당신도 충분히 특별해요 ✨
      </text>
    </svg>
    """
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("utf-8")


st.markdown("""
<div class="hero">
    <h1>🔮 전생 캐릭터 테스트 ✨</h1>
    <p>사진과 생일 월·일을 입력하면 별자리와 전생 캐릭터를 이미지 카드로 보여줘요 🌙</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🪄 정보 입력")
name = st.sidebar.text_input("이름 또는 별명", placeholder="예: 별빛요정")

month = st.sidebar.selectbox("태어난 월 🌙", list(range(1, 13)))
day = st.sidebar.selectbox("태어난 일 ⭐", list(range(1, 32)))

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📸 사진 업로드")
uploaded_file = st.file_uploader("사진을 올려주세요", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="업로드한 사진 📸", width=300)
else:
    st.info("사진을 올리면 결과 카드가 더 특별해져요 ✨")

st.markdown("</div>", unsafe_allow_html=True)

if st.button("🔮 전생 이미지 카드 만들기"):
    if not is_valid_date(month, day):
        st.error("선택한 월과 일이 맞지 않아요. 다시 선택해주세요.")
    else:
        zodiac_sign, zodiac_desc = get_zodiac(month, day)
        result = pick_result(month, day, name, uploaded_file is not None)
        user_name = name if name else "당신"

        st.balloons()

        image_url = make_svg_card(result, user_name, zodiac_sign, zodiac_desc)

        col1, col2 = st.columns([1.1, 1])

        with col1:
            st.image(image_url, use_container_width=True)

        with col2:
            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.markdown(f"## {result['emoji']} {result['name']}")
            st.write(result["desc"])
            st.write(f"⭐ **별자리:** {zodiac_sign}")
            st.write(f"🌙 **별자리 특징:** {zodiac_desc}")
            st.write(f"🏰 **전생의 장소:** {result['place']}")
            st.write(f"🪄 **특별한 능력:** {result['talent']}")

            for keyword in result["keywords"]:
                st.markdown(f'<span class="tag">#{keyword}</span>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.success("이미지 카드가 완성되었습니다 🌈 친구들과 결과를 비교해보세요!")

else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌟 사용 방법")
    st.write("1. 왼쪽에서 이름 또는 별명을 입력해요 ✏️")
    st.write("2. 생일은 월과 일만 선택해요 🌙⭐")
    st.write("3. 사진을 업로드해요 📸")
    st.write("4. 버튼을 누르면 별자리와 전생 캐릭터 이미지 카드가 나와요 🔮")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<br>
<div style="text-align:center; color:white;">
    🔮 이 앱은 재미용 콘텐츠입니다. 실제 운세나 성격 판단이 아닙니다 🌈
</div>
""", unsafe_allow_html=True)
