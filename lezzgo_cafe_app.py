# -*- coding: utf-8 -*-
"""
레쭈고! 카페! — 카페 유형 테스트 메인 페이지 (Streamlit)
실행:  streamlit run lezzgo_cafe_app.py
필요:  pip install streamlit
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="레쭈고! 카페!", page_icon="☕", layout="centered")

# ──────────────────────────────────────────────────────────────
# 전역 스타일: Streamlit 기본 UI 숨기고 화면 전체를 어둡게
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility:hidden;}
      .stApp { background:#0a0710; }
      .block-container { padding:0 !important; max-width:560px !important; }
      iframe { border:none !important; }
      /* (선택) 네이티브 버튼 폴백용 스타일 — 아래 폴백 버튼 쓸 때 적용됨 */
      div.stButton > button {
        font-family:monospace; font-size:18px; color:#0c0810;
        background:#f6efe2; border:none; border-radius:6px; padding:12px 28px;
        box-shadow:0 5px 0 #cf4a82, 0 6px 0 #0c0810;
      }
      div.stButton > button:hover { background:#fff; color:#0c0810; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
# 라우팅: 임베드된 시작 버튼이 ?start=1 로 넘어오면 quiz 페이지로 전환
# ──────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "intro"

if st.query_params.get("start") == "1":
    st.session_state.page = "quiz"
    st.query_params.clear()
if st.query_params.get("home") == "1":
    st.session_state.page = "intro"
    st.query_params.clear()

# ──────────────────────────────────────────────────────────────
# 메인(부팅) 화면 HTML — 디자인 원본을 그대로 임베드
# ──────────────────────────────────────────────────────────────
BOOT_HTML = """
<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  @import url('https://cdn.jsdelivr.net/gh/quiple/galmuri@latest/dist/galmuri.css');
  :root{
    --room:#0a0710; --device-1:#2a2030; --device-2:#15101d; --device-edge:#3a2e44;
    --screen:#170d1d; --screen-2:#1f1226; --ink:#f6efe2; --pink:#ff6fa5;
    --pink-soft:#ffa9cd; --pink-deep:#cf4a82; --black:#0c0810; --line:rgba(255,111,165,.22);
  }
  *{box-sizing:border-box;}
  html,body{height:100%;}
  body{
    margin:0; min-height:100%; display:grid; place-items:center; padding:20px 14px;
    background:radial-gradient(120% 90% at 50% 0%, #1a0f22 0%, var(--room) 60%), var(--room);
    font-family:'Galmuri11','DungGeunMo',monospace; color:var(--ink);
    -webkit-font-smoothing:none; overflow:hidden;
  }
  body::before{
    content:""; position:fixed; inset:0; z-index:0; pointer-events:none;
    background-image:radial-gradient(var(--line) 1px, transparent 1.4px);
    background-size:22px 22px; opacity:.5;
    mask:radial-gradient(80% 70% at 50% 45%, #000 30%, transparent 90%);
  }
  .device{
    position:relative; z-index:1; width:min(520px,100%); padding:18px 18px 14px;
    border-radius:26px 26px 30px 30px;
    background:linear-gradient(160deg,var(--device-1),var(--device-2));
    border:2px solid var(--device-edge);
    box-shadow:0 2px 0 rgba(255,255,255,.06) inset,0 -10px 24px rgba(0,0,0,.5) inset,
      0 24px 60px rgba(0,0,0,.7),0 0 0 6px #0c0812;
    animation:bootUp .5s ease-out both;
  }
  @keyframes bootUp{from{transform:translateY(10px) scale(.985);opacity:0;}to{transform:none;opacity:1;}}
  .screw{position:absolute;width:7px;height:7px;border-radius:50%;
    background:radial-gradient(circle at 35% 30%,#5a4c66,#1b1422);box-shadow:0 1px 1px #000;}
  .screw.tl{top:9px;left:9px;} .screw.tr{top:9px;right:9px;}
  .screen{
    position:relative; border-radius:14px; padding:22px 18px 26px;
    background:radial-gradient(130% 120% at 50% -10%,var(--screen-2),var(--screen) 70%);
    border:2px solid #0a0610; box-shadow:0 0 0 4px #0e0914,0 8px 20px rgba(0,0,0,.6) inset;
    overflow:hidden; min-height:420px; display:flex; flex-direction:column;
    animation:power .6s ease-out both;
  }
  @keyframes power{
    0%{filter:brightness(3) saturate(0);transform:scaleY(.004);}
    35%{transform:scaleY(.004);}36%{filter:brightness(2.4);}
    70%{transform:scaleY(1);}100%{filter:none;transform:scaleY(1);}
  }
  .screen::after{
    content:""; position:absolute; inset:0; z-index:5; pointer-events:none;
    background:repeating-linear-gradient(to bottom,rgba(0,0,0,.16) 0 1px,transparent 1px 3px),
      radial-gradient(120% 120% at 50% 50%,transparent 58%,rgba(0,0,0,.55) 100%);
    mix-blend-mode:multiply; animation:flick 5s steps(60) infinite;
  }
  @keyframes flick{0%,97%{opacity:1;}98%{opacity:.86;}100%{opacity:1;}}
  .hud{
    position:relative; z-index:4; display:flex; justify-content:space-between; align-items:center;
    font-family:'Galmuri9',monospace; font-size:12px; letter-spacing:.5px; color:var(--pink-soft);
  }
  .hud .stage{color:var(--ink);opacity:.7;}
  .hud .life i{color:var(--pink);margin-left:1px;font-style:normal;animation:beat 1.4s ease-in-out infinite;}
  .hud .life i:nth-child(2){animation-delay:.18s;} .hud .life i:nth-child(3){animation-delay:.36s;}
  @keyframes beat{0%,100%{transform:scale(1);}40%{transform:scale(1.25);}}
  .stage-wrap{
    position:relative; z-index:4; flex:1; display:flex; flex-direction:column;
    align-items:center; justify-content:center; text-align:center; padding:6px 0 0;
  }
  .eyebrow{
    font-family:'Galmuri9',monospace; font-size:12px; color:var(--pink-soft);
    letter-spacing:1px; margin-bottom:22px;
  }
  .title-wrap{position:relative;padding:8px 6px 4px;}
  .blob{
    position:absolute; z-index:-1; inset:-14px -10px -18px -10px; background:var(--pink);
    border-radius:46% 54% 50% 50% / 54% 50% 50% 46%; transform:rotate(-2deg);
    box-shadow:0 0 0 4px var(--pink-deep);
  }
  .blob::after{
    content:""; position:absolute; inset:0; border-radius:inherit;
    background-image:radial-gradient(var(--pink-soft) 1.5px,transparent 1.6px);
    background-size:11px 11px; opacity:.45;
  }
  h1{
    margin:0; color:var(--ink); font-family:'Galmuri11','DungGeunMo',monospace; font-weight:700;
    font-size:clamp(44px,13vw,68px); line-height:1.08; letter-spacing:1px;
    text-shadow:0 3px 0 var(--pink-deep),3px 3px 0 var(--pink-deep),4px 6px 0 var(--black);
  }
  .intro{
    margin:30px auto 4px; max-width:300px; font-family:'Galmuri11',monospace;
    font-size:14px; line-height:2.0; color:#efe7da;
  }
  .intro b{color:var(--pink-soft);font-weight:400;}
  .start{
    margin-top:26px; font-family:'Galmuri11',monospace; font-size:18px; color:var(--black);
    background:var(--ink); border:none; border-radius:6px; padding:14px 30px; cursor:pointer;
    box-shadow:0 5px 0 var(--pink-deep),0 6px 0 var(--black);
    transition:transform .06s ease,box-shadow .06s ease;
  }
  .start:hover{background:#fff;}
  .start:active,.start.pressed{transform:translateY(5px);box-shadow:0 0 0 var(--pink-deep),0 1px 0 var(--black);}
  .start:focus-visible{outline:3px solid var(--pink);outline-offset:3px;}
  .press{
    margin-top:14px; font-family:'Galmuri9',monospace; font-size:13px; letter-spacing:3px;
    color:var(--pink); animation:blink 1.05s steps(1) infinite;
  }
  @keyframes blink{50%{opacity:0;}}
  .sprite{position:absolute;z-index:3;pointer-events:none;}
  .cat{width:34px;height:28px;color:var(--ink);filter:drop-shadow(2px 2px 0 var(--black));}
  .cat.a{top:64px;left:18px;animation:bobA 3.4s ease-in-out infinite;}
  .cat.b{bottom:78px;right:20px;transform:scaleX(-1);animation:bobB 3.9s ease-in-out infinite;}
  .star{width:18px;height:18px;}
  .star.s1{top:70px;right:30px;color:var(--pink-soft);animation:tw 2.2s steps(2) infinite;}
  .star.s2{top:120px;left:42px;color:var(--ink);width:13px;height:13px;animation:tw 2.8s steps(2) infinite .4s;}
  .star.s3{bottom:120px;left:26px;color:var(--pink);animation:tw 2.5s steps(2) infinite .9s;}
  .star.s4{bottom:150px;right:46px;color:var(--pink-soft);width:12px;height:12px;animation:tw 3.1s steps(2) infinite .2s;}
  @keyframes bobA{0%,100%{transform:translateY(0);}50%{transform:translateY(-7px);}}
  @keyframes bobB{0%,100%{transform:scaleX(-1) translateY(0);}50%{transform:scaleX(-1) translateY(-7px);}}
  @keyframes tw{0%,100%{opacity:.35;transform:scale(.8);}50%{opacity:1;transform:scale(1);}}
  .deck{
    display:flex; align-items:center; gap:10px; padding:12px 8px 2px;
    font-family:'Galmuri9',monospace; font-size:11px; color:#8d7e98; letter-spacing:.5px;
  }
  .led{width:9px;height:9px;border-radius:50%;background:var(--pink);
    box-shadow:0 0 8px var(--pink);animation:beat 1.6s ease-in-out infinite;}
  .deck .brand{flex:1;}
  .deck .speaker{display:flex;gap:3px;}
  .deck .speaker i{width:3px;height:11px;border-radius:2px;background:#2c2236;}
  @media (max-width:430px){
    .screen{min-height:380px;padding:18px 12px 22px;}
    .cat.a{left:8px;} .cat.b{right:8px;} .intro{max-width:240px;}
  }
  @media (prefers-reduced-motion:reduce){ *{animation:none !important;} .press{opacity:1;} }
</style></head><body>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true">
    <symbol id="cat" viewBox="0 0 11 9" shape-rendering="crispEdges">
      <g fill="currentColor">
        <rect x="1" y="0" width="2" height="1"/><rect x="8" y="0" width="2" height="1"/>
        <rect x="1" y="1" width="3" height="1"/><rect x="7" y="1" width="3" height="1"/>
        <rect x="1" y="2" width="9" height="5"/><rect x="2" y="7" width="7" height="1"/>
      </g>
      <g fill="#170d1d"><rect x="3" y="4" width="1" height="2"/><rect x="7" y="4" width="1" height="2"/></g>
      <g fill="#ff6fa5"><rect x="5" y="5" width="1" height="1"/></g>
    </symbol>
    <symbol id="star" viewBox="0 0 7 7" shape-rendering="crispEdges">
      <g fill="currentColor">
        <rect x="3" y="0" width="1" height="7"/><rect x="0" y="3" width="7" height="1"/>
        <rect x="2" y="1" width="1" height="1"/><rect x="4" y="1" width="1" height="1"/>
        <rect x="1" y="2" width="1" height="1"/><rect x="5" y="2" width="1" height="1"/>
        <rect x="1" y="4" width="1" height="1"/><rect x="5" y="4" width="1" height="1"/>
        <rect x="2" y="5" width="1" height="1"/><rect x="4" y="5" width="1" height="1"/>
      </g>
    </symbol>
  </svg>
  <main class="device">
    <span class="screw tl"></span><span class="screw tr"></span>
    <section class="screen">
      <div class="hud">
        <span class="stage">STAGE 1 · CAFE TEST</span>
        <span class="life">LIFE <i>♥</i><i>♥</i><i>♥</i></span>
      </div>
      <svg class="sprite cat a"><use href="#cat"/></svg>
      <svg class="sprite cat b"><use href="#cat"/></svg>
      <svg class="sprite star s1"><use href="#star"/></svg>
      <svg class="sprite star s2"><use href="#star"/></svg>
      <svg class="sprite star s3"><use href="#star"/></svg>
      <svg class="sprite star s4"><use href="#star"/></svg>
      <div class="stage-wrap">
        <div class="eyebrow">☕ 쉬는시간 카페 유형 테스트</div>
        <div class="title-wrap">
          <div class="blob"></div>
          <h1>레쭈고!<br>카페!</h1>
        </div>
        <p class="intro">
          쉬는 시간 10분, 학원 앞에서 뭐 마시지?<br>
          <b>5가지 질문</b>으로 찾는<br>나의 테이크아웃 카페 취향 유형!
        </p>
        <button class="start" id="start" aria-label="카페 유형 테스트 시작하기">▶ 시작하기</button>
        <div class="press" aria-hidden="true">PRESS&nbsp;START</div>
      </div>
    </section>
    <div class="deck">
      <span class="led"></span>
      <span class="brand">i(3)&nbsp;—&nbsp;김남희 전선우 한예림</span>
      <span class="speaker"><i></i><i></i><i></i><i></i></span>
    </div>
  </main>
  <script>
    // 시작 버튼: 화면 깜빡(부팅) 연출 후 Streamlit으로 ?start=1 전달 → 다음 페이지
    const btn = document.getElementById('start');
    const screen = document.querySelector('.screen');
    btn.addEventListener('click', () => {
      btn.classList.add('pressed');
      screen.animate(
        [{filter:'brightness(1)'},{filter:'brightness(2.2)'},{filter:'brightness(1)'}],
        {duration:240, easing:'steps(3)'}
      );
      setTimeout(() => {
        try {
          const base = window.parent.location.pathname;
          window.parent.location.href = base + '?start=1';
        } catch (e) {
          window.top.location.href = '?start=1';
        }
      }, 230);
    });
  </script>
</body></html>
"""

# ──────────────────────────────────────────────────────────────
# 페이지 렌더링
# ──────────────────────────────────────────────────────────────
if st.session_state.page == "intro":
    components.html(BOOT_HTML, height=760, scrolling=False)

    # ── (폴백) 임베드 버튼이 동작하지 않는 환경이면 아래 주석을 해제해서 사용 ──
    # if st.button("▶ 시작하기"):
    #     st.session_state.page = "quiz"
    #     st.rerun()

else:  # quiz 페이지(예시 자리) — 여기에 첫 번째 질문 화면을 이어 붙이면 됩니다
    st.markdown(
        """
        <div style="text-align:center;font-family:monospace;color:#f6efe2;padding:60px 12px;">
          <div style="color:#ffa9cd;letter-spacing:2px;">STAGE 2 · QUESTION 1</div>
          <h2 style="color:#ff6fa5;margin:14px 0;">첫 번째 질문이 들어갈 자리예요!</h2>
          <p style="color:#efe7da;">여기에 카페 유형 테스트 1번 문항을 구현하면 됩니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("← 처음으로"):
        st.session_state.page = "intro"
        st.rerun()