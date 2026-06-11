# -*- coding: utf-8 -*-
"""
레쭈고! 카페! — 카페 유형 테스트 (Streamlit)
  인트로 → 3문항 테스트 → 8유형 중 하나 결과 + 추천 카페
실행:  streamlit run lezzgo_cafe_app.py
필요:  pip install streamlit
DB:    레쭈고카페_결과그룹.xlsx 기반 (데이터는 본 파일에 내장됨)
"""

import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="레쭈고! 카페!", page_icon="☕", layout="centered")

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
    position:relative; z-index:4; margin-bottom:34px;
    display:flex; justify-content:space-between; align-items:center;
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
    letter-spacing:1px; margin-bottom:34px;
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
    margin:46px auto 4px; max-width:300px; font-family:'Galmuri11',monospace;
    font-size:14px; line-height:1.95; color:#efe7da;
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
          <b>3가지 질문</b>으로 찾는<br>나의 테이크아웃 카페 취향 유형!
        </p>
        <button class="start" id="start" aria-label="카페 유형 테스트 시작하기">▶ 시작하기</button>
        <div class="press" aria-hidden="true">PRESS&nbsp;START</div>
      </div>
    </section>
    <div class="deck">
      <span class="led"></span>
      <span class="brand">LEZZGO CAFE&nbsp;—&nbsp;POCKET ED.</span>
      <span class="speaker"><i></i><i></i><i></i><i></i></span>
    </div>
  </main>
  <script>
    // 화면 속 '시작하기' → 부팅 깜빡임 후, 부모 페이지의 네이티브 '시작하기' 버튼을 대신 클릭.
    // (iframe→부모 URL 이동은 차단되지만, 같은 출처라 부모 버튼 클릭은 허용됨)
    const btn = document.getElementById('start');
    const screen = document.querySelector('.screen');
    if (btn) btn.addEventListener('click', () => {
      btn.classList.add('pressed');
      screen.animate(
        [{filter:'brightness(1)'},{filter:'brightness(2.2)'},{filter:'brightness(1)'}],
        {duration:240, easing:'steps(3)'}
      );
      setTimeout(() => {
        try {
          const list = window.parent.document.querySelectorAll('button');
          for (const b of list) {
            if (b.innerText && b.innerText.indexOf('시작하기') !== -1) { b.click(); break; }
          }
        } catch (e) {}
        setTimeout(() => btn.classList.remove('pressed'), 150);
      }, 230);
    });
  </script>
</body></html>
"""

# ──────────────────────────────────────────────────────────────
# 결과 그룹 DB (엑셀에서 추출해 내장)
# ──────────────────────────────────────────────────────────────
GROUPS = {int(k): v for k, v in json.loads(r"""{
  "1": {
    "time": "근거리",
    "time_label": "근거리 (<3분)",
    "caffeine": "일반",
    "price": "평균↓",
    "name": "⚡ 번개 가성비러",
    "concept": "코앞에서 싸게 빠르게! 쉬는 시간 최적화",
    "count": 9
  },
  "2": {
    "time": "근거리",
    "time_label": "근거리 (<3분)",
    "caffeine": "일반",
    "price": "평균↑",
    "name": "💎 럭키 단골러",
    "concept": "가까운 곳에서 제값 주고 확실한 한 잔",
    "count": 5
  },
  "3": {
    "time": "근거리",
    "time_label": "근거리 (<3분)",
    "caffeine": "디카페인",
    "price": "평균↓",
    "name": "🌙 노카페인 알뜰러",
    "concept": "카페인 빼고 가성비까지 챙기는 똑똑이",
    "count": 8
  },
  "4": {
    "time": "근거리",
    "time_label": "근거리 (<3분)",
    "caffeine": "디카페인",
    "price": "평균↑",
    "name": "✨ 건강 프리미엄러",
    "concept": "몸도 챙기고 분위기도 챙기는 프리미엄파",
    "count": 4
  },
  "5": {
    "time": "중거리",
    "time_label": "중거리 (3~5분)",
    "caffeine": "일반",
    "price": "평균↓",
    "name": "🏃 산책 절약러",
    "concept": "조금 걸어도 OK, 지갑은 가볍게",
    "count": 4
  },
  "6": {
    "time": "중거리",
    "time_label": "중거리 (3~5분)",
    "caffeine": "일반",
    "price": "평균↑",
    "name": "👑 소확행 탐험러",
    "concept": "멀어도 가치 있는 한 잔을 찾아 떠나는 미식러",
    "count": 5
  },
  "7": {
    "time": "중거리",
    "time_label": "중거리 (3~5분)",
    "caffeine": "디카페인",
    "price": "평균↓",
    "name": "🍃 느긋 웰빙러",
    "concept": "여유롭게 걸어가 부담 없이 디카페인 한 잔",
    "count": 3
  },
  "8": {
    "time": "중거리",
    "time_label": "중거리 (3~5분)",
    "caffeine": "디카페인",
    "price": "평균↑",
    "name": "🎩 프리미엄 힐링러",
    "concept": "시간도 돈도 투자하는 진정한 힐링 추구파",
    "count": 4
  }
}""").items()}
CAFES  = {int(k): v for k, v in json.loads(r"""{
  "1": [
    {
      "name": "바나프레소 강남역사거리점",
      "dist": "2분",
      "m": 91,
      "americano": 2500,
      "decaf": 3500,
      "hours": "매일 07:00 - 22:00 (21:30 라스트오더)",
      "link": "https://map.naver.com/p/entry/place/1257979297?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111332&locale=ko&svcName=map_pcv5",
      "review": "앱으로 미리 띡, 도착하면 아아 바로 픽 📱"
    },
    {
      "name": "CAFE EXPRESS 커피점",
      "dist": "2분",
      "m": 92,
      "americano": 2200,
      "decaf": 2700,
      "hours": "월~금 07:30 - 19:30 / 토 07:30 - 17:30 / 일 휴무",
      "link": "https://map.naver.com/p/search/CAFE%20EXPRESS%20%EC%BB%A4%ED%94%BC%EC%A0%90/place/1904442520?c=14.43,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111330&locale=ko&svcName=map_pcv5&searchText=CAFE%20EXPRESS%20%EC%BB%A4%ED%94%BC%EC%A0%90",
      "review": "테이크아웃 특화 가성비갑👍"
    },
    {
      "name": "커피나인 강남역2호점",
      "dist": "1분",
      "m": 97,
      "americano": 2900,
      "decaf": null,
      "hours": "매일 07:00 - 17:30 (17:00 라스트오더)",
      "link": "https://map.naver.com/p/search/%EC%BB%A4%ED%94%BC%EB%82%98%EC%9D%B8%20%EA%B0%95%EB%82%A8%EC%97%AD2%ED%98%B8%EC%A0%90/place/1662841464?c=15.00,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111330&locale=ko&svcName=map_pcv5&searchText=%EC%BB%A4%ED%94%BC%EB%82%98%EC%9D%B8%20%EA%B0%95%EB%82%A8%EC%97%AD2%ED%98%B8%EC%A0%90",
      "review": "블루리본 증명 맛잘알 커피 😎"
    },
    {
      "name": "메이크커피",
      "dist": "2분",
      "m": 146,
      "americano": 1400,
      "decaf": 3000,
      "hours": "월~금 06:50 - 18:00 (17:00 라스트오더) 토 08:30 - 15:00 (14:30 라스트오더) [일]",
      "link": "https://map.naver.com/p/entry/place/38555447?c=16.36,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111331&locale=ko&svcName=map_pcv5",
      "review": "아아계의 최저가 도전자, 부담 제로 💸"
    },
    {
      "name": "우지커피 강남역사점",
      "dist": "2분",
      "m": 146,
      "americano": 2000,
      "decaf": 3000,
      "hours": "월화수목금 07:00~21:30 토 08:00~21:30 일 08:00~19:30",
      "link": "https://map.naver.com/p/entry/place/2034836637?c=16.36,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111331&locale=ko&svcName=map_pcv5",
      "review": "싸고 큰 아아, 그게 다임 (칭찬)"
    },
    {
      "name": "카페16온스 강남역점",
      "dist": "2분",
      "m": 146,
      "americano": 1200,
      "decaf": 3000,
      "hours": "월화수목금 06:30~20:00 토일 11:00~19:00",
      "link": "https://map.naver.com/p/search/%EC%B9%B4%ED%8E%9816%EC%98%A8%EC%8A%A4%20%EA%B0%95%EB%82%A8%EC%97%AD%EC%A0%90/place/1428932952?c=15.00,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111332&locale=ko&svcName=map_pcv5&searchText=%EC%B9%B4%ED%8E%9816%EC%98%A8%EC%8A%A4%20%EA%B0%95%EB%82%A8%EC%97%AD%EC%A0%90",
      "review": "진하고 큰데 천원대?? 미친 가성비"
    },
    {
      "name": "매머드익스프레스 국기원점",
      "dist": "2분",
      "m": 146,
      "americano": 1600,
      "decaf": 2300,
      "hours": "매일 06:45 - 19:30 (19:00 라스트오더)",
      "link": "https://map.naver.com/p/entry/place/1976721879?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111332&locale=ko&svcName=map_pcv5",
      "review": "천원대 아아의 끝판왕, 가격이 곧 맛 ⚡"
    },
    {
      "name": "메가MGC커피 강남역지하도점",
      "dist": "2분",
      "m": 146,
      "americano": 1800,
      "decaf": 3000,
      "hours": "매일 07:00 - 22:00",
      "link": "https://map.naver.com/p/search/%EB%A9%94%EA%B0%80MGC%EC%BB%A4%ED%94%BC%20%EA%B0%95%EB%82%A8%EC%97%AD%EC%A7%80%ED%95%98%EB%8F%84%EC%A0%90/place/1244338137?c=15.59,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111333&locale=ko&svcName=map_pcv5&searchText=%EB%A9%94%EA%B0%80MGC%EC%BB%A4%ED%94%BC%20%EA%B0%95%EB%82%A8%EC%97%AD%EC%A7%80%ED%95%98%EB%8F%84%EC%A0%90",
      "review": "2천원에 만수르 용량, 출근길 국룰 👑"
    },
    {
      "name": "커피노운",
      "dist": "2분",
      "m": 154,
      "americano": 1500,
      "decaf": 2800,
      "hours": "데이터 없음",
      "link": "https://map.naver.com/p/search/%EC%BB%A4%ED%94%BC%EB%85%B8%EC%9A%B4/place/1507298682?c=15.00,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111332&locale=ko&svcName=map_pcv5&searchText=%EC%BB%A4%ED%94%BC%EB%85%B8%EC%9A%B4",
      "review": "옆집보다 100원 싼 아아 맛집✌"
    }
  ],
  "2": [
    {
      "name": "투썸플레이스 강남역중앙점",
      "dist": "1분 미만",
      "m": 0,
      "americano": 4700,
      "decaf": 5200,
      "hours": "매일 08:00 - 22:30",
      "link": "https://map.naver.com/p/entry/place/1097707797?c=15.59,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111333&locale=ko&svcName=map_pcv5",
      "review": "아아는 거들 뿐, 케이크가 메인 🍰"
    },
    {
      "name": "스타벅스 케이스퀘어강남점",
      "dist": "1분",
      "m": 36,
      "americano": 4700,
      "decaf": 5000,
      "hours": "매일 07:00 - 22:00",
      "link": "https://map.naver.com/p/entry/place/1140751329?c=15.59,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111333&locale=ko&svcName=map_pcv5",
      "review": "말이 필요없는 근-본"
    },
    {
      "name": "소과당 강남본점",
      "dist": "1분",
      "m": 74,
      "americano": 5000,
      "decaf": 6000,
      "hours": "매일 11:00 - 22:00 (라스트오더 21:30)",
      "link": "https://map.naver.com/p/search/%EC%86%8C%EA%B3%BC%EB%8B%B9%20%EA%B0%95%EB%82%A8%EB%B3%B8%EC%A0%90/place/1689410898?c=15.00,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111333&locale=ko&svcName=map_pcv5&searchText=%EC%86%8C%EA%B3%BC%EB%8B%B9%20%EA%B0%95%EB%82%A8%EB%B3%B8%EC%A0%90",
      "review": "아아는 거들뿐.(디저트가 본체) 🎁"
    },
    {
      "name": "백미당 강남역점",
      "dist": "1분",
      "m": 117,
      "americano": 4900,
      "decaf": null,
      "hours": "매일 11:00 - 23:00 (22:30 라스트오더)",
      "link": "https://map.naver.com/p/entry/place/2021582710?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111334&locale=ko&svcName=map_pcv5",
      "review": "사실..아아보단 디저트 페어링용 🍦"
    },
    {
      "name": "할리스 강남역점",
      "dist": "1분",
      "m": 117,
      "americano": 4700,
      "decaf": 4900,
      "hours": "월 07:30 - 23:30 화~목 07:30 - 24:00 금~토 07:30 - 다음 날 00:30 일 08:00 - 23:30",
      "link": "https://map.naver.com/p/entry/place/1052747813?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111334&locale=ko&svcName=map_pcv5",
      "review": "카공족특화 콘센트 부잣집 🔌 가성비가 살짝아쉬운 테이크아웃"
    }
  ],
  "3": [
    {
      "name": "바나프레소 강남역사거리점",
      "dist": "2분",
      "m": 91,
      "americano": 2500,
      "decaf": 3500,
      "hours": "매일 07:00 - 22:00 (21:30 라스트오더)",
      "link": "https://map.naver.com/p/entry/place/1257979297?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111335&locale=ko&svcName=map_pcv5",
      "review": "앱으로 미리 띡, 도착하면 아아 바로 픽 📱"
    },
    {
      "name": "CAFE EXPRESS 커피점",
      "dist": "2분",
      "m": 92,
      "americano": 2200,
      "decaf": 2700,
      "hours": "월~금 07:30 - 19:30 / 토 07:30 - 17:30 / 일 휴무",
      "link": "https://map.naver.com/p/entry/place/1904442520?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111334&locale=ko&svcName=map_pcv5",
      "review": "테이크아웃 특화 가성비갑👍"
    },
    {
      "name": "메이크커피",
      "dist": "2분",
      "m": 146,
      "americano": 1400,
      "decaf": 3000,
      "hours": "월~금 06:50 - 18:00 (17:00 라스트오더) 토 08:30 - 15:00 (14:30 라스트오더) [일]",
      "link": "https://map.naver.com/p/entry/place/38555447?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111335&locale=ko&svcName=map_pcv5",
      "review": "아아계의 최저가 도전자, 부담 제로 💸"
    },
    {
      "name": "우지커피 강남역사점",
      "dist": "2분",
      "m": 146,
      "americano": 2000,
      "decaf": 3000,
      "hours": "월화수목금 07:00~21:30 토 08:00~21:30 일 08:00~19:30",
      "link": "https://map.naver.com/p/entry/place/2034836637?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111335&locale=ko&svcName=map_pcv5",
      "review": "싸고 큰 아아, 그게 다임 (칭찬)"
    },
    {
      "name": "카페16온스 강남역점",
      "dist": "2분",
      "m": 146,
      "americano": 1200,
      "decaf": 3000,
      "hours": "월화수목금 06:30~20:00 토일 11:00~19:00",
      "link": "https://map.naver.com/p/entry/place/1428932952?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111335&locale=ko&svcName=map_pcv5",
      "review": "진하고 큰데 천원대?? 미친 가성비"
    },
    {
      "name": "매머드익스프레스 국기원점",
      "dist": "2분",
      "m": 146,
      "americano": 1600,
      "decaf": 2300,
      "hours": "매일 06:45 - 19:30 (19:00 라스트오더)",
      "link": "https://map.naver.com/p/entry/place/1976721879?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111332&locale=ko&svcName=map_pcv5",
      "review": "천원대 아아의 끝판왕, 가격이 곧 맛 ⚡"
    },
    {
      "name": "메가MGC커피 강남역지하도점",
      "dist": "2분",
      "m": 146,
      "americano": 1800,
      "decaf": 3000,
      "hours": "매일 07:00 - 22:00",
      "link": "https://map.naver.com/p/search/%EB%A9%94%EA%B0%80MGC%EC%BB%A4%ED%94%BC%20%EA%B0%95%EB%82%A8%EC%97%AD%EC%A7%80%ED%95%98%EB%8F%84%EC%A0%90/place/1244338137?c=15.59,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111333&locale=ko&svcName=map_pcv5&searchText=%EB%A9%94%EA%B0%80MGC%EC%BB%A4%ED%94%BC%20%EA%B0%95%EB%82%A8%EC%97%AD%EC%A7%80%ED%95%98%EB%8F%84%EC%A0%90",
      "review": "2천원에 만수르 용량, 출근길 국룰 👑"
    },
    {
      "name": "커피노운",
      "dist": "2분",
      "m": 154,
      "americano": 1500,
      "decaf": 2800,
      "hours": "데이터 없음",
      "link": "https://map.naver.com/p/search/%EC%BB%A4%ED%94%BC%EB%85%B8%EC%9A%B4/place/1507298682?c=15.00,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111332&locale=ko&svcName=map_pcv5&searchText=%EC%BB%A4%ED%94%BC%EB%85%B8%EC%9A%B4",
      "review": "옆집보다 100원 싼 아아 맛집✌"
    }
  ],
  "4": [
    {
      "name": "투썸플레이스 강남역중앙점",
      "dist": "1분 미만",
      "m": 0,
      "americano": 4700,
      "decaf": 5200,
      "hours": "매일 08:00 - 22:30",
      "link": "https://map.naver.com/p/entry/place/1097707797?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111337&locale=ko&svcName=map_pcv5",
      "review": "아아는 거들 뿐, 케이크가 메인 🍰"
    },
    {
      "name": "스타벅스 케이스퀘어강남점",
      "dist": "1분",
      "m": 36,
      "americano": 4700,
      "decaf": 5000,
      "hours": "매일 07:00 - 22:00",
      "link": "https://map.naver.com/p/entry/place/1140751329?c=15.59,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111333&locale=ko&svcName=map_pcv5",
      "review": "말이 필요없는 근-본"
    },
    {
      "name": "소과당 강남본점",
      "dist": "1분",
      "m": 74,
      "americano": 5000,
      "decaf": 6000,
      "hours": "매일 11:00 - 22:00 (라스트오더 21:30)",
      "link": "https://map.naver.com/p/search/%EC%86%8C%EA%B3%BC%EB%8B%B9%20%EA%B0%95%EB%82%A8%EB%B3%B8%EC%A0%90/place/1689410898?c=15.00,0,0,0,dh&isCorrectAnswer=true&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111333&locale=ko&svcName=map_pcv5&searchText=%EC%86%8C%EA%B3%BC%EB%8B%B9%20%EA%B0%95%EB%82%A8%EB%B3%B8%EC%A0%90",
      "review": "아아는 거들뿐.(디저트가 본체) 🎁"
    },
    {
      "name": "할리스 강남역점",
      "dist": "1분",
      "m": 117,
      "americano": 4700,
      "decaf": 4900,
      "hours": "월 07:30 - 23:30 화~목 07:30 - 24:00 금~토 07:30 - 다음 날 00:30 일 08:00 - 23:30",
      "link": "https://map.naver.com/p/entry/place/1052747813?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111334&locale=ko&svcName=map_pcv5",
      "review": "카공족특화 콘센트 부잣집 🔌 가성비가 살짝아쉬운 테이크아웃"
    }
  ],
  "5": [
    {
      "name": "돌핀커피",
      "dist": "4분",
      "m": 128,
      "americano": 1500,
      "decaf": 3500,
      "hours": "월화수목금 06:30~17:00 토 07:00~15:00 일 08:00~15:00",
      "link": "https://map.naver.com/p/entry/place/1871112069?c=15.15,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111338&locale=ko&svcName=map_pcv5",
      "review": "커여운 디자인의 대용량 아메리카노🐬"
    },
    {
      "name": "컴포즈커피 강남역사점",
      "dist": "5분",
      "m": 165,
      "americano": 1500,
      "decaf": 2800,
      "hours": "월화수목금 07:30~20:30 토일 08:00~20:00",
      "link": "https://map.naver.com/p/entry/place/702793647?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111338&locale=ko&svcName=map_pcv5",
      "review": "1,800원에 스페셜티 원두면 개이득"
    },
    {
      "name": "세컨드컵커피",
      "dist": "3분",
      "m": 174,
      "americano": 1200,
      "decaf": null,
      "hours": "매일 08:00 - 17:00 [일]",
      "link": "https://map.naver.com/p/entry/place/1125032142?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111337&locale=ko&svcName=map_pcv5",
      "review": "가성비 최고 빠른 모닝커피 한잔😉"
    },
    {
      "name": "바나프레소 강남역점",
      "dist": "3분",
      "m": 213,
      "americano": 2500,
      "decaf": 3500,
      "hours": "06:00~23:00(라스트오더 22:30)",
      "link": "https://map.naver.com/p/entry/place/1845028269?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111338&locale=ko&svcName=map_pcv5",
      "review": "앱으로 미리 띡, 도착하면 아아 바로 픽 📱"
    }
  ],
  "6": [
    {
      "name": "트리오드",
      "dist": "3분",
      "m": 150,
      "americano": 6300,
      "decaf": 7300,
      "hours": "매일 012:00 - 23:00 (22:00 라스트오더)",
      "link": "https://map.naver.com/p/entry/place/1285186695?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111339&locale=ko&svcName=map_pcv5",
      "review": "아아핑계로 케이크사러가는 집🍰"
    },
    {
      "name": "The november 라운지 강남역KG타워점",
      "dist": "3분",
      "m": 171,
      "americano": 6000,
      "decaf": 6500,
      "hours": "매일 00:00 - 24:00",
      "link": "https://map.naver.com/p/entry/place/1097569467?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111339&locale=ko&svcName=map_pcv5",
      "review": "분위기 깡패🛋, 테이크아웃하려다 눌러않을수도"
    },
    {
      "name": "Cafe BONO (보노)",
      "dist": "3분",
      "m": 174,
      "americano": 6000,
      "decaf": 9500,
      "hours": "매일 08:00 - 24:00",
      "link": "https://map.naver.com/p/entry/place/1123367577?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111338&locale=ko&svcName=map_pcv5",
      "review": "커피시키다가 브런치도 시킬수있음 주의🛑"
    },
    {
      "name": "커피빈 강남역12번출구점",
      "dist": "3분",
      "m": 209,
      "americano": 5300,
      "decaf": 5800,
      "hours": "월화수목금 06:30~22:00 토일 07:30~21:30",
      "link": "https://map.naver.com/p/entry/place/63444269?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111339&locale=ko&svcName=map_pcv5",
      "review": "제일 비싸지만 진하고 차분한 어른의 아아☕"
    },
    {
      "name": "공차 강남본점",
      "dist": "4분",
      "m": 277,
      "americano": 3900,
      "decaf": null,
      "hours": "월~토 07:00 - 22:00 일 11:00 - 21:00",
      "link": "https://map.naver.com/p/entry/place/1530672038?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111339&locale=ko&svcName=map_pcv5",
      "review": "**얼죽아인은 공차도 커피집이다**"
    }
  ],
  "7": [
    {
      "name": "돌핀커피",
      "dist": "4분",
      "m": 128,
      "americano": 1500,
      "decaf": 3500,
      "hours": "월화수목금 06:30~17:00 토 07:00~15:00 일 08:00~15:00",
      "link": "https://map.naver.com/p/entry/place/1871112069?c=15.15,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111338&locale=ko&svcName=map_pcv5",
      "review": "커여운 디자인의 대용량 아메리카노🐬"
    },
    {
      "name": "컴포즈커피 강남역사점",
      "dist": "5분",
      "m": 165,
      "americano": 1500,
      "decaf": 2800,
      "hours": "월화수목금 07:30~20:30 토일 08:00~20:00",
      "link": "https://map.naver.com/p/entry/place/702793647?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111339&locale=ko&svcName=map_pcv5",
      "review": "1,800원에 스페셜티 원두면 개이득"
    },
    {
      "name": "바나프레소 강남역점",
      "dist": "3분",
      "m": 213,
      "americano": 2500,
      "decaf": 3500,
      "hours": "06:00~23:00(라스트오더 22:30)",
      "link": "https://map.naver.com/p/entry/place/1845028269?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111339&locale=ko&svcName=map_pcv5",
      "review": "앱으로 미리 띡, 도착하면 아아 바로 픽 📱"
    }
  ],
  "8": [
    {
      "name": "트리오드",
      "dist": "3분",
      "m": 150,
      "americano": 6300,
      "decaf": 7300,
      "hours": "매일 012:00 - 23:00 (22:00 라스트오더)",
      "link": "https://map.naver.com/p/entry/place/1285186695?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111339&locale=ko&svcName=map_pcv5",
      "review": "아아핑계로 케이크사러가는 집🍰"
    },
    {
      "name": "The november 라운지 강남역KG타워점",
      "dist": "3분",
      "m": 171,
      "americano": 6000,
      "decaf": 6500,
      "hours": "매일 00:00 - 24:00",
      "link": "https://map.naver.com/p/entry/place/1097569467?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111339&locale=ko&svcName=map_pcv5",
      "review": "분위기 깡패🛋, 테이크아웃하려다 눌러않을수도"
    },
    {
      "name": "Cafe BONO (보노)",
      "dist": "3분",
      "m": 174,
      "americano": 6000,
      "decaf": 9500,
      "hours": "매일 08:00 - 24:00",
      "link": "https://map.naver.com/p/entry/place/1123367577?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111338&locale=ko&svcName=map_pcv5",
      "review": "커피시키다가 브런치도 시킬수있음 주의🛑"
    },
    {
      "name": "커피빈 강남역12번출구점",
      "dist": "3분",
      "m": 209,
      "americano": 5300,
      "decaf": 5800,
      "hours": "월화수목금 06:30~22:00 토일 07:30~21:30",
      "link": "https://map.naver.com/p/entry/place/63444269?c=15.00,0,0,0,dh&placePath=/home?from=map&fromPanelNum=1&additionalHeight=76&timestamp=202606111340&locale=ko&svcName=map_pcv5",
      "review": "제일 비싸지만 진하고 차분한 어른의 아아☕"
    }
  ]
}""").items()}

# ──────────────────────────────────────────────────────────────
# 전역 스타일 (픽셀폰트 · CRT · 핑크 버튼)
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
      @font-face{ font-family:'Galmuri11'; font-weight:400; font-display:swap;
        src:local('Galmuri11 Regular'),
            url('https://cdn.jsdelivr.net/gh/quiple/galmuri@latest/dist/Galmuri11.woff2') format('woff2'); }
      @font-face{ font-family:'Galmuri11'; font-weight:700; font-display:swap;
        src:local('Galmuri11 Bold'),
            url('https://cdn.jsdelivr.net/gh/quiple/galmuri@latest/dist/Galmuri11-Bold.woff2') format('woff2'); }
      @font-face{ font-family:'Galmuri9'; font-weight:400; font-display:swap;
        src:local('Galmuri9 Regular'),
            url('https://cdn.jsdelivr.net/gh/quiple/galmuri@latest/dist/Galmuri9.woff2') format('woff2'); }
      :root{
        --ink:#f6efe2; --pink:#ff6fa5; --pink-soft:#ffa9cd; --pink-deep:#cf4a82;
        --black:#0c0810; --screen:#170d1d; --line:rgba(255,111,165,.22);
      }
      #MainMenu, header, footer {visibility:hidden;}
      html, body, [class*="css"]{ font-family:'Galmuri11','DungGeunMo',monospace; }
      .stApp{ background:radial-gradient(130% 90% at 50% 0%, #1a0f22 0%, #0a0710 60%), #0a0710; }
      .stApp::after{
        content:""; position:fixed; inset:0; z-index:9999; pointer-events:none;
        background:repeating-linear-gradient(to bottom, rgba(0,0,0,.13) 0 1px, transparent 1px 3px),
                   radial-gradient(120% 120% at 50% 50%, transparent 60%, rgba(0,0,0,.5));
        mix-blend-mode:multiply;
      }
      .block-container{ max-width:560px !important; padding:24px 16px 64px !important; }
      iframe{ border:none !important; }

      div.stButton{ width:100% !important; text-align:center !important; }
      div[data-testid="column"], div[data-testid="stColumn"]{ text-align:center !important; }
      div.stButton > button{
        width:100% !important; max-width:380px; display:inline-block; margin:0 auto 14px;
        font-family:'Galmuri11','DungGeunMo',monospace; font-size:16px; color:var(--black);
        background:var(--ink); border:none; border-radius:8px; padding:17px 18px; text-align:center;
        box-shadow:0 5px 0 var(--pink-deep), 0 6px 0 var(--black);
        transition:transform .06s, box-shadow .06s; line-height:1.5;
      }
      div.stButton > button:hover{ background:#fff; color:var(--black); }
      div.stButton > button:active{ transform:translateY(5px); box-shadow:0 0 0 var(--pink-deep),0 1px 0 var(--black); }
      div.stButton > button:focus:not(:active){ color:var(--black); border:none; box-shadow:0 5px 0 var(--pink-deep),0 6px 0 var(--black); }
      /* '이전으로'(secondary) = 고스트 버튼 */
      div.stButton > button[kind="secondary"],
      div.stButton > button[data-testid="stBaseButton-secondary"]{
        font-size:13px; color:var(--pink-soft); background:rgba(255,111,165,.06);
        border:1px solid var(--line); padding:9px 16px; max-width:200px; box-shadow:none;
      }
      div.stButton > button[kind="secondary"]:hover,
      div.stButton > button[data-testid="stBaseButton-secondary"]:hover{
        background:rgba(255,111,165,.16); color:var(--ink); box-shadow:none; }
      div.stButton > button > div,
      div.stButton > button p,
      div.stButton > button span{ width:100%; text-align:center !important; justify-content:center !important;
        font-family:'Galmuri11','DungGeunMo',monospace !important; }

      .hud-bar{ display:flex; justify-content:space-between; align-items:center;
        font-family:'Galmuri9',monospace; font-size:12px; color:var(--pink-soft); letter-spacing:.5px; margin-bottom:34px;}
      .prog{ display:flex; gap:5px; }
      .prog i{ width:22px; height:8px; border-radius:2px; background:#2c2236; display:inline-block;}
      .prog i.on{ background:var(--pink); box-shadow:0 0 6px var(--pink);}
      .q-eyebrow{ text-align:center; font-family:'Galmuri9',monospace; font-size:12px; color:var(--pink-soft);
        letter-spacing:1px; margin-bottom:22px;}
      .q-title{ text-align:center !important; color:var(--ink) !important;
        font-family:'Galmuri11','DungGeunMo',monospace !important; font-weight:400 !important;
        font-size:clamp(22px,5.8vw,28px) !important; line-height:1.55 !important;
        margin:0 auto 40px !important; max-width:430px;
        text-shadow:2px 3px 0 var(--black) !important; padding:0 !important;}

      .r-eyebrow{ text-align:center; font-family:'Galmuri9',monospace; color:var(--pink-soft);
        letter-spacing:3px; margin-bottom:18px; font-size:13px;}
      .r-blobwrap{ position:relative; display:flex; align-items:center; justify-content:center;
        width:max-content; margin:0 auto; padding:26px 52px;}
      .r-blob{ position:absolute; inset:0; background:var(--pink);
        border-radius:50%; box-shadow:0 0 0 4px var(--pink-deep); z-index:0;}
      .r-blob::after{ content:""; position:absolute; inset:0; border-radius:inherit;
        background-image:radial-gradient(var(--pink-soft) 1.5px, transparent 1.6px); background-size:11px 11px; opacity:.4;}
      .r-name{ position:relative; z-index:1; color:var(--ink); font-family:'Galmuri11',monospace; line-height:1;
        font-size:clamp(24px,6.4vw,32px); text-shadow:2px 3px 0 var(--black);}
      .r-concept{ text-align:center !important; color:#efe7da !important; font-size:14px !important;
        font-family:'Galmuri11','DungGeunMo',monospace !important;
        line-height:1.8 !important; margin:34px auto 26px !important; max-width:380px; padding:0 !important;}
      .r-badges{ display:flex; justify-content:center; gap:8px; flex-wrap:wrap; margin-bottom:28px;}
      .r-badges .b{ font-family:'Galmuri9',monospace; font-size:12px; color:var(--ink);
        background:rgba(255,111,165,.12); border:1px solid var(--line); border-radius:5px; padding:7px 11px;}
      .r-listtitle{ font-family:'Galmuri11',monospace; color:var(--pink-soft); font-size:15px;
        margin:6px 0 16px; text-align:center;}
      .cafe{ background:var(--screen);
        border:1px solid #2a1d33; border-left:4px solid var(--pink);
        border-radius:8px; padding:14px 15px; margin-bottom:10px;}
      .cafe-top{ display:flex; justify-content:space-between; align-items:baseline; gap:8px;}
      .cafe-name{ font-family:'Galmuri11',monospace; color:var(--ink); font-size:15px;}
      .cafe-dist{ font-family:'Galmuri9',monospace; color:var(--pink-soft); font-size:12px; white-space:nowrap;}
      .cafe-review{ font-family:'Galmuri9','DungGeunMo',monospace; font-size:12px; color:var(--pink-soft);
        margin:7px 0 2px; line-height:1.5;}
      .cafe-mid{ display:flex; gap:6px; flex-wrap:wrap; margin:10px 0 8px;}
      .chip{ font-family:'Galmuri9',monospace; font-size:12px; color:var(--black);
        background:var(--ink); border-radius:4px; padding:4px 9px;}
      .chip.alt{ background:var(--pink-soft);}
      .chip.off{ background:#2c2236; color:#9a8ba6;}
      .cafe-hours{ font-family:'Galmuri9',monospace; font-size:11px; color:#9a8ba6; line-height:1.55;}
      .cafe-mapwrap{ text-align:right; margin-top:12px; }
      .cafe-map-btn{ display:inline-block; text-decoration:none !important;
        font-family:'Galmuri9',monospace; font-size:11px; color:var(--black);
        background:var(--pink-soft); border-radius:5px; padding:8px 13px;
        box-shadow:0 3px 0 var(--pink-deep); transition:transform .06s, box-shadow .06s, background .12s;}
      .cafe-map-btn:hover{ background:#fff; color:var(--black); text-decoration:none !important; }
      .cafe-map-btn:active{ transform:translateY(3px); box-shadow:0 0 0 var(--pink-deep); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
# 상태 & 라우팅
# ──────────────────────────────────────────────────────────────
if "page" not in st.session_state: st.session_state.page = "intro"
if "ans"  not in st.session_state: st.session_state.ans  = {}

qp = st.query_params
if qp.get("start") == "1":
    st.session_state.page = "q1"; st.session_state.ans = {}; st.query_params.clear()
if qp.get("home") == "1":
    st.session_state.page = "intro"; st.session_state.ans = {}; st.query_params.clear()

def go(page):
    st.session_state.page = page
    st.rerun()

def result_group(ans):
    # group = (중거리?4) + (디카페인?2) + (평균↑?1) + 1
    far     = ans.get("time") == "중거리"
    decaf   = ans.get("caffeine") == "디카페인"
    premium = ans.get("price") == "평균↑"
    return (4 if far else 0) + (2 if decaf else 0) + (1 if premium else 0) + 1

def hud(step, total):
    blocks = "".join("<i class='on'></i>" if i <= step else "<i></i>" for i in range(1, total + 1))
    st.markdown(
        f"<div class='hud-bar'><span>QUESTION {step}/{total}</span>"
        f"<span class='prog'>{blocks}</span></div>", unsafe_allow_html=True)

def question(step, title, opt_a, opt_b, key, val_a, val_b, nxt, prev):
    hud(step, 3)
    st.markdown("<div class='q-eyebrow'>☕ CAFE TYPE TEST</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='q-title'>{title}</div>", unsafe_allow_html=True)
    ca = st.columns([1, 3, 1])
    if ca[1].button(opt_a, key=f"{key}_a", type="primary", use_container_width=True):
        st.session_state.ans[key] = val_a; go(nxt)
    cb = st.columns([1, 3, 1])
    if cb[1].button(opt_b, key=f"{key}_b", type="primary", use_container_width=True):
        st.session_state.ans[key] = val_b; go(nxt)
    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    ck = st.columns([2, 2, 2])
    if ck[1].button("← 이전으로", key=f"{key}_back", type="secondary", use_container_width=True):
        go(prev)

def won(v):
    return f"{v:,}원" if v else None

def cafe_card(cf):
    am = won(cf["americano"])
    de = won(cf["decaf"])
    am_chip = f"<span class='chip'>아메리카노 {am}</span>" if am else "<span class='chip off'>아메리카노 정보없음</span>"
    de_chip = f"<span class='chip alt'>디카페인 {de}</span>" if de else "<span class='chip off'>디카페인 미판매</span>"
    review = (cf.get("review") or "").replace("*", "").strip()
    review_html = f"<div class='cafe-review'>{review}</div>" if review else ""
    link = cf.get("link") or ""
    map_btn = (f"<div class='cafe-mapwrap'><a class='cafe-map-btn' href='{link}' "
               f"target='_blank' rel='noopener'>📍 네이버 지도에서 보기 →</a></div>") if link else ""
    return (
        "<div class='cafe'>"
        f"<div class='cafe-top'><span class='cafe-name'>{cf['name']}</span>"
        f"<span class='cafe-dist'>🚶 {cf['dist']}</span></div>"
        f"{review_html}"
        f"<div class='cafe-mid'>{am_chip}{de_chip}</div>"
        f"<div class='cafe-hours'>🕒 {cf['hours']}</div>"
        f"{map_btn}"
        "</div>"
    )

# ──────────────────────────────────────────────────────────────
# 페이지
# ──────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "intro":
    components.html(BOOT_HTML, height=820, scrolling=False)
    # 실제 페이지 이동은 이 네이티브 버튼이 담당합니다.
    # (iframe→부모 URL 이동이 막히는 환경 대비. 화면 속 '▶ 시작하기'를 누르면 이 버튼이 자동 클릭됨)
    st.markdown(
        "<div style='text-align:center;font-family:Galmuri9,monospace;color:#9a8ba6;"
        "font-size:11px;margin:-8px 0 4px;'>화면이 안 넘어가면 아래 버튼을 눌러주세요 ▾</div>",
        unsafe_allow_html=True)
    c = st.columns([1, 2, 1])
    with c[1]:
        if st.button("▶  시작하기", key="start_btn", type="primary", use_container_width=True):
            go("q1")

elif page == "q1":
    question(
        1, "쉬는 시간, 얼마나 멀리까지<br>갈 수 있어?",
        "⚡ 코앞이 좋아 — 3분 안에 픽업!", "🚶 좀 걸어도 OK — 5분까지 가능",
        "time", "근거리", "중거리", "q2", "intro")

elif page == "q2":
    question(
        2, "오늘 너의 한 잔은?",
        "☕ 카페인 풀충전 아메리카노", "🌙 속 편하게 디카페인으로",
        "caffeine", "일반", "디카페인", "q3", "q1")

elif page == "q3":
    question(
        3, "지갑 사정은 어때?",
        "💸 가성비가 최고 — 저렴하게!", "💎 제값 내고 확실한 퀄리티!",
        "price", "평균↓", "평균↑", "result", "q2")

elif page == "result":
    no = result_group(st.session_state.ans)
    grp, cafes = GROUPS[no], CAFES[no]
    badges = "".join(f"<span class='b'>{x}</span>"
                     for x in [grp["time_label"], grp["caffeine"], grp["price"]])
    cards = "".join(cafe_card(cf) for cf in cafes)
    st.markdown(
        "<div class='r-eyebrow'>★ RESULT ★</div>"
        f"<div class='r-blobwrap'><div class='r-blob'></div>"
        f"<span class='r-name'>{grp['name']}</span></div>"
        f"<div class='r-concept'>{grp['concept']}</div>"
        f"<div class='r-badges'>{badges}</div>"
        f"<div class='r-listtitle'>🏆 너에게 딱인 카페 {len(cafes)}곳</div>"
        f"{cards}",
        unsafe_allow_html=True)
    st.write("")
    rc = st.columns([1, 3, 1])
    if rc[1].button("🔄 다시 테스트하기", type="primary", use_container_width=True):
        st.session_state.ans = {}; go("intro")