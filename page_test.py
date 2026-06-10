import streamlit as st

st.set_page_config(
    page_title="레쭈고! 카페!",
    page_icon="☕",
    layout="centered"
)

# CSS 스타일
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap');

.stApp {
    background:
        linear-gradient(rgba(255,255,255,0.78), rgba(255,255,255,0.78)),
        repeating-linear-gradient(
            0deg,
            #eaf5ff 0px,
            #eaf5ff 4px,
            #d7ebff 4px,
            #d7ebff 8px
        );
    font-family: 'Noto Sans KR', sans-serif;
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* 전체 게임 화면 박스 */
.main-box {
    max-width: 760px;
    margin: 20px auto 30px auto;
    padding: 32px 28px;
    border: 5px solid #2f6eea;
    border-radius: 28px;
    background: #fffdf2;
    box-shadow: 
        8px 8px 0px #8ab6ff,
        0 0 0 8px #fff59d;
    position: relative;
    overflow: hidden;
}

/* Y2K 그리드 배경 */
.main-box::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(#cfe4ff 1px, transparent 1px),
        linear-gradient(90deg, #cfe4ff 1px, transparent 1px);
    background-size: 28px 28px;
    opacity: 0.48;
    z-index: 0;
}

.content {
    position: relative;
    z-index: 1;
    text-align: center;
}

/* 상단 라벨 */
.sub-label {
    display: inline-block;
    background: #2f6eea;
    color: white;
    padding: 7px 18px;
    border-radius: 999px;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 14px;
    box-shadow: 3px 3px 0 #99c8ff;
    letter-spacing: 1px;
}

/* 메인 타이틀 */
.pixel-title {
    font-size: 68px;
    line-height: 1.05;
    color: #ffffff;
    letter-spacing: -2px;
    font-weight: 900;
    text-shadow:
        4px 4px 0 #2f6eea,
        8px 8px 0 #9dd7ff,
        -3px -3px 0 #2f6eea;
    margin-bottom: 10px;
}

/* 아이콘 줄 */
.icon-row {
    font-size: 34px;
    margin: 18px 0;
    letter-spacing: 10px;
}

/* 설명 박스 */
.desc-box {
    background: rgba(255, 255, 255, 0.95);
    border: 4px solid #2f6eea;
    border-radius: 20px;
    padding: 20px 22px;
    margin: 26px auto 8px auto;
    color: #31528f;
    font-size: 15px;
    font-weight: 500;
    line-height: 1.7;
    box-shadow: 5px 5px 0 #bcdcff;
}

.desc-box b {
    color: #2f6eea;
    font-weight: 800;
}

/* 별 장식 */
.star {
    position: absolute;
    font-size: 28px;
    color: #2f6eea;
    z-index: 1;
}

.star.one { top: 32px; left: 38px; }
.star.two { top: 76px; right: 48px; }
.star.three { bottom: 46px; left: 54px; }
.star.four { bottom: 72px; right: 58px; }

/* 시작 버튼 */
.stButton > button {
    width: 100%;
    background: #ffffff;
    color: #2f6eea;
    border: 4px solid #2f6eea;
    border-radius: 16px;
    padding: 14px 20px;
    font-size: 22px;
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 800;
    box-shadow: 5px 5px 0 #8ab6ff;
    transition: all 0.15s ease-in-out;
}

.stButton > button:hover {
    transform: translate(3px, 3px);
    box-shadow: 2px 2px 0 #8ab6ff;
    background: #fff59d;
    color: #245bd6;
    border-color: #2f6eea;
}

/* 하단 카드 영역 */
.card-wrap {
    max-width: 760px;
    margin: 24px auto 0 auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}

.mini-card {
    background: #f7fbff;
    border: 3px solid #2f6eea;
    border-radius: 18px;
    padding: 16px 10px;
    box-shadow: 4px 4px 0 #c7e2ff;
    color: #31528f;
    font-size: 18px;
    font-weight: 700;
    text-align: center;
}

.mini-card-icon {
    font-size: 30px;
    margin-bottom: 6px;
}

.footer-text {
    max-width: 760px;
    margin: 22px auto 0 auto;
    text-align: center;
    font-size: 15px;
    font-weight: 700;
    color: #6a87bd;
    letter-spacing: 1px;
}

/* 모바일 대응 */
@media (max-width: 640px) {
    .pixel-title {
        font-size: 48px;
    }

    .desc-box {
        font-size: 10px;
    }

    .card-wrap {
        grid-template-columns: 1fr;
    }
}
</style>
""")

# 메인 페이지
st.html("""
<div class="main-box">
    <div class="star one">★</div>
    <div class="star two">✦</div>
    <div class="star three">✧</div>
    <div class="star four">★</div>

    <div class="content">
        <div class="sub-label">TAKE-OUT CAFE TEST</div>

        <div class="pixel-title">
            레쭈고!<br>
            카페!
        </div>

        <div class="icon-row">☕ 🧊</div>

        <div class="desc-box">
            쉬는 시간 안에 다녀올 수 있는<br>
            <b>학원 근처 테이크아웃 카페</b>를 추천해드려요!<br>
            거리, 가격, 영업 여부를 기준으로<br>
            나에게 맞는 카페 타입을 찾아보세요!
        </div>
    </div>
</div>
""")

# 시작 버튼
start = st.button("PRESS START BUTTON")

if start:
    st.session_state["page"] = "test"
    st.success("유형 테스트를 시작합니다!")

# 하단 기능 카드
st.html("""
<div class="card-wrap">
    <div class="mini-card">
        <div class="mini-card-icon">🚶‍♀️</div>
        가까운 거리
    </div>

    <div class="mini-card">
        <div class="mini-card-icon">💸</div>
        합리적 가격
    </div>

    <div class="mini-card">
        <div class="mini-card-icon">🕒</div>
        영업 여부
    </div>
</div>

<div class="footer-text">
    MEGA IT ACADEMY CAFE DASHBOARD PROJECT
</div>
""")